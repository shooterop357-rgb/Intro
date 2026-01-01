import json
import os
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ================= CONFIG =================
BOT_TOKEN = "8161458476:AAH76ALCfc-zWa3Lwh8nitkjw82i8QJYat8"
DATA_FILE = "profiles.json"

OWNER_LINK = "@iugrp"
DEV_LINK = "@Frx_shooter"
SUPPORT_LINK = "@hiestarboy"
CHANNEL_LINK = "https://t.me/all_state_gc"

# ================= STORAGE =================
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

def load():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ================= KEYBOARDS =================
START_KB = ReplyKeyboardMarkup(
    [
        ["👑 Owner", "🧠 Developer"],
        ["💬 Support", "📢 Official Channel"],
        ["❓ Help"],
        ["✨ Set Identity"],
    ],
    resize_keyboard=True
)

FORM_KB = ReplyKeyboardMarkup(
    [["⏭ Next", "⬅️ Previous"], ["❌ Cancel"]],
    resize_keyboard=True
)

AFTER_SUBMIT_KB = ReplyKeyboardMarkup(
    [["✏️ Edit Identity"], ["❓ Help"]],
    resize_keyboard=True
)

# ================= START =================
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != "private":
        return

    text = (
        f"✨ 𝗪𝗲𝗹𝗰𝗼𝗺𝗲, {update.effective_user.first_name}! ✨\n\n"
        "𝗧𝗵𝗶𝘀 𝗶𝘀 𝘆𝗼𝘂𝗿 𝗽𝗲𝗿𝘀𝗼𝗻𝗮𝗹 𝘀𝗽𝗮𝗰𝗲 𝘁𝗼 𝘀𝗵𝗮𝗽𝗲 "
        "𝘆𝗼𝘂𝗿 𝗶𝗱𝗲𝗻𝘁𝗶𝘁𝘆 𝘆𝗼𝘂𝗿 𝘄𝗮𝘆.\n\n"
        "𝗟𝗲𝘁’𝘀 𝗴𝗲𝘁 𝘀𝘁𝗮𝗿𝘁𝗲𝗱 👇"
    )

    await ctx.bot.send_message(
    chat_id=update.effective_chat.id,
    text=text,
    reply_markup=START_KB
)
# ================= HELP =================
async def help_msg(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 INTRO BOT\n\n"
        "• Set identity in DM only\n"
        "• Use /intro in groups (reply required)\n"
        "• No buttons work in groups\n"
        "• Profile visible after admin approval"
    )

# ================= TEXT HANDLER =================
async def text_handler(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.message.text.strip()
    data = load()

    # -------- GROUP: no buttons --------
    if chat.type != "private":
        return

    uid = str(update.effective_user.id)
    user = data.setdefault(uid, {"submitted": False, "profile": {}})

    # -------- BUTTON LINKS --------
    if msg == "👑 Owner":
        await update.message.reply_text(OWNER_LINK)
        return
    if msg == "🧠 Developer":
        await update.message.reply_text(DEV_LINK)
        return
    if msg == "💬 Support":
        await update.message.reply_text(SUPPORT_LINK)
        return
    if msg == "📢 Official Channel":
        await update.message.reply_text(CHANNEL_LINK)
        return
    if msg == "❓ Help":
        await help_msg(update, ctx)
        return

    # -------- START / EDIT --------
    if msg in ["✨ Set Identity", "✏️ Edit Identity"]:
        ctx.user_data["step"] = "age"
        await update.message.reply_text(
            "🎂 Enter Age (13–60):", reply_markup=FORM_KB
        )
        return

    # -------- CANCEL --------
    if msg == "❌ Cancel":
        ctx.user_data.clear()
        await update.message.reply_text(
            "❌ Process cancelled.", reply_markup=START_KB
        )
        return

    step = ctx.user_data.get("step")

    # -------- FORM STEPS --------
    if step == "age":
        if not msg.isdigit() or not (13 <= int(msg) <= 60):
            await update.message.reply_text("❌ Age must be 13–60.")
            return
        user["profile"]["age"] = msg
        ctx.user_data["step"] = "location"
        await update.message.reply_text("📍 Enter Location:")
        save(data)
        return

    if step == "location":
        user["profile"]["location"] = msg
        ctx.user_data["step"] = "gender"
        await update.message.reply_text("🧬 Gender (Male/Female):")
        save(data)
        return

    if step == "gender":
        if msg.lower() not in ["male", "female"]:
            await update.message.reply_text("Type Male or Female.")
            return
        user["profile"]["gender"] = (
            "🧬 Gender - Male 💁‍♂️" if msg.lower() == "male"
            else "🧬 Gender - Female 💁‍♀️"
        )
        ctx.user_data["step"] = "relationship"
        await update.message.reply_text("💓 Relationship (Single/Mingle):")
        save(data)
        return

    if step == "relationship":
        user["profile"]["relationship"] = (
            "💓 Relationship - Single 🖤" if msg.lower() == "single"
            else "💓 Relationship - Mingle ♥️"
        )
        ctx.user_data["step"] = "song"
        await update.message.reply_text("🎵 Favorite Song:")
        save(data)
        return

    if step == "song":
        user["profile"]["song"] = msg
        ctx.user_data["step"] = "actor"
        await update.message.reply_text("🎬 Favorite Actor:")
        save(data)
        return

    if step == "actor":
        user["profile"]["actor"] = msg
        ctx.user_data["step"] = "hobby"
        await update.message.reply_text("🎯 Favorite Hobby:")
        save(data)
        return

    if step == "hobby":
        user["profile"]["hobby"] = msg
        ctx.user_data["step"] = "bio"
        await update.message.reply_text("📝 Short Bio:")
        save(data)
        return

    if step == "bio":
        user["profile"]["bio"] = msg
        user["submitted"] = True
        ctx.user_data.clear()
        save(data)

        await update.message.reply_text(
            "✅ Your identity has been submitted successfully.\n"
            "Please contact your group administration to approve your profile.\n"
            "For security reasons, you cannot set your profile by yourself.",
            reply_markup=AFTER_SUBMIT_KB
        )
        return

# ================= /INTRO =================
async def intro(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Reply to a user.")
        return

    data = load()
    target = update.message.reply_to_message.from_user
    uid = str(target.id)
    user = data.get(uid)

    mention = f'<a href="tg://user?id={target.id}">{target.first_name}</a>'

    if not user or not user.get("submitted"):
        await update.message.reply_text(
            f"❌ Someone wants to know about you, {mention}.\n"
            "Please set your identity by messaging me.",
            parse_mode="HTML"
        )
        return

    p = user["profile"]
    await update.message.reply_text(
        f"👤 Profile\n\n"
        f"🆔 User ID: {target.id}\n"
        f"🎂 Age: {p['age']}\n"
        f"📍 Location: {p['location']}\n"
        f"{p['gender']}\n"
        f"{p['relationship']}\n"
        f"🎵 Song: {p['song']}\n"
        f"🎬 Actor: {p['actor']}\n"
        f"🎯 Hobby: {p['hobby']}\n\n"
        f"📝 Bio:\n{p['bio']}"
    )

# ================= MAIN =================
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("intro", intro))
app.add_handler(MessageHandler(filters.TEXT, text_handler))

print("✅ BOT RUNNING (MERGED FINAL)")
app.run_polling()
