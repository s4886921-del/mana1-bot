import os
import random
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, ContextTypes
)

TOKEN = os.environ.get("BOT_TOKEN")

POEMS = [
    "منال.. في اسمكِ موسيقى لا تنتهي، وفي عينيكِ عالم لا أريد أن أغادره أبداً 🤍",
    "أحبكِ بهدوء البحر حين يسكن، وبعنف الموج حين يشتاق 🌊",
    "لو سألتني عن أجمل شيء رأيته، سأصمت قليلاً ثم أقول: ابتسامتكِ 🌸",
    "منال.. أنتِ لستِ فقط حبيبتي، أنتِ الفكرة التي تسكن رأسي في كل لحظة هادئة ✨",
    "حنانكِ يشفي ما لا تشفيه الكلمات، وأنا أشكر كل يوم أن وجدتكِ 🤍",
    "لما أحزن، أفكر فيكِ فيرجع النور. أنتِ علاجي الذي لا أحتاج معه دواءً آخر 🌙",
    "عيونكِ تحكي قصصاً لم تقليها بعد، وأنا أحب أن أكون القارئة الوحيدة لها 💫",
    "أنتِ الشخص الذي أريد أن أشاركه أتفه تفاصيل يومي وأجمل أحلامي 🌹",
    "منال.. في كل مرة تضحكين، تقنعيني أن الدنيا لا تزال تستحق 🌷",
    "أحبكِ مثل النجوم تحب السماء — بصمت، وبثبات، وإلى الأبد ⭐",
    "لو كان الحب كتاباً، أنتِ كل صفحاته — البداية والنهاية وكل ما بينهما 📖",
    "ضحكتكِ وحدها تكفيني عن كل شيء في هذه الدنيا 🤍",
]

LOVE_REPLIES = [
    "وأنا أحبكِ أكثر مما تتخيلين يا منال 🤍",
    "قلبي كله لكِ، الآن وكل يوم 🌹",
    "أحبكِ بكل تفاصيلكِ الصغيرة والكبيرة ✨",
    "وأنا أحبكِ مثل النجوم تحب الليل — دائماً وبصمت 🌙",
    "كلمتك هذي تكفيني عن كل شيء 🤍",
    "أحبكِ أنا أيضاً، ولا توجد كلمة تكفي لتعبر عن كم 💫",
]

manal_chat_id = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global manal_chat_id
    manal_chat_id = update.effective_chat.id
    with open("chat_id.txt", "w") as f:
        f.write(str(manal_chat_id))
    await update.message.reply_text(
        "🌙 أهلاً منال..\nهذا البوت أرسله لكِ حبيبتكِ 🤍\nكل يوم راح تصلكِ مفاجآت صغيرة من قلبها إليكِ ✨"
    )

async def send_poem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    poem = random.choice(POEMS)
    await update.message.reply_text(poem)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global manal_chat_id
    manal_chat_id = update.effective_chat.id
    with open("chat_id.txt", "w") as f:
        f.write(str(manal_chat_id))

    text = update.message.text.strip()

    love_words = ["أحبك", "احبك", "بحبك", "أحبكِ", "احبج", "حبيبتي", "وحشتيني", "اشتقتلك", "اشتقت"]
    if any(word in text for word in love_words):
        await update.message.reply_text(random.choice(LOVE_REPLIES))
        return

    if any(word in text for word in ["صباح", "صبح"]):
        await update.message.reply_text("صباح النور يا منال 🌸 يومك مثل ابتسامتك — مضيء ودافئ 🤍")
        return

    if any(word in text for word in ["مساء", "مسا"]):
        await update.message.reply_text("مساء الورد يا أجمل شيء في يومي 🌙🤍")
        return

    if any(word in text for word in ["حزينة", "زعلانة", "تعبانة", "زهقت"]):
        await update.message.reply_text(
            "يا منال.. حزنكِ يؤلمني مثلكِ تماماً 🤍\nلكن تذكري — هذه اللحظة ستمضي، وأنتِ أقوى مما تعتقدين.\nوأنا هنا دائماً معكِ 🌙"
        )
        return

    await update.message.reply_text(random.choice(POEMS))

async def auto_poem(context: ContextTypes.DEFAULT_TYPE):
    try:
        with open("chat_id.txt", "r") as f:
            chat_id = f.read().strip()
        if chat_id:
            await context.bot.send_message(chat_id=int(chat_id), text=random.choice(POEMS))
    except:
        pass

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("poem", send_poem))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.job_queue.run_repeating(auto_poem, interval=random.randint(14400, 28800), first=60)
    print("البوت يعمل!")
    app.run_polling()

if __name__ == "__main__":
    main()
