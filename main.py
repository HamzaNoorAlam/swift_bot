from flask import Flask, request
import telebot
import gspread
from oauth2client.service_account import ServiceAccountCredentials

TOKEN = '7729548281:AAGKGkf8rz83mK5Sh-a4vAZnqgZRkxGc2zM'
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("SwiftTracker").sheet1

@app.route('/swift_bot', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200

@bot.message_handler(func=lambda m: True)
def handle_query(message):
    query = message.text.strip()
    data = sheet.get_all_records()
    for row in data:
        if row['UETR'] == query:
            reply = f"📄 *UETR Result:*\n\n🔁 UETR: `{row['UETR']}`\n📆 Date: {row['Date']}\n⏰ Time: {row['Time']}\n💶 Amount: {row['Amount (EUR)']}\n📌 Status: {row['Status']}"
            bot.send_message(message.chat.id, reply, parse_mode='Markdown')
            return
    bot.send_message(message.chat.id, "❌ UETR not found.")

if __name__ == "__main__":
    app.run()
