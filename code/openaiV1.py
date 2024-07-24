import requests

# url = "https://api.openai.com/v1/chat/completions"
url = "https://apikeyplus.com/v1/chat/completions"

headers = {
  'Content-Type': 'application/json',
  # 填写 OpenKEY 生成的令牌/KEY，注意前面的 Bearer 要保留，并且和 KEY 中间有一个空格。
  'Authorization': 'Bearer sk-kY0d4xy7dIz52GZY6bD1C6D9A380412398Cb924cCc14Af52'
}


data = {
  "model": "gpt-4o",
  "messages": [
                                      {"role": "user", "content": "扮演一个水声科学家，以通俗易懂的方式回答水声科学相关问题。我会写一些水声的问答，你的工作就是根据以上问题用通俗易懂的话语扩充若干条问答数据用于大模型微调数据集，将复杂的问答用简单短小的问答代替，问题扩展原则：1.针对一个说明性的问题进行详细全面的回答，从不同方面加以解释和补充。2.确保扩展出的问题与原有背景密切相关，避免脱离语境或显得突兀。3.对每个扩展的问题都提供足够的信息，使其成为一个完整、有价值且容易理解的小问答。4.如果问答中给出教程链接，请保持网址链接文本不变，并在扩充的问答数据适当位置给出。5.使用'##{\"instruction\":\"[问题]\",\"input\":\"[指令]\",\"output\":\"[回答]\"}@@'的json格式，已方便我使用json.loads进行解析。"},
        {"role": "assistant", "content": '''{
        "instruction": "什么是水下浮标",
        "input": "",
        "output": "水下浮标是种用于海洋环境中的设备，用于测量和监测海洋参数和环境。它可以在海水中浮动，并通过传感器和仪器收集数据，例如海洋温度、盐度、压力等。水下浮标通常由浮体、传感器、电子设备和通信系统组成，可以通过无线或有线方式将数据传输到地面站或其他接收设备。水下浮标在海洋科学研究、海洋观测和气候变化研究中起着重要的作用。"
    }
    }
'''}
                                    ],
    "temperature": 0.8,
    "max_tokens": 2000,
    "top_p": 0.5,
    "frequency_penalty": 0.6,
    "presence_penalty": 0.2
}

response = requests.post(url, headers=headers, json=data)

print("Status Code", response.status_code)
print("JSON Response ", response.json())
