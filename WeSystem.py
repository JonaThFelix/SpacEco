import requests
import pandas as pd
import streamlit as st
import plotly.express as px

# Função para fazer requisição à API de clima
def obter_dados_tempo(cidade, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Erro ao obter dados. Verifique o nome da cidade.")
        return None

# Função principal da aplicação
def main():
    st.title("Visualização de Dados Meteorológicos")

    # Input da cidade
    cidade = st.text_input("Digite o nome da cidade:")

    if st.button("Buscar"):
        api_key = "3664c6dd18f87e85973dca7dc26baf47"
        dados_tempo = obter_dados_tempo(cidade, api_key)

        if dados_tempo:
            temperatura = dados_tempo['main']['temp']
            pressao = dados_tempo['main']['pressure']
            umidade = dados_tempo['main']['humidity']

            # Exibir dados meteorológicos
            st.subheader("Dados Meteorológicos:")
            st.write(f"Temperatura: {temperatura} K")
            st.write(f"Pressão: {pressao} hPa")
            st.write(f"Umidade: {umidade}%")

            # Preparar dados para os gráficos
            df = pd.DataFrame({
                'Variável': ['Temperatura (K)', 'Pressão (hPa)', 'Umidade (%)'],
                'Valor': [temperatura, pressao, umidade]
            })

            # Gráfico de barras
            st.subheader("Gráfico de Barras:")
            st.bar_chart(df.set_index('Variável'))

            # Gráfico de linha com conversão de temperatura para Celsius
            temperatura_celsius = temperatura - 273.15
            df_tempo_celsius = pd.DataFrame({
                'Tempo': ['Temperatura (°C)', 'Pressão (hPa)', 'Umidade (%)'],
                'Valor': [temperatura_celsius, pressao, umidade]
            })

            st.subheader("Gráfico de Linha (°C):")
            st.line_chart(df_tempo_celsius.set_index('Tempo'))

            # Gráfico de pizza
            st.subheader("Gráfico de Pizza:")
            fig = px.pie(df, values='Valor', names='Variável', title='Distribuição das Variáveis Meteorológicas')
            st.plotly_chart(fig)

if __name__ == "__main__":
    main()
