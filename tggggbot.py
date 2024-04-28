import telebot
import requests

TOKEN = '7001145529:AAEM6n1G__XpOZgef7UyDmfPjb0fs2Jp4ec'
ADMIN_CODE = '123456'
API_URL = 'https://pay.raif.ru/pay/rfuture/'
API_KEY = 'AD9728855389407D9CD36C52E50DB2FA'

def check_payment_status(payment_id):

    return

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Введите код доступа:')

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == ADMIN_CODE:
        bot.send_message(message.chat.id, 'Доступ разрешен. Введите код товара для проверки статуса оплаты:')
        bot.register_next_step_handler(message, handle_product_code)
    else:
        bot.reply_to(message, 'Неверный код доступа.')

def get_account_balance(account_id):
    headers = {'Authorization': f'Bearer {API_KEY}'}
    response = requests.get(f'{API_URL}accounts/{account_id}/balance', headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data['balance']
    else:
        return None

account_balance = get_account_balance('1234567890')
if account_balance:
    print(f'Баланс счета: {account_balance}')
else:
    print('Ошибка получения баланса счета.')

def handle_product_code(message):
    product_code = message.text
    payment_status = check_payment_status(product_code)
    if payment_status == 'paid':
        bot.reply_to(message, f'Товар с кодом {product_code} оплачен.')
    else:
        bot.reply_to(message, f'Товар с кодом {product_code} не оплачен.')



bot.polling()

