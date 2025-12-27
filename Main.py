import os
from pyrogram import Client
from dotenv import load_dotenv

load_dotenv()  # .env faylini yuklaydi

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")
GROUP_ID = int(os.getenv("GROUP_ID"))

app = Client("my_account", api_id=API_ID, api_hash=API_HASH, phone_number=PHONE_NUMBER)

@app.on_message()
async def check_voice_chat(client, message):
    chat = await client.get_chat(GROUP_ID)
    if hasattr(chat, "has_active_voice_chat") and chat.has_active_voice_chat:
        # PyTgCalls bilan join qilish logikasi shu yerda bo‘ladi
        print("Voice chat mavjud, join qilamiz!")

app.run()
