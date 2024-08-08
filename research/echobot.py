from aiogram import Bot, Dispatcher, executor, types   # refer aiogram official Document
from dotenv import load_dotenv
import os
import logging

load_dotenv()

# loading the API 
TELE_API=os.getenv("TELETOKEN")

# logging the info
logging.basicConfig(level=logging.INFO)

# Initializing the BOT --> It also needs Dispatcher
bot=Bot(token=TELE_API)
dp=Dispatcher(bot=bot)

# Lets make our bot understand the command --> /help, /start likewise
# refer aiogram document
@dp.message_handler(commands=['start', 'help'])
async def command_handler(cmdmsg:types.Message):
    """This function takes the "/start" or "/help" command and reply on that command

    Args:
        command (types.Message): /help or /start
    """
    await cmdmsg.reply("Hi I am a BOT\nPowered by: AIOgram\nCreated by: Urvil Dhanani")

# lets create an EchoBot
@dp.message_handler()
async def echo(msg:types.Message):
    """This function will reply the same message entered by user 

    Args:
        msg (types.Message): Any message
    """
    await msg.answer(msg.text)


if __name__ == "__main__":
    executor.start_polling(dispatcher=dp,
                           skip_updates=True)  # executor will execute the BOT with above function 




