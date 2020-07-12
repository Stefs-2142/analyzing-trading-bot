from keyboards import main_shares_keyboard
from telegram.ext import ConversationHandler


def greet_user(update, context):
    # Дописать нормальный текст
    update.message.reply_text("Привет!", reply_markup=main_shares_keyboard())


def unknown_text(update, context):
    """
    Функция, обрабатывающая любой текст, который не является текстом из
    кнопок, которые начинают Conversation
    """
    reply = ("Нажмите на одну из доступных кнопок")
    update.message.reply_text(reply, reply_markup=main_shares_keyboard())


def operation_cancel(update, context):
    """
    Функция fallback команды "Отмена" - удаляет данные из контекстов и
    завершает текущий Conversation
    """
    context.user_data.pop('ticker', None)
    context.user_data.pop('candidates', None)
    context.user_data.pop('action', None)
    update.message.reply_text(
        'Операция прервана', reply_markup=main_shares_keyboard()
    )
    return ConversationHandler.END
