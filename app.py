import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd


import pandas as pd
from pyproj import Proj, transform


# def utm_to_latlon(easting, northing, zone_number, zone_letter):
#     utm_proj = Proj(proj='utm', zone=zone_number, ellps='WGS84', south=(zone_letter < 'S'))
#     latlon_proj = Proj(proj='latlong', datum='WGS84')
#     longitude, latitude = transform(utm_proj, latlon_proj, easting, northing)
#     return latitude, longitude

# # Leia o arquivo CSV em um DataFrame
# df = pd.read_csv('monitoramento.csv')

# # Suponha que as colunas do DataFrame sejam 'Leste', 'Norte', 'Elevacao', 'Data' e 'Prisma'
# # E que você tenha um número de zona UTM e uma letra de zona UTM fixos para todos os pontos
# zone_number = 23  # Substitua pelo seu número de zona UTM
# zone_letter = 'K'  # Substitua pela sua letra de zona UTM

# df['Latitude'], df['Longitude'] = zip(*df.apply(lambda row: utm_to_latlon(row['Leste'], row['Norte'], zone_number, zone_letter), axis=1))

# # Escreva o DataFrame modificado em um novo arquivo CSV
# df.to_csv('new_monitoramento.csv', index=False)


# Suponha que 'df' é seu DataFrame e inclui colunas para 'Norte', 'Leste', 'Elevacao', 'Data' e 'Prisma'
df = pd.read_csv('new_monitoramento.csv')

app = dash.Dash(__name__)


px.set_mapbox_access_token(open("./mapbox_token").read())

fig = px.scatter_mapbox(df, lat='Latitude', lon='Longitude', color='Elevacao', size_max=15, zoom=10)

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
