import random
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
from config import TOKEN

# Определяем константы для состояний
ASK_QUESTION, ANSWER_QUESTION = range(2)

# Клавиатура для выбора действия
ask_reply_markup = ReplyKeyboardMarkup([['Подбросить монетку', 'Случайное число'], ['Задать вопрос']], resize_keyboard=True)

def start(update: Update, context: CallbackContext) -> None:
    """Отправляет приветственное сообщение и предлагает выбор действия."""
    update.message.reply_text('Привет! Что вы хотите сделать?', reply_markup=ask_reply_markup)

def flip_a_coin(update: Update, context: CallbackContext) -> None:
    """Подбрасывает монетку."""
    result = random.choice(['Орел', 'Решка'])
    update.message.reply_text(f'Выпало: {result}', reply_markup=ask_reply_markup)

def random_number(update: Update, context: CallbackContext) -> None:
    """Выдает случайное число от 0 до 100."""
    number = random.randint(0, 100)
    update.message.reply_text(f'Случайное число: {number}', reply_markup=ask_reply_markup)

def ask_question(update: Update, context: CallbackContext) -> int:
    """Запрашивает вопрос у пользователя."""
    update.message.reply_text('Задайте ваш вопрос:', reply_markup=ReplyKeyboardRemove())
    return ASK_QUESTION

def answer_question(update: Update, context: CallbackContext) -> int:
    """Отвечает на вопрос 'Да' или 'Нет'."""
    answer = random.choice(['Да', 'Нет'])
    update.message.reply_text(f'Ответ: {answer}', reply_markup=ask_reply_markup)
    return ConversationHandler.END

def main() -> None:
    """Запускает бота."""
    updater = Updater(TOKEN)

    # Обработчик команды /start
    updater.dispatcher.add_handler(CommandHandler('start', start))

    # Обработчик диалога с пользователем
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^(Задать вопрос)$'), ask_question)],
        states={
            ASK_QUESTION: [MessageHandler(Filters.text & ~Filters.command, answer_question)],
        },
        fallbacks=[],
        per_user=False
    )

    updater.dispatcher.add_handler(conv_handler)

    # Обработчики для кнопок
    updater.dispatcher.add_handler(MessageHandler(Filters.regex('^(Подбросить монетку)$'), flip_a_coin))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex('^(Случайное число)$'), random_number))

    # Запускаем бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()