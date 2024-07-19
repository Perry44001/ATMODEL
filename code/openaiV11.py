import openai

# openai.api_base = "https://api.openai.com/v1" # 换成代理，一定要加 v1
openai.api_base = "https://apikeyplus.com/v1" # 换成代理，一定要加 v1
# openai.api_key = "API_KEY"
openai.api_key = "sk-kY0d4xy7dIz52GZY6bD1C6D9A380412398Cb924cCc14Af52"

for resp in openai.ChatCompletion.create(
                                    model="gpt-3.5-turbo",
                                    messages=[
                                      {"role": "user", "content": "证明费马大定理"}
                                    ],
                                    # 流式输出
                                    stream = True):
    if 'content' in resp.choices[0].delta:
        print(resp.choices[0].delta.content, end="", flush=True)
