import json

def process_nested_json(json_data):
    if isinstance(json_data, list):
        processed_list = []
        for item in json_data:
            processed_item = process_nested_json(item)
            if processed_item is not None:
                processed_list.append(processed_item)
        return processed_list
    elif isinstance(json_data, dict):
        # 检查最里层的JSON对象是否包含 "instruction", "output", "input"
        if "instruction" in json_data and "output" in json_data and "input" in json_data:
            # 对字典中的每个值递归处理
            return {key: process_nested_json(value) for key, value in json_data.items()}
        else:
            # 如果缺少任何一个关键字，返回None，表示要删除这个对象
            return None
    else:
        # 如果是基本数据类型，直接返回
        return json_data

def clean_json_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    processed_data = process_nested_json(data)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, ensure_ascii=False, indent=4)

# 使用方法
input_file = 'E:\\ATCHATGROOP\\ATMODEL\\kcdata\\ATFTdata_20240806_V1.0.json'
output_file = 'E:\\ATCHATGROOP\\ATMODEL\\kcdata\\ATFTdata_20240806_V1.0_cleaned.json'
clean_json_file(input_file, output_file)
