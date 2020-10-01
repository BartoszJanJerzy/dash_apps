import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import pandas as pd

#biblioteka do prevent-uptade
from dash.exceptions import PreventUpdate

# biblioteka do tabel
import dash_table
#zewnetrzny styl wizualny
external_stylesheets = ['http://codepen.io/chriddyp/pen/bWLwgP.css']
# a ciemny: https://codepen.io/chriddyp/pen/LYpwVWm

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)  # tworzenie klasy Dash
server = app.server

colors = {
    'very_dark':'#0A0908',
    'dark':'#22333B',
    'very_light':'#EAE0D5',
    'light':'#C6AC8F',
    'brown':'5E503F',
    'light_grey':'#e0e0e0'
}

# _______________________________________________________________________
# DANE
# _______________________________________________________________________
# tabela
table_3anova_ache = pd.read_excel('tabela_3anova_ache.xlsx')
table_3anova_buche = pd.read_excel('tabela_3anova_buche.xlsx')
table_dawka_ache = pd.read_excel('tabela_dawka_ache.xlsx')
table_dawka_buche = pd.read_excel('tabela_dawka_buche.xlsx')
table_godziny_ache = pd.read_excel('tabela_godziny_ache.xlsx')
table_godziny_buche = pd.read_excel('tabela_godziny_buche.xlsx')
table_doby_buche = pd.read_excel('tabela_doby_buche.xlsx')
table_doby_ache = pd.read_excel('tabela_doby_ache.xlsx')

df_raw = pd.read_excel('raw_data.xlsx')
df_mozg = df_raw[['id','dawka','doba','godziny','AChE_mozg','BuchE_mozg']]
df_mozg.set_index('id',inplace=True)


# _______________________________________________________________________
# UKŁAD APLIKAJI
# _______________________________________________________________________
app.layout = html.Div([

    # SEKCJA NAGŁÓWEK
    html.Div(id='div-head', children=(
        html.H1(id="head-1", children="Raport wyników - zatrucie substancją AA",
                        style={ #STYLE DO NAGŁÓWKA
                            'font-size':30,
                            'font-family':'Georgia',
                            'text-align':'center',

                            'border':'3px solid #5E503F',
                            'padding':'20px 100px 20px 100px',
                            'margin-top':10,
                            'width':'60%',

                            'color':colors['very_light'],
                            'background-color':colors['dark'],
                            'border-radius':'40px'
                        })
    ), style={
        'display':'flex',
        'justify-content':'center',
        'align-items':'center',
    }),

    # html.Hr(),
    # html.Br(),

    # SEKCJA WYBÓR WYKRESÓW
        html.Div(id='options-cont', children=(
            html.Div([
                html.H2(children='Wybierz wykres',
                        style={
                            'font-size':25,
                            'font-family':'Georgia',
                            'color':colors['very_light'],
                }),

                dcc.Checklist(
                    id='check-1',
                    options=[
                        {'label':'Pomiar aktywności AChE','value':'ache'},
                        {'label':'Pomiar aktywności BuchE','value':'buche'}
                    ],
                    value = ['ache'],
                    labelStyle={'display':'block'},
                    style={'color':colors['very_light']}
                ),

                html.Br(),

                dcc.RadioItems(
                    id='radio-1',
                    options=[
                        {'label':'Efekt głowny czynnika DAWKA', 'value':'dawka'},
                        {'label':'Efekt głowny czynnika GODZINA', 'value':'godzina'},
                        {'label':'Efekt głowny czynnika DOBA', 'value':'doba'},
                        {'label':'Efekt interakcyjny DAWKA*GODZINA', 'value':'dawka*godzina'},
                        {'label':'Efekt interakcyjny GODZINA*DOBA', 'value':'godzina*doba'},
                        {'label':'Efekt interakcyjny DAWKA*DOBA', 'value':'dawka*doba'},
                        {'label':'Efekt interakcyjny DAWKA*GODZINA*DOBA', 'value':'dawka*godzina*doba'},
                    ],
                    value = 'dawka',
                    labelStyle={'display':'block'},
                    style={
                        'font-family':'Georgia',
                        'color':colors['very_light']}
                )], style={'margin-right':20}),

            html.Br(),

            html.Div([
                html.H2(children='Interpretacja wyników',
                        style={
                            'font-size':25,
                            'font-family':'Georgia',
                            'color':colors['very_light']}),
                html.H3(id='inter',
                        children='Interpretacja wyników',
                        style={
                            'font-size':20,
                            'font-family':'Georgia',
                            # 'border':'1px solid',
                            'color':colors['very_light']}),
            ], style={
                'border':'1px solid #C6AC8F',
                'padding':'10px',
                'margin-left':20,
                'width':600,
                'max-height':350,
            }),


        ), style={
            'padding':20,
            'width':'90%',
            'margin':'0px auto',

            'display':'flex',
            'justify-content':'center',
            'align-items':'center',

            'background-color':colors['dark'],
            'border-radius':'40px',
            'border':'3px solid #5E503F',
        }),

    html.Br(),

    html.Div([
        # SEKCJA WYKRES
        html.Div(children=([
            dcc.Graph(id='graph-1',
                      style={
                          'max-width':850,
                          'margin':'0px auto'
                      }),
        ]),
                 style={
                    'padding':'20px',
                    'width':850,
                    'margin-right':'10px',

                     # 'float':'right',

                    'background-color':colors['dark'],
                    'border-radius':'40px',
                    'border':'3px solid #5E503F',
                 }),

        # SEKCJA TABELE
        html.Div(id='tabele', children=(
            html.Div(children=(
                html.H3(id='ache_table_heading',
                        style={
                            'font-size': 14,
                            'font-family': 'Georgia',
                            # 'border':'1px solid',
                            'margin': '0px',
                            'color': colors['very_light']}),

                html.Div(id='table_ache',
                         style={
                             'min-width': 400,
                             # 'margin': '0px 50px 0px 40px',
                             'font-size': 12,
                             'font-family': 'Georgia',
                             # 'color':colors['very_light'],
                         }),
            )),

            html.Div(children=(
                html.H3(id='buche_table_heading',
                        style={
                            'font-size': 14,
                            'font-family': 'Georgia',
                            # 'border':'1px solid',
                            'margin': '0px',
                            'color': colors['very_light']}),

                html.Div(id='table_buche',
                         style={
                             'min-width': 400,
                             'margin': '0px',
                             'font-size': 12,
                             'font-family': 'Georgia',
                             # 'color':colors['very_light'],
                         }),
            ))
            ), style={
                'padding':'20px 0px 20px 0px',
                'width':550,
                'margin-left':'10px',

                # 'float':'left',

                'display':'flex',
                'flex-direction':'column',
                'justify-content':'center',
                'align-items':'center',

                'background-color':colors['dark'],
                'border-radius':'40px',
                'border':'3px solid #5E503F',
            })
        ], style={
        'width':'95%',
        'margin':'0px auto',

        'display':'flex',
        'flex-direction':'row',
        'justify-content':'center',
        'align-items':'center',

        'background-color':colors['very_dark'],
    }),

    html.Br(),

], style={
    'background-color':colors['very_dark'],
    'width':'100%',
    'height':'100%',
    'margin':'0px',
    'padding':'0px'
})
# _______________________________________________________________________


# _______________________________________________________________________
# FUNKJCE
# _______________________________________________________________________

# 1: efekty główne
dawki = ['0mg','0,5mg','5mg']   # dane do osi X
groups = df_raw.groupby(by='dawka') # grupowanie do wyciagniecia średniej z grup
temp = groups.mean()    # średnia z grup: dane do osi Y
df_dawka = temp[['AChE_mozg','BuchE_mozg']] # selekcja do AChe i Buche
labels_dawka_ache = ['11,14','12,81','12,92']
labels_dawka_buche = ['1,67','1,92','1,92']

godziny = ['7h','12h']
groups = df_raw.groupby(by='godziny')
temp = groups.mean()
df_godziny = temp[['AChE_mozg','BuchE_mozg']]
labels_godziny_ache = ['12,12','12,50']
labels_godziny_buche = ['1,59','2,09']


doby = ['4 doba','7 doba','10 doba']
groups = df_raw.groupby(by='doba')
temp = groups.mean()
df_doby = temp[['AChE_mozg','BuchE_mozg']]
labels_doby_ache = ['3,01', '14,57', '19,26']
labels_doby_buche = ['1,53', '1,99', '2,00']


def new_trace(ache_or_buche,x_values,y_values, labels, effect):
    '''

    :param ache_or_buche: 0-ache, 1-buche
    :param x_values:
    :param y_values:
    :param labels: points' lables on the graph
    :param effect: independent variable effect from radio-items
    :return: graph
    '''

    if ache_or_buche == 0:
        trace = go.Scatter(name='Aktywność AChE',
                           x=x_values,
                           y=y_values,
                           marker_color='#00183d',
                           mode='markers+lines',
                           # text=labels,
                           # textposition='bottom center',
                           # textfont=dict(size=16),
                           showlegend=True
                           )
        return trace
    else:
        trace = go.Scatter(name='Aktywność BuchE',
                                x=x_values,
                                y=y_values,
                                marker_color='#ffa600',
                                mode='markers+lines',
                                # text=labels,
                                # textposition='bottom center',
                                # textfont=dict(size=16),
                                showlegend = True
                                )
        return trace

# efekt interakcji 2-czynniki
groups_dawka_godzina = df_raw.groupby(by=['dawka','godziny']) #grupowanie danych
temp = groups_dawka_godzina.mean() #wyciąganie średniej
temp.reset_index(inplace=True) #reset indeksu
del temp['id'] #usuwanie niepotrzebnych kolumn na kopi df
del temp['doba']
del temp['AChE_mies']
del temp['BuchE_mies']
df_dawka_godziny = temp.copy()
buche_dawka_7h = [df_dawka_godziny['BuchE_mozg'][0],df_dawka_godziny['BuchE_mozg'][2],df_dawka_godziny['BuchE_mozg'][4]] #przygotowanie listy danych do wykresu
buche_dawka_12h = [df_dawka_godziny['BuchE_mozg'][1],df_dawka_godziny['BuchE_mozg'][3],df_dawka_godziny['BuchE_mozg'][5]]
ache_dawka_7h = [df_dawka_godziny['AChE_mozg'][0],df_dawka_godziny['AChE_mozg'][2],df_dawka_godziny['AChE_mozg'][4]]
ache_dawka_12h = [df_dawka_godziny['AChE_mozg'][1],df_dawka_godziny['AChE_mozg'][3],df_dawka_godziny['AChE_mozg'][5]]

groups_godzina_doba = df_raw.groupby(by=['godziny','doba'])
temp = groups_godzina_doba.mean()
temp.reset_index(inplace=True)
del temp['id']
del temp['dawka']
del temp['AChE_mies']
del temp['BuchE_mies']
df_godziny_doba = temp.copy()
buche_doba_7h = [df_godziny_doba['BuchE_mozg'][0],df_godziny_doba['BuchE_mozg'][1],df_godziny_doba['BuchE_mozg'][2]]
buche_doba_12h = [df_godziny_doba['BuchE_mozg'][3],df_godziny_doba['BuchE_mozg'][4],df_godziny_doba['BuchE_mozg'][5]]
ache_doba_7h = [df_godziny_doba['AChE_mozg'][0],df_godziny_doba['AChE_mozg'][1],df_godziny_doba['AChE_mozg'][2]]
ache_doba_12h = [df_godziny_doba['AChE_mozg'][3],df_godziny_doba['AChE_mozg'][4],df_godziny_doba['AChE_mozg'][5]]

groups_dawka_doba = df_raw.groupby(by=['dawka','doba'])
temp = groups_dawka_doba.mean()
temp.reset_index(inplace=True)
del temp['id']
del temp['godziny']
del temp['AChE_mies']
del temp['BuchE_mies']
df_dawka_doba = temp.copy()
buche_doba_0mg = [df_dawka_doba['BuchE_mozg'][0],df_dawka_doba['BuchE_mozg'][1],df_dawka_doba['BuchE_mozg'][2]]
buche_doba_05mg = [df_dawka_doba['BuchE_mozg'][3],df_dawka_doba['BuchE_mozg'][4],df_dawka_doba['BuchE_mozg'][5]]
buche_doba_5mg = [df_dawka_doba['BuchE_mozg'][6],df_dawka_doba['BuchE_mozg'][7],df_dawka_doba['BuchE_mozg'][8]]
ache_doba_0mg = [df_dawka_doba['AChE_mozg'][0],df_dawka_doba['AChE_mozg'][1],df_dawka_doba['AChE_mozg'][2]]
ache_doba_05mg = [df_dawka_doba['AChE_mozg'][3],df_dawka_doba['AChE_mozg'][4],df_dawka_doba['AChE_mozg'][5]]
ache_doba_5mg = [df_dawka_doba['AChE_mozg'][6],df_dawka_doba['AChE_mozg'][7],df_dawka_doba['AChE_mozg'][8]]

print()

def new_trace_2(ache_or_buche,names,x_values,y_values):

    traces = []
    styles = [None,'dash','dot','']
    how_many = len(names)

    for i in range(how_many):
        if ache_or_buche == 0:
            trace = go.Scatter(name=f'Aktywność AChE: {names[i]}',
                               x=x_values,
                               y=y_values[i],
                               marker_color='#00183d',
                               mode='lines+markers',
                               line=dict(dash=styles[i]),
                               # text=labels_1,
                               # textposition='bottom center',
                               # textfont=dict(size=16),
                               showlegend=True
                               )
            traces.append(trace)
        else:
            trace = go.Scatter(name=f'Aktywność BuchE: {names[i]}',
                               x=x_values,
                               y=y_values[i],
                               marker_color='#ffa600',
                               mode='lines+markers',
                               line=dict(dash=styles[i]),
                               # text=labels_1,
                               # textposition='bottom center',
                               # textfont=dict(size=16),
                               showlegend=True
                               )
            traces.append(trace)

    return traces

# efekt interakcji: 3 czynniki
dawka_0 = df_raw['dawka'] == 0 #przygotowanie filtrów do subplotów
dawka_1 = df_raw['dawka'] == 1
dawka_2 = df_raw['dawka'] == 2

groups_doba_godziny_0 = df_raw[dawka_0].groupby(by=['doba','godziny']) #grupowanie danych
temp = groups_doba_godziny_0.mean() #wyciąganie średniej
temp.reset_index(inplace=True) #reset indeksu
del temp['id'] #usuwanie niepotrzebnych kolumn
del temp['AChE_mies']
del temp['BuchE_mies']
df_doba_godziny_0 = temp.copy()
ache_doba_7h_0 = [df_doba_godziny_0['AChE_mozg'][0],df_doba_godziny_0['AChE_mozg'][2],df_doba_godziny_0['AChE_mozg'][4]] #przygotowanie listy danych
ache_doba_12h_0 = [df_doba_godziny_0['AChE_mozg'][1],df_doba_godziny_0['AChE_mozg'][3],df_doba_godziny_0['AChE_mozg'][5]]
buche_doba_7h_0 = [df_doba_godziny_0['BuchE_mozg'][0],df_doba_godziny_0['BuchE_mozg'][2],df_doba_godziny_0['BuchE_mozg'][4]]
buche_doba_12h_0 = [df_doba_godziny_0['BuchE_mozg'][1],df_doba_godziny_0['BuchE_mozg'][3],df_doba_godziny_0['BuchE_mozg'][5]]

groups_doba_godziny_1 = df_raw[dawka_1].groupby(by=['doba','godziny'])
temp = groups_doba_godziny_1.mean()
temp.reset_index(inplace=True)
del temp['id']
del temp['AChE_mies']
del temp['BuchE_mies']
df_doba_godziny_1 = temp.copy()
ache_doba_7h_1 = [df_doba_godziny_1['AChE_mozg'][0],df_doba_godziny_1['AChE_mozg'][2],df_doba_godziny_1['AChE_mozg'][4]]
ache_doba_12h_1 = [df_doba_godziny_1['AChE_mozg'][1],df_doba_godziny_1['AChE_mozg'][3],df_doba_godziny_1['AChE_mozg'][5]]
buche_doba_7h_1 = [df_doba_godziny_1['BuchE_mozg'][0],df_doba_godziny_1['BuchE_mozg'][2],df_doba_godziny_1['BuchE_mozg'][4]]
buche_doba_12h_1 = [df_doba_godziny_1['BuchE_mozg'][1],df_doba_godziny_1['BuchE_mozg'][3],df_doba_godziny_1['BuchE_mozg'][5]]

groups_doba_godziny_2 = df_raw[dawka_2].groupby(by=['doba','godziny'])
temp = groups_doba_godziny_2.mean()
temp.reset_index(inplace=True)
del temp['id']
del temp['AChE_mies']
del temp['BuchE_mies']
df_doba_godziny_2 = temp.copy()
ache_doba_7h_2 = [df_doba_godziny_2['AChE_mozg'][0],df_doba_godziny_2['AChE_mozg'][2],df_doba_godziny_2['AChE_mozg'][4]]
ache_doba_12h_2 = [df_doba_godziny_2['AChE_mozg'][1],df_doba_godziny_2['AChE_mozg'][3],df_doba_godziny_2['AChE_mozg'][5]]
buche_doba_7h_2 = [df_doba_godziny_2['BuchE_mozg'][0],df_doba_godziny_2['BuchE_mozg'][2],df_doba_godziny_2['BuchE_mozg'][4]]
buche_doba_12h_2 = [df_doba_godziny_2['BuchE_mozg'][1],df_doba_godziny_2['BuchE_mozg'][3],df_doba_godziny_2['BuchE_mozg'][5]]

ache_3factor_list = [ache_doba_7h_0, ache_doba_12h_0,
                     ache_doba_7h_1, ache_doba_12h_1,
                     ache_doba_7h_2, ache_doba_12h_2]
buche_3factor_list = [buche_doba_7h_0, buche_doba_12h_0,
                      buche_doba_7h_1, buche_doba_12h_1,
                      buche_doba_7h_2, buche_doba_12h_2]


def new_trace_3(ache_or_buche,names,x_values,y_values):

    traces = []
    styles = [None,'dash','dot']
    how_many = len(y_values)
    colors_ache = ['#00850b','#00850b', '#8f7300','#8f7300','#8c1500','#8c1500']
    colors_buche = ['#00ff15','#00ff15', '#ffcd00','#ffcd00','#ff2600','#ff2600']
    j = 0

    for i in range(how_many):
        if ache_or_buche == 0:
            trace = go.Scatter(name=f'Aktywność AChE: {names[j]}',
                               x=x_values,
                               y=y_values[i],
                               marker_color=colors_ache[i],
                               mode='lines+markers',
                               line=dict(dash=styles[j]),
                               # text=labels_1,
                               # textposition='bottom center',
                               # textfont=dict(size=16),
                               showlegend=True
                               )
            traces.append(trace)
            j += 1
        else:
            trace = go.Scatter(name=f'Aktywność BuchE: {names[j]}',
                               x=x_values,
                               y=y_values[i],
                               marker_color=colors_buche[i],
                               mode='lines+markers',
                               line=dict(dash=styles[j]),
                               # text=labels_1,
                               # textposition='bottom center',
                               # textfont=dict(size=16),
                               showlegend=True
                               )
            traces.append(trace)
            j += 1

        if j == 2:
            j = 0

    return traces

# tworzenie tabeli dash
def make_dash_table(df):
    '''
    :param df: DataFrame to table
    :return: dash table made from given DataFrame
    '''
    return dash_table.DataTable(
                columns = [{'name':col, 'id':col} for col in df.columns],
                data = df.to_dict('records')
            )
# _______________________________________________________________________



# _______________________________________________________________________
# FUNKCJE INTERAKTYWNE
# _______________________________________________________________________

# rysowanie wykresów
@app.callback(
    Output('graph-1','figure'),
    [
        Input('radio-1','value'),
        Input('check-1','value'),
    ]
)
def draw_graph(radio,check):
    traces = []
    if radio == 'dawka*godzina*doba':
        fig = make_subplots(rows=3, cols=1, subplot_titles=('AA = 0mg', 'AA = 0,5mg', 'AA = 5mg'))
    else:
        fig = make_subplots(rows=1, cols=1)

    # TWORZENIE WYKRESÓW WYBRANYCH PRZEZ UZYTKOWNIKA
    if 'ache' in check:
        if radio == 'dawka':
            trace = new_trace(0, dawki, df_dawka['AChE_mozg'], labels_dawka_ache, radio)
            traces.append(trace)
        elif radio == 'godzina':
            trace = new_trace(0, godziny, df_godziny['AChE_mozg'], labels_godziny_ache, radio)
            traces.append(trace)
        elif radio == 'doba':
            trace = new_trace(0, doby, df_doby['AChE_mozg'], labels_doby_ache, radio)
            traces.append(trace)
        elif radio == 'dawka*godzina':
            traces = new_trace_2(0,['7h','12h'],dawki,[ache_dawka_7h,ache_dawka_12h])
        elif radio == 'godzina*doba':
            traces = new_trace_2(0,['7h','12h'],doby,[ache_doba_7h,ache_doba_12h])
        elif radio == 'dawka*doba':
            traces = new_trace_2(0,['0mg','0,5mg','5mg'],doby,[ache_doba_0mg,ache_doba_05mg,ache_doba_5mg])
        elif radio == 'dawka*godzina*doba':
            traces = new_trace_3(0,['7h','12h'],doby,ache_3factor_list)

        # DODANIE WYKRESU W ODPOWIEDNIM WIERSZU
        if len(traces) == 6:
            r = 1
            i = 1
            for t in traces:
                if i in [3,5]:
                    r += 1
                fig.add_trace(t, row=r, col=1)
                i += 1

        else:
            for t in traces:
                fig.add_trace(t, row=1, col=1)

    if 'buche' in check:
        if radio == 'dawka':
            trace = new_trace(1, dawki, df_dawka['BuchE_mozg'], labels_dawka_buche, radio)
            traces.append(trace)
        elif radio == 'godzina':
            trace = new_trace(1, godziny, df_godziny['BuchE_mozg'], labels_godziny_buche, radio)
            traces.append(trace)
        elif radio == 'doba':
            trace = new_trace(1, doby, df_doby['BuchE_mozg'], labels_doby_buche, radio)
            traces.append(trace)
        elif radio == 'dawka*godzina':
            traces = new_trace_2(1, ['7h', '12h'], dawki, [buche_dawka_7h, buche_dawka_12h])
        elif radio == 'godzina*doba':
            traces = new_trace_2(1, ['7h', '12h'], doby, [buche_doba_7h, buche_doba_12h])
        elif radio == 'dawka*doba':
            traces = new_trace_2(1, ['0mg', '0,5mg', '5mg'], doby,[buche_doba_0mg, buche_doba_05mg, buche_doba_5mg])
        elif radio == 'dawka*godzina*doba':
            traces = new_trace_3(1,['7h','12h'],doby,buche_3factor_list)

        # DODANIE WYKRESU W ODPOWIEDNIM WIERSZU
        if len(traces) == 6:
            r = 1
            i = 1
            for t in traces:
                if i in [3, 5]:
                    r += 1
                fig.add_trace(t, row=r, col=1)
                i += 1

        else:
            for t in traces:
                fig.add_trace(t, row=1, col=1)

    if check == []:
        fig = go.Figure()

    # TYTUŁ WYKRESU CZ.1
    if radio in ['dawka','godzina','doba']:
        title = 'Efekt główny czynnika'
    else:
        title = 'Efekt interakcyjny czynników'

    # TYTUŁ WYKRESU CZ.1
    ache_or_buche = ''
    if 'ache' in check and 'buche' in check:
        ache_or_buche = 'dla aktywności AChE i BuchE  w mózgowiu'
    elif 'ache' in check:
        ache_or_buche = 'dla aktywności AChE  w mózgowiu'
    elif 'buche' in check:
        ache_or_buche = 'dla aktywności BuchE  w mózgowiu'
    else:
        ache_or_buche = ''

    fig.update_layout(title=f'{title} {radio.upper()} {ache_or_buche}',
                      width=850,
                      # height=700,
                      font=dict(
                          family='Georgia',
                          size=12
                        ))
    fig.update_yaxes(rangemode='tozero')

    return fig

# komunikat z interpretacją wyników
@app.callback(
    Output('inter','children'),
    [
        Input('radio-1','value'),
        Input('check-1','value'),
    ]
)
def interpretation(radio,check):
    text_ache = ''
    text_buche = ''
    heading_ache = ''
    heading_buche = ''

    if 'ache' in check:
        heading_ache = 'AChE'
        if radio == 'dawka':
            text_ache = 'Na podsatwie testu ANOVA NIE obserwuje się istotnych różnic w aktywności AChE w mózgowiu\
             wynikających z podania różnych dawek AA (F(86,2)=0,41, p=0,663)'
        elif radio == 'godzina':
            text_ache = 'Na podsatwie test t-Studenta NIE obserwuje się istotnych różnic w aktywności AChE w mózgowiu\
             wynikających z różnych godzin pomiarowaych (t(87)=-0,21, p=0,835)'
        elif radio == 'doba':
            text_ache = 'Wyniki testu ANOVA oraz testów post-hoc (Tukey) wskazują na istotne różnice w aktywności AChE w mózgowiu\
             między wszsytkimi dobami (F(86,2)=93,35, p<0,001). Efekt ten uznaje się za bardzo duży (η2 = 68%)'
        elif radio == 'dawka*godzina':
            text_ache = 'Na podstawie testu 3-ANOVA NIE obserwuje się istotnego efektu interakcji dla aktywności AChE w mózgowiu\
             (F(71,2)=1,01, p=0,369)'
        elif radio == 'godzina*doba':
            text_ache = 'Na podstawie testu 3-ANOVA NIE obserwuje się istotnego efektu interakcji dla aktywności AChE w mózgowiu\
             (F(71,2)=0,81, p=0,451)'
        elif radio == 'dawka*doba':
            text_ache = 'Na podstawie testu 3-ANOVA NIE obserwuje się istotnego efektu interakcji dla aktywności AChE w mózgowiu\
             (F(71,4)=1,05, p=0,387)'
        elif radio == 'dawka*godzina*doba':
            text_ache = 'Na podstawie testu 3-ANOVA NIE obserwuje się istotnego efektu interakcji dla aktywności AChE w mózgowiu\
             (F(71,4)=0,97, p=0,429)'

    if 'buche' in check:
        heading_buche = 'BuchE'
        if radio == 'dawka':
            text_buche = 'Na podsatwie testu ANOVA NIE obserwuje się istotnych różnic w aktywności BuchE w mózgowiu\
             wynikających z podania różnych dawek AA (F(86,2)=1,70, p=0,188'
        elif radio == 'godzina':
            text_buche = 'Wyniki testu t-Studenta wskazują na istotnie wyższą aktywność BuchE w mózgowiu\
             pdoczas pomiarów o godz. 12:00 niż o godz. 7:00 (t(87)=-4,29, p<0,001). Efekt ten uznaje się za duży (d=0,91).'
        elif radio == 'doba':
            text_buche = 'Wyniki testu ANOVA oraz testów post-hoc (Tukey) wskazują na istotne różnice w aktywności BuchE w mózgowiu\
             między 4-tą a 7-mą oraz 4-tą a 100tą dobą (F(86,2)=6,89, p=0,002). Efekt ten uznaje się za przeciętny (η2 = 14%)'
        elif radio == 'dawka*godzina':
            text_buche = 'Wynik testu 3-ANOVA wykazał istotny efekt interakcji dla aktywności BuchE w mózgowiu\
             (F(71,2)=8,87, p<0,001)'
        elif radio == 'godzina*doba':
            text_buche = 'Na podstawie testu ANOVA NIE obserwuje się istotnego efektu interakcji dla aktywności AChE w mózgowiu\
             (F(71,4)=2,28, p=0,0,70)'
        elif radio == 'dawka*doba':
            text_buche = 'Wynik testu 3-ANOVA wykazał istotny efekt interakcji dla aktywności BuchE w mózgowiu\
             (F(71,2)=5,73, p=0,005)'
        elif radio == 'dawka*godzina*doba':
            text_buche = 'Wynik testu 3-ANOVA wykazał istotny efekt interakcji dla aktywności BuchE w mózgowiu\
             (F(71,4)=6,81, p<0,001)'

    # FORMAT INTERPRETACJI
    if 'ache' in check and 'buche' in check:
        text = [heading_ache,html.Br(),text_ache,html.Br(),html.Br(),heading_buche,html.Br(),text_buche]
    elif 'ache' in check:
        text = [heading_ache, html.Br(), text_ache]
    elif 'buche' in check:
        text = [heading_buche, html.Br(), text_buche]
    else:
        text = ''

    return text


# wrzucanie tabel
@app.callback(
    [
        Output('ache_table_heading','children'),
        Output('table_ache','children'),
        # Output('table_ache','style'),
        Output('buche_table_heading','children'),
        # Output('buche_table_heading','style'),
        Output('table_buche','children')
    ],
    [
        Input('radio-1','value'),
        Input('check-1','value'),
    ]
)
def draw_table(radio,check):
    table_ache = ''
    table_buche = ''
    heading_ache = ''
    heading_buche = ''

    if 'ache' in check:
        heading_ache = 'Tabela dla aktywności AChE'
        if radio == 'dawka':
            table_ache = make_dash_table(table_dawka_ache)
        elif radio == 'godzina':
            table_ache = make_dash_table(table_godziny_ache)
        elif radio == 'doba':
            table_ache = make_dash_table(table_doby_ache)
        else:
            table_ache = make_dash_table(table_3anova_ache)


    if 'buche' in check:
        heading_buche = 'Tabela dla aktywności BuchE'
        if radio == 'dawka':
            table_buche = make_dash_table(table_dawka_buche)
        elif radio == 'godzina':
            table_buche = make_dash_table(table_godziny_buche)
        elif radio == 'doba':
            table_buche = make_dash_table(table_doby_buche)
        else:
            table_buche = make_dash_table(table_3anova_buche)

    # FORMATOWANIE TABEL
    if 'ache' in check and 'buche' in check:
        tables = [[heading_ache, html.Br()], [table_ache, html.Br()], [heading_buche, html.Br()], [table_buche, html.Br()]]
    elif 'ache' in check:
        tables =  [[heading_ache, html.Br()], [table_ache, html.Br()],None,None]
    elif 'buche' in check:
        tables = [[heading_buche, html.Br()], [table_buche, html.Br()],None,None]
    else:
        tables = [html.Br(), html.Br(),None,None]

    # STYLE TABEL
    # style_ache = ''
    # style_buche = ''
    # if radio in ['dawka','godziny','doby']:
    #     if 'ache' in check and 'buche' in check:
    #         style_ache =

    return tables



if __name__ == '__main__':
    app.run_server(debug=True)
