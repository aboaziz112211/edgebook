# ChartEdge Bot — Setup Guide

## Step 1 — Create the bot on Telegram
1. Open Telegram → search **@BotFather**
2. Send `/newbot`
3. Name it: `ChartEdge AI`
4. Username: `chartedgeai_bot` (or any available name)
5. BotFather gives you a **token** — copy it

## Step 2 — Get your Telegram user ID
1. Search **@userinfobot** on Telegram
2. Send `/start` — it replies with your numeric ID (e.g. `123456789`)

## Step 3 — Deploy on Railway (free)
1. Go to **railway.app** → sign up (free)
2. Click **New Project → Deploy from GitHub repo**
3. Upload this folder to a GitHub repo first, OR use Railway CLI
4. Set these environment variables in Railway:
   - `BOT_TOKEN` = the token from BotFather
   - `ADMIN_ID` = your numeric Telegram ID

## Step 4 — Done
The bot is live. Users message it, you get notified, you run `/gen` to create extension codes.

## Bot Commands
| Command | Who | What |
|---------|-----|------|
| `/start` | Anyone | Welcome message |
| `/help` | Anyone | List commands |
| `/status` | Anyone | Trial status info |
| `/extend` | Anyone | Sends you an alert to generate a code |
| `/gen [days]` | You only | Generates an extension code |

## How extension works
1. User's trial expires → they see the expired screen in EdgeBook
2. They message your bot → you get a Telegram notification
3. You reply with `/gen 180` → bot generates a code and shows it to you
4. You forward the code to the user
5. User pastes it in EdgeBook → unlocked for another 6 months
