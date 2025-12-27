import asyncio
import os
from dotenv import load_dotenv
from loguru import logger
from pyrogram import Client, filters
from pytgcalls import PyTgCalls

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

logger.add("bot.log", rotation="5 MB")

# User states
users = {}

app = Client(
    "config_bot",
    bot_token=BOT_TOKEN
)

voice_clients = {}

@app.on_message(filters.command("start") & filters.private)
async def start(_, message):
    users[message.from_user.id] = {"step": 1}
    await message.reply(
        "🔧 Sozlashni boshlaymiz.\n\n"
        "1️⃣ API_ID ni yuboring"
    )

@app.on_message(filters.private & ~filters.command("start"))
async def wizard(_, message):
    uid = message.from_user.id
    if uid not in users:
        return

    step = users[uid]["step"]

    try:
        if step == 1:
            users[uid]["api_id"] = int(message.text)
            users[uid]["step"] = 2
            await message.reply("2️⃣ API_HASH ni yuboring")

        elif step == 2:
            users[uid]["api_hash"] = message.text.strip()
            users[uid]["step"] = 3
            await message.reply("3️⃣ GROUP_ID ni yuboring")

        elif step == 3:
            users[uid]["group_id"] = int(message.text)
            await message.reply("✅ Saqlandi. Voice watcher ishga tushyapti...")
            users[uid]["step"] = 4
            await start_voice(uid)

    except Exception as e:
        logger.error(e)
        await message.reply("❌ Noto‘g‘ri qiymat. Qaytadan urin.")

async def start_voice(uid):
    cfg = users[uid]

    client = Client(
        f"user_{uid}",
        api_id=cfg["api_id"],
        api_hash=cfg["api_hash"]
    )

    vc = PyTgCalls(client)
    voice_clients[uid] = vc

    @client.on_message(filters.chat(cfg["group_id"]))
    async def watcher(_, __):
        chat = await client.get_chat(cfg["group_id"])
        if chat.has_active_voice_chat:
            logger.info(f"🎙 Voice chat topildi: {cfg['group_id']}")
            # bu yerda join_group_call bo‘ladi (audio bilan)

    await client.start()
    await vc.start()

    logger.info(f"Voice watcher ishga tushdi: user={uid}")

if __name__ == "__main__":
    app.run()
