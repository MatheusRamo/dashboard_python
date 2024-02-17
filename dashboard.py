import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Suponha que 'df' é seu DataFrame e inclui colunas para 'Norte', 'Leste', 'Elevacao', 'Data' e 'Prisma'
df = pd.read_csv('seu_arquivo.csv')

app = dash.Dash(__name__)

fig = px.scatter_mapbox(df, lat='Norte', lon='Leste', color='Elevacao', size_max=15, zoom=10)

app.layout = html.Div([
    dcc.Graph(id='map', figure=fig),
    html.Div(id='prisma-selecionado', style={'margin-top': '20px'})
])

@app.callback(
    Output('prisma-selecionado', 'children'),
    [Input('map', 'clickData')])
def display_click_data(clickData):
    if clickData is None:
        return 'Clique em um prisma para ver as informações de elevação.'
    else:
        prisma = clickData['points'][0]['customdata']
        elevacao = df[df['Prisma'] == prisma]['Elevacao'].values[0]
        return f'Você selecionou o prisma {prisma}. A elevação é {elevacao}.'

if __name__ == '__main__':
    app.run_server(debug=True)
