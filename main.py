import pandas as pd
import folium
import branca

# Carregue seus dados em um DataFrame do Pandas
# Suponha que seus dados estejam em um arquivo CSV com colunas para 'Data', 'Prisma', 'Norte', 'Leste' e 'Elevacao'
df = pd.read_csv('new_monitoramento.csv')
# Converta a coluna 'Data' para o tipo de data
df['Data'] = pd.to_datetime(df['Data'])
df = df.sort_values('Data')

# Calcule a diferença de elevação diária para cada prisma
df['Diferenca_Elevacao'] = df.groupby('Prisma')['Elevacao'].diff()
df['Diferenca_Norte'] = df.groupby('Prisma')['Norte'].diff()
df['Diferenca_Leste'] = df.groupby('Prisma')['Leste'].diff()


# Crie um mapa centrado na média de suas coordenadas
m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=17, tiles = None)
folium.TileLayer(tiles = "cartodbpositron").add_to(m)
folium.TileLayer(tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                 attr = 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
                name = "Imagem Satélite").add_to(m)

folium.LayerControl().add_to(m)

# , icon=folium.DivIcon(html=f"""<h5 style="font-family: courier new; color: blue; font-weight: bold;">{prisma}</h5>""")
# Adicione um marcador para cada prisma
for prisma in df['Prisma'].unique():
    df_prisma = df[df['Prisma'] == prisma]
    # Use a última localização disponível para o marcador
    location = df_prisma.iloc[-1][['Latitude', 'Longitude']]
    # Crie uma string HTML com as diferenças de elevação para cada dia
    html = '<h1>' "Prisma: "+ prisma + '</h1>'
    for i, row in df_prisma.iterrows():
        html += f"""
        <h4> Data:  { str(row['Data'].date())} </h4>
        <ul>
            <li>Diferença de Elevação: {str(round(row['Diferenca_Elevacao'], 5))}</li>
            <li>Diferença em Norte:  {str(round(row['Diferenca_Norte'], 5))}</li>
            <li>Diferença em Leste:  {str(round(row['Diferenca_Leste'], 5))}</li>
        </ul>
        """
    iframe = folium.IFrame(html=html, width=400, height=400)
    popup = folium.Popup(iframe, max_width=2650)
    # Adicione o marcador ao mapa
    folium.Marker(location, popup=popup).add_to(m)


print(df)
# Salve o mapa em um arquivo HTML
m.save('mapa.html')
