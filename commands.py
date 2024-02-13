import traceback
from env import USERS, CHAR
import logging
import html
import json
from gpt_api import request_chat_gpt, request_dall_e
from telegram.constants import ChatAction, ParseMode
from telegram import Update
from telegram.ext import (
    ContextTypes,
)


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.WARNING
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.sendChatAction(
        chat_id=update.message.chat_id, action=ChatAction.TYPING, read_timeout=10
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hola, soy el mensajero entre ustéd, su estupidez y chatGPT.\n\n"
        "Simplemente escribe un mensaje y yo te daré la respuesta.\n\n"
        "Por el momento no se guarda contexto de la conversación, disculpe las molestias",
    )


async def img(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    id = user.id
    promp = update.message.text.replace("/img", "").replace("@YOUR_BOT_NAME", "")

    await context.bot.sendChatAction(
        chat_id=update.message.chat_id, action=ChatAction.UPLOAD_PHOTO, read_timeout=15
    )

    if id in USERS:
        response = request_dall_e(promp)
        await context.bot.sendChatAction(
            chat_id=update.message.chat_id, action=ChatAction.UPLOAD_PHOTO, read_timeout=10
        )

        try:
            await context.bot.send_photo(
                chat_id=update.effective_chat.id, photo=open(response, "rb")
            )

            await context.bot.send_document(
                chat_id=update.effective_chat.id, document=open(response, "rb")
            )

        except Exception:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=response,
            )

    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="No tienes permiso para usar este bot",
        )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    id = user.id

    await context.bot.sendChatAction(
        chat_id=update.message.chat_id, action=ChatAction.TYPING, read_timeout=15
    )

    if id in USERS:
        response = request_chat_gpt(update.message.text)
        await context.bot.sendChatAction(
            chat_id=update.message.chat_id, action=ChatAction.TYPING, read_timeout=10
        )
        if type(response) is str:
            char = CHAR
            for c in char:
                if c in response:
                    response: str = response.replace(c, "\\" + c)
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text=response, parse_mode="MarkdownV2"
            )

    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="No tienes permiso para usar este bot",
        )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a telegram message to notify the developer."""

    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list: list[str] = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb_string: str = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message: str = (
        f"An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )
    # Finally, send the message
    await context.bot.send_message(
        chat_id=update.message.chat_id, text=message, parse_mode=ParseMode.HTML
    )
