import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import base64
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# STYLE
from style import style_link, style_button, style_img, style_loading, style_loading_2, style_comment, style_order, style_whole

index = html.Div([
    html.Div('Aplikacja do zamawiania pizzy:',style={'font-size':20}),
    html.Div('Napisałem tą aplikację w ramach swojej nauki programowania. Przy okazji zebrałem informacje jakich składników użyć przy pieczeniu pizzy dla dziewczyny. '
             ,style={'font-size':20}),
    html.Div('Aplikacja pozwala na złożenie zamówienia oraz porpawienie go (dzięki linkowaniu). Następnie zamównie wysyłane jest w formie tekstu na skrzynkę pocztową Gmail',style={'font-size':20}),

    html.Br(),
    html.Br(),
    html.Br(),
    dcc.Link('Kliknij aby przejść dalej'.upper(), href='/prepare',
             style=style_link)
])

prepare_page = html.Div([
    html.H1("Proszę wybrać sposób przygotowania pizzy", style={'font-size':30}),
    dcc.RadioItems(id='sposob-radio',
                   options=[
                       {'label':'Pizza pieczona', 'value':'piecz'},
                       {'label':'Pizza gotowana', 'value':'got'}
                   ],
                   labelStyle={'display':'block'},
                   style={'font-size':20}),

    html.Br(),
    html.Div(id='zamowienie-div-1'),
    html.Br(),
    dcc.Link('A teraz przejdź do składników'.upper(), href='/ingre',
             style=style_link),
])

ingredients_page = html.Div([
    html.H1("Proszę dobrać  ulubione składniki", style={'font-size':30}),
    html.H2("Składniki mięsne", style=style_comment),
    dcc.Checklist(id='skladniki-check-1',
                   options=[
                       {'label':'Kurczak', 'value':'kurczak'},
                       {'label':'Salami', 'value':'salami'},
                       {'label':'Boczek', 'value':'boczek'},
                       {'label':'Nie lubię mięsa i wolę wege...', 'value':'wege'},
                   ],
                   labelStyle={'display':'block'},
                  value=[],
                  style={'font-size':20}),

    html.H2("Sery", style=style_comment),
    dcc.Checklist(id='skladniki-check-2',
                   options=[
                       {'label':'Ser żółty (standard)', 'value':'zolty'},
                       {'label':'Mozzarella', 'value':'mozzarella'},
                       {'label':'Pleśniowy', 'value':'plesn'},
                   ],
                   labelStyle={'display':'block'},
                  value=[],
                  style={'font-size':20}),


    html.H2('Pozostałe składniki', style=style_comment),
    dcc.Checklist(id='skladniki-check-3',
                   options=[
                       {'label':'Pieczarki', 'value':'pieczarki'},
                       {'label':'Cebula żółta', 'value':'cebula-zolt'},
                       {'label':'Cebula czerwona', 'value':'cebula-czerw'},
                       {'label':'Kukurydza', 'value':'kukurydza'},
                       {'label':'Czerwona fasola', 'value':'czerwona fasola'},
                       {'label':'Groszek', 'value':'groszek'},
                       {'label':'Ananas', 'value':'ananas'},
                       {'label':'Papryka', 'value':'papryka'},
                   ],
                   labelStyle={'display':'block'},
                  value=[],
                  style={'font-size':20}),

    html.Br(),
    html.Br(),
    dcc.Link('Dokończ zamówienie'.upper(), href='/extra', style=style_link),
    dcc.Link('Wybierz inny sposób przygotowania.'.upper(), href='/prepare', style=style_link)
])

extra_info_page = html.Div([
    html.H1('Zaproponuj godzinę przygotowania', style={'font-size':30}),
    html.H3('(nie wcześniej niż godz. 17:00)', style=style_comment),
    dcc.Textarea(
            id='time_info',
            placeholder='Napisz tutaj...',
            # style={'width':'50%'}, #domyślna szerokość
            value='', # value to wpisany tekst
            style={'width':300, 'height':50}
        ),

    html.Br(),
    html.Br(),
    html.Br(),

    html.H1('Czy chcesz coś dodać od siebie?', style={'font-size':30}),
    html.H3('(np. uzupełnienie zamówienia, uwagi co do działania aplikacji)', style=style_comment),

    dcc.Textarea(
            id='extra_info',
            placeholder='Napisz tutaj...',
            # style={'width':'50%'}, #domyślna szerokość
            value='', # value to wpisany tekst
            style={'width':600, 'height':100}
        ),

    html.Br(),
    html.Br(),
    html.Br(),
    dcc.Link('Zmień sposób przygotowania pizzy'.upper(), href='/prepare', style=style_link),
    dcc.Link('Popraw listę składników'.upper(), href='/ingre', style=style_link),

])

def SendMail(text):
    print(text)

    me = 'pizzachoiceapp@gmail.com'
    recipient = 'bartoszjanjerzy@gmail.com'
    subject = 'Kolacja z Martą'

    email_server_host = 'smtp.gmail.com'
    port = 587
    email_username = me
    email_password = 'pizzachoiceapp2020'

    msg = MIMEMultipart('alternative')
    msg['From'] = me
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(text, 'plain', 'utf-8'))

    server = smtplib.SMTP(email_server_host, port)
    server.ehlo()
    server.starttls()
    server.login(email_username, email_password)
    server.sendmail(me, recipient, msg.as_string())
    server.close()