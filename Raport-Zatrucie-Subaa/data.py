import plotly.graph_objects as go
import pandas as pd

# biblioteka do tabel
import dash_table

# dane ogólne
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

# 2: efekt interakcji w czynniki
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

# 3: interacja 3 czynników
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

def make_dash_table(df):
    '''
    :param df: DataFrame to table
    :return: dash table made from given DataFrame
    '''
    return dash_table.DataTable(
                columns = [{'name':col, 'id':col} for col in df.columns],
                data = df.to_dict('records')
    )