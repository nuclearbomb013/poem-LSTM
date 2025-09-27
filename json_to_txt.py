# import json
# import os
# folder_path='D:\\poems\\chinese-poetry-master\\全唐诗'
# prefix='poet'
# txt_path='D:\\poems\\txt'
# for each_file in os.listdir(folder_path):
#     if each_file.startswith(prefix) and each_file.endswith('.json'):
#         file_path=os.path.join(folder_path,each_file)
#         with open(file_path,'r',encoding='utf-8') as f:
#              poems = json.load(f)
#         txt_filename = os.path.splitext(each_file)[0] + ".txt"
#         temp_txt_path=os.path.join(txt_path, txt_filename)
#         with open(temp_txt_path,'w',encoding='utf-8') as out_f:
#             for poem in poems:
#                 content_list = poem.get("paragraphs", [])
#                 # list 拼成字符串
#                 content = "".join(content_list)
#                 content = content.strip()  # 去掉首尾空格
#                 if content:
#                  out_f.write(content + "\n")
import os
import re
import json
folder_path = r'D:\\poems\\chinese-poetry-master\\全唐诗'
prefix = 'poet'
txt_path = r'D:\\poems\\txt1'

for each_file in os.listdir(folder_path):
    if each_file.startswith(prefix) and each_file.endswith('.json'):
        file_path = os.path.join(folder_path, each_file)
        with open(file_path, 'r', encoding='utf-8') as f:
            poems = json.load(f)#poems是每个json的内容

        txt_filename = os.path.splitext(each_file)[0] + ".txt"
        temp_txt_path = os.path.join(txt_path, txt_filename)

        with open(temp_txt_path, 'w', encoding='utf-8') as out_f:
            for poem in poems:
                content_list = poem.get("paragraphs", [])
                content = "".join(content_list)
                content = content.strip()

                # 去掉括号（中括号、圆括号、书名号）里的注释
                content = re.sub(r"（.*?）", "", content)  # 全角括号
                content = re.sub(r"\(.*?\)", "", content)  # 半角括号
                content = re.sub(r"\[.*?\]", "", content)  # 中括号
                content = re.sub(r"【.*?】", "", content)  # 书名号

                if content:
                    out_f.write(content + "\n")

print("处理完成！所有 txt 已生成并去掉括号注释。")
