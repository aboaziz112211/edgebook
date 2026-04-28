import os, base64, ctypes, logging
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ── CONFIG ────────────────────────────────────────────────────
BOT_TOKEN   = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
ADMIN_ID    = int(os.environ.get("ADMIN_ID", "0"))   # your Telegram user ID
SALT        = "CEai2025xQ"
TRIAL_MONTHS = 6

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
log = logging.getLogger(__name__)

# ── SAME CHECKSUM LOGIC AS JS ─────────────────────────────────
def _cs(s: str) -> str:
    h = 0
    for c in s:
        h = ctypes.c_int32(ctypes.c_int32(31 * h).value + ord(c)).value
    return format(ctypes.c_uint32(h).value, "x")

def generate_ext_code(days: int = 180) -> tuple[str, str]:
    exp = datetime.now() + timedelta(days=days)
    exp_str = exp.strftime("%Y-%m-%d")
    payload = f"ext|{exp_str}"
    raw = f"{payload}|{_cs(payload + SALT)}"
    key = base64.b64encode(raw.encode()).decode()
    return key, exp_str

# ── COMMANDS ──────────────────────────────────────────────────
async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    kb = [[InlineKeyboardButton("📊 EdgeBook Info", url="https://t.me/CHARTEDGEAI")]]
    await update.message.reply_text(
        f"👋 Welcome to *ChartEdge AI*, {user.first_name}!\n\n"
        "EdgeBook is a professional trading dashboard for daily traders.\n\n"
        "📌 *Free trial:* 6 months from first launch\n"
        "🔄 *To extend:* Send a message here and the creator will send you an extension code\n\n"
        "Type /help to see available commands.",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(kb)
    )

async def cmd_help(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    is_admin = update.effective_user.id == ADMIN_ID
    msg = (
        "📋 *Available Commands*\n\n"
        "/start — Welcome message\n"
        "/status — Check your trial status\n"
        "/extend — Request a trial extension\n"
    )
    if is_admin:
        msg += (
            "\n🔑 *Admin Commands*\n"
            "/gen [days] — Generate extension code (default 180 days)\n"
            "/gen 90 — Generate 90-day extension code\n"
        )
    await update.message.reply_text(msg, parse_mode="Markdown")

async def cmd_status(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⏳ *Trial Status*\n\n"
        "Your trial start date is recorded in your browser's local storage.\n"
        "Open EdgeBook and check the warning banner at the top — it will show how many days you have left.\n\n"
        "Need an extension? Type /extend",
        parse_mode="Markdown"
    )

async def cmd_extend(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    # If admin, generate immediately
    if user.id == ADMIN_ID:
        await update.message.reply_text(
            "You are the admin. Use /gen [days] to generate an extension code.\n"
            "Example: /gen 180"
        )
        return
    # Notify admin
    msg = (
        f"🔔 *Extension Request*\n\n"
        f"👤 User: {user.full_name}\n"
        f"🆔 ID: `{user.id}`\n"
        f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        f"Use /gen to generate a code and send it to this user."
    )
    try:
        await ctx.bot.send_message(ADMIN_ID, msg, parse_mode="Markdown")
    except Exception:
        pass
    await update.message.reply_text(
        "✅ Your extension request has been sent to the creator.\n\n"
        "You will receive an extension code shortly. "
        "Paste it into the expired screen in EdgeBook to unlock another 6 months.",
        parse_mode="Markdown"
    )

async def cmd_gen(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ Admin only.")
        return
    days = 180
    if ctx.args:
        try: days = int(ctx.args[0])
        except ValueError: pass
    code, exp_str = generate_ext_code(days)
    await update.message.reply_text(
        f"🔑 *Extension Code Generated*\n\n"
        f"📅 Extends to: `{exp_str}` (+{days} days)\n\n"
        f"*Code (tap to copy):*\n`{code}`\n\n"
        f"Send this code to the user. They paste it into the expired screen in EdgeBook.",
        parse_mode="Markdown"
    )

async def handle_message(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text or ""
    # Notify admin of any user message
    if user.id != ADMIN_ID:
        msg = (
            f"💬 *Message from user*\n\n"
            f"👤 {user.full_name} (`{user.id}`)\n"
            f"📝 {text}"
        )
        try:
            await ctx.bot.send_message(ADMIN_ID, msg, parse_mode="Markdown")
        except Exception:
            pass
        await update.message.reply_text(
            "Thanks for reaching out! The creator has been notified and will get back to you shortly.\n\n"
            "If you need an extension code, type /extend"
        )

# ── MAIN ──────────────────────────────────────────────────────
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start",  cmd_start))
    app.add_handler(CommandHandler("help",   cmd_help))
    app.add_handler(CommandHandler("status", cmd_status))
    app.add_handler(CommandHandler("extend", cmd_extend))
    app.add_handler(CommandHandler("gen",    cmd_gen))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    log.info("ChartEdge bot starting...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
