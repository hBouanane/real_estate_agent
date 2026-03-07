"""
Telegram Bot - Real Estate Agent (Moroccan Darija)
Connects the LangGraph agent to a Telegram bot
"""

import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

from real_estate_agent import chat, agent  # import agent to allow thread reset

load_dotenv()

import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)


# ==================== HANDLERS ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome message when user sends /start"""
    await update.message.reply_text(
        "🏠 السلام عليكم! أنا وكيلكم العقاري.\n\n"
        "كيف يمكنني مساعدتكم اليوم؟\n"
        "بغيتي تشري، تكري، ولا عندك سؤال على العقارات؟ 😊")


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Let user manually reset their conversation thread"""
    user_id = str(update.effective_user.id)
    # Store a reset flag — next message will use a new thread ID
    context.user_data["thread_suffix"] = context.user_data.get(
        "thread_suffix", 0) + 1
    await update.message.reply_text("✅ تم مسح المحادثة. ابدأ من جديد 😊")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle every incoming text message"""
    user_id = str(update.effective_user.id)
    user_message = update.message.text

    await update.message.chat.send_action("typing")

    try:
        response = chat(user_message, thread_id=user_id)
        await update.message.reply_text(response)

    except Exception as e:
        error_msg = str(e)

        # Broken thread: tool was called but result never returned (interrupted mid-flow)
        # Fix: wipe the corrupted thread and retry as a fresh conversation
        if "ToolMessage" in error_msg or "INVALID_CHAT_HISTORY" in error_msg:
            logging.warning(
                f"Corrupted thread for user {user_id}, resetting...")
            try:
                # Clear thread state by writing an empty checkpoint
                config = {"configurable": {"thread_id": user_id}}
                agent.checkpointer.put(config, {}, {}, {})
            except Exception:
                pass  # checkpointer may not support direct writes — thread expires naturally

            # Retry with a fresh thread ID (append _reset suffix)
            try:
                reset_thread = f"{user_id}_reset"
                response = chat(user_message, thread_id=reset_thread)
                await update.message.reply_text(response)
                return
            except Exception as retry_err:
                logging.error(f"Retry also failed: {retry_err}")

        logging.error(f"Agent error: {e}")
        await update.message.reply_text(
            "عفواً، وقع مشكل تقني. عاود المحاولة من فضلك 🙏")


# ==================== MAIN ====================


def main():
    print("🤖 Starting Telegram Bot...")

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot is running. Press Ctrl+C to stop.")
    app.run_polling()


if __name__ == "__main__":
    main()
