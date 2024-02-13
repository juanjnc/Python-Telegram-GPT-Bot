from env import OPENAI_API_KEY, MODEL_GPT, MODEL_DALL_E
from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO
import pathlib


client = OpenAI(api_key=OPENAI_API_KEY)


def request_chat_gpt(user_message):
    """
    Supports any model of ChatGPT
    """
    try:
        completion = client.chat.completions.create(
            model=MODEL_GPT, messages=[{"role": "user", "content": user_message}]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"\nOoops, something went wrong: \n\n{e}")
        return f"Ooops, something went wrong: \n\n\n{e}"


def request_dall_e(user_message):
    """
    Supports aonly Dall-E 3
    """
    try:
        response = client.images.generate(
            model=MODEL_DALL_E,
            prompt=user_message,
            size="1024x1024",
            quality="hd",
            n=1,
        )
        data: str | None = response.data[0].url

        res = requests.get(data)
        img = Image.open(BytesIO(res.content))
        img.save("return.png")
        fp = "./return.png"
        return fp

    except Exception as e:
        print(f"\nOoops, something went wrong: \n\n{e}")
        return f"Ooops, something went wrong: \n\n\n{e}"
