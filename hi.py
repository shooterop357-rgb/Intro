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
        "groups": {}  # group_id -> photo_file_id
    })

# ================= KEYBOARDS =================
INLINE_WELCOME = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("👑 Owner", url=OWNER_LINK),
        InlineKeyboardButton("🧠 Developer", url=DEV_LINK),
    ],
    [
        InlineKeyboardButton("💬 Support", url=SUPPORT_LINK),
        InlineKeyboardButton("📢 Official Channel", url=CHANNEL_LINK),
    ],
    [
        InlineKeyboardButton("❓ Help", callback_data="help"),
    ],
])

KB_SET = ReplyKeyboardMarkup([["✨ Set Identity"]], resize_keyboard=True)
KB_EDIT = ReplyKeyboardMarkup([["✏️ Edit Identity"]], resize_keyboard=True)
KB_GENDER = ReplyKeyboardMarkup([["Male 💁‍♂️", "Female 💁‍♀️"]], resize_keyboard=True)
KB_REL = ReplyKeyboardMarkup([["Single 🖤", "Mingle ♥️"]], resize_keyboard=True)
KB_SKIP_CANCEL = ReplyKeyboardMarkup([["Skip", "Cancel"]], resize_keyboard=True)

# ================= START =================
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != "private":
        return

    text = (
        f"✨ Welcome, {update.effective_user.first_name}! ✨\n\n"
        "This is your personal space to shape your identity your way.\n\n"
        "Share only what feels right — everything stays in your control.\n\n"
        "Let’s get started 👇"
    )

    await update.message.reply_text(
        text,
        reply_markup=INLINE_WELCOME
    )
    await update.message.reply_text(
        "Tap below to begin:",
        reply_markup=KB_SET
    )

# ================= HELP =================
async def help_cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.edit_message_text(
        "🤖 INTRO BOT HELP\n\n"
        "• Set identity in DM only\n"
        "• Use /intro in groups (reply required)\n"
        "• Admins approve profile photos\n"
        "• Skipped info shows as N/A\n"
        "• No buttons work in groups"
    )

# ================= TEXT HANDLER (DM) =================
async def text_dm(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != "private":
        return

    msg = update.message.text.strip()
    data = load()
    uid = str(update.effective_user.id)
    user = get_user(data, uid)

    # START / EDIT
    if msg in ["✨ Set Identity", "✏️ Edit Identity"]:
        ctx.user_data.clear()
        user["identity"] = {k: "N/A" for k in user["identity"]}
        ctx.user_data["step"] = "name"
        save(data)
        await update.message.reply_text("👤 Enter Name:", reply_markup=ReplyKeyboardRemove())
        return

    # CANCEL
    if msg == "Cancel":
        ctx.user_data.clear()
        await update.message.reply_text("Cancelled.", reply_markup=KB_SET)
        return

    step = ctx.user_data.get("step")
    if not step:
        return

    def val(x): return "N/A" if x.lower() == "skip" else x

    if step == "name":
        user["identity"]["name"] = val(msg)
        ctx.user_data["step"] = "age"
        await update.message.reply_text("🎂 Enter Age (10–50):")
    elif step == "age":
        if not msg.isdigit() or not (10 <= int(msg) <= 50):
            await update.message.reply_text("❌ Age must be 10–50.")
            return
        user["identity"]["age"] = msg
        ctx.user_data["step"] = "location"
        await update.message.reply_text("📍 Enter Location:")
    elif step == "location":
        user["identity"]["location"] = val(msg)
        ctx.user_data["step"] = "gender"
        await update.message.reply_text("🧬 Select Gender:", reply_markup=KB_GENDER)
    elif step == "gender":
        user["identity"]["gender"] = (
            "🧬 Gender - Male 💁‍♂️" if "Male" in msg else "🧬 Gender - Female 💁‍♀️"
        )
        ctx.user_data["step"] = "relationship"
        await update.message.reply_text("💓 Relationship:", reply_markup=KB_REL)
    elif step == "relationship":
        user["identity"]["relationship"] = (
            "💓 Relationship - Single 🖤" if "Single" in msg else "💓 Relationship - Mingle ♥️"
        )
        ctx.user_data["step"] = "song"
        await update.message.reply_text("🎵 Favorite Song:", reply_markup=KB_SKIP_CANCEL)
    elif step == "song":
        user["identity"]["song"] = val(msg)
        ctx.user_data["step"] = "actor"
        await update.message.reply_text("🎬 Favorite Actor:", reply_markup=KB_SKIP_CANCEL)
    elif step == "actor":
        user["identity"]["actor"] = val(msg)
        ctx.user_data["step"] = "hobby"
        await update.message.reply_text("🎯 Favorite Hobby:", reply_markup=KB_SKIP_CANCEL)
    elif step == "hobby":
        user["identity"]["hobby"] = val(msg)
        ctx.user_data["step"] = "bio"
        await update.message.reply_text("📝 Short Bio:", reply_markup=KB_SKIP_CANCEL)
    elif step == "bio":
        user["identity"]["bio"] = val(msg)
        user["submitted"] = True
        ctx.user_data.clear()
        await update.message.reply_text(
            "✅ Identity submitted successfully.\n\n"
            "Please contact your group administration to set your profile photo.",
            reply_markup=KB_EDIT
        )

    save(data)

# ================= INTRO (GROUP) =================
async def intro(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Please reply to a user to use this command.")
        return

    data = load()
    target = update.message.reply_to_message.from_user
    uid = str(target.id)
    user = data.get(uid)

    mention = f'<a href="tg://user?id={target.id}">{target.first_name}</a>'

    if not user or not user.get("submitted"):
        await update.message.reply_text(
            f"❌ Someone wants to know about you, {mention}.\n"
            "Please set your profile by messaging me in DM.",
            parse_mode="HTML"
        )
        return

    p = user["identity"]
    await update.message.reply_text(
        f"👤 Profile\n\n"
        f"👤 Name: {p['name']}\n"
        f"🎂 Age: {p['age']}\n"
        f"📍 Location: {p['location']}\n"
        f"{p['gender']}\n"
        f"{p['relationship']}\n"
        f"🎵 Song: {p['song']}\n"
        f"🎬 Actor: {p['actor']}\n"
        f"🎯 Hobby: {p['hobby']}\n\n"
        f"📝 Bio:\n{p['bio']}"
    )

# ================= NEW MEMBER =================
async def welcome_member(update: ChatMemberUpdated, ctx: ContextTypes.DEFAULT_TYPE):
    if update.chat.type == "private":
        return
    if update.new_chat_member.status == "member":
        user = update.new_chat_member.user
        mention = f'<a href="tg://user?id={user.id}">{user.first_name}</a>'
        await ctx.bot.send_message(
            update.chat.id,
            f"👋 Welcome {mention}!\n\nPlease set your information by messaging me in DM.",
            parse_mode="HTML"
        )

# ================= MAIN =================
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("intro", intro))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_dm))
app.add_handler(ChatMemberHandler(welcome_member, ChatMemberHandler.CHAT_MEMBER))
app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_member))
app.add_handler(MessageHandler(filters.UpdateType.CALLBACK_QUERY, help_cb))

print("✅ INTRO BOT RUNNING (FINAL BUILD)")
app.run_polling()
