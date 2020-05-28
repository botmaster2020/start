import telebot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup,InlineKeyboardMarkup,InlineKeyboardButton
import smtplib                                                                                              
import mimetypes                                        
from email import encoders                                  
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart 

bot = telebot.TeleBot('967141436:AAGD95tco2icFWTj086otcAFwMMzYw9fNYg')

def send_email(addr_to, msg_subj, msg_text, files=''):
    addr_from = "a.alex.2000@mail.ru"                           # Отправитель
    password  = "Rashin006"                                  # Пароль


    msg = MIMEMultipart()                                   # Создаем сообщение
    msg['From']    = addr_from                              # Адресат
    msg['To']      = addr_to                                # Получатель
    msg['Subject'] = msg_subj                               # Тема сообщения

    body = msg_text                                         # Текст сообщения
    msg.attach(MIMEText(body, 'plain'))                     # Добавляем в сообщение текст
    
    # filepath = 'Бета модель данных 2203.csv'
    filepath = files                                        # название файла

    ctype, encoding = mimetypes.guess_type(filepath)        # Определяем тип файла на основе его расширения
    if ctype is None or encoding is not None:               # Если тип файла не определяется
        ctype = 'application/octet-stream'                  # Будем использовать общий тип
    maintype, subtype = ctype.split('/', 1)   

    fp = open(filepath, 'rb')
    file = MIMEBase(maintype, subtype)              # Используем общий MIME-тип
    file.set_payload(fp.read())                     # Добавляем содержимое общего типа (полезную нагрузку)
    fp.close()
    encoders.encode_base64(file)                    # Содержимое должно кодироваться как Base64
    file.add_header('Content-Disposition', 'attachment', filename=filepath) # Добавляем заголовки
    msg.attach(file) 
 
    #======== Этот блок настраивается для каждого почтового провайдера отдельно ===============================================
    # server = smtplib.SMTP_SSL('*****yandex.ru', 465)        # Создаем объект SMTP
    server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
    #server.starttls()                                      # Начинаем шифрованный обмен по TLS
    #server.set_debuglevel(True)                            # Включаем режим отладки, если не нужен - можно закомментировать
    server.login(addr_from, password)                       # Получаем доступ
    server.send_message(msg)                                # Отправляем сообщение
    server.quit()

def key():
    button1 = InlineKeyboardButton('Получить отчёт', callback_data='1')
    
    klav = InlineKeyboardMarkup(row_width=1)
    klav.add(button1)
    return klav


@bot.callback_query_handler(func=lambda call: True)
def reaction(call):
    c = call.data
    who = call.message.chat.id

    if c == '1':
        with open('file.pdf', 'rb') as doc:
            bot.send_document(who, doc)
        # send_email('goncharuk.ea@gazprom-neft.ru', 'Отчёт', 'Start', files='file.pdf')
    bot.answer_callback_query(call.id)


@bot.message_handler(commands=['start'])
def start(message):
    who = message.chat.id
    bot.send_message(who, 'Получите отчёт на почту goncharuk.ea@gazprom-neft.ru', reply_markup=key())

print('go')
bot.polling(none_stop=True)
