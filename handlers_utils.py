from keyboards import main_shares_keyboard


# Функция-обработчик команды /start
def greet_user(update, context):
    # Дописать нормальный текст
    update.message.reply_text("Привет!", reply_markup=main_shares_keyboard())


# Функция-обработчик команды /start
def unknown_text(update, context):
    reply = ("Команда не найдена, пожалуйста, "
             "нажмите на одну из доступных кнопок")
    update.message.reply_text(reply, reply_markup=main_shares_keyboard())


def operation_cancel(update, context):
    context.user_data.pop('ticker', None)
    update.message.reply_text(
        'Операция прервана', reply_markup=main_shares_keyboard()
    )
    return ConversationHandler.END
