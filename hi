import json
import os
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = "8161458476:AAH76ALCfc-zWa3Lwh8nitkjw82i8QJYat8"
OWNER_ID = 5436530930
DATA_FILE = "profiles.json"

# ------------------ STORAGE ------------------

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

with open(DATA_FILE, "r") as f:
    profiles = json.load(f)

def save():
    with open(DATA_FILE, "w") as f:
        json.dump(profiles, f, indent=2)

def get_user(uid):
    if uid not in profiles:
        profiles[uid] = {
            "submitted": False,
            "approved_groups": {},
            "name": "",
            "age": "",
            "location": "",
            "gender": "",
            "relationship": "",
            "song": "",
            "actor": "",
            "hobby": "",
            "bio": ""
        }
    return profiles[uid]

# ------------------ START ------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    uid = str(user.id)
    p = get_user(uid)

    if p["submitted"]:
        await update.message.reply_text(
            "✨ Welcome back!\n\nYour identity is already submitted.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✏️ Edit Identity", callback_data="edit")]
            ])
        )
    else:
        await update.message.reply_text(
            "✨ Welcome!\n\nCreate your digital identity.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✨ Set Identity", callback_data="start_form")]
            ])
        )

# ------------------ FORM FLOW ------------------

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = str(q.from_user.id)
    p = get_user(uid)

    if q.data == "start_form" or q.data == "edit":
        context.user_data["step"] = "age"
        await q.message.reply_text("🎂 Enter Age (10–50):")

    elif q.data == "gender_male":
        p["gender"] = "🧬 Gender - Male 💁‍♂️"
        save()
        context.user_data["step"] = "relationship"
        await q.message.reply_text(
            "💓 Relationship Status:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🖤 Single", callback_data="rel_single")],
                [InlineKeyboardButton("♥️ Mingle", callback_data="rel_mingle")]
            ])
        )

    elif q.data == "gender_female":
        p["gender"] = "🧬 Gender - Female 💁‍♀️"
        save()
        context.user_data["step"] = "relationship"
        await q.message.reply_text(
            "💓 Relationship Status:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🖤 Single", callback_data="rel_single")],
                [InlineKeyboardButton("♥️ Mingle", callback_data="rel_mingle")]
            ])
        )

    elif q.data == "rel_single":
        p["relationship"] = "💓 Relationship - Single 🖤"
        save()
        context.user_data["step"] = "song"
        await q.message.reply_text("🎵 Favorite Song (or type Skip):")

    elif q.data == "rel_mingle":
        p["relationship"] = "💓 Relationship - Mingle ♥️"
        save()
        context.user_data["step"] = "song"
        await q.message.reply_text("🎵 Favorite Song (or type Skip):")

# ------------------ TEXT HANDLER ------------------

async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    p = get_user(uid)
    step = context.user_data.get("step")

    msg = update.message.text.strip()

    if step == "age":
        if not msg.isdigit() or not (10 <= int(msg) <= 50):
            await update.message.reply_text("❌ Age must be between 10 and 50.")
            return
        p["age"] = msg
        save()
        context.user_data["step"] = "location"
        await update.message.reply_text("📍 Enter Location:")

    elif step == "location":
        p["location"] = msg
        save()
        context.user_data["step"] = "gender"
        await update.message.reply_text(
            "🧬 Select Gender:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💁‍♂️ Male", callback_data="gender_male")],
                [InlineKeyboardButton("💁‍♀️ Female", callback_data="gender_female")]
            ])
        )

    elif step == "song":
        p["song"] = "" if msg.lower() == "skip" else msg
        save()
        context.user_data["step"] = "actor"
        await update.message.reply_text("🎬 Favorite Actor (or Skip):")

    elif step == "actor":
        p["actor"] = "" if msg.lower() == "skip" else msg
        save()
        context.user_data["step"] = "hobby"
        await update.message.reply_text("🎯 Favorite Hobby (or Skip):")

    elif step == "hobby":
        p["hobby"] = "" if msg.lower() == "skip" else msg
        save()
        context.user_data["step"] = "bio"
        await update.message.reply_text("📝 Short Bio (or Skip):")

    elif step == "bio":
        p["bio"] = "" if msg.lower() == "skip" else msg
        p["submitted"] = True
        save()
        context.user_data.clear()

        await update.message.reply_text(
            "✅ Your identity has been submitted successfully.\n\n"
            "Please contact your group administration to approve your profile.\n"
            "For security reasons, you cannot set your profile by yourself.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✏️ Edit Identity", callback_data="edit")]
            ])
        )

# ------------------ /INTRO ------------------

async def intro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Please reply to a user's message.")
        return

    target = update.message.reply_to_message.from_user
    uid = str(target.id)
    p = profiles.get(uid)

    mention = f"[{target.first_name}](tg://user?id={target.id})"

    if not p or not p["submitted"]:
        await update.message.reply_text(
            f"❌ User has not submitted identity yet, {mention}.\n"
            "Someone wants to know about you.\n"
            "Please set your profile by messaging me.",
            parse_mode="Markdown"
        )
        return

    text = (
        "👤 Profile\n\n"
        f"🆔 User ID: {target.id}\n"
        f"👤 Name: {target.first_name}\n"
        f"🎂 Age: {p['age']}\n"
        f"📍 Location: {p['location']}\n"
        f"{p['gender']}\n"
        f"{p['relationship']}\n"
        f"🎵 Song: {p['song']}\n"
        f"🎬 Actor: {p['actor']}\n"
        f"🎯 Hobby: {p['hobby']}\n\n"
        f"📝 Bio:\n{p['bio']}"
    )

    await update.message.reply_text(text)

# ------------------ MAIN ------------------

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("intro", intro))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text))

print("Bot running...")
app.run_polling()
