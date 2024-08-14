import json
import re
import os

folder_path = 'E:/ATCHATGROOP/ATMODEL/kcdata/reGroupKC'  # 替换为你的JSON文件夹路径
output_path = 'E:/ATCHATGROOP/ATMODEL/kcdata/reGroupKCR'       # 输出文件的路径

for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        file_path = os.path.join(folder_path, filename)
        # 读取原始的TXT文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # 使用正则表达式找到并删除 ```...```json``` 之间的内容
        pattern = r'```.*?```json'  # 匹配 ```json ... ``` 之间的内容
        modified_content = re.sub(pattern, ',', content, flags=re.DOTALL)

        outname = filename[0:-5] + 'R.json'
        out_path = os.path.join(output_path, outname)
        # 将修改后的内容写入一个新的TXT文件
        with open(out_path, 'w', encoding='utf-8') as new_file:
            new_file.write(modified_content)

        print("内容已成功修改并写入新的json文件")
