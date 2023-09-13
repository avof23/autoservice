"""This file contains template dictionary with all text message used in this project"""
template = {
    'en': {'welcome': '''Welcome to AutoServiceBot. 
You can write your auto to service for a specific date. 
After registration, you can see the status of your order and other information on it.
For help, type /help''',

           'help': '''Bot Functions:
    /help - Print This help
    /register - Register Auto to service
    /status - Get status of your order
    /cancel - Cancel ordering register process''',

           'workchoice': 'Select the work you plan to do',
           'workselect': 'Selected works',
           'datechoice': 'Select your visit date',
           'dateselect': 'Selected date',
           'timechoice': 'Select time of visit',
           'timeselect': 'Selected time',
           'pricetext': 'Price',
           'orderreq': 'Please enter your Order ID\n after command /status',
           'incorrectid': 'Incorrect Order ID!',
           'answerorder': 'Order ID: {id}\nStatus: {status} Start in: {start_date}\nSumm: {order_summ} Master name: {master}',
           'cancel': 'Canceled register process'
           },

    'ru': {'welcome': '''Добро пожаловать в AutoServiceBot. 
Вы можете записать ваше auto на service на определенную дату. 
После записи вы можете посмотреть статус вашего заказа и прочую информацию по нему.
Для вывода справки наберите /help''',

           'help': '''Функции Бота:
    /help - Вывод справки
    /register - Запись авто на сервис
    /status - Получить статус заказа
    /cancel - Отмена процесса записи''',

           'workchoice': 'Выберите работы которые планируете делать',
           'workselect': 'Выберанные работы',
           'datechoice': 'Выберите дату посещения',
           'dateselect': 'Выберанная дата',
           'timechoice': 'Выберите время посещения',
           'timeselect': 'Выбранное время',
           'pricetext': 'Цена',
           'orderreq': 'Пожалуйста введите свой номер Заказа\n после команды /status',
           'incorrectid': 'Некорректный номер Заказа!',
           'answerorder': 'Номер Заказа: {id}\nСтатус: {status} Начало: {start_date}\nСумма: {order_summ} Мастер: {master}',
           'cancel': 'Отменен процесс регистрации'
           }
}
