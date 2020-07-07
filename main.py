from handlers_utils import greet_user, unknown_text
from models import User, Asset
from settings import API_KEY
from telegram.ext import Updater, CommandHandler
from telegram.ext import MessageHandler, Filters, ConversationHandler
from ticker_utils import get_ticker_price, ticker_pricing

import datetime
import logging
import settings


logging.basicConfig(filename='bot.log', level=logging.INFO)



def add_start(update, context):
    update.message.reply_text('Введите название тикера')
    context.user_data['ticker'] = [update.effective_user.id] 
    return add_step_1
    
def add_step_1(update, context):
    ticker = update.message.text.split()[0]
    ticker_current_price = get_ticker_price(ticker)
    if ticker_current_price is False:
        update.message.reply_text(
            'Введенный тикер не найден. Повторите ввод '
            'или нажмите кнопку "Отмена" чтобы прервать '
            'выполнение операции'
        )
        return add_step_1
    current_date = f"{datetime.datetime.now():%Y-%m-%d}"
    context.user_data['ticker'].extend([
        ticker, False, current_date, ticker_current_price
    ])
    update.message.reply_text(
        f'Текущая стоимость {ticker} - {ticker_current_price}. '
        'Если вы хотите отслеживать иную начальную стоимость - '
        'отправьте её ответным сообщением. Для продолжения нажмите'
        ' на кнопку "Использовать текущую цену"'
    )
    return add_step_2

def add_step_2(update, context):
    if update.message.text != 'Использовать текущую цену':
        try:
            ticker_current_price = float(update.message.text)
        except ValueError:
            update.message.reply_text(
                'В введенной стоимости присутствуют ошибки. '
                'Повторите ввод или нажмите кнопку '
                '"Использовать текущую цену".'
            )
            return add_step_2
        context.user_data['ticker'][2] = ticker_current_price
    else:
        print(context.user_data['ticker'])
        return ConversationHandler.END 
    
    
def add_step_3(update, context):
    pass    
    
def operation_cancel(update, context):
    context.user_data.pop('ticker', None) 
    return ConversationHandler.END    

def main():
    atb_bot = Updater(settings.API_KEY, use_context=True)
    
    dp = atb_bot.dispatcher
    
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(ConversationHandler(
        entry_points = [MessageHandler(Filters.regex('Добавить\s+актив'), add_start)],
        states = {
            add_step_1:[
                MessageHandler(Filters.text & (~Filters.regex('(Отмена)')), add_step_1)
            ],
            add_step_2:[
                MessageHandler(Filters.text & (~Filters.regex('(Отмена)')), add_step_2)
            ],
            add_step_3:[
                MessageHandler(Filters.text & (~Filters.regex('(Отмена)')), add_step_3)
            ],
        },
        fallbacks = [MessageHandler(Filters.regex('(Отмена)'), operation_cancel)]
    ))
    dp.add_handler(MessageHandler(Filters.text, unknown_text))
    
    logging.info("Bot started")
    atb_bot.start_polling()
    atb_bot.idle()


if __name__ == "__main__":
    main()
