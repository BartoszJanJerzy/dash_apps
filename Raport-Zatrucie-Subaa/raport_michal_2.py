import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots

# _______________________________________________________________________
# STYLE
from style import colors, style_head, style_head_2, style_graph_choice, style_interpretation_h2, style_interpretation_h3,\
    style_interpretation_cont, style_options_cont, style_graph, style_ache_table, style_ache_table_2,\
    style_buche_table, style_buche_table_2, style_tabele, style_tabele_2, style_whole

#zewnetrzny styl wizualny
external_stylesheets = ['http://codepen.io/chriddyp/pen/bWLwgP.css']

# _______________________________________________________________________
# DANE
from data import table_3anova_buche, table_doby_buche, table_dawka_buche, table_godziny_ache, table_godziny_buche,\
    table_3anova_ache, table_doby_ache, table_dawka_ache, df_raw, df_mozg

# _______________________________________________________________________
# UKŁAD APLIKAJI
# _______________________________________________________________________
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)  # tworzenie klasy Dash
server = app.server

app.layout = html.Div([

    # SEKCJA NAGŁÓWEK
    html.Div(id='div-head', children=(
        html.H1(id="head-1", children="Raport wyników - zatrucie substancją AA",
                        style=style_head)
    ), style=style_head_2),

    # SEKCJA WYBÓR WYKRESÓW
        html.Div(id='options-cont', children=(
            html.Div([
                html.H2(children='Wybierz wykres',
                        style=style_graph_choice),

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
                        style=style_interpretation_h2),
                html.H3(id='inter',
                        children='Interpretacja wyników',
                        style=style_interpretation_h3),
            ], style=style_interpretation_cont),


        ), style=style_options_cont),

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
            style=style_graph),

        # SEKCJA TABELE
        html.Div(id='tabele', children=(
            html.Div(children=(
                html.H3(id='ache_table_heading',
                        style=style_ache_table),

                html.Div(id='table_ache',
                         style=style_ache_table_2),
            )),

            html.Div(children=(
                html.H3(id='buche_table_heading',
                        style=style_buche_table),

                html.Div(id='table_buche',
                         style=style_buche_table_2),
            ))
            ), style=style_tabele)
        ], style=style_tabele_2),

    html.Br(),

], style=style_whole)
# _______________________________________________________________________


# _______________________________________________________________________
# FUNKJCE
# _______________________________________________________________________

# 1: efekty główne
from data import dawki, df_dawka, labels_dawka_ache, labels_dawka_buche,\
    godziny, df_godziny, labels_godziny_ache, labels_godziny_buche, \
    doby, df_doby, labels_doby_ache, labels_doby_buche, new_trace

# efekt interakcji 2-czynniki
from data import buche_dawka_7h, buche_dawka_12h, ache_dawka_7h, ache_dawka_12h,\
    buche_doba_7h, buche_doba_12h, ache_doba_7h, ache_doba_12h,\
    ache_doba_05mg, ache_doba_5mg, ache_doba_0mg, buche_doba_0mg, buche_doba_05mg, buche_doba_5mg, new_trace_2

# efekt interakcji: 3 czynniki
from data import ache_3factor_list, buche_3factor_list, new_trace_3

# tworzenie tabeli dash
from data import make_dash_table
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

    return tables

if __name__ == '__main__':
    app.run_server(debug=True)