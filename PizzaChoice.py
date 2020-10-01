import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import base64
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#zewnetrzny styl wizualny
external_stylesheets = ['http://codepen.io/chriddyp/pen/bWLwgP.css']
# a ciemny: https://codepen.io/chriddyp/pen/LYpwVWm

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)  # tworzenie klasy Dash
server = app.server

'''aplikacja ma kilka podstron, których skrypt znajduje się poza główną apką
dlatego aby uzyć id komponentów z tych podstron trzeba dać to:'''
app.config.suppress_callback_exceptions=True

# przygotowanie obrazu
pizza = r'pizza.png'
encoded_pizza = base64.b64encode(open(pizza,"rb").read())

style_link = {
    'font-size':12,
    'color':'#292e29',
    'text-decoration':'none',

    'border':'1px solid #9aab9a',
    'border-radius':5,
    'padding':'10px 30px',
    'margin':'0px 20px 0px 0px'
}

style_button = {
    'font-size':12,
    'color':'#292e29',
    'background-color':'rgba(255,255,255,0)',
    'text-decoration':'none',

    'border':'1px solid #9aab9a',
    'border-radius':5,
    'padding':'10px 30px 10px 30px',
    'margin':'0px 20px 0px 0px'
}

# _______________________________________________________________________
# UKŁAD APLIKAJI:
# - wybór składników do pizzy
# - wysłanie e-mail z zapisanym info
# _______________________________________________________________________
app.layout = html.Div([
    dcc.Store(id='reset'),

    dcc.Location(id='url',refresh=False),

    # kontener na teksty
    html.Div([
        html.Img(src=f'data:image/png;base64,{encoded_pizza.decode()}',
                 style={
                     'width':1400,
                     'border-radius':40,

                     'margin':'0px auto'
                 })]),

        # sekcja z wyborami
        dcc.Loading(
                id='loading-2',
                children=[
                    html.Div(id='page-content',
                             style={
                                 # 'border':'1px solid black',
                                 'border-radius': 20,

                                 'width': 700,
                                 'padding': 20,

                                 'position': 'absolute',
                                 'top': 50,
                                 'left': 100,

                                 'background-color': 'rgba(255,255,255,0.7)',
                             }),
                ],
                type='circle',
                color='white',
            style={
                'position':'absolute',
                'top':-800,
                'left':400,
            }
            ),

        # sekcja z zamówieniem
        html.Div(id='zobacz_zamowienie', children=[
            html.H1('ZAMÓWIENIE', style={'font-size':30}),

            html.Div('Sposób przygotowania:', style={'font-size':20}),
            html.Div(id='sposob', style={'font-size':20, 'font-style':'italic'}),
            html.Br(),
            html.Div('Składniki:', style={'font-size':20}),
            html.Div(id='skladniki', style={'font-size':20, 'font-style':'italic'}),
            html.Br(),
            html.Div('Godzina kolacji:', style={'font-size': 20}),
            html.Div(id='godzina', style={'font-size': 20, 'font-style': 'italic'}),
            html.Br(),
            html.Div('Dodatkowe informacje:', style={'font-size':20}),
            html.Div(id='info', style={'font-size':20, 'font-style':'italic'}),

            html.Br(),
            html.Br(),
            html.Br(),
            html.Button(id='send-button', children='Wyślij zamówienie'.upper(), n_clicks=0, style=style_button),
            html.Br(),
            html.Br(),
            html.Button(id='change-button', children='Popraw zamówienie'.upper(), n_clicks=0, style=style_button),

        ], style={
            # 'border':'1px solid green',
            'border-radius': 20,

            'width': 300,
            'padding': 20,

            'position':'absolute',
            'top':50,
            'right':100,

            'background-color':'rgba(255,255,255,0.7)',
            'text-align':'center'
        })
    ], style={
        'width':1400,
        'margin':'0px auto',
        # 'border':'3px solid green',
        'position':'relative',
    })

# _______________________________________________________________________
# PODSTRONY

# index_page
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

# sposób przygotowania
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
]),

# wybór składników
ingredients_page = html.Div([
    html.H1("Proszę dobrać  ulubione składniki", style={'font-size':30}),
    html.H2("Składniki mięsne", style={'font-size':20, 'font-style':'italic'}),
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

    html.H2("Sery", style={'font-size':20, 'font-style':'italic'}),
    dcc.Checklist(id='skladniki-check-2',
                   options=[
                       {'label':'Ser żółty (standard)', 'value':'zolty'},
                       {'label':'Mozzarella', 'value':'mozzarella'},
                       {'label':'Pleśniowy', 'value':'plesn'},
                   ],
                   labelStyle={'display':'block'},
                  value=[],
                  style={'font-size':20}),


    html.H2('Pozostałe składniki', style={'font-size':20, 'font-style':'italic'}),
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

]),

extra_info_page = html.Div([
    html.H1('Zaproponuj godzinę przygotowania', style={'font-size':30}),
    html.H3('(nie wcześniej niż godz. 17:00)', style={'font-size':20, 'font-style':'italic'}),
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
    html.H3('(np. uzupełnienie zamówienia, uwagi co do działania aplikacji)', style={'font-size':20, 'font-style':'italic'}),

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
# ___________________________________________________________________


# ___________________________________________________________________
# FUNKCJE INTERAKTYWNE
# ___________________________________________________________________

@app.callback(
    Output('page-content', 'children'),
    [
        Input('url','pathname'),
        Input('send-button','n_clicks'),
        Input('zobacz_zamowienie', 'children'),
        Input('change-button', 'n_clicks'),
    ]
)
def display_page(pathname, n_clicks_send, text, n_clicks_change):
    page = index

    if n_clicks_send <= n_clicks_change:
        # zmiana strony
        if pathname == '/ingre':
            page = ingredients_page
        elif pathname == '/extra':
            page = extra_info_page
        elif pathname == '/prepare':
            page = prepare_page
        else:
            page = index

    else:
        '''
        naciśnięto 'stwórz zamówienie
        '''
        # WYSŁANIE MAILA
        # tekst maila
        new_text = "{}\n\n{}\n{}\n\n{}\n{}\n\n{}\n{}\n\n{}\n{}".format(text[0]['props']['children'],text[1]['props']['children'],
                                                             text[2]['props']['children'],text[4]['props']['children'],text[5]['props']['children'],
                                                             text[7]['props']['children'],text[8]['props']['children'],
                                                             text[10]['props']['children'],text[11]['props']['children'])

        print(new_text)

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

        msg.attach(MIMEText(new_text, 'plain','utf-8'))

        server = smtplib.SMTP(email_server_host, port)
        server.ehlo()
        server.starttls()
        server.login(email_username, email_password)
        server.sendmail(me, recipient, msg.as_string())
        server.close()

        # print('error sending email')
        # print(type(new_text))
        # print(new_text)

        page = html.Div([
            html.H1('Dziękuję za złożenie zamówienia', style={'font-size':20}),
            html.H1('Kolacja zostanie przygotowana według Twoich wskazówek', style={'font-size':20}),
        ], style={'text-align':'center'})

    return page

# update pizza 1
@app.callback(
    Output('sposob', 'children'),
    [
        Input('sposob-radio', 'value'),
    ]
)
def UptadePizza_1(sposob):
    text1 = ''

    # uptade sposoób
    if sposob == 'piecz':
        text1 = 'Pizza pieczona'
    elif sposob == 'got':
        text1 = 'Pizza gotowana'
    else:
        pass

    return text1

# update pizza 2
@app.callback(
    Output('skladniki', 'children'),
    [
        Input('skladniki-check-1','value'),
        Input('skladniki-check-2','value'),
        Input('skladniki-check-3','value'),
    ]
)
def UptadePizza_2(miesa, sery, inne):
    text1 = ''
    text2 = ''

    # uptade składniki

    if 'wege' in miesa:
        text1 = ''
    else:
        if 'kurczak' in miesa:
            text1 += 'kurczak, '
        if 'salami' in miesa:
            text1 += 'salami, '
        if 'boczek' in miesa:
            text1 += 'boczek, '

    if 'zolty' in sery:
        text2 += 'żółty ser, '
    if 'mozzarella' in sery:
        text2 += 'ser mozzarella, '
    if 'plesn' in sery:
        text2 += 'ser pleśniowy, '
    if 'pieczarki' in inne:
        text2 += 'pieczarki, '
    if 'cebula-zolt' in inne:
        text2 += 'cebula, '
    if 'cebula-czerw' in inne:
        text2 += 'cebula czerwona, '
    if 'kukurydza' in inne:
        text2 += 'kukurydza, '
    if 'czerwona fasola' in inne:
        text2 += 'czerwona fasola, '
    if 'groszek' in inne:
        text2 += 'groszek, '
    if 'ananas' in inne:
        text2 += 'ananas, '
    if 'papryka' in inne:
        text2 += 'papryka, '

    return [text1,text2]

# update pizza 3
@app.callback(
    [
        Output('godzina', 'children'),
        Output('info', 'children'),
    ],
    [
        Input('time_info', 'value'),
        Input('extra_info', 'value'),
    ]
)
def UptadePizza_3(time, text):
    return time, text


if __name__ == '__main__':
    app.run_server(debug=True)