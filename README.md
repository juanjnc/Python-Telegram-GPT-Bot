# Python telegram bot with GPT and Dall-E
This is a basic bot using python-telegram-bot, dotenv and openai modules for Python.

Simply type a message and the bot will reply back to you.
Currently the bot is unable to manage the context of the conversation.

For a image generated with Dall-E install PILLOW and use the /img command before writing the prompt (looks like ```/img a black cat```)

## Installation

1. Install the dependencies:
```sh
pip install python-telegram-bot python-dotenv openai pillow
```

2. Update the ".env" file with your data:
```sh
TELEGRAM_API_TOKEN = "YOUR_TOKEN"
OPENAI_API_KEY = "YOUR_TOKEN"
#Telegram ID is used as a white list
USERS = '[TELEGRAM_ID_1,TELEGRAM_ID_2,TELEGRAM_ID_3,TELEGRAM_ID_4,]'
MODEL_GPT = "TARGET_MODEL"
MODEL_DALL_E = "dall-e-3"
```
3. In the img() function in commands.py replace @YOUR_BOT_NAME with the @ of your bot

You can get your TELEGRAM_API_TOKEN following this guide:
https://core.telegram.org/bots/features#botfather

You can get your OPENAI_API_KEY following this guide:
https://platform.openai.com/api-keys

You can get the MODEL name following this guide:
https://platform.openai.com/docs/models

There are many ways to get your user_id and many bots that manage it.

If you don't want to use the IDs just change the echo() function to this one, do the same changes in the img() function for DALL-E:
```python
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.sendChatAction(
        chat_id=update.message.chat_id, action=ChatAction.TYPING, read_timeout=15
        )
    response = request_chat_gpt(update.message.text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)
```

## License

MIT
