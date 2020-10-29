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

# STYLE
from style import style_link, style_button, style_img, style_loading, style_loading_2, style_comment, style_order, style_whole

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
                 style=style_img)]),

        # sekcja z wyborami
        dcc.Loading(
                id='loading-2',
                children=[
                    html.Div(id='page-content',
                             style=style_loading),
                ],
                type='circle',
                color='white',
            style=style_loading_2
            ),

        # sekcja z zamówieniem
        html.Div(id='zobacz_zamowienie', children=[
            html.H1('ZAMÓWIENIE', style={'font-size':30}),

            html.Div('Sposób przygotowania:', style={'font-size':20}),
            html.Div(id='sposob', style=style_comment),
            html.Br(),
            html.Div('Składniki:', style={'font-size':20}),
            html.Div(id='skladniki', style=style_comment),
            html.Br(),
            html.Div('Godzina kolacji:', style={'font-size': 20}),
            html.Div(id='godzina', style=style_comment),
            html.Br(),
            html.Div('Dodatkowe informacje:', style={'font-size':20}),
            html.Div(id='info', style=style_comment),

            html.Br(),
            html.Br(),
            html.Br(),
            html.Button(id='send-button', children='Wyślij zamówienie'.upper(), n_clicks=0, style=style_button),
            html.Br(),
            html.Br(),
            html.Button(id='change-button', children='Popraw zamówienie'.upper(), n_clicks=0, style=style_button),

        ], style=style_order)
    ], style=style_whole)

# _______________________________________________________________________
# PODSTRONY

from data import index, prepare_page, ingredients_page, extra_info_page, SendMail

# ___________________________________________________________________

# ___________________________________________________________________
# FUNKCJE INTERAKTYWNE

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
        new_text = f"{text[0]['props']['children']}\n\n{text[1]['props']['children']}\n{text[2]['props']['children']}\n\n" \
                   f"{text[4]['props']['children']}\n{text[5]['props']['children']}\n\n{text[7]['props']['children']}\n" \
                   f"{text[8]['props']['children']}\n\n{text[10]['props']['children']}\n{text[11]['props']['children']}"
        SendMail(new_text)

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