from telegram import Update, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ConversationHandler, CommandHandler, ContextTypes, MessageHandler, filters

from handlers.base_handler import BaseHandler

PUBG_PICK, ERANGEL_OR_SANYK, SOLO, BUSH, ENERGETIK, SANYK = range(6)


class AdventureHandler(BaseHandler):
    @classmethod
    def register(cls, app):
        conversation_handler = ConversationHandler(
            entry_points=[CommandHandler('startgame', cls.startgame)],
            states={
                PUBG_PICK: [MessageHandler(filters.Regex('^(Viktor|Anna)$'), cls.PUBG_PICK)],
                ERANGEL_OR_SANYK: [MessageHandler(filters.Regex('^(SOLO|SANYK)$'),
                                                       cls.ERANGEL_OR_SANYK)],
                SOLO: [MessageHandler(filters.Regex('^(Bush|ENERGETIK)$'), cls.SOLO)],
                SANYK: [MessageHandler(filters.Regex('^(PassToGoal|PassTeamBro)$'), cls.SANYK)],
            },
            fallbacks=[CommandHandler('exit', cls.exit)]
        )

        app.add_handler(conversation_handler)

    @staticmethod
    async def startgame(update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [InlineKeyboardButton('Viktor'), InlineKeyboardButton('Anna')],
            [InlineKeyboardButton('/exit'), InlineKeyboardButton('/startgame')]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

        await update.message.reply_text(
            f'Привіт {update.effective_user.first_name}! Якого персонажа ти вибереш?',
            reply_markup=reply_markup)

        return PUBG_PICK

    @staticmethod
    async def exit(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(f'Ви вийшли з розмови.')

        return ConversationHandler.END

    @staticmethod
    async def PUBG_PICK(update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [InlineKeyboardButton('SOLO'), InlineKeyboardButton('SANYK')],
            [InlineKeyboardButton('/exit'), InlineKeyboardButton('/startgame')]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

        await update.message.reply_text(
            f'Який режим вибирете?',
            reply_markup=reply_markup)

        PUBG_PICK = update.message.text
        context.user_data['PUBG_pick'] = PUBG_PICK

        return ERANGEL_OR_SANYK

    @staticmethod
    async def ERANGEL_OR_SANYK(update: Update, context: ContextTypes.DEFAULT_TYPE):

        ERANGEL_OR_SANYK = update.message.text
        context.user_data['ERANGEL_OR_SANYK'] = ERANGEL_OR_SANYK

        if update.message.text == 'SOLO':
            keyboard = [
                [InlineKeyboardButton('Bush'), InlineKeyboardButton('ENERGETIK')],
                [InlineKeyboardButton('/exit'), InlineKeyboardButton('/startgame')]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

            await update.message.reply_text(text=f"Вітаю {update.effective_user.first_name}!"
                                                 f" Ви вибрали {context.user_data['ERANGEL_OR_SANYK']}!"
                                                 f" І йдете туда за {context.user_data['pubg_pick']}",
                                                 reply_markup=reply_markup)

            ERANGEL_OR_SANYK = update.message.text
            context.user_data['ERANGEL_OR_SANYK'] = ERANGEL_OR_SANYK

            return SOLO

        else:
            keyboard = [
                [InlineKeyboardButton('PassToGoal'), InlineKeyboardButton('PassTeamBro')],
                [InlineKeyboardButton('/exit'), InlineKeyboardButton('/startgame')]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

            await update.message.reply_text(text=f"Вітаю воїн!"
                                                 f" Ти вибрав {context.user_data['ERANGEL_OR_SANYK']}!"
                                                 f" І ідеш туда за {context.user_data['pubg_pick']}",
                                                 reply_markup=reply_markup)

            ERANGEL_OR_SANYK = update.message.text
            context.user_data['ERANGEL_OR_SANYK'] = ERANGEL_OR_SANYK

            return SANYK

    @staticmethod
    async def SOLO(update: Update, context: ContextTypes.DEFAULT_TYPE):

        if update.message.text == 'Bush':
            keyboard = [
                [InlineKeyboardButton('/exit'), InlineKeyboardButton('/startgame')]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

            await update.message.reply_text(
                f'Ех блін {update.effective_user.first_name}!:( Ви вирішили просидіти у кущах всю ігру.'
                f' Під кінець ігри у вас не було унергетик і вас вбили.',
                reply_markup=reply_markup)

            return ConversationHandler.END

        else:
            keyboard = [
                [InlineKeyboardButton('/exit'), InlineKeyboardButton('/startgame')]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

            await update.message.reply_text(
                f'Це погано. Ви вирішили ви рішили вибити енергетик вийшли з будинку і вас вбила криса',
                reply_markup=reply_markup)

            return ConversationHandler.END

    @staticmethod
    async def SANYK(update: Update, context: ContextTypes.DEFAULT_TYPE):

        if update.message.text == 'PassToGoal':
            keyboard = [
                [InlineKeyboardButton('/exit'), InlineKeyboardButton('/startgame')]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

            await update.message.reply_text(
                f' Ви вирішили самі нокнути тіпа і ви його нокнули!'
                f' Всі на своєму екрані бачуть надпис: {context.user_data["pubg_pick"]} нокає тіпа!',
                reply_markup=reply_markup)

            return ConversationHandler.END

        else:
            keyboard = [
                [InlineKeyboardButton('/exit'), InlineKeyboardButton('/startgame')]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

            await update.message.reply_text(
                f'Ви вирішили дати кіл тімейту а він лох в чєла в фолопені непопав по ньому,'
                f' і противники нас двох забрали',
                reply_markup=reply_markup)

            return ConversationHandler.END
