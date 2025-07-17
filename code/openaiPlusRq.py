import requests
import json
import re
import sys
import logging
from datetime import datetime

# 获取当前日期和时间
now = datetime.now()

# 按指定格式 yyyy-mm-dd-HH-MM-SS 格式化
formatted_time = now.strftime('%Y-%m-%d-%H-%M-%S')

print(formatted_time)  # 输出示例：2024-07-18-22-03-30

# 配置logging模块
logging.basicConfig(
    filename='E:\\ATCHATGROOP\\ATMODEL\\log\\output' + formatted_time + '.log',   # 日志文件名
    level=logging.INFO,      # 日志级别（根据需要调整）
    format='%(asctime)s - %(levelname)s - %(message)s',  # 日志格式
    encoding='utf-8'         # 指定编码格式为 utf-8
)

# 重写 print 函数，将输出重定向到 logging.info
def printlog(*args, **kwargs):
    message = ' '.join(map(str, args))
    logging.info(message)
    
    
# url = "https://api.openai.com/v1/chat/completions"
url = "https://apikeyplus.com/v1/chat/completions"

headers = {
  'Content-Type': 'application/json',
  # 填写 OpenKEY 生成的令牌/KEY，注意前面的 Bearer 要保留，并且和 KEY 中间有一个空格。
  'Authorization': 'B**'
}


def generate_gpt_responses(input_file_path, output_file_path, j):
    try:
        jj= j
        j = j - 1 # 因为j是从1开始的，所以要减1
        with open(input_file_path, 'r', encoding='utf-8') as infile:
            dataset = json.load(infile)

        # 准备输入文本
        instruction_texts = [item['instruction'] for item in dataset]
        input_texts = [item['input'] for item in dataset]
        output_texts = [item['output'] for item in dataset]

        # 第一次打开扩充文件时，我们希望使用"["把json组包裹住
        # json组中是原始json扩充出的多个json集合
        # 如果文件本来就有内容（比如说是中间断了，想要继续扩增），请不要用下面几行，会把文件清除
        if j <= 0:
            with open(output_file_path, 'w', encoding='utf-8') as outfile:
                print('[', file=outfile)

        # 批量调用GPT模型生成新数据
        for i in range(j, len(input_texts)):
            # 打印当前处理的输入输出对
            print(f"\n\nGenerating data for input {(i+1)/len(input_texts)*100:.1f}% {i+1}/{len(input_texts)}")
            printlog(f"\n\nGenerating data for input {(i+1)/len(input_texts)*100:.1f}% {i+1}/{len(input_texts)}")

            # 构造一条消息，包含原始的指令、输入、输出，以及提示扩充数据的提示
            # 注意：这里的提示内容请根据实际情况修改，比如："请根据上面的问答扩充问答10条数据，使用'{\"instruction\":\"[问题]\",\"input\":\"[指令]\",\"output\":\"[回答]\"}'的json格式" 
            jj = i + 1
            # Non-streaming:
            print("----- standard request -----")
            printlog("----- standard request -----")
            data={
                "model": "gpt-4o",
                "messages": [
                    {"role": "user", "content": '''我想让你担任水声科学家。我会写一些水声的问答，你的工作就是根据以上问题用通俗易懂的话语扩充若干条问答数据用于大模型微调数据集，将复杂的问答用简单短小的问答代替，问题扩展原则：1.针对一个说明性的问题进行详细全面的回答，从不同方面加以解释和补充。2.确保扩展出的问题与原有背景密切相关，避免脱离语境或显得突兀。3.对每个扩展的问题都提供足够的信息，使其成为一个完整、有价值且容易理解的小问答。4.如果问答中给出教程链接，请保持网址链接文本不变，并在扩充的问答数据适当位置给出。5.使用'#*%{"instruction":"[问题]","input":"[指令]","output":"[回答]"}@~*的.json格式，注意用#*%和@~*包裹住json，已方便我使用json.loads进行解析。'''},
                    {
                    "role": "assistant",
                    "content": '{"instruction":"' + instruction_texts[i] + '","input":""' + input_texts[i] 
                        + ',"output":"' + output_texts[i] + '"}',
                    },
                            ],
                "temperature": 0.8,
                "max_tokens": 2000,
                "top_p": 0.5,
                "frequency_penalty": 0.6,
                "presence_penalty": 0.2
            }
            print("message:\n", data)
            printlog("message:\n", data)
            response = requests.post(url, headers=headers, json=data)
            
            output = response.json()['choices'][0]['message']['content'].strip()
            print("\nresponse:\n", output)
            printlog("\nresponse:\n", output)
            # 防止json中间缺少逗号导致的格式错误，使用通配符读取数据
            # pattern = r'\{"instruction":"([^}]*)\"\}'
            # pattern = r'\{"instruction":"(.*?)"\}'
            # pattern = r'##\{"instruction":"(.*?)"\}@@'
            pattern = r'#*%(.*?)@~*'

            matches = re.findall(pattern, output)
            # 我们将每个扩充后的结果放在一个list
            output_jsons = [dataset[i]]
            for match in matches:
                jsonstr = match
                try:
                    outjson = json.loads(jsonstr)
                    output_jsons.append(outjson)
                except:
                    print("json格式错误，请检查输入输出是否正确")
                    printlog("json格式错误，请检查输入输出是否正确")
            # 把结果输出到扩充文件中去，用append添加到末尾的方式，防止中间断掉，整段白跑
            if i != len(input_texts)-1: # 如果不是最后一个json，则在json组符号][加入逗号","
                with open(output_file_path, 'a', encoding='utf-8') as outfile:
                    json.dump(output_jsons, outfile, ensure_ascii=False, indent=4)
                    print(',', file=outfile)
            else: # 如果是最后一个json，则使用]把所有json组包裹起来
                with open(output_file_path, 'a', encoding='utf-8') as outfile:
                    json.dump(output_jsons, outfile, ensure_ascii=False, indent=4)
                    print(']', file=outfile)
        return jj + 1
    except Exception as e:
        print(e)
        printlog(e)
        return jj + 1

def main(input_file_path, output_file_path, rk):
    with open(input_file_path, 'r', encoding='utf-8') as infile:
        dataset = json.load(infile)
    k = rk
    while(k <= len(dataset)): # 循环调用generate_gpt_responses函数，直到处理完所有输入输出对
        k = generate_gpt_responses(input_file_path, output_file_path, k)

    # 保存扩增后的数据集
    print(f"Data augmentation complete. The augmented dataset is saved to {output_file_path}")
    printlog(f"Data augmentation complete. The augmented dataset is saved to {output_file_path}")

if __name__ == "__main__":
    input_file_path = 'E:/ATCHATGROOP/ATMODEL/data/test.json'
    output_file_path = 'E:/ATCHATGROOP/ATMODEL/kcdata/OAPLUStest.json'
    rk = 1
    cmdstr = "python"
    for sargv in sys.argv:
        cmdstr+=' '+sargv
    printlog("cmd:", cmdstr)

    for i in range(1, len(sys.argv)):
        if sys.argv[i] == '-i':
            input_file_path = sys.argv[i + 1]
        elif sys.argv[i] == '-o':
            output_file_path = sys.argv[i + 1]
        elif sys.argv[i] == '-r':
            rk = int(sys.argv[i + 1])

    if input_file_path and output_file_path and rk:
        main(input_file_path, output_file_path, rk)
    else:
        print("请提供正确的超参数")
        printlog("请提供正确的超参数")
