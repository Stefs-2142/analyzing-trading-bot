﻿from keyboards import main_shares_keyboard, main_menu_keyboard
from keyboards import main_binance_keyboard
from telegram.ext import ConversationHandler


def greet_user(update, context):
    # Дописать нормальный текст
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


def unknown_text(update, context):
    """
    Функция, обрабатывающая любой текст, который не является текстом из
    кнопок, которые начинают Conversation
    """
    reply = ("Нажмите на одну из доступных кнопок")
    update.message.reply_text(reply, reply_markup=main_menu_keyboard())


def operation_cancel(update, context):
    """
    Функция fallback команды "Отмена" - удаляет данные из контекстов и
    завершает текущий Conversation
    """

    # shares_context
    context.user_data.pop('ticker', None)
    context.user_data.pop('candidates', None)
    context.user_data.pop('action', None)

    # binance_context
    context.user_data.pop('ticker_pair', None)
    context.user_data.pop('order_side', None)
    context.user_data.pop('order_type', None)
    context.user_data.pop('quantity', None)
    context.user_data.pop('balance', None)

    update.message.reply_text(
        'Операция прервана', reply_markup=main_menu_keyboard()
    )
    return ConversationHandler.END


def show_help(update, context):
    with open('help.txt', 'r') as stocks_info:
        reply_text = stocks_info.read()
    update.message.reply_text(reply_text)
