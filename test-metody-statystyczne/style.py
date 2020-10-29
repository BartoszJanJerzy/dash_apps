colors = {
    'dark-grey':'#212121',
    'light-grey':'#b3b3b3',
    'light-green':'#9dcc9d',
    'light-red':'#cc7c7c',
}

style_container = {
    'background-color':colors['dark-grey'],
    'min-height':2000
}

style_h1 = {
    'width':700,
    'margin':'0px auto',
    'border':f'2px solid {colors["light-grey"]}',
    'border-radius':10,

    'text-align':'center',
    'font-size':40,
    'color':colors['light-grey'],
    'padding':'10px 100px'
}

style_h2 = {
    'width': 700,
    'margin': '50px auto 0px auto',

    'text-align': 'center',
    'font-size':30,
    'color': colors['light-grey'],
}

style_button = {
    'width':200,
    'margin':'10px auto',
    'padding':'10px 50px',
    'border':f'2px solid {colors["light-grey"]}',
    'border-radius':10,

    'background-color':'rgba(4, 89, 4, 0.25)',
    'color': colors['light-grey'],
    'text-align': 'center',
    'text-decoration':'none',
    'font-size': 30,
}

style_question = {
    'font-size': 20,
    'color': colors['light-grey'],
}

style_answer_true = {
    'font-size': 20,
    'color': colors['light-green'],
}

style_answer_false = {
    'font-size': 20,
    'color': colors['light-red'],
}