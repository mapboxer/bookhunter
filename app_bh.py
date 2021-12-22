# -*- coding: utf-8 -*-

#for local run app: streamlit run D:\UsersProjekt\2_PyCharm\freelance01\app.py
import streamlit as st
from googlesearch import search
from PIL import Image
import pandas as pd
import smtplib, ssl
from email.message import EmailMessage

st.set_page_config(
     page_title="Book Hunter",
     page_icon=":book:",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'About': "This a test app!"
     }
 )




# create bata base connection or others actions
# def status_mail(x, df):
#     pass
#     #df['status'][x] = 1

    
def sand_email_to(link, sender_email, password, receiver_email):
    """Send email function"""
    message = f"""\
    Добрый день.

    На вашем ресурсе, по адресу:
    {link}
    размещен нелегальный контент.
    Просим вас удалить указанный выше контент, в течении 2 суток.

    С уважением, Book Hunter!"""
    # if u want change standart message

    # message = st.text_area('Текс сообщения, при необходимости, отредактируйте:', message)
    # message = message.encode('ansii')
    st.subheader('Текст сообщения: ')
    st.write(message)






    choise = st.radio('Выберите действие: ', ['Не отправлять письмо', 'Отправить письмо'])
    st.write('-' * 25)
    if choise == 'Отправить письмо':
       try:
            msg = EmailMessage()
            msg.set_content(message)
            msg['Subject'] = f'Автоматическое уведомление'
            msg['From'] = sender_email
            msg['To'] = receiver_email
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login(sender_email, password)
            s.send_message(msg)
            #s.sendmail(msg)
            s.quit()

            st.subheader('Письмо отправлено.')
            st.write('-' * 25)
        except:
            st.subheader("Проверьте предоставлен ли доступ сторонним приложениям к вашему аккаунту электронной почты и корректно ли заполнены поля отправителя, пароля и адресата.")
            st.write('-' * 25)



links = []
# logo
#with st.sidebar.form('menu'):
image = Image.open(r"./logo.jpg")
st.sidebar.image(image, use_column_width=True)

st.sidebar.title('Выберите поисковую систему:')
search_sys = st.sidebar.radio('', ['Google']) # , 'Bing'
st.sidebar.title('Введите количество результатов поиска:')
nums_res = st.sidebar.number_input('', 1, 100)
st.sidebar.title('Введите язык поиска:')
lang = st.sidebar.radio('', ['ru', 'en'])
st.sidebar.title('Введите поисковый запрос:')
query = st.sidebar.text_input('')

if query:
    for j in search(query, num_results=nums_res, lang=lang):
        links.append(j)

if len(links) > 0:
    df = pd.DataFrame(links)
    df['action'] = 'Перейти к отправке письма'
    df['status'] = 0
    st.title("Результат поиска")
    for x in range(len(df)):
        #with st.form(str(x), clear_on_submit = False):
            st.write(f"Запись № {x}")
            st.write(df[0][x])
            status = df['action'][x]
            #submitted = st.form_submit_button(status)
            submitted = st.radio(f'Выберите действие с записью № {x}: ', ["Ни чего не делать",'Сформировать письмо'])

            st.write('-'*25)
            if submitted == 'Сформировать письмо':
                # connect to data base or others operation
                # df['action'][x] = 'SEND'
                # status_mail(x, df)
                sender_email = st.text_input('От кого (в настоящее время поддерживается только Google gmail):')
                password = st.text_input('Пароль от почты:')
                st.text('Внимание! Для отправки сообщения необходимо разрашить доступ к почте, от сторонних приложений.')
                receiver_email = st.text_input('Кому:')
                sand_email_to(df[0][x], sender_email, password, receiver_email)










