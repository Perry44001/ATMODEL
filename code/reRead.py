import re
import json

def extract_text_between_markers(file_path, output_file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        print('[', file=outfile)
    
    # 使用正则表达式找到#*%到@~*之间的文本
    pattern = re.compile(r'#\*%(.*?)@~\*', re.DOTALL)
    matches = pattern.findall(content)
    pattern2 = re.compile(r'{\'role\': \'assistant\', \'content\': \'(.*?)\\n\'}], \'temperature\': 0.8', re.DOTALL)
    matches2 = pattern2.findall(content)
    i = 0
    outjsons = []
    for match in matches:
        if match == '{"instruction":"[问题]","input":"[指令]","output":"[回答]"}' :
            if i==0: # 跳过第一个json
                continue
            else:
                outjsons.append(output_jsons)
                continue
        elif match == '和': # 不能跳过第一个json，所以这里要单独处理
            try:
                output_jsons = [json.loads(matches2[i])]
            except:
                temp_string = matches2[i]
                # Step 1: Replace existing \\n with a placeholder
                temp_string = temp_string.replace(',\\n"input":"",\\n"output"', ',\n"input":"",\n"output"')
                temp_string = temp_string.replace(',\n"input":"",\n"output"', 'INHOLDER')

                # Step 2: Replace \n with \\n
                # temp_string = temp_string.replace('\\', '\\\\')
                temp_string = temp_string.replace('\n', '\\n')

                # Step 3: Replace the placeholder back to \\n
                temp_string = temp_string.replace('INHOLDER', ',\n"input":"",\n"output"')
                temp_string = temp_string.replace('\xa0', '')

                output_jsons = [json.loads(temp_string)]
            i += 1
        else:
            try:
                outjson = json.loads(match)
                output_jsons.append(outjson)
            except:
                # Step 1: Replace existing \\n with a placeholder
                temp_string = match
                temp_string = re.sub(',\n"input":"",\n"output"', 'INHOLDER', temp_string)


                # Step 2: Replace \n with \\n
                temp_string = temp_string.replace('\\', '\\\\')
                temp_string = temp_string.replace('\n', '\\n')
                # temp_string = temp_string.replace("\'", "\\\\'")

                # Step 3: Replace the placeholder back to \\n
                temp_string = temp_string.replace('INHOLDER', ',\n"input":"",\n"output"')
                temp_string = temp_string.replace('\xa0', '')
                temp_string = temp_string.replace('\'', '`')
                match = temp_string
                try:
                    outjson = json.loads(match)
                    output_jsons.append(outjson)
                except:
                    print("json格式错误，请检查输入输出是否正确")
            #     print("json格式错误，请检查输入输出是否正确")
    
    outjsons.append(output_jsons)
    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        json.dump(outjsons, outfile, ensure_ascii=False, indent=4)

# 示例文件路径
file_path = 'E:\\ATCHATGROOP\\ATMODEL\\log\\output2024-07-24-01-59-10.log'
output_file_path = 'E:\\ATCHATGROOP\\ATMODEL\\kcdata\\OAPLUS_420240103-20240705.json'
# 提取文本
extracted_text = extract_text_between_markers(file_path, output_file_path)
if extracted_text:
    print("提取的文本:")
    print(extracted_text)
else:
    print("未找到匹配的文本")

