﻿from models import Asset
from keyboards import main_shares_keyboard, cancel_keyboard, edit_del_keyboard
from keyboards import edit_choose_keyboard
from telegram.ext import ConversationHandler


import logging


def edit_delete_start(update, context):
    user_assets = Asset().get_user_assets(update.effective_user.id)
    if len(user_assets) == 0:
        update.message.reply_text('У вас нет отслеживаемых инструментов')
        return ConversationHandler.END
    context.user_data['candidates'] = []

    reply_text = 'Вами отслеживаются следующие активы:\r\n\r\n'
    # [[1, 'YNDX.ME'], [2, 'SBER.ME'], [3, 'RSTI.ME']]
    for i, asset in enumerate(user_assets, start=1):
        asset_name = asset[0]
        context.user_data['candidates'].append([i, asset_name])
        reply_text += f'{i}. {asset[0]}\r\n'
    reply_text += (
        '\r\nДля изменения или удаления актива '
        'отправьте его номер или название ответным сообщением.'
    )
    update.message.reply_text(
        reply_text, reply_markup=cancel_keyboard()
    )
    return edit_delete_choose


def edit_delete_choose(update, context):
    user_assets = context.user_data['candidates']
    try:
        selected = int(update.message.text)
        del_ticker = [
            i[1] for i in user_assets if i[0] == selected
        ]
    except ValueError:
        selected = update.message.text
        del_ticker = [
            i[1] for i in user_assets if i[1] == selected
        ]
    if del_ticker:
        context.user_data['candidates'] = del_ticker[0]
        update.message.reply_text(
            'Укажите желаемое действие',
            reply_markup=edit_del_keyboard()
        )
        return delete_price_choose
    else:
        update.message.reply_text(
            'Введеный номер или тикер не найден - повторите ввод.',
            reply_markup=cancel_keyboard()
        )
        return edit_delete_choose


def delete_price_choose(update, context):
    if update.message.text == 'Удалить':
        Asset().del_asset(update.effective_user.id, context.user_data['candidates'])
        update.message.reply_text(
            'Инструмент успешно удален!', reply_markup=main_shares_keyboard()
        )
        logging.info(
            f'Deleted asset {del_ticker} for user {update.effective_user.id}'
        )
        context.user_data.pop('candidates', None)
        return ConversationHandler.END
    else:
        update.message.reply_text(
            'Укажите стоимость для изменения', reply_markup=edit_choose_keyboard()
        )
        return edit_choose_confirm


def edit_choose_confirm(update, context):
    if update.message.text == 'Максимальная':
        context.user_data['action'] = True
    elif  update.message.text == 'Минимальная':
        context.user_data['action'] = False
    update.message.reply_text(
        'Укажите новую стоимость', reply_markup=cancel_keyboard()
    )
    return edit_price

def edit_price(update, context):
    error_text = (
        'Повторите ввод или нажмите кнопку "Отмена".'
    )
    try:
        new_price = float(update.message.text.replace(',', '.'))
    except ValueError:
        update.message.reply_text(
            f'В введенной стоимости присутствуют ошибки. {error_text}',
            reply_markup=cancel_keyboard()
        )
        return edit_price
    if new_price <= 0:
        update.message.reply_text(
            f'Стоимость не может быть равной или ниже нуля. {error_text}',
            reply_markup=cancel_keyboard()
        )
        return edit_price
    else:
        user_id = update.effective_user.id
        ticker = context.user_data['candidates']
        if context.user_data['action'] == True:
            Asset().edit_t_price(user_id, ticker, new_price)
            logging.info(
                f'Target price for asset {ticker} was updated by user {user_id}'
            )
        else:
            Asset().edit_m_price(user_id, ticker, new_price)
            logging.info(
                f'Min price for asset {ticker} was updated by user {user_id}'
            )
        context.user_data.pop('candidates', None)
        context.user_data.pop('action', None)
        update.message.reply_text(
            'Стоимость успешно изменена!',
            reply_markup=main_shares_keyboard()
        )
        return ConversationHandler.END
