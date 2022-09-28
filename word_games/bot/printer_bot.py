import logging
import os
import re

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from .sp2400python import *
load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

port = 5
printer = sp2400python(f"/dev/ttyS{port}")
fonts = {
    "NLQ": printer.FONT_NLQ,
    "SANS SERIF": printer.FONT_SANS_SERIF,
    "COURIER": printer.FONT_COURIER,
    "PRESTIGE": printer.FONT_PRESTIGE,
    "SCRIPT": printer.FONT_SCRIPT,
    "GOTHIC": printer.FONT_GOTHIC
}

printer.sendCommand(printer.QUALITY_NLQ)
printer.setFont(fonts["SANS SERIF"])

logging.info(f"Setting port {port}")
        


builder = Application.builder()
builder.token(os.environ['TOKEN']).build()
application = builder.build()

def escape_markdown( text):
    """
    Helper function to escape telegram markup symbols
    """
    text = text.replace('“', '_').replace('”', '_')
    escape_chars = '\[()+-.!~>=|'
    return re.sub(r'([%s])' % escape_chars, r'\\\1', text)


async def start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

    mkd_start = """
    *Witaj w maszynie Orlowskiego* \n
    Wpisz komendę `/cmd` aby wydać rozporządzenie. \n
    W tym interfejsie otrzymasz wszystkie potrzebne komunikaty. \n
    """
    mkd_start = escape_markdown(mkd_start)
    await context.bot.send_message(chat_id=update.effective_chat.id,
    text=mkd_start, parse_mode='MarkdownV2')


async def cmd_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_says = " ".join(context.args)
    if not user_says:
        await update.message.reply_text(escape_markdown(r"Wpisz komendę: `/cmd Treść`"),
        parse_mode='MarkdownV2')
        return
    await update.message.reply_text("Wysłano polecenie: " + user_says)
    # todo drukarka i inne rzeczy
    printer.printLine(user_says)


application.add_handler(CommandHandler("start", start_callback))
application.add_handler(CommandHandler("cmd", cmd_callback))
