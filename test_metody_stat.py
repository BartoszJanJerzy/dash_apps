import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output

# biblioteka do tabel
import dash_table

#biblioteka do prevent-uptade
from dash.exceptions import PreventUpdate

#zewnetrzny styl wizualny
external_stylesheets = ['http://codepen.io/chriddyp/pen/bWLwgP.css']
# a ciemny: https://codepen.io/chriddyp/pen/LYpwVWm

colors = {
    'light':'#E0E1DD',
    'light-blue':'#415A77',
    'blue':'#1B263B'

}

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)  # tworzenie klasy Dash
# server = app.server

# _______________________________________________________________________
# UKŁAD APLIKAJI
# _______________________________________________________________________
app.layout = html.Div([

    html.Br(),

    html.H1("Zadania z metod statystycznych",
            style={
                'border-radius':20,
                'border':f'5px solid {colors["blue"]}',
                'background-color':colors['light'],

                'width':'90%',
                'padding':20,
                'margin':'0px auto',

                'text-align':'center',
                'font-size':30,
            }),

    html.Br(),

    # sekcja pytań prawda/fałsz
    html.Div(id='test-cont', children=([

        html.Div("Zaznacz, czy zdanie jest prawdziwe, czy fałszywe",
                 style={'font-size':14}),
        html.Br(),

        # pytanie 1
        html.Div(id='zad1', children="1. Analiza regresji służy głównie do badania wpływu "
                                     "zmiennych niezależnych na zmienną zależną"),
        dcc.RadioItems(id='radio-zad1', options=[
            {'label':'Prawda', 'value':'true'},
            {'label':'Fałsz', 'value':'false'}
        ], labelStyle={'display':'block'}),
        html.Div(id='opis1'),
        html.Br(),

        # pytanie 2
        html.Div(id='zad2', children="2. Zwiększając liczbę badanych osób zwiększamy również moc testu"),
        dcc.RadioItems(id='radio-zad2', options=[
            {'label':'Prawda', 'value':'true'},
            {'label':'Fałsz', 'value':'false'}
        ], labelStyle={'display':'block'}),
        html.Div(id='opis2'),
        html.Br(),

        # pytanie 3
        html.Div(id='zad3', children="3. Jeżeli zależy nam na zmniejszeniu przedziału ufności bez strat "
                                     "w zakładanym poziomie ufności, to wystarczy ograniczyć "
                                     "liczbę osób badanych."),
        dcc.RadioItems(id='radio-zad3', options=[
            {'label':'Prawda', 'value':'true'},
            {'label':'Fałsz', 'value':'false'}
        ], labelStyle={'display':'block'}),
        html.Div(id='opis3'),
        html.Br(),

        # pytanie 4
        html.Div(id='zad4', children="4. Moc testu nie wiąże się z błędem II rodzaju"),
        dcc.RadioItems(id='radio-zad4', options=[
            {'label':'Prawda', 'value':'true'},
            {'label':'Fałsz', 'value':'false'}
        ], labelStyle={'display':'block'}),
        html.Div(id='opis4'),
        html.Br(),

        # pytanie 5
        html.Div(id='zad5', children="5. Ponieważ uzyskałem wyniki p=0,5 oraz β=0,20 to mogę stwierdzić, "
                                     "że szukane różnice międzygrupowe nie istnieją."),
        dcc.RadioItems(id='radio-zad5', options=[
            {'label':'Prawda', 'value':'true'},
            {'label':'Fałsz', 'value':'false'}
        ], labelStyle={'display':'block'}),
        html.Div(id='opis5'),
        html.Br(),

        # pytanie 6
        html.Div(id='zad6', children="6. Rotacja Varimax zakłada brak korelacji między czynnikami, "
                                     "natomiast rotacja Oblimin na nie pozwala."),
        dcc.RadioItems(id='radio-zad6', options=[
            {'label':'Prawda', 'value':'true'},
            {'label':'Fałsz', 'value':'false'}
        ], labelStyle={'display':'block'}),
        html.Div(id='opis6'),
        html.Br(),

        # pytanie 7
        html.Div(id='zad7', children="7. Korelacja między neurotycznością a lękiem jest bardzo wysoka, "
                                     "dlatego aby ją zbadać potrzeba znacznie większej ilości osób "
                                     "niż do zweryfikowania korelacji niższej między "
                                     "potrzebą domknięcia poznawczego, a pokorą intelektualną."),
        dcc.RadioItems(id='radio-zad7', options=[
            {'label':'Prawda', 'value':'true'},
            {'label':'Fałsz', 'value':'false'}
        ], labelStyle={'display':'block'}),
        html.Div(id='opis7'),
        html.Br(),

        # pytanie 8
        html.Div(id='zad8', children="8. Jeżeli chcemy mieć większy poziom ufności w szacowaniu "
                                     "średniej danego parametru w populacji, to należy uargumentować "
                                     "hipotezę jednostronną, dobadać większą ilość osób "
                                     "lub pozwolić na rozszerzenie przedziału ufności."),
        dcc.RadioItems(id='radio-zad8', options=[
            {'label':'Prawda', 'value':'true'},
            {'label':'Fałsz', 'value':'false'}
        ], labelStyle={'display':'block'}),
        html.Div(id='opis8'),
        html.Br(),

        # pytanie 9
        html.Div(id='zad9', children="9. Test Friedmana używamy gdy w modelu badania posiadamy "
                                     "jedna grupę, jedną zmienną zależną mierzoną na skali rangowej "
                                     "oraz wiele pomiarów tej zmiennej"),
        dcc.RadioItems(id='radio-zad9', options=[
            {'label':'Prawda', 'value':'true'},
            {'label':'Fałsz', 'value':'false'}
        ], labelStyle={'display':'block'}),
        html.Div(id='opis9'),
        html.Br(),

        # pytanie 10
        html.Div(id='zad10', children="10. Test U Manna-Whitneya używamy gdy posiadamy dwie grupy "
                                     "badanych, zmienną zależną mierzoną na skali rangowej oraz "
                                     "jeden pomair tej zmiennej"),
        dcc.RadioItems(id='radio-zad10', options=[
            {'label':'Prawda', 'value':'true'},
            {'label':'Fałsz', 'value':'false'}
        ], labelStyle={'display':'block'}),
        html.Div(id='opis10'),
        html.Br(),

        # pytanie 11
        html.Div(id='zad11', children="11. Model MANCOVA zakłada większą ilość zmiennych niezależnych "
                                      "niż model 1-ANOVA"),
        dcc.RadioItems(id='radio-zad11', options=[
            {'label':'Prawda', 'value':'true'},
            {'label':'Fałsz', 'value':'false'}
        ], labelStyle={'display':'block'}),
        html.Div(id='opis11'),
        html.Br(),

        # pytanie 12
        html.Div(id='zad12', children="12. Osoby badane podzielono wg płci. Dlatego też płeć można "
                                      "nazwać zmienną manipulacyjną"),
        dcc.RadioItems(id='radio-zad12', options=[
            {'label':'Prawda', 'value':'true'},
            {'label':'Fałsz', 'value':'false'}
        ], labelStyle={'display':'block'}),
        html.Div(id='opis12'),
        html.Br(),

        # pytanie 13
        html.Div(id='zad13', children="13. Osoby badane są w trzech różnych grupach i sprawdza się "
                                      "różnice w zdolności skupiania uwagi. Zmierzono ich IQ jako "
                                      "dodatkową charakterystykę, dlatego można ją nazwać zmienną "
                                      "kowariancyjną"),
        dcc.RadioItems(id='radio-zad13', options=[
            {'label':'Prawda', 'value':'true'},
            {'label':'Fałsz', 'value':'false'}
        ], labelStyle={'display':'block'}),
        html.Div(id='opis13'),
        html.Br(),

        # pytanie 14
        html.Div(id='zad14', children="14. Ilośc badanych osób nie wiąże się błędem II rodzaju"),
        dcc.RadioItems(id='radio-zad14', options=[
            {'label':'Prawda', 'value':'true'},
            {'label':'Fałsz', 'value':'false'}
        ], labelStyle={'display':'block'}),
        html.Div(id='opis14'),
        html.Br(),

        # pytanie 15
        html.Div(id='zad15', children="15. II zasada randomizacji zakłada losowy przydział osób badanych "
                                      "do grup wyodrębnionych na podsatwie zmiennych niezależnych"),
        dcc.RadioItems(id='radio-zad15', options=[
            {'label':'Prawda', 'value':'true'},
            {'label':'Fałsz', 'value':'false'}
        ], labelStyle={'display':'block'}),
        html.Div(id='opis15'),
        html.Br(),
    ]), style={
        'width':'85%',
        'margin':'0px auto',
        'padding':20,

        'border':f'5px solid {colors["blue"]}',
        'border-radius':20,

        'font-size':12,
        'background-color':colors['light']
    }),
        html.Br(),
], style={'background-color':colors['light-blue']})
# _______________________________________________________________________



# _______________________________________________________________________
# --- FUNKCJE INTERAKTYWNE
# _______________________________________________________________________
# info zwrotne 1
@app.callback(
    Output('opis1', 'children'),
    Output('opis1', 'style'),
    [
        Input('radio-zad1', 'value'),
    ]
)
def info_zwrotne_1(value):
    result = ''
    why = ''
    color = ''

    why = 'Analiza regresji używana jest głównie do badania związku miedzy predyktorami a zmienną objasnianą(zależną)'

    if value == 'true':
        result = 'Źle!'
        color = 'red'
    elif value == 'false':
        result = 'Dobrze!'
        color = 'green'
    else:
        raise PreventUpdate

    return ([result, html.Br(), why], {'color':color, 'font-size':12,})

# info zwrotne 2
@app.callback(
    Output('opis2', 'children'),
    Output('opis2', 'style'),
    [
        Input('radio-zad2', 'value'),
    ]
)
def info_zwrotne_2(value):
    result = ''
    why = ''
    color = ''

    why = 'Im wiecej osób badamy, tym bardziej pomniejszamy błąd II rodzaju, więc moc testu wzrasta'

    if value == 'false':
        result = 'Źle!'
        color = 'red'
    elif value == 'true':
        result = 'Dobrze!'
        color = 'green'
    else:
        raise PreventUpdate

    return ([result, html.Br(), why], {'color':color, 'font-size':12,})

# info zwrotne 3
@app.callback(
    Output('opis3', 'children'),
    Output('opis3', 'style'),
    [
        Input('radio-zad3', 'value'),
    ]
)
def info_zwrotne_3(value):
    result = ''
    why = ''
    color = ''

    why = 'Zmniejszenie liczby osób spowoduje odwrotny efekt - przedział ufności rozszerzy się'

    if value == 'true':
        result = 'Źle!'
        color = 'red'
    elif value == 'false':
        result = 'Dobrze!'
        color = 'green'
    else:
        raise PreventUpdate

    return ([result, html.Br(), why], {'color':color, 'font-size':12,})

# info zwrotne 4
@app.callback(
    Output('opis4', 'children'),
    Output('opis4', 'style'),
    [
        Input('radio-zad4', 'value'),
    ]
)
def info_zwrotne_4(value):
    result = ''
    why = ''
    color = ''

    why = 'Ze wzoru wynika coś całkiem innego: moc_testu = 1 - β'

    if value == 'true':
        result = 'Źle!'
        color = 'red'
    elif value == 'false':
        result = 'Dobrze!'
        color = 'green'
    else:
        raise PreventUpdate

    return ([result, html.Br(), why], {'color':color, 'font-size':12,})

# info zwrotne 5
@app.callback(
    Output('opis5', 'children'),
    Output('opis5', 'style'),
    [
        Input('radio-zad5', 'value'),
    ]
)
def info_zwrotne_5(value):
    result = ''
    why = ''
    color = ''

    why = 'Poziom β jest zbyt wysoki (przekracza 0,1). Dlatego lepiej stwierdzić, że "różnic nie zaobserwowano"'

    if value == 'true':
        result = 'Źle!'
        color = 'red'
    elif value == 'false':
        result = 'Dobrze!'
        color = 'green'
    else:
        raise PreventUpdate

    return ([result, html.Br(), why], {'color':color, 'font-size':12,})

# info zwrotne 6
@app.callback(
    Output('opis6', 'children'),
    Output('opis6', 'style'),
    [
        Input('radio-zad6', 'value'),
    ]
)
def info_zwrotne_6(value):
    result = ''
    why = ''
    color = ''

    why = 'Varimax -> brak korelacji, Oblimin -> korelacje'

    if value == 'false':
        result = 'Źle!'
        color = 'red'
    elif value == 'true':
        result = 'Dobrze!'
        color = 'green'
    else:
        raise PreventUpdate

    return ([result, html.Br(), why], {'color':color, 'font-size':12,})

# info zwrotne 7
@app.callback(
    Output('opis7', 'children'),
    Output('opis7', 'style'),
    [
        Input('radio-zad7', 'value'),
    ]
)
def info_zwrotne_7(value):
    result = ''
    why = ''
    color = ''

    why = 'Im wieksza korelacja (większy efekt) tym mniej osób potrzeba aby ją zaobserwować'

    if value == 'true':
        result = 'Źle!'
        color = 'red'
    elif value == 'false':
        result = 'Dobrze!'
        color = 'green'
    else:
        raise PreventUpdate

    return ([result, html.Br(), why], {'color':color, 'font-size':12,})

# info zwrotne 8
@app.callback(
    Output('opis8', 'children'),
    Output('opis8', 'style'),
    [
        Input('radio-zad8', 'value'),
    ]
)
def info_zwrotne_8(value):
    result = ''
    why = ''
    color = ''

    why = 'Wszsytkie te czynności pozwalają na zwiększenie przedziału ufności'

    if value == 'false':
        result = 'Źle!'
        color = 'red'
    elif value == 'true':
        result = 'Dobrze!'
        color = 'green'
    else:
        raise PreventUpdate

    return ([result, html.Br(), why], {'color':color, 'font-size':12,})

# info zwrotne 9
@app.callback(
    Output('opis9', 'children'),
    Output('opis9', 'style'),
    [
        Input('radio-zad9', 'value'),
    ]
)
def info_zwrotne_9(value):
    result = ''
    why = ''
    color = ''

    why = 'Co tu duzo gadać, zdanie jest prawdziwe... (zob. wybór testów różnic)'

    if value == 'false':
        result = 'Źle!'
        color = 'red'
    elif value == 'true':
        result = 'Dobrze!'
        color = 'green'
    else:
        raise PreventUpdate

    return ([result, html.Br(), why], {'color':color, 'font-size':12,})

# info zwrotne 10
@app.callback(
    Output('opis10', 'children'),
    Output('opis10', 'style'),
    [
        Input('radio-zad10', 'value'),
    ]
)
def info_zwrotne_10(value):
    result = ''
    why = ''
    color = ''

    why = 'Co tu duzo gadać, zdanie jest prawdziwe... (zob. wybór testów różnic)'

    if value == 'false':
        result = 'Źle!'
        color = 'red'
    elif value == 'true':
        result = 'Dobrze!'
        color = 'green'
    else:
        raise PreventUpdate

    return ([result, html.Br(), why], {'color':color, 'font-size':12,})

# info zwrotne 11
@app.callback(
    Output('opis11', 'children'),
    Output('opis11', 'style'),
    [
        Input('radio-zad11', 'value'),
    ]
)
def info_zwrotne_11(value):
    result = ''
    why = ''
    color = ''

    why = 'Oba modele są jednoczynnikowe (zakałdają 1ną zmienną niezależną). ' \
          'W takim wypadku nie trzeba zapisywać 1ki przed modelem... ale też nie jest to błędem'

    if value == 'true':
        result = 'Źle!'
        color = 'red'
    elif value == 'false':
        result = 'Dobrze!'
        color = 'green'
    else:
        raise PreventUpdate

    return ([result, html.Br(), why], {'color':color, 'font-size':12,})

# info zwrotne 12
@app.callback(
    Output('opis12', 'children'),
    Output('opis12', 'style'),
    [
        Input('radio-zad12', 'value'),
    ]
)
def info_zwrotne_12(value):
    result = ''
    why = ''
    color = ''

    why = 'Płeć pozwala na kalsyfikację osób, dlatego jest zmienną niezależną-klasyfikacyjną'

    if value == 'true':
        result = 'Źle!'
        color = 'red'
    elif value == 'false':
        result = 'Dobrze!'
        color = 'green'
    else:
        raise PreventUpdate

    return ([result, html.Br(), why], {'color':color, 'font-size':12,})

# info zwrotne 13
@app.callback(
    Output('opis13', 'children'),
    Output('opis13', 'style'),
    [
        Input('radio-zad13', 'value'),
    ]
)
def info_zwrotne_13(value):
    result = ''
    why = ''
    color = ''

    why = 'Zmienna kowariancyjna to dodatkowa zmienna charakteryzujaca osoby badane. ' \
          'Mierzona jest na skali ilościowej oraz wiąże się ze zmienną zależną'

    if value == 'false':
        result = 'Źle!'
        color = 'red'
    elif value == 'true':
        result = 'Dobrze!'
        color = 'green'
    else:
        raise PreventUpdate

    return ([result, html.Br(), why], {'color':color, 'font-size':12,})

# info zwrotne 14
@app.callback(
    Output('opis14', 'children'),
    Output('opis14', 'style'),
    [
        Input('radio-zad14', 'value'),
    ]
)
def info_zwrotne_14(value):
    result = ''
    why = ''
    color = ''

    why = 'Im więcej osób zbadamy, tym mniejszy staje się błąd II rodzaju (beta). ' \
          'Oznacza, to że badanie jest bardziej wrażliwe na poszukiwany efekt.'

    if value == 'true':
        result = 'Źle!'
        color = 'red'
    elif value == 'false':
        result = 'Dobrze!'
        color = 'green'
    else:
        raise PreventUpdate

    return ([result, html.Br(), why], {'color':color, 'font-size':12,})

# info zwrotne 15
@app.callback(
    Output('opis15', 'children'),
    Output('opis15', 'style'),
    [
        Input('radio-zad15', 'value'),
    ]
)
def info_zwrotne_15(value):
    result = ''
    why = ''
    color = ''

    why = 'Co tu duzo gadać, zdanie jest prawdziwe...'

    if value == 'false':
        result = 'Źle!'
        color = 'red'
    elif value == 'true':
        result = 'Dobrze!'
        color = 'green'
    else:
        raise PreventUpdate

    return ([result, html.Br(), why], {'color':color, 'font-size':12,})
# _______________________________________________________________________

if __name__ == '__main__':
    app.run_server(debug=True)