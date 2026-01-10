def read_cfg(filename):
    """KARMA 파일에서 CFG 부분 읽기"""
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    # 처음 20줄 보기 좋게 출력
    print("======== input file (20 lines) ========")
    for i in range(min(20, len(lines))):  # 파일이 20줄보다 짧을 경우 대비
        print(f"{lines[i].rstrip()}")
    print("=" * 50)

    cfg_lines = []
    cfg_header = None
    in_cfg = False
    
    for line in lines:
        if 'CFG' in line:
            cfg_header = line  # CFG 헤더 라인 저장
            # CFG 옆 숫자 추출
            parts = line.split()
            if len(parts) > 1:
                cfg_lines.append(parts[1])
            in_cfg = True
            continue
        if in_cfg:
            if line.strip().startswith('%'):
                break
            if line.strip():
                cfg_lines.append(line.strip())
    
    return cfg_lines, lines, cfg_header

def print_cfg(cfg_lines):
    """CFG 출력"""
    print("\nCFG (1/8 map):")
    for i, line in enumerate(cfg_lines):
        print(f"Row {i}: {line}")

def write_cfg(filename, original_lines, new_cfg_lines, cfg_header):
    """수정된 CFG를 반영한 새 KARMA 파일 저장"""
    # 원본 파일명에서 확장자 분리
    if '.' in filename:
        base_name = filename.rsplit('.', 1)[0]
        extension = '.' + filename.rsplit('.', 1)[1]
    else:
        base_name = filename
        extension = ''
    
    # 기존 파일들의 번호 확인
    import os
    import re
    
    existing_numbers = []
    for f in os.listdir('.'):
        # KARMA.IN_1, KARMA.IN_2 등의 패턴 찾기
        pattern = re.escape(base_name) + re.escape(extension) + r'_(\d+)$'
        match = re.match(pattern, f)
        if match:
            existing_numbers.append(int(match.group(1)))
    
    # 다음 번호 결정
    next_number = max(existing_numbers) + 1 if existing_numbers else 1
    new_filename = f"{base_name}{extension}_{next_number}"
    
    # CFG 헤더에서 숫자 추출
    cfg_number = None
    if cfg_header:
        parts = cfg_header.split()
        if len(parts) > 1:
            cfg_number = parts[1]
    
    # 새 파일 생성
    with open(new_filename, 'w') as f:
        in_cfg = False
        cfg_written = False
        skip_first_data_line = False
        
        for line in original_lines:
            if 'CFG' in line and not cfg_written:
                # CFG 헤더 쓰기
                f.write(line)
                # 새로운 CFG 데이터 쓰기 (첫 번째 줄 제외 - 이미 CFG 옆에 있음)
                for i, cfg_line in enumerate(new_cfg_lines):
                    if i == 0:
                        # 첫 번째 줄은 CFG 헤더에 이미 포함되어 있으므로 스킵
                        continue
                    f.write(cfg_line + '\n')
                in_cfg = True
                cfg_written = True
                continue
            
            if in_cfg:
                # CFG 섹션이 끝날 때까지 원본 라인 스킵
                if line.strip().startswith('%'):
                    in_cfg = False
                    f.write(line)
                elif not line.strip():
                    # 빈 줄은 유지
                    f.write(line)
                # CFG 데이터 라인은 스킵 (이미 새 데이터를 썼으므로)
                continue
            else:
                f.write(line)
    
    print(f"\n새 파일 저장됨: {new_filename}")
    return new_filename

# 실행
if __name__ == "__main__":
    filename = "KARMA.IN"
    cfg, original_lines, cfg_header = read_cfg(filename)
    print_cfg(cfg)
    
    # 예시: CFG 수정 (실제 사용시에는 원하는 방식으로 수정)
    modified_cfg = cfg.copy()
    # modified_cfg[0] = "8"  # CFG 옆 숫자 수정
    # modified_cfg[1] = "modified_value"  # 두 번째 줄부터 수정
    
    # 수정된 CFG로 새 파일 저장
    write_cfg(filename, original_lines, modified_cfg, cfg_header)