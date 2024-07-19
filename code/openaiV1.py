import requests

# url = "https://api.openai.com/v1/chat/completions"
url = "https://apikeyplus.com/v1/chat/completions"

headers = {
  'Content-Type': 'application/json',
  # 填写 OpenKEY 生成的令牌/KEY，注意前面的 Bearer 要保留，并且和 KEY 中间有一个空格。
  'Authorization': 'Bearer sk-kY0d4xy7dIz52GZY6bD1C6D9A380412398Cb924cCc14Af52'
}


data = {
    "model": "text-davinci-003",
    "messages": [
        {"role": "system", "content": "你是一个水声科学家。"},
        {"role": "user", "content": "请解释声学多普勒流速剖面仪的工作原理。"}
    ],
    "temperature": 0.7,
    "max_tokens": 150,
    "top_p": 1.0,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0
}


data = {
  "model": "gpt-4o",
  "messages": [
        {"role": "user", "content": "我想让你担任水声科学家。我会写一些水声的问答，你的工作就是根据以上问题用通俗易懂的话语扩充几条问答数据用于大模型微调数据集，将复杂的问答用简单短小的问答代替，使用'##{\"instruction\":\"[问题]\",\"input\":\"[指令]\",\"output\":\"[回答]\"}@@'的格式，如果问答中给出教程链接，请保持网址链接文本不变，并在扩充的问答数据适当位置给出。"},
        {"role": "assistant", "content": '''{
      "instruction": "我想进行接收信号仿真，比如发射信号经过搭建的水声信道得到不同位置的接收信号",
      "input": "",
      "output": "进行接收信号分析涉及到水声信道的建模和接收信号的处理。以下是一般的步骤：\n\n水声信道建模：\n水声信道受水域环境（海水声速、海底地形、底质等）、声源、接收深度、声源频率等因素的影响，导致信号在传播过程中发生衰减、多径效应等。\n选择适当的水声信道模型，例如BELLHOP（射线追踪模型），以计算水声信道多径效应（到达结构：主要包括到达的幅度、时延、相位等信息）。\n如果您要得到不同位置处的接收信号仿真，可以改变env文件中的Sz（声源深度）、Rr（接收距离）和Rz（接收深度）参数计算得到不同收发位置的到达结构。\n信号发射：\n\n设计信号源：选择合适的信号源，如CW、LFM、HFM等。\n发射信号：确定信号的特性（频率、幅度、调制方式等）。\n将发射信号和水声信道计算的多径效应结合，使用时域卷积、频域相乘或者时延法得到不同位置的接收信号。\n具体公式如下 y(t) = x(t) * h(t)，其中 y(t) 为接收信号，x(t) 为发射信号，h(t) 为水声信道的冲激响应，*为卷积符号。\n视频链接【11时延法实现到达结构输出信号】 https://www.bilibili.com/video/BV1DK41147eE/?share_source=copy_web&vd_source=da3bd6e68ced42ab3b6a4778db8cb6d2。\n\n加入环境噪声：对卷积后得到的信号加入高斯白噪声或者海洋有色噪声，视频链接：【06 如何给水声信号添加不同信噪比的噪声】 https://www.bilibili.com/video/BV1ub4y1g7aD/?share_source=copy_web&vd_source=da3bd6e68ced42ab3b6a4778db8cb6d2"
    }
'''}],
    "temperature": 0.8,
    "max_tokens": 2000,
    "top_p": 0.5,
    "frequency_penalty": 0.6,
    "presence_penalty": 0.2
}

response = requests.post(url, headers=headers, json=data)

print("Status Code", response.status_code)
print("JSON Response ", response.json())
