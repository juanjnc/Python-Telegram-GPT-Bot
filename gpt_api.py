from env import OPENAI_API_KEY, MODEL
from openai import OpenAI



client = OpenAI(api_key=OPENAI_API_KEY)


def request_chat_gpt(user_message):
    try:
        completion = client.chat.completions.create(
            model=MODEL, messages=[{"role": "user", "content": user_message}]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"\nOoops, something went wrong: \n\n{e}")
        return f"Ooops, something went wrong: \n\n\n{e}"
