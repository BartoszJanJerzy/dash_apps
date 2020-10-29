import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import time

#biblioteka do prevent-uptade
from dash.exceptions import PreventUpdate

# _______________________________________________________________________
# STYLE

#zewnetrzny styl wizualny
external_stylesheets = ['http://codepen.io/chriddyp/pen/bWLwgP.css']
# a ciemny: https://codepen.io/chriddyp/pen/LYpwVWm

from style import style_h1, style_h2, style_button, style_container, style_answer_true, style_answer_false
# _______________________________________________________________________

# _______________________________________________________________________
# DANE

from data import questions, answers, questionPages

# _______________________________________________________________________


# _______________________________________________________________________
# UKŁAD APLIKAJI
# _______________________________________________________________________
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)  # tworzenie klasy Dash
server = app.server

app.layout = html.Div([
    html.Br(),

    html.H1("Zadania z metod statystycznych", style=style_h1),
    html.Div(
        html.Button(id='start-button', children='Start', n_clicks=0, style=style_button),
    style={'width':500, 'margin':'0px auto', 'text-align':'center'}),
    html.H2(id='h2',children="Zaznacz, czy zdanie jest prawdziwe, czy fałszywe", style={'display':'none'}),

    html.Br(),

    html.Div(questionPages[0], style={'margin':'0px 100px 0px 100px'})
], style=style_container)
# _______________________________________________________________________



# _______________________________________________________________________
# FUNKCJE INTERAKTYWNE
# _______________________________________________________________________

def MakeCallbacks(current, answers, reverse, pages):
    @app.callback(
        [
            Output(f'answer-{current}', 'style'),
            Output(f'answer-{current}', 'children'),
            Output(f'radio-quest-{current}', 'options'),
            Output(f'next-quest-{current}', 'children')
        ],
        [
            Input(f'radio-quest-{current}', 'value'),
        ]
    )
    def MakeAnswer(value):
        result = ''
        color = ''
        nextPage = ''
        answer = ''
        style_answer = ''

        options = [
            {'label': 'Prawda', 'value': 'true', 'disabled': True},
            {'label': 'Fałsz', 'value': 'false', 'disabled': True}
        ]

        if reverse == 1:
            if value == 'true':
                result = 'Twoja odpowiedź "Prawda" jest zła!'
                style_answer = style_answer_false
            elif value == 'false':
                result = 'Twoja odpowiedź "Fałsz" jest dobra!'
                style_answer = style_answer_true
            else:
                raise PreventUpdate
        else:
            if value == 'true':
                result = 'Twoja odpowiedź "Prawda" jest dobra!'
                style_answer = style_answer_true
            elif value == 'false':
                result = 'Twoja odpowiedź "Fałsz" jest zła!'
                style_answer = style_answer_false
            else:
                raise PreventUpdate

        if current == len(answers):
            nextPage = html.Div([
                html.A(children='Powtórz test',href='https://test-metody-stat.herokuapp.com/', style=style_button),
                html.Br(),
                html.Br(),
                html.Hr(),
            ])
            answer = answers[current - 1]
        else:
            nextPage = pages[current]
            answer = answers[current - 1]

        return (style_answer,
                [result, html.Br(), answer],
                options,
                nextPage)

# SHOW QUESTION 1
@app.callback(
    [
        Output('quest-1-container', 'style'),
        Output('h2', 'style'),
        Output('start-button', 'style')
    ],
    Input('start-button', 'n_clicks')
)
def ShowFirstQuestion(n_clicks):
    if n_clicks > 0:
        return {'display':'block'}, style_h2, {'display':'none'}
    else:
        return {'display':'none'}, {'display':'none'}, style_button

# ANSWER & SHOW NEXT QUESTIONS
MakeCallbacks(1,answers,1,questionPages)
MakeCallbacks(2,answers,0,questionPages)
MakeCallbacks(3,answers,1,questionPages)
MakeCallbacks(4,answers,1,questionPages)
MakeCallbacks(5,answers,1,questionPages)
MakeCallbacks(6,answers,0,questionPages)
MakeCallbacks(7,answers,1,questionPages)
MakeCallbacks(8,answers,0,questionPages)
MakeCallbacks(9,answers,0,questionPages)
MakeCallbacks(10,answers,0,questionPages)
MakeCallbacks(11,answers,1,questionPages)
MakeCallbacks(12,answers,1,questionPages)
MakeCallbacks(13,answers,0,questionPages)
MakeCallbacks(14,answers,1,questionPages)
MakeCallbacks(15,answers,0,questionPages)

# _______________________________________________________________________

if __name__ == '__main__':
    app.run_server(debug=True)
