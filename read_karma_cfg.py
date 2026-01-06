def read_cfg(filename):
    """KARMA 파일에서 CFG 부분 읽기"""
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    # 처음 10줄 보기 좋게 출력
    print("======== input file (10 lines) ========")
    for i in range(20):
        print(f"{lines[i].rstrip()}")
    print("=" * 50)

    cfg_lines = []
    in_cfg = False
    
    for line in lines:
        if 'CFG' in line:
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
    
    return cfg_lines

def print_cfg(cfg_lines):
    """CFG 출력"""
    print("CFG:")
    for i, line in enumerate(cfg_lines):
        print(f"Row {i}: {line}")

# 실행
if __name__ == "__main__":
    filename = "KARMA.IN"
    cfg = read_cfg(filename)
    print_cfg(cfg)