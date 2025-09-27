import glob
import os

txt_path = r"D:\\poems\\txt_deep_cleaned"
output_file = r"D:\\poems\\corpus.txt"

# 找到所有 txt 文件
files = glob.glob(os.path.join(txt_path, "*.txt"))

corpus = ""
for fname in files:
    with open(fname, "r", encoding="utf-8") as f:
        text = f.read().strip()
        if text:
            # 保持每个文件之间有换行，避免粘连
            corpus += text + "\n"

# 保存为一个大 txt
with open(output_file, "w", encoding="utf-8") as f:
    f.write(corpus)

print(f"拼接完成，共 {len(files)} 个文件 → {output_file}")

