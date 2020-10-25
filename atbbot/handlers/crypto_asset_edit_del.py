import logging

from telegram.ext import ConversationHandler

from db.models import Asset

from keyboards import (back_keyboard, edit_del_crypto_keyboard,
                       edit_choose_crypto_keyboard, main_crypto_shares_keyboard)

from .utils import clear_all_crypto, clear_all_shares


def edit_delete_start_crypto(update, context):
    """
    Выгружаем из БД отслеживаемые пользователем крипто инструменты,
    если у пользователя таких нет - сообщаем ему об этом
    """
    user_assets = Asset().get_user_assets(update.effective_user.id, False)
    if not user_assets:
        update.message.reply_text('У вас нет отслеживаемых инструментов.')
        return ConversationHandler.END
    context.user_data['candidates'] = []

    reply_text = 'Вами отслеживаются следующие активы:\r\n\r\n'
    """
    Проходим циклом по выгруженным активам, выводим их пользователю и
    записываем в контекст список состоящий из номера актива
    и его идентификатора, получаем примерно такой список на выходе
    [[1, 'YNDX.ME'], [2, 'SBER.ME'], [3, 'RSTI.ME']]
    """
    for i, asset in enumerate(user_assets, start=1):
        asset_name = asset[0]
        context.user_data['candidates'].append([i, asset_name])
        reply_text += f'{i}. {asset[0]}\r\n'
    reply_text += (
        '\r\nДля изменения или удаления актива '
        'отправьте его номер или название ответным сообщением.'
    )
    update.message.reply_text(
        reply_text, reply_markup=back_keyboard()
    )
    return '1'


def edit_delete_choose_crypto(update, context):
    user_assets = context.user_data['candidates']
    """
    Ловим от пользоватея номер или название актива, сначала
    проверяем что именно отправил пользователь - номер или
    идентфикатор, а потом проверяем что такая сущность
    присутствует в списке, который лежит в контексте, т.е.
    проверяем что пользователь ввел корректные данные
    """
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
    """
    Если пользователь ввел правильный номер/идентификатор, то
    переписываем переменную в контекста на название тикера,
    которым юзер хочет произвести действие
    Запрашиваем у пользователя желаемое действие
    """
    if del_ticker:
        context.user_data['candidates'] = del_ticker[0]
        update.message.reply_text(
            'Укажите желаемое действие',
            reply_markup=edit_del_crypto_keyboard()
        )
        return '2'
    else:
        update.message.reply_text(
            'Введеный номер или тикер не найден - повторите ввод.',
            reply_markup=back_keyboard()
        )
        return '1'


def delete_price_choose_crypto(update, context):
    """
    Если пользователь хочет удалить инструмент из отслеживаемых -
    делаем это и уведомляет пользователя, дополнительные проверки
    отсутствуют, т.к. данные об инструменте уже завалидированы ранее
    """
    if update.message.text == 'Delete':
        Asset().del_asset(
            update.effective_user.id, context.user_data['candidates']
        )
        update.message.reply_text(
            'Инструмент успешно удален!', reply_markup=main_crypto_shares_keyboard()
        )
        logging.info(
            f"Deleted asset {context.user_data['candidates']} for user {update.effective_user.id}"
        )
        clear_all_shares(update, context)
        clear_all_crypto(update, context)
        return ConversationHandler.END
    elif update.message.text == 'Edit':
        """
        Если пользователь хочет изменить данные об инструменте - запрашиваем
        какие именно
        """
        update.message.reply_text(
            'Укажите стоимость для изменения',
            reply_markup=edit_choose_crypto_keyboard()
        )
        return '3'
    else:
        update.message.reply_text(
            'Выберите доступную команду.', reply_markup=back_keyboard()
            )
        return '2'


def edit_choose_confirm_crypto(update, context):
    """
    Получаем ответ от пользователя и записываем его в
    новую переменную контекста в виде True/False
    """
    if update.message.text == 'Max':
        context.user_data['action'] = True
    elif update.message.text == 'Min':
        context.user_data['action'] = False
    update.message.reply_text(
        'Укажите новую стоимость', reply_markup=back_keyboard()
    )
    return '4'


def edit_price_crypto(update, context):
    """
    Выполняем проверки на корректность ввода пользователя:
    является ли ввод float и не меньше или равен он нулю
    """
    error_text = (
        'Повторите ввод или нажмите кнопку "Отмена".'
    )
    try:
        new_price = float(update.message.text.replace(',', '.'))
    except ValueError:
        update.message.reply_text(
            f'В введенной стоимости присутствуют ошибки. {error_text}',
            reply_markup=back_keyboard()
        )
        return '4'
    if new_price <= 0:
        update.message.reply_text(
            f'Стоимость не может быть равной или ниже нуля. {error_text}',
            reply_markup=back_keyboard()
        )
        return '4'
    # Если всё ок - изменяем стоимость соответствующим методом класса
    user_id = update.effective_user.id
    ticker = context.user_data['candidates']

    if context.user_data['action']:
        Asset().edit_t_price(user_id, ticker, new_price)
        logging.info(
            f'Target price for {ticker} was updated by user {user_id}'
        )
    else:
        Asset().edit_m_price(user_id, ticker, new_price)
        logging.info(
            f'Min price for {ticker} was updated by user {user_id}'
        )
    update.message.reply_text(
        'Стоимость успешно изменена!',
        reply_markup=main_crypto_shares_keyboard()
    )
    clear_all_shares(update, context)
    return ConversationHandler.END
