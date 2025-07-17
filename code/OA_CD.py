import requests
import json
import re
import sys
import logging
from datetime import datetime
import time

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
    j = j - 1 # 因为j是从1开始的，所以要减1
    with open(input_file_path, 'r', encoding='utf-8') as infile:
        dataset = json.load(infile)

    # 准备输入文本
    instruction_texts = [item['instruction'] for item in dataset]
    input_texts = [item['input'] for item in dataset]
    output_texts = [item['output'] for item in dataset]

    # 批量调用GPT模型生成新数据
    for i in range(j, len(input_texts)):
        # 打印当前处理的输入输出对
        print(f"\n\nGenerating data for input {(i+1)/len(input_texts)*100:.1f}% {i+1}/{len(input_texts)}")
        printlog(f"\n\nGenerating data for input {(i+1)/len(input_texts)*100:.1f}% {i+1}/{len(input_texts)}")
        print("----- standard request -----")
        printlog("----- standard request -----")
        for k in range(0,10):
            if k == 0:
                data={
                    "model": "gpt-4o",
                    "messages": [
                        {"role": "user", "content": '''我要构建一个业务数据集，用于大模型微调，格式如下：
                            [
                            {
                                "instruction": "用户指令（必填）",
                                "output": "模型回答（必填）"
                            }
                            ]
                            请利用以下的关于声学工具箱编程的数据扩充这个数据集，改变用户指令和模型回答，根据问题适当扩充代码，但注意正确性，如果有网址保证网址的正确性，在扩充数据集中，不要出现换行，使用换行符\\n代替：
                            '''+'{"instruction":"' + instruction_texts[i] + '","input":""' + input_texts[i] 
                            + ',"output":"' + output_texts[i] + '"}'},
                                ],
                }
            else:
                data={
                    "model": "gpt-4o",
                    "messages": [
                        {"role": "user", "content": '''我要构建一个业务数据集，用于大模型微调，格式如下：
                            [
                            {
                                "instruction": "用户指令（必填）",
                                "output": "模型回答（必填）"
                            }
                            ]
                             请利用以下的关于声学工具箱编程的数据扩充这个数据集，改变用户指令和模型回答，根据问题适当扩充代码，但注意正确性，如果有网址保证网址的正确性，并请与上文回答有所区别，不要出现换行，使用换行符\\n代替：
                            '''+'{"instruction":"' + instruction_texts[i] + '","input":""' + input_texts[i] 
                            + ',"output":"' + output_texts[i] + '"}'},]
                }
            print("message:\n", data)
            printlog("message:\n", data)
            
            time.sleep(10) # 防止频繁请求，延迟10秒
            output = ''
            try:
                response = requests.post(url, headers=headers, json=data)
                output = response.json()['choices'][0]['message']['content'].strip()
            except Exception as e:
                print(e)
                printlog(e)
            print("\nresponse:\n", output)
            printlog("\nresponse:\n", output)
            with open(output_file_path, 'a', encoding='utf-8') as outfile:
                print(output, file=outfile)

def main(input_file_path, output_file_path, rk):
    with open(input_file_path, 'r', encoding='utf-8') as infile:
        dataset = json.load(infile)

    if(rk <= len(dataset)):
        generate_gpt_responses(input_file_path, output_file_path, rk)

    # 保存扩增后的数据集
    print(f"Data augmentation complete. The augmented dataset is saved to {output_file_path}")
    printlog(f"Data augmentation complete. The augmented dataset is saved to {output_file_path}")

if __name__ == "__main__":
    input_file_path = 'E:/ATCHATGROOP/ATMODEL/data/test.json'
    output_file_path = 'E:/ATCHATGROOP/ATMODEL/kcdata/OAPLUSLooptest.json'
    cmdstr = "python"
    rk = 1
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
