from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage
import json
import re
import sys

#星火认知大模型Spark Max的URL值，其他版本大模型URL值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_URL = 'wss://spark-api.xf-yun.com/v3.5/chat'
#星火认知大模型调用秘钥信息，请前往讯飞开放平台控制台（https://console.xfyun.cn/services/bm35）查看
SPARKAI_APP_ID = 'f6b98b6f'
SPARKAI_API_SECRET = 'NmRhYzU5MjRhYzM4ODgyOGNmYzU5Zjlh'
SPARKAI_API_KEY = 'd20cd4922bf62a209ee3a5cc221b147c'
#星火认知大模型Spark Max的domain值，其他版本大模型domain值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_DOMAIN = 'generalv3.5'

spark = ChatSparkLLM(
    spark_api_url=SPARKAI_URL,
    spark_app_id=SPARKAI_APP_ID,
    spark_api_key=SPARKAI_API_KEY,
    spark_api_secret=SPARKAI_API_SECRET,
    spark_llm_domain=SPARKAI_DOMAIN,
    streaming=False,
)

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

            # 构造一条消息，包含原始的指令、输入、输出，以及提示扩充数据的提示
            # 注意：这里的提示内容请根据实际情况修改，比如："请根据上面的问答扩充问答10条数据，使用'{\"instruction\":\"[问题]\",\"input\":\"[指令]\",\"output\":\"[回答]\"}'的json格式" 
            jj = i + 1
            messages = [ChatMessage(
                role="user",
                content='instruction:' + instruction_texts[i] + '\ninput:' + input_texts[i] 
                + '\noutput:' + output_texts[i] + "\n请根据上面的问答扩充问答10条数据，使用'{\"instruction\":\"[问题]\",\"input\":\"[指令]\",\"output\":\"[回答]\"}'的格式"
                )]
            print("message:\n[{}]".format(messages[0].content.strip()))
            handler = ChunkPrintHandler()
            response = spark.generate([messages], callbacks=[handler])
            output = response.generations[0][0].text.strip() # 大模型输出文本

            print("\nresponse:\n", output)
            # 防止json中间缺少逗号导致的格式错误，使用通配符读取数据
            # pattern = r'\{"instruction":"([^}]*)\"\}'
            pattern = r'\{"instruction":"(.*?)"\}'
            matches = re.findall(pattern, output)
            # 我们将每个扩充后的结果放在一个list
            output_jsons = []
            for match in matches:
                jsonstr = '{"instruction":"'+match+'"}'
                try:
                    outjson = json.loads(jsonstr)
                    output_jsons.append(outjson)
                except:
                    print("json格式错误，请检查输入输出是否正确")
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
        return jj + 1

def main(input_file_path, output_file_path, rk):
    with open(input_file_path, 'r', encoding='utf-8') as infile:
        dataset = json.load(infile)
    k = rk
    while(k <= len(dataset)): # 循环调用generate_gpt_responses函数，直到处理完所有输入输出对
        k = generate_gpt_responses(input_file_path, output_file_path, k)

    # 保存扩增后的数据集
    print(f"Data augmentation complete. The augmented dataset is saved to {output_file_path}")

if __name__ == "__main__":
    input_file_path = 'E:/ATCHATGROOP/ATMODEL/data/test.json'
    output_file_path = 'E:/ATCHATGROOP/ATMODEL/kcdata/testKC.json'
    rk = 1
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

