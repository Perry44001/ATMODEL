import re

def extract_bracket_contents(text):
    pattern = r'\{([^}]*)\}'
    matches = re.findall(pattern, text)
    return matches

text = "这是一个示例字符串，其中包含一些花括号：{内容1}，还有另一个：{内容2}"
result = extract_bracket_contents(text)
print(result)
