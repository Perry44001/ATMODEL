import os
import json

# 定义数据集文件夹路径
data_dir = "E:\\ATCHATGROOP\\ATMODEL\\kcdata\\20240803Data"

# 获取所有 JSON 文件的文件名
json_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]

# 初始化数据集信息字典
dataset_info = {
    "description": "Lama finetuning dataset",
    "data_files": [],
    "input_schema": ["instruction", "input", "output"]
}

# 遍历所有 JSON 文件，收集数据文件信息
for file in json_files:
    dataset_info["data_files"].append({
        "file": file,
        "description": "Contains instructions, inputs, and outputs for Lama finetuning"
    })

# 指定输出路径
output_path = os.path.join(data_dir, "dataset_info.json")

# 将 dataset_info 写入 JSON 文件
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(dataset_info, f, ensure_ascii=False, indent=4)

print(f"dataset_info.json has been created at {output_path}")
