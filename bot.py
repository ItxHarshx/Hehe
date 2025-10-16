from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

# --- Replace this with your bot token ---
BOT_TOKEN = "7875224003:AAFW-TztpFggianZrar9pT9UcTte6pY5sdo"

# Store games in a dictionary: chat_id -> board and turn
games = {}

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "👋 Welcome to Tic-Tac-Toe!\nUse /newgame to start a game."
    )

def newgame(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    games[chat_id] = {
        "board": [" "] * 9,  # 3x3 board
        "turn": "X"
    }
    update.message.reply_text("🆕 New game started! X goes first.\nUse /move <position> (1-9).")
    show_board(update, chat_id)

def show_board(update: Update, chat_id):
    board = games[chat_id]["board"]
    text = f"""
{board[0]} | {board[1]} | {board[2]}
---------
{board[3]} | {board[4]} | {board[5]}
---------
{board[6]} | {board[7]} | {board[8]}
"""
    update.message.reply_text(text)

def move(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    if chat_id not in games:
        update.message.reply_text("No game in progress. Use /newgame to start.")
        return

    try:
        pos = int(context.args[0]) - 1
        if pos < 0 or pos > 8:
            raise ValueError
    except (IndexError, ValueError):
        update.message.reply_text("Please provide a valid position (1-9).")
        return

    board = games[chat_id]["board"]
    turn = games[chat_id]["turn"]

    if board[pos] != " ":
        update.message.reply_text("❌ That spot is already taken!")
        return

    board[pos] = turn

    if check_winner(board, turn):
        show_board(update, chat_id)
        update.message.reply_text(f"🎉 {turn} wins!")
        del games[chat_id]
        return

    if " " not in board:
        show_board(update, chat_id)
        update.message.reply_text("⚖️ It's a tie!")
        del games[chat_id]
        return

    # Switch turn
    games[chat_id]["turn"] = "O" if turn == "X" else "X"
    show_board(update, chat_id)
    update.message.reply_text(f"It's {games[chat_id]['turn']}'s turn!")

def check_winner(board, player):
    win_conditions = [
        [0,1,2],[3,4,5],[6,7,8],  # rows
        [0,3,6],[1,4,7],[2,5,8],  # columns
        [0,4,8],[2,4,6]           # diagonals
    ]
    return any(all(board[i]==player for i in cond) for cond in win_conditions)

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("newgame", newgame))
    dp.add_handler(CommandHandler("move", move))

    updater.start_polling()
    print("🤖 Tic-Tac-Toe Bot is running...")
    updater.idle()

if __name__ == "__main__":
    main()
