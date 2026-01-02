import json
import os
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    ChatMemberUpdated,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
    ChatMemberHandler,
)

# ================= CONFIG =================
BOT_TOKEN = "8161458476:AAH76ALCfc-zWa3Lwh8nitkjw82i8QJYat8"

OWNER_LINK = "https://t.me/iugrp"
DEV_LINK = "https://t.me/Frx_shooter"
SUPPORT_LINK = "https://t.me/hiestarboy"
CHANNEL_LINK = "https://t.me/all_state_gc"

DATA_FILE = "data.json"

# ================= STORAGE =================
def load():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_user(data, uid):
    return data.setdefault(uid, {
        "submitted": False,
        "identity": {
            "name": "N/A",
            "age": "N/A",
            "location": "N/A",
            "gender": "N/A",
            "relationship": "N/A",
            "song": "N/A",
            "actor": "N/A",
            "hobby": "N/A",
            "bio": "N/A",
        },
        "groups": {}
    })

# ================= ADMIN CHECK =================
async def is_group_admin(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> bool:
    member = await ctx.bot.get_chat_member(
        update.effective_chat.id,
        update.effective_user.id
    )
    return member.status in ("administrator", "creator")

# ================= INLINE KEYBOARDS =================
def welcome_inline():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("👑 𝗢𝘄𝗻𝗲𝗿", url=OWNER_LINK),
            InlineKeyboardButton("🧠 𝗗𝗲𝘃𝗲𝗹𝗼𝗽𝗲𝗿", url=DEV_LINK),
        ],
        [
            InlineKeyboardButton("💬 𝗦𝘂𝗽𝗽𝗼𝗿𝘁", url=SUPPORT_LINK),
            InlineKeyboardButton("📢 𝗢𝗳𝗳𝗶𝗰𝗶𝗮𝗹 𝗖𝗵𝗮𝗻𝗻𝗲𝗹", url=CHANNEL_LINK),
        ],
        [
            InlineKeyboardButton("❓ 𝗛𝗲𝗹𝗽", callback_data="help"),
        ],
    ])

def help_inline():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ 𝗕𝗮𝗰𝗸", callback_data="back")]
    ])

# ================= REPLY KEYBOARDS =================
KB_SET = ReplyKeyboardMarkup([["✨ 𝗦𝗲𝘁 𝗜𝗱𝗲𝗻𝘁𝗶𝘁𝘆"]], resize_keyboard=True)
KB_EDIT = ReplyKeyboardMarkup([["✏️ 𝗘𝗱𝗶𝘁 𝗜𝗱𝗲𝗻𝘁𝗶𝘁𝘆"]], resize_keyboard=True)
KB_GENDER = ReplyKeyboardMarkup([["𝗠𝗮𝗹𝗲 💁‍♂️", "𝗙𝗲𝗺𝗮𝗹𝗲 💁‍♀️"]], resize_keyboard=True)
KB_REL = ReplyKeyboardMarkup([["𝗦𝗶𝗻𝗴𝗹𝗲 🖤", "𝗠𝗶𝗻𝗴𝗹𝗲 ♥️"]], resize_keyboard=True)
KB_SKIP_CANCEL = ReplyKeyboardMarkup([["𝗦𝗸𝗶𝗽", "𝗖𝗮𝗻𝗰𝗲𝗹"]], resize_keyboard=True)

# ================= START =================
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != "private":
        return

    text = (
        f"✨ 𝗪𝗲𝗹𝗰𝗼𝗺𝗲, {update.effective_user.first_name}! ✨\n\n"
        "𝗧𝗵𝗶𝘀 𝗶𝘀 𝘆𝗼𝘂𝗿 𝗽𝗲𝗿𝘀𝗼𝗻𝗮𝗹 𝘀𝗽𝗮𝗰𝗲 𝘁𝗼 𝘀𝗵𝗮𝗽𝗲 𝘆𝗼𝘂𝗿 𝗶𝗱𝗲𝗻𝘁𝗶𝘁𝘆 𝘆𝗼𝘂𝗿 𝘄𝗮𝘆.\n\n"
        "𝗦𝗵𝗮𝗿𝗲 𝗼𝗻𝗹𝘆 𝘄𝗵𝗮𝘁 𝗳𝗲𝗲𝗹𝘀 𝗿𝗶𝗴𝗵𝘁 — 𝗲𝘃𝗲𝗿𝘆𝘁𝗵𝗶𝗻𝗴 𝘀𝘁𝗮𝘆𝘀 𝗶𝗻 𝘆𝗼𝘂𝗿 𝗰𝗼𝗻𝘁𝗿𝗼𝗹.\n\n"
        "𝗟𝗲𝘁’𝘀 𝗴𝗲𝘁 𝘀𝘁𝗮𝗿𝘁𝗲𝗱 👇"
    )

    await update.message.reply_text(text, reply_markup=welcome_inline())
    await update.message.reply_text(
        "𝗧𝗮𝗽 𝗯𝗲𝗹𝗼𝘄 𝘁𝗼 𝗯𝗲𝗴𝗶𝗻:",
        reply_markup=KB_SET
    )

# ================= HELP / BACK =================
async def help_cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    if q.data == "help":
        await q.edit_message_text(
            "🤖 𝗜𝗡𝗧𝗥𝗢 𝗕𝗢𝗧 — 𝗛𝗘𝗟𝗣\n\n"
            "• 𝗜𝗱𝗲𝗻𝘁𝗶𝘁𝘆 𝘀𝗲𝘁𝘂𝗽 𝗼𝗻𝗹𝘆 𝘄𝗼𝗿𝗸𝘀 𝗶𝗻 𝗽𝗿𝗶𝘃𝗮𝘁𝗲 𝗰𝗵𝗮𝘁 (𝗗𝗠)\n"
            "• 𝗨𝘀𝗲 /intro 𝗶𝗻 𝗴𝗿𝗼𝘂𝗽𝘀 𝘁𝗼 𝘃𝗶𝗲𝘄 𝗽𝗿𝗼𝗳𝗶𝗹𝗲𝘀\n"
            "• 𝗣𝗿𝗼𝗳𝗶𝗹𝗲 𝗽𝗵𝗼𝘁𝗼 𝗶𝘀 𝗳𝗲𝘁𝗰𝗵𝗲𝗱 𝗳𝗿𝗼𝗺 𝘂𝘀𝗲𝗿’𝘀 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺 𝗗𝗣\n"
            "• 𝗣𝗿𝗼𝗳𝗶𝗹𝗲 𝗰𝗼𝗺𝗺𝗮𝗻𝗱𝘀 𝗮𝗿𝗲 𝗿𝗲𝘀𝘁𝗿𝗶𝗰𝘁𝗲𝗱 𝘁𝗼 𝗴𝗿𝗼𝘂𝗽 𝗮𝗱𝗺𝗶𝗻𝘀\n"
            "• 𝗦𝗸𝗶𝗽𝗽𝗲𝗱 𝗳𝗶𝗲𝗹𝗱𝘀 𝗮𝗽𝗽𝗲𝗮𝗿 𝗮𝘀 𝗡/𝗔",
            reply_markup=help_inline()
        )
    elif q.data == "back":
        await q.edit_message_text(
            f"✨ 𝗪𝗲𝗹𝗰𝗼𝗺𝗲, {q.from_user.first_name}! ✨\n\n"
            "𝗧𝗵𝗶𝘀 𝗶𝘀 𝘆𝗼𝘂𝗿 𝗽𝗲𝗿𝘀𝗼𝗻𝗮𝗹 𝘀𝗽𝗮𝗰𝗲 𝘁𝗼 𝘀𝗵𝗮𝗽𝗲 𝘆𝗼𝘂𝗿 𝗶𝗱𝗲𝗻𝘁𝗶𝘁𝘆 𝘆𝗼𝘂𝗿 𝘄𝗮𝘆.\n\n"
            "𝗦𝗵𝗮𝗿𝗲 𝗼𝗻𝗹𝘆 𝘄𝗵𝗮𝘁 𝗳𝗲𝗲𝗹𝘀 𝗿𝗶𝗴𝗵𝘁 — 𝗲𝘃𝗲𝗿𝘆𝘁𝗵𝗶𝗻𝗴 𝘀𝘁𝗮𝘆𝘀 𝗶𝗻 𝘆𝗼𝘂𝗿 𝗰𝗼𝗻𝘁𝗿𝗼𝗹.\n\n"
            "𝗟𝗲𝘁’𝘀 𝗴𝗲𝘁 𝘀𝘁𝗮𝗿𝘁𝗲𝗱 👇",
            reply_markup=welcome_inline()
        )

# ================= IDENTITY (DM) =================
async def text_dm(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != "private":
        return

    msg = update.message.text.strip()
    data = load()
    uid = str(update.effective_user.id)
    user = get_user(data, uid)

    # ✅ FIRST: allow Set / Edit Identity (reset submitted)
    if msg in ["✨ 𝗦𝗲𝘁 𝗜𝗱𝗲𝗻𝘁𝗶𝘁𝘆", "✏️ 𝗘𝗱𝗶𝘁 𝗜𝗱𝗲𝗻𝘁𝗶𝘁𝘆"]:
        ctx.user_data.clear()
        user["submitted"] = False
        user["identity"] = {k: "N/A" for k in user["identity"]}
        ctx.user_data["step"] = "name"
        save(data)
        await update.message.reply_text(
            "👤 𝗘𝗻𝘁𝗲𝗿 𝗡𝗮𝗺𝗲:",
            reply_markup=ReplyKeyboardRemove()
        )
        return

    # 🔒 AUTO DELETE AFTER SUBMIT (ONLY WHEN NOT EDITING)
    if user.get("submitted"):
        try:
            await update.message.delete()
        except:
            pass
        return

    if msg == "𝗖𝗮𝗻𝗰𝗲𝗹":
        ctx.user_data.clear()
        await update.message.reply_text(
            "𝗜𝗱𝗲𝗻𝘁𝗶𝘁𝘆 𝘀𝗲𝘁𝘂𝗽 𝗰𝗮𝗻𝗰𝗲𝗹𝗹𝗲𝗱.",
            reply_markup=KB_SET
        )
        return

    step = ctx.user_data.get("step")
    if not step:
        return

    def val(x):
        return "N/A" if x.lower() == "skip" else x

    if step == "name":
        user["identity"]["name"] = val(msg)
        ctx.user_data["step"] = "age"
        await update.message.reply_text(
            "🎂 𝗘𝗻𝘁𝗲𝗿 𝗔𝗴𝗲 (𝟭𝟬–𝟱𝟬):"
        )

    elif step == "age":
        if not msg.isdigit() or not (10 <= int(msg) <= 50):
            await update.message.reply_text(
                "❌ 𝗔𝗴𝗲 𝗺𝘂𝘀𝘁 𝗯𝗲 𝗯𝗲𝘁𝘄𝗲𝗲𝗻 𝟭𝟬 𝗮𝗻𝗱 𝟱𝟬."
            )
            return
        user["identity"]["age"] = msg
        ctx.user_data["step"] = "location"
        await update.message.reply_text(
            "📍 𝗘𝗻𝘁𝗲𝗿 𝗟𝗼𝗰𝗮𝘁𝗶𝗼𝗻:"
        )

    elif step == "location":
        user["identity"]["location"] = val(msg)
        ctx.user_data["step"] = "gender"
        await update.message.reply_text(
            "🧬 𝗦𝗲𝗹𝗲𝗰𝘁 𝗚𝗲𝗻𝗱𝗲𝗿:",
            reply_markup=KB_GENDER
        )

    elif step == "gender":
        if msg not in ["𝗠𝗮𝗹𝗲 💁‍♂️", "𝗙𝗲𝗺𝗮𝗹𝗲 💁‍♀️"]:
            await update.message.reply_text(
                "❌ 𝗣𝗹𝗲𝗮𝘀𝗲 𝘀𝗲𝗹𝗲𝗰𝘁 𝗴𝗲𝗻𝗱𝗲𝗿 𝘂𝘀𝗶𝗻𝗴 𝗯𝘂𝘁𝘁𝗼𝗻𝘀 𝗼𝗻𝗹𝘆.",
                reply_markup=KB_GENDER
            )
            return
        user["identity"]["gender"] = f"🧬 𝗚𝗲𝗻𝗱𝗲𝗿 — {msg}"
        ctx.user_data["step"] = "relationship"
        await update.message.reply_text(
            "💓 𝗦𝗲𝗹𝗲𝗰𝘁 𝗥𝗲𝗹𝗮𝘁𝗶𝗼𝗻𝘀𝗵𝗶𝗽:",
            reply_markup=KB_REL
        )

    elif step == "relationship":
        if msg not in ["𝗦𝗶𝗻𝗴𝗹𝗲 🖤", "𝗠𝗶𝗻𝗴𝗹𝗲 ♥️"]:
            await update.message.reply_text(
                "❌ 𝗣𝗹𝗲𝗮𝘀𝗲 𝘀𝗲𝗹𝗲𝗰𝘁 𝗿𝗲𝗹𝗮𝘁𝗶𝗼𝗻𝘀𝗵𝗶𝗽 𝘂𝘀𝗶𝗻𝗴 𝗯𝘂𝘁𝘁𝗼𝗻𝘀 𝗼𝗻𝗹𝘆.",
                reply_markup=KB_REL
            )
            return
        user["identity"]["relationship"] = f"💓 𝗥𝗲𝗹𝗮𝘁𝗶𝗼𝗻𝘀𝗵𝗶𝗽 — {msg}"
        ctx.user_data["step"] = "song"
        await update.message.reply_text(
            "🎵 𝗙𝗮𝘃𝗼𝗿𝗶𝘁𝗲 𝗦𝗼𝗻𝗴:",
            reply_markup=KB_SKIP_CANCEL
        )

    elif step == "song":
        user["identity"]["song"] = val(msg)
        ctx.user_data["step"] = "actor"
        await update.message.reply_text(
            "🎬 𝗙𝗮𝘃𝗼𝗿𝗶𝘁𝗲 𝗔𝗰𝘁𝗼𝗿:",
            reply_markup=KB_SKIP_CANCEL
        )

    elif step == "actor":
        user["identity"]["actor"] = val(msg)
        ctx.user_data["step"] = "hobby"
        await update.message.reply_text(
            "🎯 𝗙𝗮𝘃𝗼𝗿𝗶𝘁𝗲 𝗛𝗼𝗯𝗯𝘆:",
            reply_markup=KB_SKIP_CANCEL
        )

    elif step == "hobby":
        user["identity"]["hobby"] = val(msg)
        ctx.user_data["step"] = "bio"
        await update.message.reply_text(
            "📝 𝗦𝗵𝗼𝗿𝘁 𝗕𝗶𝗼:",
            reply_markup=KB_SKIP_CANCEL
        )

    elif step == "bio":
        user["identity"]["bio"] = val(msg)
        user["submitted"] = True
        ctx.user_data.clear()
        await update.message.reply_text(
            "✅ 𝗜𝗱𝗲𝗻𝘁𝗶𝘁𝘆 𝗦𝘂𝗯𝗺𝗶𝘁𝘁𝗲𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆.\n\n"
            "𝗣𝗹𝗲𝗮𝘀𝗲 𝗰𝗼𝗻𝘁𝗮𝗰𝘁 𝘆𝗼𝘂𝗿 𝗴𝗿𝗼𝘂𝗽 𝗮𝗱𝗺𝗶𝗻𝗶𝘀𝘁𝗿𝗮𝘁𝗶𝗼𝗻 𝘁𝗼 𝘀𝗲𝘁 𝘆𝗼𝘂𝗿 𝗽𝗿𝗼𝗳𝗶𝗹𝗲 𝗽𝗵𝗼𝘁𝗼.",
            reply_markup=KB_EDIT
        )

    save(data)

# ================= PROFILE COMMANDS (ADMIN ONLY) =================
async def setprofile(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        return
    if not await is_group_admin(update, ctx):
        await update.message.reply_text(
            "❌ 𝗧𝗵𝗶𝘀 𝗰𝗼𝗺𝗺𝗮𝗻𝗱 𝗶𝘀 𝗳𝗼𝗿 𝗴𝗿𝗼𝘂𝗽 𝗮𝗱𝗺𝗶𝗻𝗶𝘀𝘁𝗿𝗮𝘁𝗼𝗿𝘀 𝗼𝗻𝗹𝘆."
        )
        return
    if not update.message.reply_to_message:
        await update.message.reply_text(
            "❌ 𝗥𝗲𝗽𝗹𝘆 𝘁𝗼 𝗮 𝘂𝘀𝗲𝗿 𝘁𝗼 𝘀𝗲𝘁 𝘁𝗵𝗲𝗶𝗿 𝗽𝗿𝗼𝗳𝗶𝗹𝗲."
        )
        return

    data = load()
    target = update.message.reply_to_message.from_user
    uid = str(target.id)
    gid = str(update.effective_chat.id)
    user = get_user(data, uid)

    photos = await ctx.bot.get_user_profile_photos(target.id, limit=1)
    if photos.total_count == 0:
        await update.message.reply_text(
            "❌ 𝗨𝘀𝗲𝗿 𝗵𝗮𝘀 𝗻𝗼 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺 𝗽𝗿𝗼𝗳𝗶𝗹𝗲 𝗽𝗵𝗼𝘁𝗼."
        )
        return

    user["groups"][gid] = photos.photos[0][-1].file_id
    save(data)
    await update.message.reply_text(
        "✅ 𝗣𝗿𝗼𝗳𝗶𝗹𝗲 𝗽𝗵𝗼𝘁𝗼 𝘀𝗲𝘁 𝗳𝗿𝗼𝗺 𝘂𝘀𝗲𝗿’𝘀 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺 𝗗𝗣."
    )


async def updateprofile(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        return
    if not await is_group_admin(update, ctx):
        await update.message.reply_text(
            "❌ 𝗧𝗵𝗶𝘀 𝗰𝗼𝗺𝗺𝗮𝗻𝗱 𝗶𝘀 𝗳𝗼𝗿 𝗴𝗿𝗼𝘂𝗽 𝗮𝗱𝗺𝗶𝗻𝗶𝘀𝘁𝗿𝗮𝘁𝗼𝗿𝘀 𝗼𝗻𝗹𝘆."
        )
        return
    if not update.message.reply_to_message:
        await update.message.reply_text(
            "❌ 𝗥𝗲𝗽𝗹𝘆 𝘁𝗼 𝗮 𝘂𝘀𝗲𝗿 𝘁𝗼 𝘂𝗽𝗱𝗮𝘁𝗲 𝘁𝗵𝗲𝗶𝗿 𝗽𝗿𝗼𝗳𝗶𝗹𝗲."
        )
        return

    data = load()
    target = update.message.reply_to_message.from_user
    uid = str(target.id)
    gid = str(update.effective_chat.id)
    user = get_user(data, uid)

    photos = await ctx.bot.get_user_profile_photos(target.id, limit=1)
    if photos.total_count == 0:
        await update.message.reply_text(
            "❌ 𝗨𝘀𝗲𝗿 𝗵𝗮𝘀 𝗻𝗼 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺 𝗽𝗿𝗼𝗳𝗶𝗹𝗲 𝗽𝗵𝗼𝘁𝗼."
        )
        return

    user["groups"][gid] = photos.photos[0][-1].file_id
    save(data)
    await update.message.reply_text(
        "♻️ 𝗣𝗿𝗼𝗳𝗶𝗹𝗲 𝗽𝗵𝗼𝘁𝗼 𝘂𝗽𝗱𝗮𝘁𝗲𝗱 𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆."
    )


async def removeprofile(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        return
    if not await is_group_admin(update, ctx):
        await update.message.reply_text(
            "❌ 𝗧𝗵𝗶𝘀 𝗰𝗼𝗺𝗺𝗮𝗻𝗱 𝗶𝘀 𝗳𝗼𝗿 𝗴𝗿𝗼𝘂𝗽 𝗮𝗱𝗺𝗶𝗻𝗶𝘀𝘁𝗿𝗮𝘁𝗼𝗿𝘀 𝗼𝗻𝗹𝘆."
        )
        return
    if not update.message.reply_to_message:
        await update.message.reply_text(
            "❌ 𝗥𝗲𝗽𝗹𝘆 𝘁𝗼 𝗮 𝘂𝘀𝗲𝗿 𝘁𝗼 𝗿𝗲𝗺𝗼𝘃𝗲 𝘁𝗵𝗲𝗶𝗿 𝗽𝗿𝗼𝗳𝗶𝗹𝗲."
        )
        return

    data = load()
    target = update.message.reply_to_message.from_user
    uid = str(target.id)
    gid = str(update.effective_chat.id)
    user = get_user(data, uid)

    if gid in user["groups"]:
        del user["groups"][gid]
        save(data)
        await update.message.reply_text(
            "🗑 𝗣𝗿𝗼𝗳𝗶𝗹𝗲 𝗽𝗵𝗼𝘁𝗼 𝗿𝗲𝗺𝗼𝘃𝗲𝗱."
        )


# ================= INTRO (GROUP) =================
async def intro(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        return

    data = load()

    target = (
        update.message.reply_to_message.from_user
        if update.message.reply_to_message
        else update.effective_user
    )

    uid = str(target.id)
    gid = str(update.effective_chat.id)
    user = data.get(uid)

    mention = f'<a href="tg://user?id={target.id}">{target.first_name}</a>'

    if not user or not user.get("submitted"):
        await update.message.reply_text(
            f"{mention} 𝗵𝗮𝘀 𝗻𝗼𝘁 𝘀𝗲𝘁 𝗶𝗱𝗲𝗻𝘁𝗶𝘁𝘆 𝘆𝗲𝘁.\n"
            "𝗣𝗹𝗲𝗮𝘀𝗲 𝘀𝗲𝘁 𝘆𝗼𝘂𝗿 𝗶𝗱𝗲𝗻𝘁𝗶𝘁𝘆 𝗶𝗻 𝗗𝗠.",
            parse_mode="HTML"
        )
        return

    p = user["identity"]
    caption = (
        "👤 𝗣𝗥𝗢𝗙𝗜𝗟𝗘\n\n"
        f"👤 𝗡𝗮𝗺𝗲: {p['name']}\n"
        f"🎂 𝗔𝗴𝗲: {p['age']}\n"
        f"📍 𝗟𝗼𝗰𝗮𝘁𝗶𝗼𝗻: {p['location']}\n"
        f"{p['gender']}\n"
        f"{p['relationship']}\n"
        f"🎵 𝗦𝗼𝗻𝗴: {p['song']}\n"
        f"🎬 𝗔𝗰𝘁𝗼𝗿: {p['actor']}\n"
        f"🎯 𝗛𝗼𝗯𝗯𝘆: {p['hobby']}\n\n"
        "📝 𝗕𝗜𝗢:\n"
        f"{p['bio']}"
    )

    if gid in user.get("groups", {}):
        await update.message.reply_photo(photo=user["groups"][gid], caption=caption)
    else:
        await update.message.reply_text(caption)


# ================= NEW MEMBER (FIXED) =================
async def welcome_member(update: ChatMemberUpdated, ctx: ContextTypes.DEFAULT_TYPE):
    chat = update.chat_member.chat

    if chat.type == "private":
        return

    new = update.chat_member.new_chat_member
    old = update.chat_member.old_chat_member

    if old.status in ("left", "kicked") and new.status == "member":
        u = new.user
        mention = f'<a href="tg://user?id={u.id}">{u.first_name}</a>'

        await ctx.bot.send_message(
            chat.id,
            f"👋 𝗪𝗲𝗹𝗰𝗼𝗺𝗲 {mention}!\n\n"
            "🆔 𝗣𝗹𝗲𝗮𝘀𝗲 𝘀𝗲𝘁 𝘆𝗼𝘂𝗿 𝗶𝗱𝗲𝗻𝘁𝗶𝘁𝘆 𝗯𝘆 𝗺𝗲𝘀𝘀𝗮𝗴𝗶𝗻𝗴 𝗺𝗲 𝗶𝗻 𝗗𝗠.\n"
            "🖼 𝗣𝗿𝗼𝗳𝗶𝗹𝗲 𝗽𝗵𝗼𝘁𝗼 𝘄𝗶𝗹𝗹 𝗯𝗲 𝘀𝗲𝘁 𝗯𝘆 𝗴𝗿𝗼𝘂𝗽 𝗮𝗱𝗺𝗶𝗻𝗶𝘀𝘁𝗿𝗮𝘁𝗶𝗼𝗻.",
            parse_mode="HTML"
        )


# ================= MAIN =================
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("intro", intro))
app.add_handler(CommandHandler("setprofile", setprofile))
app.add_handler(CommandHandler("updateprofile", updateprofile))
app.add_handler(CommandHandler("removeprofile", removeprofile))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_dm))
app.add_handler(CallbackQueryHandler(help_cb, pattern="^(help|back)$"))
app.add_handler(ChatMemberHandler(welcome_member, ChatMemberHandler.CHAT_MEMBER))

print("INTRO BOT RUNNING | Developed by @Frx_Shooter")
app.run_polling()
