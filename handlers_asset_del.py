from models import Asset
from keyboards import main_shares_keyboard, cancel_keyboard
from telegram.ext import ConversationHandler


import logging


def delete_start(update, context):
    user_assets = Asset().get_user_assets(update.effective_user.id)
    if len(user_assets) == 0:
        update.message.reply_text('У вас нет отслеживаемых инструментов')
        return ConversationHandler.END
    context.user_data['del_candidates'] = []

    reply_text = 'Вами отслеживаются следующие активы:\r\n\r\n'
    # [[1, 'YNDX.ME'], [2, 'SBER.ME'], [3, 'RSTI.ME']]
    for i, asset in enumerate(user_assets, start=1):
        asset_name = asset[0]
        context.user_data['del_candidates'].append([i, asset_name])
        reply_text += f'{i}. {asset[0]}\r\n'
    reply_text += '\r\nДля удаления актива отправьте его номер ответным сообщением.'

    update.message.reply_text(
        reply_text, reply_markup=cancel_keyboard()
    )
    return delete_confirm


def delete_confirm(update, context):
    try:
        selected = int(update.message.text)
        del_ticker = [i[1] for i in context.user_data['del_candidates'] if i[0] == selected]
    except ValueError:
        selected = update.message.text
        del_ticker = [i[1] for i in context.user_data['del_candidates'] if i[1] == selected]

    if del_ticker:
        Asset().del_asset(update.effective_user.id, del_ticker[0])
        update.message.reply_text(
            'Инструмент успешно удален!', reply_markup=main_shares_keyboard()
        )
        logging.info(
            f'Deleted asset {del_ticker} for user {update.effective_user.id}'
        )
        context.user_data.pop('del_candidates', None)
        return ConversationHandler.END
    else:
        update.message.reply_text(
            'Введеный номер или тикер не найден - повторите ввод.', reply_markup=cancel_keyboard()
        )
        return delete_confirm
