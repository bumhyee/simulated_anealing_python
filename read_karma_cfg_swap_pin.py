import random
import os
import glob

def read_karma_file(filename):
    """Read entire KARMA file"""
    with open(filename, 'r') as f:
        lines = f.readlines()
    return lines

def extract_cfg_section(lines):
    """Extract CFG section (start/end indices and CFG data)"""
    cfg_start = None
    cfg_end = None
    cfg_lines = []
    
    for i, line in enumerate(lines):
        if 'CFG' in line:
            cfg_start = i
            # Include the number next to CFG
            parts = line.split()
            if len(parts) > 1:
                cfg_lines.append(parts[1])
            continue
        
        if cfg_start is not None and cfg_end is None:
            if line.strip().startswith('%'):
                cfg_end = i
                break
            if line.strip():
                cfg_lines.append(line.strip())
    
    return cfg_start, cfg_end, cfg_lines

def find_positions(cfg_data):
    """Find positions of 4 and all 1s (excluding first line which is CFG size)"""
    pos_4 = None
    pos_1_list = []
    
    # Start from index 1 since first line (index 0) is CFG size
    for row_idx, line in enumerate(cfg_data[1:], start=1):
        elements = line.split()
        for col_idx, element in enumerate(elements):
            if element == '4':
                pos_4 = (row_idx, col_idx)
            elif element == '1':
                pos_1_list.append((row_idx, col_idx))
    
    return pos_4, pos_1_list

def swap_positions(cfg_data, pos1, pos2):
    """Swap values at two positions"""
    cfg_matrix = []
    
    # Keep CFG size line as is
    cfg_matrix.append(cfg_data[0])
    
    # Convert remaining lines to lists
    for line in cfg_data[1:]:
        cfg_matrix.append(line.split())
    
    # Swap
    row1, col1 = pos1
    row2, col2 = pos2
    cfg_matrix[row1][col1], cfg_matrix[row2][col2] = cfg_matrix[row2][col2], cfg_matrix[row1][col1]
    
    # Convert back to strings
    result = [cfg_matrix[0]]  # CFG size
    for row in cfg_matrix[1:]:
        result.append(' '.join(row))
    
    return result

def get_next_filename():
    """Generate next sequential filename (KARMA_00001.IN, KARMA_00002.IN, ...)"""
    existing_files = glob.glob("KARMA_*.IN")
    
    if not existing_files:
        return "KARMA_00001.IN"
    
    # Extract numbers from existing files
    numbers = []
    for f in existing_files:
        try:
            # Extract number from filename like KARMA_00001.IN
            num_str = f.replace("KARMA_", "").replace(".IN", "")
            numbers.append(int(num_str))
        except ValueError:
            continue
    
    if not numbers:
        return "KARMA_00001.IN"
    
    # Get next number
    next_num = max(numbers) + 1
    return f"KARMA_{next_num:05d}.IN"

def write_karma_file(filename, lines, cfg_start, cfg_end, new_cfg_data):
    """Write KARMA file with updated CFG to a new file"""
    new_lines = lines[:cfg_start+1]  # Up to CFG line
    
    # Add new CFG data (with indentation)
    for line in new_cfg_data:
        new_lines.append(f"     {line}\n")
    
    # Add lines after CFG
    new_lines.extend(lines[cfg_end:])
    
    # Generate new filename
    new_filename = get_next_filename()
    
    with open(new_filename, 'w') as f:
        f.writelines(new_lines)
    
    return new_filename

def main():
    filename = "KARMA.IN"
    
    print("="*60)
    print("CFG Random SWAP Program (4 ↔ 1)")
    print("="*60)
    
    # 1. Read file
    lines = read_karma_file(filename)
    
    # 2. Extract CFG section
    cfg_start, cfg_end, cfg_data = extract_cfg_section(lines)
    
    print("\n[Original CFG]")
    for i, line in enumerate(cfg_data):
        print(f"Row {i}: {line}")
    
    # 3. Find positions of 4 and 1s
    pos_4, pos_1_list = find_positions(cfg_data)
    
    if pos_4 is None:
        print("\n❌ Error: Could not find '4' in CFG.")
        return
    
    if not pos_1_list:
        print("\n❌ Error: Could not find '1' in CFG.")
        return
    
    print(f"\n[Position Info]")
    print(f"Position of 4: Row {pos_4[0]}, Col {pos_4[1]}")
    print(f"Number of 1s: {len(pos_1_list)}")
    
    # 4. Randomly select a 1
    selected_1 = random.choice(pos_1_list)
    print(f"Selected 1 position: Row {selected_1[0]}, Col {selected_1[1]}")
    
    # 5. Swap
    new_cfg_data = swap_positions(cfg_data, pos_4, selected_1)
    
    print("\n[CFG After SWAP]")
    for i, line in enumerate(new_cfg_data):
        print(f"Row {i}: {line}")
    
    # 6. Save to new file
    new_filename = write_karma_file(filename, lines, cfg_start, cfg_end, new_cfg_data)
    
    print(f"\n✅ New file created: '{new_filename}'")
    print(f"   Original file '{filename}' remains unchanged")
    print(f"   4: Row {pos_4[0]}, Col {pos_4[1]} → Row {selected_1[0]}, Col {selected_1[1]}")
    print(f"   1: Row {selected_1[0]}, Col {selected_1[1]} → Row {pos_4[0]}, Col {pos_4[1]}")
    print("="*60)

if __name__ == "__main__":
    main()