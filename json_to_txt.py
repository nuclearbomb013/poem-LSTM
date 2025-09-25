import json
import os
folder_path='D:\\poems\\chinese-poetry-master\\全唐诗'
prefix='poet'
txt_path='D:\\poems\\txt'
for each_file in os.listdir(folder_path):
    if each_file.startswith(prefix) and each_file.endswith('.json'):
        file_path=os.path.join(folder_path,each_file)
        with open(file_path,'r',encoding='utf-8') as f:
             poems = json.load(f)
        txt_filename = os.path.splitext(each_file)[0] + ".txt"
        temp_txt_path=os.path.join(txt_path, txt_filename)
        with open(temp_txt_path,'w',encoding='utf-8') as out_f:
            for poem in poems:
                content_list = poem.get("paragraphs", [])
                # list 拼成字符串
                content = "".join(content_list)
                content = content.strip()  # 去掉首尾空格
                if content:
                 out_f.write(content + "\n")



# # 1. 读取 JSON 文件
# with open("D:\\poems\\chinese-poetry-master\\全唐诗\\poet.song.0.json", "r", encoding="utf-8") as f:
#     poems = json.load(f)

# # 2. 打开输出文件
# with open("D:\\poems\\txt\\poet.song.0.txt", "w", encoding="utf-8") as out_f:
#     for poem in poems:
#         content_list = poem.get("paragraphs", [])
#         # list 拼成字符串
#         content = "".join(content_list)
#         content = content.strip()  # 去掉首尾空格
#         if content:
#             out_f.write(content + "\n")

# print(f"处理完成，共写入 {len(poems)} 首唐诗到 txt")