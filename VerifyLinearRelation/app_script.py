import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import base64


'''
1. Wrzucam plik .csv
2. Wyświetla tabelę do zweryfikowania danych
3. Wybieram kolumnę X i kolumnę Y
4. Sprawdza regresje liniową, 2', 3' i 4'
5. Wyświetla interaktywny wykres
'''

# _______________________________________________________________________
# IMPORTOWANIE MODUŁÓW
# style
from style import external_stylesheets, style_whole, style_dropdown, style_dropdown_div, style_uplaod_page, \
    style_select_subplot, style_compared_r2, style_button, style_button_2, style_first, style_second, style_author

# sekcje
from sections import upload_page, ComparedR2Page, select_variable_page, WrongFilePage, TablePage

# funkcje
from functions import parse_contents, CompareR2, SelectNumberCols, MakeGraphData, MakeGraph
# _______________________________________________________________________

# przygotowanie obrazu
background = r'background1.png'
encoded_background = base64.b64encode(open(background,"rb").read())

# _______________________________________________________________________
# UKŁAD APLIKAJI
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)  # tworzenie klasy Dash
app.config.suppress_callback_exceptions=True
server = app.server

'''
                 html.Img(src=f'data:image/png;base64,{encoded_background.decode()}',
                          style={'position':'absolute', 'top':0, 'z-index':0}),
'''

app.layout = html.Div([

    html.Div(id='first-page',
             children=[
                 html.Div("Bartosz Wójtowicz, kontakt: bartoszjanjerzy@gmail.com", style=style_author),
                 upload_page
             ],
             style=style_first),

    html.Div(id='second-page',
             children=[
                 html.Div("Bartosz Wójtowicz, kontakt: bartoszjanjerzy@gmail.com", style=style_author),
                 select_variable_page
             ],
             style={'display':'none'})
],
style=style_whole)
# _______________________________________________________________________

# WYŚWIETLANIE PODSTRON
@app.callback(
    Output('page-content','children'),
    [
        Input('url','pathname'),
    ]
)
def display_page(pathname):
    if pathname == '/tech':
        pass
    else:
        return upload_page

# SPRAWDZENIE POPRAWNOŚCI PLIKU
@app.callback(
    [
        Output('verify-file-div', 'children'),
        Output('upload-data', 'style'),
        Output('choose-data-div', 'style'),
        Output('second-page', 'style')
    ],
    Input('upload-data','contents'),
    State('upload-data','filename'),
)
def VerifyUploadedFile(contents, filename):
    children = ''
    style = {'display':'none'}

    if filename.lower().endswith('.csv'):
        raw_data = parse_contents(contents, 'csv')
        children = TablePage(raw_data)

        return children, style, style_dropdown_div, style_second

    elif len(filename) == 0:
        raise PreventUpdate

    else:
        children = WrongFilePage(filename)

        return children, style, style_dropdown_div, style


# POTWIERDZENIE PLIKU

@app.callback(
    [
        Output('confirm-data-button','style'),
        Output('x-dropdown', 'options'),
        Output('y-dropdown', 'options')
    ],
    Input('confirm-data-button', 'n_clicks'),
    State('upload-data','contents')
)
def HideTable_ShowResults(n_clicks, contents):
    style_none = {'display':'none'}

    if n_clicks >= 1:
        raw_data = parse_contents(contents, 'csv')
        columns = raw_data.columns
        df = SelectNumberCols(raw_data, columns)
        columns = df.columns

        print(columns)

        # lista kolumn do drop-down
        options_list = []
        for c in columns:
            option = {'label': c, 'value': c}
            options_list.append(option)

        return style_none, options_list, options_list
    else:
        return style_button, [], []

# POKAŻ WARTOŚCI R^2 + WYKRES
@app.callback(
    [
        Output('compared-r2-div', 'children'),
        Output('compared-r2-div', 'style'),
        Output('select-subplots-div', 'style'),
        Output('graph-div', 'children')
    ],
    [
        Input('x-dropdown','value'),
        Input('y-dropdown','value'),
        Input('upload-data', 'contents'),
        Input('subplots-checklist', 'value'),
    ]
)
def ShowComparedR2(x,y, contents, selected_subplots):

    if x and y:
        raw_data = parse_contents(contents, 'csv')
        columns = raw_data.columns
        df = SelectNumberCols(raw_data, columns)

        # dane do regresji
        X = df[x].to_numpy().reshape(-1, 1)
        Y = df[y].to_numpy().reshape(-1, 1)

        # porównanie R^2
        linear_r2, deg2_r2, deg3_r2, deg4_r2 = CompareR2(X, Y)

        # sekcja z R^2
        children = ComparedR2Page(x, y, linear_r2, deg2_r2, deg3_r2, deg4_r2)

        # dane do wykresów
        temp_df_deg1, temp_df_deg2, temp_df_deg3, temp_df_deg4 = MakeGraphData(X,Y)

        # wykres
        graph = MakeGraph(df[x], df[y], linear_r2, temp_df_deg1,
                          deg2_r2, temp_df_deg2, deg3_r2, temp_df_deg3, deg4_r2, temp_df_deg4, selected_subplots, x, y)

        return children, style_compared_r2, style_select_subplot, dcc.Graph(figure=graph)
    else:
        raise PreventUpdate


if __name__ == '__main__':
    app.run_server(debug=True)
