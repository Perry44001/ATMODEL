import os
import json
import re

def find_and_parse_json(text):
    # 正则表达式模式，匹配以花括号包裹的 JSON 对象
    json_pattern = r'\{.*?\}'

    # 在文本中查找所有匹配的 JSON 对象
    # 使用正则表达式查找JSON数据
    matches = re.findall(r'\{.*?\}', text, re.DOTALL)
    # matches = re.findall(json_pattern, text)

    # 解析找到的 JSON 对象
    parsed_json = []
    for match in matches:
        try:
            data = json.loads(match)
        except json.JSONDecodeError:
            data = ''
        parsed_json.append(data)
    # parsed_json = [json.loads(match) for match in matches]

    return parsed_json

def flatten_json(json_data):
    # 将所有嵌套的JSON对象提取到同一级
    flattened = []
    if isinstance(json_data, list):
        for item in json_data:
            flattened.extend(flatten_json(item))
    elif isinstance(json_data, dict):
        if "instruction" in json_data and "output" in json_data:
            if "input" not in json_data:
                new_json_data = {}

                # 插入 'introduction' 键值对
                new_json_data["instruction"] = json_data["instruction"]

                # 插入 'input' 键值对
                new_json_data["input"] = ""

                # 插入 'output' 键值对
                new_json_data["output"] = json_data["output"]

                # 重新赋值回原字典
                json_data = {}
                json_data = new_json_data
            flattened.append(json_data)
    return flattened


def merge_json_files(folder_path, output_path):
    merged_data = []

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                # data = json.load(f)
                txt_content = f.read()
                data = find_and_parse_json(txt_content)
                # merged_data = data
        processed_data = flatten_json(data)
        output_file = os.path.join(output_path, filename[:-5] + 'R.json')
        # 将合并后的数据写入输出文件
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(processed_data, f, ensure_ascii=False, indent=4)

# 使用方法
folder_path = 'E:/ATCHATGROOP/ATMODEL/kcdata/reLenKC'  # 替换为你的JSON文件夹路径
output_path = 'E:/ATCHATGROOP/ATMODEL/kcdata/reLenKCR'       # 输出文件的路径
merge_json_files(folder_path, output_path)
