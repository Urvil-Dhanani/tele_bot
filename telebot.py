from aiogram import Bot, Dispatcher, executor, types   # refer aiogram official Document
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
import logging

load_dotenv()

# loading the API 
TELE_API=os.getenv("TELETOKEN")
GROQ_API=os.getenv("GROQ_API_KEY")

# Initializing the BOT
bot=Bot(token=TELE_API)
dispatcher=Dispatcher(bot=bot)

# # To remember the past conversation
# class Reference:
#     def __init__(self) -> None:
#         self.response=""

# reference=Reference()

# # clearing the past
# def clear_past():
#     reference.response=""

# lets define the command handler
# /start command
@dispatcher.message_handler(commands=['start'])
async def welcome(cmd:types.Message):
    """A handler to welcome and assist

    Args:
        cmd (types.Message): /start
    """
    await cmd.answer(text="Hi I am a Chat Bot\nCreated by: Urvil Dhanani\nWrite /help for the help menu\nHow can I assist you?")

# /help command
@dispatcher.message_handler(commands=['help'])
async def helper(cmd:types.Message):
    """This handler will show the other commands 

    Args:
        cmd (types.Message): /help
    """
    help_command = """
    Hi There, I'm a bot created by Urvil.
    Please follow these commands:

    /start - to start the conversation
    /clear - to clear the past conversation and context.
    /help - to get this help menu.    
    """
    await cmd.answer(text=help_command)

# /clear command
@dispatcher.message_handler(commands=['clear'])
async def clear_memory(cmd:types.Message):
    """This handler will clear the past memory

    Args:
        cmd (types.Message): /clear
    """
    
    await cmd.answer("Past conversation and context are cleared !!!")


# Session History 
memory_store={}
def fatch_session_history(session_id:str)->BaseChatMessageHistory:
    if session_id not in memory_store:
        memory_store[session_id]=ChatMessageHistory()
    return memory_store[session_id]






# users input
@dispatcher.message_handler()
async def chat_bot(message:types.Message):
    """This handler will process the user input and generate a response using LLModel: llama3-8b-8192

    Args:
        message (types.Message): user input
    """
    

    llm=ChatGroq(model="llama3-8b-8192",
                 groq_api_key=GROQ_API,
                 temperature=0.7,
                 max_tokens=100)
    
    parser=StrOutputParser()
    
    llm_with_history=RunnableWithMessageHistory(runnable=llm,
                                                get_session_history=fatch_session_history)
    response=llm_with_history.invoke(input=message.text,
                                     config={"configurable":{"session_id":"my_chat"}})
    await message.answer(response.content)




if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dispatcher=dispatcher,
                           skip_updates=True)