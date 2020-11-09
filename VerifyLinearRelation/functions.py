# biblitoeki do wykresów
import plotly.graph_objects as go

# biblitoeki do danych
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score
import pandas as pd

import base64
import io

# FUNKCJE
# file upload function
def parse_contents(contents, type):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if type == 'csv':
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif type == 'xlsx':
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))

    except Exception as e:
        print(e)
        return None

    return df


# usuniecie kolumn nie-liczbowych
def SelectNumberCols(df, columns):
    for c in columns:
        if df[c].dtype in ['int64', 'float']:
            pass
        else:
            del df[c]

    return df

# regresje
def CompareR2(X, Y):
    # regresja liniowa
    regressor = LinearRegression()
    regressor.fit(X, Y)
    y_pred_lin = regressor.predict(X)
    linear_r2 = r2_score(Y, y_pred_lin)

    # regresja stopnia 2
    poly = PolynomialFeatures(degree=2)
    X_2 = poly.fit_transform(X)
    regressor.fit(X_2,Y)
    y_pred_2 = regressor.predict(X_2)
    squared_r2 = r2_score(Y, y_pred_2)

    # regresja stopnia 3
    poly = PolynomialFeatures(degree=3)
    X_3 = poly.fit_transform(X)
    regressor.fit(X_3,Y)
    y_pred_3 = regressor.predict(X_3)
    deg3_r2 = r2_score(Y, y_pred_3)

    # regresja stopnia 4
    poly = PolynomialFeatures(degree=4)
    X_4 = poly.fit_transform(X)
    regressor.fit(X_4,Y)
    y_pred_4 = regressor.predict(X_4)
    deg4_r2 = r2_score(Y, y_pred_4)

    return linear_r2, squared_r2, deg3_r2, deg4_r2

def MakeGraphData(X, Y):
    # regresja liniowa
    regressor = LinearRegression()
    regressor.fit(X, Y)
    y_pred_lin = regressor.predict(X)
    linear_r2 = r2_score(Y, y_pred_lin)

    # dane do punktó regresji
    temp_df_deg1 = pd.DataFrame(X, columns=['x_col'])
    temp_df_deg1.sort_values(by='x_col', inplace=True)
    temp_df_1 = pd.DataFrame(y_pred_lin)
    temp_df_deg1['y_col'] = temp_df_1

    # regresja kwadratowa
    poly = PolynomialFeatures(degree=2)
    X_2 = poly.fit_transform(X)
    regressor.fit(X_2,Y)
    y_pred_2 = regressor.predict(X_2)
    squared_r2 = r2_score(Y, y_pred_2)

    # dane do punktów regresji
    temp_df_deg2 = pd.DataFrame(X, columns=['x_col'])
    temp_df_deg2.sort_values(by='x_col', inplace=True)
    temp_df_2 = pd.DataFrame(y_pred_2)
    temp_df_deg2['y_col'] = temp_df_2

    # regresja stopnia 3
    poly = PolynomialFeatures(degree=3)
    X_3 = poly.fit_transform(X)
    regressor.fit(X_3,Y)
    y_pred_3 = regressor.predict(X_3)
    deg3_r2 = r2_score(Y, y_pred_3)

    # dane do punktów regresji
    temp_df_deg3 = pd.DataFrame(X, columns=['x_col'])
    temp_df_deg3.sort_values(by='x_col', inplace=True)
    temp_df_3 = pd.DataFrame(y_pred_3)
    temp_df_deg3['y_col'] = temp_df_3

    # regresja stopnia 4
    poly = PolynomialFeatures(degree=4)
    X_4 = poly.fit_transform(X)
    regressor.fit(X_4,Y)
    y_pred_4 = regressor.predict(X_4)
    deg4_r2 = r2_score(Y, y_pred_4)

    # dane do punktów regresji
    temp_df_deg4 = pd.DataFrame(X, columns=['x_col'])
    temp_df_deg4.sort_values(by='x_col', inplace=True)
    temp_df_4 = pd.DataFrame(y_pred_4)
    temp_df_deg4['y_col'] = temp_df_4

    return temp_df_deg1, temp_df_deg2, temp_df_deg3, temp_df_deg4

def MakeGraph(df_X, df_Y, linear_r2, temp_df_deg1, deg2_r2, temp_df_deg2, deg3_r2, temp_df_deg3, deg4_r2, temp_df_deg4, selected_subplots, x_name, y_name):

    subplots = [
        go.Scatter(
            name='Wykres rozrzutu',
            x=df_X,
            y=df_Y,
            mode='markers',
            marker=dict(color='#a8a8a8')
        )
    ]

    if 'linear' in selected_subplots:
        new_plot = go.Scatter(
            name=f'Regresja liniowa: R^2={round(linear_r2,4)}',
            x=temp_df_deg1['x_col'],
            y=temp_df_deg1['y_col'],
            mode='lines',
            marker=dict(color='#A1C181')
        )
        subplots.append(new_plot)

    if 'deg2' in selected_subplots:
        new_plot = go.Scatter(
            name=f"Regresja stopnia 2': R^2={round(deg2_r2,4)}",
            x=temp_df_deg2['x_col'],
            y=temp_df_deg2['y_col'],
            mode='lines',
            marker=dict(color='#FCCA46')
        )
        subplots.append(new_plot)

    if 'deg3' in selected_subplots:
        new_plot = go.Scatter(
            name=f"Regresja stopnia 3': R^2={round(deg3_r2,4)}",
            x=temp_df_deg3['x_col'],
            y=temp_df_deg3['y_col'],
            mode='lines',
            marker=dict(color='#FE7F2D')
        )
        subplots.append(new_plot)

    if 'deg4' in selected_subplots:
        new_plot = go.Scatter(
            name=f"Regresja stopnia 4': R^2={round(deg4_r2,4)}",
            x=temp_df_deg4['x_col'],
            y=temp_df_deg4['y_col'],
            mode='lines',
            marker=dict(color='#233D4D')
        )
        subplots.append(new_plot)

    graph = go.Figure(
        data=subplots,
        layout=go.Layout(
            title='Wykres porównawczy regresji',
            width=900,
            height=700,
            showlegend=True,
            xaxis_title = x_name,
            yaxis_title = y_name,
            legend_title = 'Legenda',
        ))

    return graph