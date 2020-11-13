import dash_core_components as dcc
import dash_html_components as html

# biblioteka do tabel
import dash_table


#style
from style import style_upload, style_uplaod_page, style_table, style_table_div, style_button, style_h1, style_h2, \
    style_h3, style_h4, style_comment, style_graph, style_verify, style_button_div, style_dropdown, style_button_2, \
    style_button_3


# PODSTRONY
upload_page = html.Div(children=[
                           html.Div(id='headings-div', children=[
                               html.H1('Witaj głodny rzetelnej nauki człowieku!', style=style_h1),
                               html.H2('Jestem aplikacją, która sprawdzi czy podane przez Ciebie zmienne '
                                       'mają związek liniowy...', style=style_h2),
                               html.H2('... a może okaże się, że jest on nieco bardziej złożony?',
                                       style=style_h2),

                               html.Br(),

                               html.H3('Przede wszystkim, daj mi swój plik z bazą wyników.', style=style_h3),
                               html.H3('Przyjmuję tylko format ".csv".', style=style_h3),
                               html.H4('(Jeśli dasz mi dużą bazę, to zaczekaj kilka chwil zanim ją wyświetlę)',
                                       style=style_comment),

                               dcc.Upload(
                                   id='upload-data',
                                   children=html.Div('Przeciągnij plik tutaj lub kliknij na mnie'),
                                   filename='',
                                   style=style_upload,
                               ),
                           ]),

                           html.Div(id='verify-file-div', style=style_verify)
                       ],
                       style=style_uplaod_page)

def ComparedR2Page(x, y, linear, deg2, deg3, deg4):
    return html.Div(id='compared-r2',
                    children=[
                        html.H3(f"Predyktor X: {x}    Zmienna zależna Y: {y}", style=style_h3),
                        html.H4(f"R^2 regresji liniowej wynosi {linear}", style=style_h4),
                        html.H4(f"R^2 regresji stopnia 2' wynosi {deg2}", style=style_h4),
                        html.H4(f"R^2 regresji stopnia 3' wynosi {deg3}", style=style_h4),
                        html.H4(f"R^2 regresji stopnia 4' wynosi {deg4}", style=style_h4),
                    ])

def TablePage(raw_data):
    return html.Div(id='upload-data-div',
                 children=[
                 html.Br(),
                 html.Div(id='button-div',
                          children=[
                              html.A(html.Button(id='confirm-data-button',
                                                 children='Jeśli to są Twoje, to kliknij i przejdź dalej!',
                                                 n_clicks=0,
                                                 style=style_button),
                                     href='#refresh-button-2'),
                              html.A(html.Button(id='refresh-button',
                                                 children='Lub kliknij tutaj i daj mi inny plik!',
                                                 style=style_button_2
                                                 ),
                                     href='/', ),
                          ],
                          style=style_button_div),
                 html.Br(),
                 dcc.Loading(children=html.Div(id='table-div',
                                               children=(
                                                  dash_table.DataTable(
                                                      id='table',
                                                      columns=[{'name': col, 'id': col} for col in raw_data.columns],
                                                      data=raw_data.to_dict('records'),
                                                      style_table=style_table
                                                  )
                                              ),
                                              style=style_table_div),
                             style={'margin':'200px auto',
                                    'transform':'scale(2)'}
                             )

                 ]),

select_variable_page = html.Div(id='',
                                children=[
                                    html.Div(id='choose-data-div',
                                                             children=[
                                                                 html.H3('Wybierz predytor X', style=style_h3),
                                                                 dcc.Dropdown(
                                                                  id='x-dropdown',
                                                                  style=style_dropdown
                                                                ),

                                                              html.Br(),

                                                              html.H3('Wybierz zmienną zależną Y', style=style_h3),
                                                              dcc.Dropdown(
                                                                  id='y-dropdown',
                                                                  style=style_dropdown
                                                              ),
                                                          ]
                                             ),

                                    html.Div(id='compared-r2-div'),

                                    html.Div(id='select-subplots-div',
                                             children=[
                                                 html.H3('Wybierz regresję do zilustrowania', style=style_h3),
                                                 dcc.Checklist(
                                                     id='subplots-checklist',
                                                     options=[
                                                         {'label': 'Regresja liniowa', 'value': 'linear'},
                                                         {'label': "Regresja stopnia 2'", 'value': 'deg2'},
                                                         {'label': "Regresja stopnia 3'", 'value': 'deg3'},
                                                         {'label': "Regresja stopnia 4'", 'value': 'deg4'},
                                                     ],
                                                     labelStyle={'display': 'block', 'font-size': 20},
                                                     value=[],
                                                 )
                                             ],
                                             style={'display': 'none'}),

                                    html.Div(id='graph-div', style=style_graph),

                                    html.A(html.Button(id='refresh-button-2',
                                                       children='Może chcesz dac inny plik?',
                                                       style=style_button_3),
                                           href='/')
                                ])

def WrongFilePage(filename):
    return html.Div([
        html.H3(f'Niestety... Nie potrafię wykorzystać Twójego pliku "{filename}".', style=style_h3),
        html.A(html.Button(children='Kliknij tutaj i spróbuj jeszcze raz', style=style_button_2), href='/'),
    ])