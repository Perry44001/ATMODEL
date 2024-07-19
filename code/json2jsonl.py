import os
import json
import jsonlines

# json转为jsonl
def convert_json_to_jsonl(json_file, jsonl_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    with jsonlines.open(jsonl_file, 'w') as writer:
        writer.write(data)

# jsonl转为json
def convert_jsonl_to_json(jsonl_file, json_file):
    with jsonlines.open(jsonl_file, 'r') as reader:
        data = [obj for obj in reader]

    with open(json_file, 'w', encoding='utf-8') as file:
        json.dump(data, file)

if __name__ == "__main__":
    # input_file_path = 'E:/ATCHATGROOP/ATMODEL/data/test.json'
    # output_file_path = 'E:/ATCHATGROOP/ATMODEL/kcdata/testKC.json'
    # rk = 1
    # for i in range(1, len(sys.argv)):
    #     if sys.argv[i] == '-i':
    #         input_file_path = sys.argv[i + 1]
    #     elif sys.argv[i] == '-o':
    #         output_file_path = sys.argv[i + 1]
    #     elif sys.argv[i] == '-r':
    #         rk = int(sys.argv[i + 1])

    # if input_file_path and output_file_path and rk:
    #     main(input_file_path, output_file_path, rk)
    # else:
    #     print("请提供正确的超参数")
    path = 'E:/ATCHATGROOP/ATMODEL/kcdata/'
    # 取path下面所有.json的路径
    json_files = [os.path.join(path, file) for file in os.listdir(path) if file.endswith('.json')]
    print(json_files)
    for json_file in json_files:
        jsonl_file = json_file.replace('.json', '.jsonl')
        convert_json_to_jsonl(json_file, jsonl_file)
        print(f"{json_file} 转为 {jsonl_file} 成功")