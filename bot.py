from telegram.ext.updater import Updater
from telegram.ext.commandhandler import CommandHandler, Filters
from telegram.ext.messagehandler import MessageHandler
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.error import RetryAfter
from threading import Thread
from telegram import Bot
from _divar import Divar
import time

class BotDivar:
    _set_values = False
    _help_text = "Help:\n"\
                    "/set_values - set values\n"\
                    "/start_divar - start divar(after set values)\n"\
                    "/stop_divar - stop divar\n"
    def __init__(self, token, channel_id):
        self.token = token
        self.channel_id = channel_id
        self.updater = Updater(token, use_context=True)
        self.bot = Bot(token)
        self.dispatcher = self.updater.dispatcher
        
        self.dispatcher.add_handler(CommandHandler('start', self.start_bot))
        self.dispatcher.add_handler(CommandHandler('set_values', self.set_values))
        self.dispatcher.add_handler(CommandHandler('start_divar', self.start))
        self.dispatcher.add_handler(CommandHandler('stop_divar', self.stop_divar))
        self.dispatcher.add_handler(MessageHandler(Filters.text, self._reply))

    def start_polling(self):
        self.updater.start_polling()

    def start_bot(self, update: Update, context: CallbackContext):
        msg = "Please set values with /set_values"
        update.message.reply_text(msg)
        
    def set_values(self, update: Update, context: CallbackContext):
        self._set_values = True
        msg = "Please specify the values in the following format:\n"\
            "url!<url>\n"\
            "max_deposit!<max_deposit>(optional)\n"\
            "max_rent!<max_rent>(optional)"
        update.message.reply_text(msg)
        
    def send_msg(self, msg):
        # split size of msg to avoid telegram error
        try:
            self.bot.send_message(self.channel_id, msg)
        except RetryAfter as e:
            print(e.retry_after)
            time.sleep(e.retry_after+1)
            self.bot.send_message(self.channel_id, msg)
        
    def start(self, update: Update, context: CallbackContext):
        if "url" in self.__dict__:
            divar = Divar(url=self.url, callback=self.send_msg)
            self.thread = Thread(target=divar.eligible_home_rent(self.max_deposit, self.max_rent))
            self.thread.start()
            
    def stop_divar(self, update: Update, context: CallbackContext):
        if "thread" in self.__dict__:
            del self.thread
            
    def _reply(self, update: Update, context: CallbackContext):
        message = update.message.text
        if self._set_values:
            self._set_values = False
            try:
                # Convert to dict
                message = message.split("\n")
                message = {k: v for k, v in (x.split("!") for x in message)}
                self.url = message.get("url")
                self.max_deposit = float(message.get("max_deposit")) if message.get("max_deposit") else None
                self.max_rent = float(message.get("max_rent")) if message.get("max_rent") else None
                msg = "Values set successfully"
                update.message.reply_text(msg)
            except:
                update.message.reply_text("ERROR\nPlease contact ali :)")
        else:
            pass
    
if __name__ == "__main__":  
    token = "5575572260:AAHH9lBYfI7OPz8r9SkC0CcZbKRJAnKz7oc"
    chanel_id = "@farzamdivar"
    # chanel_id = "@aka1378"
    bot = BotDivar(token, channel_id=chanel_id)
    bot.start_polling()