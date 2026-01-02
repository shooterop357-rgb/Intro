import json
import os
import time
from telegram import (
    Update,
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
DATA_FILE = "data.json"

INTRO_COOLDOWN = 10  # seconds
intro_cooldown = {}  # user_id -> last_used_time

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
async def is_admin(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    member = await ctx.bot.get_chat_member(
        update.effective_chat.id,
        update.effective_user.id
    )
    return member.status in ("administrator", "creator")

# ================= KEYBOARDS =================
KB_SET = ReplyKeyboardMarkup([["✨ Set Identity"]], resize_keyboard=True)
KB_EDIT = ReplyKeyboardMarkup([["✏️ Edit Identity"]], resize_keyboard=True)
KB_GENDER = ReplyKeyboardMarkup([["Male 💁‍♂️", "Female 💁‍♀️"]], resize_keyboard=True)
KB_REL = ReplyKeyboardMarkup([["Single 🖤", "Mingle ♥️"]], resize_keyboard=True)
KB_SKIP_CANCEL = ReplyKeyboardMarkup([["Skip", "Cancel"]], resize_keyboard=True)

# ================= START =================
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != "private":
        return
    await update.message.reply_text(
        f"✨ Welcome, {update.effective_user.first_name}!\n\nTap below to begin:",
        reply_markup=KB_SET
    )

# ================= DM FLOW + AUTO DELETE =================
async def text_dm(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != "private":
        return

    msg = update.message.text.strip()
    data = load()
    uid = str(update.effective_user.id)
    user = get_user(data, uid)

    # 🔒 AUTO DELETE AFTER SUBMIT
    if user["submitted"]:
        if msg not in ["✨ Set Identity", "✏️ Edit Identity"]:
            try:
                await update.message.delete()
            except:
                pass
            return

    if msg in ["✨ Set Identity", "✏️ Edit Identity"]:
        ctx.user_data.clear()
        user["identity"] = {k: "N/A" for k in user["identity"]}
        ctx.user_data["step"] = "name"
        save(data)
        await update.message.reply_text("👤 Enter Name:", reply_markup=ReplyKeyboardRemove())
        return

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
        if msg not in ["Male 💁‍♂️", "Female 💁‍♀️"]:
            await update.message.reply_text("❌ Use buttons only.", reply_markup=KB_GENDER)
            return
        user["identity"]["gender"] = f"🧬 Gender - {msg}"
        ctx.user_data["step"] = "relationship"
        await update.message.reply_text("💓 Relationship:", reply_markup=KB_REL)

    elif step == "relationship":
        if msg not in ["Single 🖤", "Mingle ♥️"]:
            await update.message.reply_text("❌ Use buttons only.", reply_markup=KB_REL)
            return
        user["identity"]["relationship"] = f"💓 Relationship - {msg}"
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
            "✅ Identity submitted successfully.\n\nContact group administration to set profile photo.",
            reply_markup=KB_EDIT
        )

    save(data)

# ================= INTRO COMMAND (FREE + COOLDOWN) =================
async def intro(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        return

    user_id = update.effective_user.id
    now = time.time()

    if not await is_admin(update, ctx):
        last = intro_cooldown.get(user_id, 0)
        if now - last < INTRO_COOLDOWN:
            wait = int(INTRO_COOLDOWN - (now - last))
            await update.message.reply_text(f"⏳ Wait {wait}s before using /intro again.")
            return
        intro_cooldown[user_id] = now

    data = load()

    # 🎯 Target decide
    if update.message.reply_to_message:
        target = update.message.reply_to_message.from_user
    else:
        target = update.effective_user

    uid = str(target.id)
    gid = str(update.effective_chat.id)
    user = data.get(uid)

    mention = f'<a href="tg://user?id={target.id}">{target.first_name}</a>'

    if not user or not user.get("submitted"):
        await update.message.reply_text(
            f"{mention} has not set identity yet.",
            parse_mode="HTML"
        )
        return

    p = user["identity"]
    caption = (
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

    if gid in user.get("groups", {}):
        await update.message.reply_photo(
            photo=user["groups"][gid],
            caption=caption
        )
    else:
        await update.message.reply_text(caption)

# ================= MAIN =================
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("intro", intro))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_dm))

print("✅ INTRO BOT RUNNING (FREE INTRO + COOLDOWN ENABLED)")
app.run_polling()
