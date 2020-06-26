# Функция-обработчик команды /start
def greet_user(update, context):
    # Дописать нормальный текст
    update.message.reply_text("Привет!")


# Функция-обработчик команды /start
def unknown_text(update, context):
    reply = ("Команда не найдена, пожалуйста, "
             "нажмите на одну из доступных кнопок")
    update.message.reply_text(reply)
