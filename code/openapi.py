import openai
import json
import os

# 设置OpenAI API密钥
openai.api_key = 's**'

# 读取已有的数据集
input_file_path = 'E:/ATCHATGROOP/ATMODEL/data/xxu.json'
output_file_path = 'E:/ATCHATGROOP/ATMODEL/kcdata/xxuKC.json'

with open(input_file_path, 'r', encoding='utf-8') as infile:
    dataset = json.load(infile)

# 批量调用GPT模型生成新数据
def generate_gpt_responses(input_texts):
    responses = []
    for input_text in input_texts:
        response = openai.Completion.create(
            model="text-davinci-003",  # 选择合适的GPT模型
            prompt=input_text,
            max_tokens=50  # 根据需要调整生成文本的长度
        )
        responses.append(response.choices[0].text.strip())
    return responses

# 准备输入文本
input_texts = [item['input'] for item in dataset]

# 生成新的输出
new_outputs = generate_gpt_responses(input_texts)

# 将新输出添加到数据集中
for i, item in enumerate(dataset):
    item['output'] = new_outputs[i]

# 保存扩增后的数据集
with open(output_file_path, 'w', encoding='utf-8') as outfile:
    json.dump(dataset, outfile, ensure_ascii=False, indent=4)

print(f"Data augmentation complete. The augmented dataset is saved to {output_file_path}")
