# from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
# from sparkai.core.messages import ChatMessage
import json
import os
import re

# 读取已有的数据集
input_file_path = 'E:/ATCHATGROOP/ATMODEL/data/test.json'
output_file_path = 'E:/ATCHATGROOP/ATMODEL/kcdata/testKC.json'

#星火认知大模型Spark Max的URL值，其他版本大模型URL值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_URL = 'wss://spark-api.xf-yun.com/v3.5/chat'
#星火认知大模型调用秘钥信息，请前往讯飞开放平台控制台（https://console.xfyun.cn/services/bm35）查看
SPARKAI_APP_ID = 'f6b98b6f'
SPARKAI_API_SECRET = 'NmRhYzU5MjRhYzM4ODgyOGNmYzU5Zjlh'
SPARKAI_API_KEY = 'd20cd4922bf62a209ee3a5cc221b147c'
#星火认知大模型Spark Max的domain值，其他版本大模型domain值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_DOMAIN = 'generalv3.5'

# spark = ChatSparkLLM(
#     spark_api_url=SPARKAI_URL,
#     spark_app_id=SPARKAI_APP_ID,
#     spark_api_key=SPARKAI_API_KEY,
#     spark_api_secret=SPARKAI_API_SECRET,
#     spark_llm_domain=SPARKAI_DOMAIN,
#     streaming=False,
# )

with open(input_file_path, 'r', encoding='utf-8') as infile:
    dataset = json.load(infile)

# 批量调用GPT模型生成新数据
def generate_gpt_responses(instruction_texts, input_texts, output_texts):
    responses = []
    for i in range(0, len(input_texts)):
        # messages = [ChatMessage(
        #     role="user",
        #     content='instruction:' + instruction_texts[i] + '\ninput:' + input_texts[i] 
        #     + '\noutput:' + output_texts[i] + "请根据上面的问答扩充问答2条数据，使用'{\"instruction\":\"[问题]\",\"input\":\"[指令]\",\"output\":\"[回答]\"}'的json格式，json之间用','逗号间隔"
        #     )]
        # print("\n\nmessage: ", messages)
        # # handler = ChunkPrintHandler()
        # response = spark.generate([messages], callbacks=[handler])

        # if i != len(input_texts) -1: # 最后一组json不需要逗号结尾
        #     output = response.generations[0][0].text.strip() + ','
        # else:
        #     output = response.generations[0][0].text.strip()
        output = '{"instruction":"水下浮标有哪些种类？","input":"指令","output":"水下浮标有多种类型，包括固定式、漂流式和自动回航式等。固定式水下浮标通常被放置在特定位置，用于长期监测；漂流式水下浮标则随着水流漂移，可 以覆盖更广的区域；自动回航式水下浮标可以在完成任务后自动返回到起始位置。"}\n\n{"instruction":"水下浮标如何保护海洋生物？","input":"指令","output":"水下浮标在设计和操作过程中应尽量减少对海洋生物的干扰。例如，使用低噪音设备，避免使用有害化学物质，以及合理设置采样频率和深度等。此外，定 期检查和维护设备，确保其正常运行，减少故障和损坏的可能性。通过这些措施，水下浮标可以在收集数据的同时，最大限度地减少对海洋生态系统的影响。"}'
        pattern = r'\{([^}]*)\}'
        matches = re.findall(pattern, output)
        for match in matches:
            jsonstr = '{'+match+'}'
            outjson = json.loads(jsonstr)
            responses.append(outjson)

        # print("matches", matches)
        # print("\nresponse: ", response.generations[0][0].text.strip())
        # responses.append(output)
        # outputs = json.loads(response.generations[0][0].text.strip()) # 我希望格式化的输出
        # output_instruction_texts[i] = outputs['instruction']
        # output_input_texts[i] = outputs['input']
    return responses

# 准备输入文本
instruction_texts = [item['instruction'] for item in dataset]
input_texts = [item['input'] for item in dataset]
output_texts = [item['output'] for item in dataset]


# 生成新的输出
new_outputs = generate_gpt_responses(instruction_texts, input_texts, output_texts)

# 将新输出添加到数据集中
# new_outputs = ['{"instruction":"水下浮标有哪些种类？","input":"指令","output":"水下浮标有多种类型，包括固定式、漂流式和自动回航式等。固定式水下浮标通常被放置在特定位置，用于长期监测；漂流式水下浮标则随着水流漂移，可 以覆盖更广的区域；自动回航式水下浮标可以在完成任务后自动返回到起始位置。"}','{"instruction":"水下浮标如何保护海洋生物？","input":"指令","output":"水下浮标在设计和操作过程中应尽量减少对海洋生物的干扰。例如，使用低噪音设备，避免使用有害化学物质，以及合理设置采样频率和深度等。此外，定 期检查和维护设备，确保其正常运行，减少故障和损坏的可能性。通过这些措施，水下浮标可以在收集数据的同时，最大限度地减少对海洋生态系统的影响。"}']
# for json_str in new_outputs:
#     outputs_json = json.loads(json_str)
#     output_instruction_texts = [item['instruction'] for item in dataset]
#     output_input_texts = [item['input'] for item in dataset]
#     output_output_texts = [item['output'] for item in dataset]

# 保存扩增后的数据集
with open(output_file_path, 'w', encoding='utf-8') as outfile:
    json.dump(new_outputs, outfile, ensure_ascii=False, indent=4)

print(f"Data augmentation complete. The augmented dataset is saved to {output_file_path}")

# #星火认知大模型Spark Max的URL值，其他版本大模型URL值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
# SPARKAI_URL = 'wss://spark-api.xf-yun.com/v3.5/chat'
# #星火认知大模型调用秘钥信息，请前往讯飞开放平台控制台（https://console.xfyun.cn/services/bm35）查看
# SPARKAI_APP_ID = 'f6b98b6f'
# SPARKAI_API_SECRET = 'NmRhYzU5MjRhYzM4ODgyOGNmYzU5Zjlh'
# SPARKAI_API_KEY = 'd20cd4922bf62a209ee3a5cc221b147c'
# #星火认知大模型Spark Max的domain值，其他版本大模型domain值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
# SPARKAI_DOMAIN = 'generalv3.5'

# def call_with_messages():
#     spark = ChatSparkLLM(
#         spark_api_url=SPARKAI_URL,
#         spark_app_id=SPARKAI_APP_ID,
#         spark_api_key=SPARKAI_API_KEY,
#         spark_api_secret=SPARKAI_API_SECRET,
#         spark_llm_domain=SPARKAI_DOMAIN,
#         streaming=False,
#     )
#     messages = [ChatMessage(
#         role="user",
#         content='你好呀'
#     )]
#     handler = ChunkPrintHandler()
#     a = spark.generate([messages], callbacks=[handler])
#     print(a)

