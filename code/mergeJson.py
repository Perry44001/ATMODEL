import os
import json

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


def merge_json_files(folder_path, output_file):
    merged_data = []

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        if filename.endswith('R.json'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                merged_data.append(data)
    processed_data = flatten_json(merged_data)

    # 将合并后的数据写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, ensure_ascii=False, indent=4)

# 使用方法
folder_path = 'E:/ATCHATGROOP/ATMODEL/kcdata/reGroupKCR'  # 替换为你的JSON文件夹路径
output_file = 'E:/ATCHATGROOP/ATMODEL/kcdata/data0814.json'       # 输出文件的路径
merge_json_files(folder_path, output_file)
