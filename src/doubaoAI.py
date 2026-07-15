import os
from openai import OpenAI
# import asyncio

# 请确保您已将 API Key 存储在环境变量 ARK_API_KEY 中
# 初始化Ark客户端，从环境变量中读取您的API Key
client = OpenAI( 
    # 此为默认路径，您可根据业务所在地域进行配置
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    # 从环境变量中获取您的 API Key。此为默认方式，您可根据需要进行修改
    api_key = "" #<<<<在这里填写上你的API key
)
#!!--这里是AI查询的主要代码，修改这里的代码就可以接入其他的AI提供商了--!!#
#请接入一个支持视觉的模型
def aiAsk(img_base64:str,question:str="解答图中的问题"): 
    response = client.chat.completions.create(
        # 指定您创建的方舟推理接入点 ID，此处已帮您修改为您的推理接入点 ID
        model="doubao-1.5-vision-pro-250328",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": img_base64 #豆包使用带有特征头部的base64编码jpg/png图片
                        },
                    },
                    {"type": "text", "text": question},
                ],
            }
        ],
    )
    print(response.choices[0].message.content)
    return(response.choices[0].message.content)