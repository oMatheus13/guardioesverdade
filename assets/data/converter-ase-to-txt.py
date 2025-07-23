import struct

def read_ase(file_path):
    colors = []
    with open(file_path, "rb") as f:
        header = f.read(4)  # ASEF
        version = f.read(4)
        total_blocks = struct.unpack(">I", f.read(4))[0]

        for _ in range(total_blocks):
            block_type = struct.unpack(">H", f.read(2))[0]
            block_length = struct.unpack(">I", f.read(4))[0]
            data = f.read(block_length)

            if block_type == 0x0001:  # Color entry
                name_length = struct.unpack(">H", data[:2])[0] * 2
                name = data[2:2+name_length].decode("utf-16-be").rstrip("\x00")
                color_model = data[2+name_length:2+name_length+4].decode()
                # RGB floats start after name and color model (variable)
                if color_model == "RGB ":
                    start = 2 + name_length + 4
                    r, g, b = struct.unpack(">fff", data[start:start+12])
                    r = int(r * 255)
                    g = int(g * 255)
                    b = int(b * 255)
                    hex_color = "#{:02X}{:02X}{:02X}".format(r, g, b)
                    colors.append((name, hex_color))
    return colors

# Uso
ase_file = r"D:\Projetos13_\Web\guardioesverdade\assets\data\gv-colors.ase"
cores = read_ase(ase_file)

# Salvar em txt
with open("cores_extraidas.txt", "w", encoding="utf-8") as f:
    for nome, cor in cores:
        f.write(f"{nome}: {cor}\n")

print(f"{len(cores)} cores extraídas e salvas em 'cores_extraidas.txt'.")
