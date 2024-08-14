import json
import os

def validate_llama_format(json_data):
    # 检查JSON对象是否包含所有必须的字段
    if isinstance(json_data, dict):
        if all(key in json_data for key in ["instruction", "input", "output"]):
            return True
        else:
            return False
    return False

def flatten_json(json_data):
    # 将所有嵌套的JSON对象提取到同一级
    flattened = []
    if isinstance(json_data, list):
        for item in json_data:
            flattened.extend(flatten_json(item))
    elif isinstance(json_data, dict):
        if validate_llama_format(json_data):
            flattened.append(json_data)
        for key, value in json_data.items():
            flattened.extend(flatten_json(value))
    return flattened

def clean_json_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 将所有的JSON对象展平到同一级，并过滤不符合格式的对象
    cleaned_data = flatten_json(data)

    # 将结果写入新的JSON文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=4)

# 使用方法
input_file = 'E:\\ATCHATGROOP\\ATMODEL\\kcdata\\ATFTdata_20240806_V1.0_cleaned.json'
output_file = 'E:\\ATCHATGROOP\\ATMODEL\\kcdata\\ATFTdata_20240806_V1.0_flattened_cleaned.json'
clean_json_file(input_file, output_file)
