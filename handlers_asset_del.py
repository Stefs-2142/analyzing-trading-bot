from models import Asset
from keyboards import main_shares_keyboard, cancel_keyboard
from telegram.ext import ConversationHandler


import logging


def delete_start(update, context):
    user_assets = Asset().get_user_assets(update.effective_user.id)
    reply_text = 'Вами отслеживаются следующие активы:\r\n\r\n'
    for i, asset in enumerate(user_assets, start=1):
        asset_name = asset[0]
        reply_text += f'{i}. {asset[0]}\r\n'
    reply_text += '\r\nДля удаления актива отправьте его номер ответным сообщением.'
    update.message.reply_text(
        reply_text, reply_markup=main_shares_keyboard()
    )    
    return delete_confirm
    
    
def delete_confirm(update, context):
    return ConversationHandler.END