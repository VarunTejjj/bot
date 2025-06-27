from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# === Your Bot Token ===
BOT_TOKEN = '7402238600:AAFbiFIiY9xIZfklqpSCxrDWzfj4U57lQSg'

# === Group Chat IDs ===
GROUP_ID_1 = -1002823596317
GROUP_ID_2 = -1002524124036
GROUP_ID_3 = -4671387156

# === Group Invite Links ===
JOIN_LINK_1 = 'https://t.me/+JASzCdO6FV45MWRl'
JOIN_LINK_2 = 'https://t.me/+BNCw_Dqr3M9jZGY1'
JOIN_LINK_3 = 'https://t.me/+e3JDbcKng_g3NmJl'

# === Inline Buttons ===
def get_join_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👥 Join Group 1", url=JOIN_LINK_1)],
        [InlineKeyboardButton("👥 Join Group 2", url=JOIN_LINK_2)],
        [InlineKeyboardButton("👥 Join Group 3", url=JOIN_LINK_3)],
        [InlineKeyboardButton("✅ I've Joined All", callback_data="check_join")]
    ])

# === /start Command ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    name = user.full_name

    joined = await check_all_groups(context, user_id)

    if joined:
        await update.message.reply_text(
            f"✅ *Welcome {name}!* You've already joined all groups.\n\n_Unlocking content..._",
            parse_mode="Markdown"
        )
        await send_access_content(context, user_id)
    else:
        await update.message.reply_text(
            f"👋 Hello *{name}*, please join *ALL 3 groups* below to use this bot:",
            parse_mode="Markdown",
            reply_markup=get_join_buttons()
        )

# === Callback: Recheck Join Status ===
async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    user_id = user.id
    name = user.full_name

    await query.answer()

    joined = await check_all_groups(context, user_id)

    if joined:
        await query.edit_message_text(
            f"✅ *Thank you {name}!* You're verified.\n\n_Sending your content..._",
            parse_mode="Markdown"
        )
        await send_access_content(context, user_id)
    else:
        await query.edit_message_text(
            "❌ You're still missing one or more groups.\n\nPlease join all and click again.",
            parse_mode="Markdown",
            reply_markup=get_join_buttons()
        )

# === Group Join Check ===
async def check_all_groups(context, user_id):
    try:
        member1 = await context.bot.get_chat_member(GROUP_ID_1, user_id)
        member2 = await context.bot.get_chat_member(GROUP_ID_2, user_id)
        member3 = await context.bot.get_chat_member(GROUP_ID_3, user_id)

        valid = ['member', 'administrator', 'creator']

        return all([
            member1.status in valid,
            member2.status in valid,
            member3.status in valid
        ])
    except:
        return False

# === Send Final Content ===
async def send_access_content(context, user_id):
    await context.bot.send_message(
        chat_id=user_id,
        text=(
            "🎉 *Access Granted!*\n\n"
            "🌐 [Watch Child Corn](https://childhotcorn.free.nf/)\n"
            "📁 [Watch New Hot Leaks](https://childhotcorn.free.nf/)\n"
            "📣 Stay updated in our groups!\n\n"
            "_Thanks for being part of the community!_"
        ),
        parse_mode='Markdown'
    )

# === Run Bot ===
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_join, pattern="check_join"))
    app.run_polling()
