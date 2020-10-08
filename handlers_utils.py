﻿from keyboards import main_shares_keyboard, main_menu_keyboard
from keyboards import main_binance_keyboard
from keyboards import main_krypto_shares_keyboard
from telegram.ext import ConversationHandler


def greet_user(update, context):
    # Дописать нормальный текст

    clear_all_shares(update, context)
    clear_all_crypto(update, context)

    update.message.reply_text(
        "Привет! Выбери нужный раздел.", reply_markup=main_menu_keyboard())


def shares_comands(update, context):
    """
    Функция, представляет доступные
    команды для работы с акциями
    """
    reply = 'Доступные команды.'
    update.message.reply_text(reply, reply_markup=main_shares_keyboard())


def binance_comands(update, context):
    """
    Функция, представляет доступные
    команды для работы с Binance
    """
    reply = 'Доступные команды.'
    update.message.reply_text(reply, reply_markup=main_binance_keyboard())


def crypto_shares_comands(update, context):
    """
    Функция, представляет доступные
    команды для работы с уведомлениями Binance
    """
    reply = 'Доступные команды.'
    update.message.reply_text(reply, reply_markup=main_krypto_shares_keyboard())


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


def show_help(update, context):
    """Функция вызывающая подсказку."""
    with open('help.txt', 'r') as stocks_info:
        reply_text = stocks_info.read()
    update.message.reply_text(reply_text)
