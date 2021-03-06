﻿from functools import wraps

from telegram import ParseMode
from telegram.ext import ConversationHandler

from keyboards import (main_binance_keyboard, main_menu_keyboard,
                       main_shares_keyboard, main_crypto_shares_keyboard)

from settings import ADMIN_ID


def autorization(func):
    """
    Данный декоратор проверяет user_id пользователя.
    Если пользоветля нет в списке админов - часть функционала
    недостпуна, например выставление ордеров.
    """

    @wraps(func)
    def wrapper(update, context):
        if update.effective_user['id'] == ADMIN_ID:
            return func(update, context)
        else:
            message = '❌ Недоступно в demo-режиме.\n Для получения доступа обратитесь к https://t.me/Stefs'
            update.message.reply_text(
                message,
                reply_markup=main_binance_keyboard())
    return wrapper


def greet_user(update, context):

    clear_all_shares(update, context)
    clear_all_crypto(update, context)

    try:
        name = update.effective_user['first_name']
    except KeyError:
        name = update.effective_user['username']

    update.message.reply_text(
        f"Привет <b>{name}</b>! Выбери нужный раздел.",
        reply_markup=main_menu_keyboard(),
        parse_mode=ParseMode.HTML)


def shares_comands(update, context):
    """
    Функция, представляет доступные
    команды для работы с акциями
    Добавляем флаг location для отслеживания местоположения
    пользоателя: В Crypto-разделе или в Classic-разделе.
    """
    context.user_data['location'] = 'classic'
    reply = 'Доступные команды.'
    update.message.reply_text(reply, reply_markup=main_shares_keyboard())


def binance_comands(update, context):
    """
    Функция, представляет доступные
    команды для работы с Binance
    Добавляем флаг location для отслеживания местоположения
    пользоателя: В Crypto-разделе или в Classic-разделе.
    """
    context.user_data['location'] = 'crypto'
    reply = 'Доступные команды.'
    update.message.reply_text(reply, reply_markup=main_binance_keyboard())
    return ConversationHandler.END


def crypto_shares_comands(update, context):
    """
    Функция, представляет доступные
    команды для работы с уведомлениями Binance,
    также вызывается из fallback команды 'Назад'.
    Удаляет данные из контекстов и
    завершает текущий Conversation
    """

    reply = 'Доступные команды.'
    update.message.reply_text(reply, reply_markup=main_crypto_shares_keyboard())
    clear_all_shares(update, context)
    clear_all_crypto(update, context)
    return ConversationHandler.END


def unknown_text(update, context):
    """
    Функция, обрабатывающая любой текст, который не является текстом из
    кнопок, которые начинают Conversation
    """
    reply = ("Выберите доступный раздел.")
    update.message.reply_text(reply, reply_markup=main_menu_keyboard())


def clear_all_crypto(update, context):
    """Очищает данные из контекста."""

    context.user_data.pop('ticker_pair', None)
    context.user_data.pop('order_side', None)
    context.user_data.pop('order_type', None)
    context.user_data.pop('quantity', None)
    context.user_data.pop('balance', None)
    context.user_data.pop('price', None)


def clear_all_shares(update, context):
    """Очищает данные из контекста."""

    context.user_data.pop('ticker', None)
    context.user_data.pop('candidates', None)
    context.user_data.pop('action', None)


def operation_cancel(update, context):
    """
    Функция fallback команды "Отмена" - удаляет данные из контекстов и
    завершает текущий Conversation
    """

    # shares_context
    clear_all_shares(update, context)

    # binance_context
    clear_all_crypto(update, context)

    update.message.reply_text(
        'Операция прервана', reply_markup=main_menu_keyboard()
    )
    return ConversationHandler.END


def back_to_menu(update, context):
    """
    Функция fallback команды "Назад" - удаляет данные из контекстов и
    завершает текущий Conversation
    В зависимости от местонахождения юзера, в меню Binance (crypto) или
    в классических инструментах (classic) - возвращает в соотеветсвующую
    клавиуатуру, меню.
    """
    if context.user_data.get('location') == 'crypto':
        update.message.reply_text(
            'Доступные команды', reply_markup=main_binance_keyboard()
            )
    else:
        update.message.reply_text(
            'Доступные команды', reply_markup=main_shares_keyboard()
            )

    # shares_context
    clear_all_shares(update, context)

    # binance_context
    clear_all_crypto(update, context)

    return ConversationHandler.END


def show_help(update, context):
    """Функция вызывающая подсказку."""
    with open('help.txt', 'r') as stocks_info:
        reply_text = stocks_info.read()
    update.message.reply_text(reply_text)
