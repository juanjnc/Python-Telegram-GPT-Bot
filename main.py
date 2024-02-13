import commands
from env import TELEGRAM_API_TOKEN
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
)



def main():
    application = ApplicationBuilder().token(TELEGRAM_API_TOKEN).build()

    start_handler = CommandHandler("start", commands.start)
    img_handler = CommandHandler("img", commands.img)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), commands.echo)
    application.add_handler(start_handler)
    application.add_handler(img_handler)
    application.add_handler(echo_handler)
    application.add_error_handler(commands.error_handler)
    application.run_polling()


if __name__ == "__main__":
    print("GPT-BOT is alive")
    main()
