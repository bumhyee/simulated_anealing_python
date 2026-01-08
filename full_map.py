import os
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# Global settings
# ============================================================
BASE_IN_FILE = "KARMA.IN"
OUTPUT_DIR = "output"
PNG_DIR = "png"

NUM_CASES = 5
ALLOWED_TYPES = [1, 2, 4, 5]

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(PNG_DIR, exist_ok=True)

# ============================================================
# Read CFG (center pin + 1/8 map)
# ============================================================
def read_karma_cfg(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    center_pin = None
    eighth_map = []
    in_cfg = False

    for line in lines:
        if line.strip().startswith("CFG"):
            parts = line.split()
            center_pin = int(parts[1])
            in_cfg = True
            continue

        if in_cfg:
            if line.strip().startswith('%'):
                break
            if line.strip():
                eighth_map.append([int(x) for x in line.split()])

    return center_pin, eighth_map

# ============================================================
# Randomize 1/8 map (center excluded)
# ============================================================
def randomize_eighth_map(base_map):
    new_map = []
    for row in base_map:
        new_row = [np.random.choice(ALLOWED_TYPES) for _ in row]
        new_map.append(new_row)
    return new_map

# ============================================================
# Expand 1/8 → full core (center pin explicit)
# ============================================================
def expand_eighth_to_full(eighth_map, center_pin):
    n_rows = len(eighth_map)
    max_cols = max(len(row) for row in eighth_map)

    radius = max(n_rows, max_cols)
    full_size = 2 * radius + 1
    center = radius

    full_map = np.zeros((full_size, full_size), dtype=int)

    # 중앙 pin
    full_map[center, center] = center_pin

    # 1/8 영역 배치 (↘)
    for i in range(n_rows):
        for j in range(len(eighth_map[i])):
            full_map[center + i, center + j] = eighth_map[i][j]

    # 대각 대칭
    for i in range(n_rows):
        for j in range(i + 1, n_rows):
            full_map[center + i, center + j] = \
                full_map[center + j, center + i]

    # 좌우 대칭
    for i in range(full_size):
        for j in range(center):
            full_map[i, j] = full_map[i, full_size - 1 - j]

    # 상하 대칭
    for i in range(center):
        full_map[i, :] = full_map[full_size - 1 - i, :]

    return full_map


# ============================================================
# Save full CFG
# ============================================================
def save_full_cfg(full_map, path):
    with open(path, 'w') as f:
        f.write("Full Core Configuration\n")
        f.write("=" * 60 + "\n")
        for row in full_map:
            f.write(" ".join(f"{int(x):2d}" for x in row) + "\n")
        f.write("=" * 60 + "\n")
    print(f"  ✔ CFG saved: {path}")

# ============================================================
# Write new KARMA.IN with full CFG
# ============================================================
def write_full_karma_in(original_in, full_map, output_path):
    with open(original_in, 'r') as f:
        lines = f.readlines()

    new_lines = []
    in_cfg = False

    for line in lines:
        if line.strip().startswith("CFG"):
            in_cfg = True
            new_lines.append(f"   CFG  {full_map.shape[0]}\n")
            continue

        if in_cfg:
            if line.strip().startswith('%'):
                for row in full_map:
                    new_lines.append(
                        "     " + " ".join(str(int(x)) for x in row) + "\n"
                    )
                new_lines.append(line)
                in_cfg = False
            continue

        new_lines.append(line)

    with open(output_path, 'w') as f:
        f.writelines(new_lines)

    print(f"  ✔ IN saved : {output_path}")

# ============================================================
# Visualization (last case)
# ============================================================
def visualize_maps(eighth_map, full_map):
    fig, axes = plt.subplots(1, 2, figsize=(15, 7))

    ax1, ax2 = axes

    max_len = max(len(r) for r in eighth_map)
    eighth_array = np.zeros((len(eighth_map), max_len))
    for i, row in enumerate(eighth_map):
        for j, v in enumerate(row):
            eighth_array[i, j] = v

    im1 = ax1.imshow(eighth_array, cmap="tab20c")
    ax1.set_title("1/8 Core Pattern")
    plt.colorbar(im1, ax=ax1)

    im2 = ax2.imshow(full_map, cmap="tab20c")
    ax2.set_title("Full Core Configuration")
    plt.colorbar(im2, ax=ax2)

    plt.tight_layout()
    plt.savefig(os.path.join(PNG_DIR, "karma_cfg_expansion.png"), dpi=150)
    plt.show()

# ============================================================
# Case generator
# ============================================================
def generate_case(case_id, base_eighth_map, center_pin):
    case_dir = os.path.join(OUTPUT_DIR, f"case_{case_id:03d}")
    os.makedirs(case_dir, exist_ok=True)

    eighth_map = randomize_eighth_map(base_eighth_map)
    full_map = expand_eighth_to_full(eighth_map, center_pin)

    save_full_cfg(full_map, os.path.join(case_dir, "KARMA_FULL.CFG"))
    write_full_karma_in(
        BASE_IN_FILE,
        full_map,
        os.path.join(case_dir, "KARMA_FULL.IN")
    )

    return eighth_map, full_map

# ============================================================
# Main
# ============================================================
def main():
    print("=" * 60)
    print("KARMA CFG – Sequential Full Core Generator")
    print("=" * 60)

    center_pin, base_eighth_map = read_karma_cfg(BASE_IN_FILE)

    for case_id in range(1, NUM_CASES + 1):
        print(f"\n🚀 Generating case_{case_id:03d}")
        eighth_map, full_map = generate_case(
            case_id, base_eighth_map, center_pin
        )

    visualize_maps(eighth_map, full_map)
    print("\n✅ All cases generated successfully.")

if __name__ == "__main__":
    main()
