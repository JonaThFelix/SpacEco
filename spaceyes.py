'''
***************************************************************************************************************************
***************************************************************************************************************************

                                   Estudo para projeto Inter 2024.1

                            >> PROJETO SPACEYES, NATIVO EM PYTHON PARA USO EM DESKTOP <<


> Importar as bibliotecas necessárias tkinter, requests, pandas e matplotlib
  > se a biblioteca não instalar no console ou cmd pelo "pip install exemplo", testar com
    "py -m pip install exemplo";

> Verificar a versão do Python;
> Verificar a versão do PIP;
> Verifique as versões das bibliotecas com pip freeze;
> Se possível, use o Pycharm, é mais fácil.

API Disponível em : https://home.openweathermap.org/users/sign_in
API Info : A API é Free;
API_KEY : 3664c6dd18f87e85973dca7dc26baf47

***************************************************************************************************************************
***************************************************************************************************************************
'''


import tkinter as tk
from tkinter import messagebox
import requests
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------- REQUISIÇÃO QUE CHAMA A API ----------------------------------------------------#

def obter_dados_tempo(cidade, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        dados = response.json()
        return dados
    else:
        messagebox.showerror("Erro", "Erro ao obter dados. Verifique a cidade.")
        return None


# --------------------------------- GERAÇÃO DE RELATÓRIOS ----------------------------------------------------#
def gerar_relatorio(dados):
    if dados:
        cidade = dados['name']
        pais = dados['sys']['country']
        temperatura = dados['main']['temp']
        pressao = dados['main']['pressure']
        umidade = dados['main']['humidity']
        descricao = dados['weather'][0]['description']
        vento = dados['wind']['speed']
        nascer_do_sol = dados['sys']['sunrise']
        por_do_sol = dados['sys']['sunset']

        relatorio = f"""
        Dados do Tempo para {cidade}, {pais}:
        Temperatura: {temperatura} K
        Pressão: {pressao} hPa
        Umidade: {umidade}%
        Descrição: {descricao}
        Velocidade do Vento: {vento} m/s
        Nascer do Sol: {nascer_do_sol}
        Pôr do Sol: {por_do_sol}
        """
        resultado.config(state=tk.NORMAL)
        resultado.delete(1.0, tk.END)
        resultado.insert(tk.END, relatorio + "\n")
        resultado.config(state=tk.DISABLED)
    else:
        messagebox.showerror("Erro", "Não foi possível gerar o relatório. Verifique os dados fornecidos.")


# --------------------------------- GERAÇÃO DE GRÁFICOS ----------------------------------------------------#
def gerar_grafico(dados, opcao):
    if dados:
        df = pd.DataFrame(dados)
        if opcao == 1:
            df.plot(kind='bar', x='nome', y='valor', legend=None)
        elif opcao == 2:
            df.plot(kind='line', x='nome', y='valor', marker='o')
        elif opcao == 3:
            df.plot(kind='scatter', x='nome', y='valor')
        elif opcao == 4:
            df.plot(kind='area', x='nome', y='valor', stacked=False)
        elif opcao == 5:
            df.plot(kind='pie', y='valor', labels=df['nome'], autopct='%1.1f%%')
        else:
            messagebox.showerror("Erro", "Opção inválida para o gráfico.")
            return

        plt.title('Condições do Tempo')
        plt.xlabel('Variável')
        plt.ylabel('Valor')
        plt.show()
    else:
        messagebox.showerror("Erro", "Não foi possível gerar o gráfico. Verifique os dados fornecidos.")


def mostrar_opcoes_grafico_popup():
    opcoes = "Opções de Gráfico:\n" \
             "1. Gráfico de Barras\n" \
             "2. Gráfico de Linha\n" \
             "3. Gráfico de Dispersão\n" \
             "4. Gráfico de Área\n" \
             "5. Gráfico de Pizza"
    messagebox.showinfo("Opções de Gráfico", opcoes)


def buscar_dados_tempo():
    cidade = entrada_cidade.get()
    api_key = "3664c6dd18f87e85973dca7dc26baf47"
    dados_tempo = obter_dados_tempo(cidade, api_key)
    gerar_relatorio(dados_tempo)


def gerar_grafico_selecionado(opcao):
    cidade = entrada_cidade.get()
    api_key = "3664c6dd18f87e85973dca7dc26baf47"
    dados_tempo = obter_dados_tempo(cidade, api_key)
    if dados_tempo:
        dados_grafico = {
            'nome': ['Temperatura', 'Pressão', 'Umidade', 'Vento'],
            'valor': [
                dados_tempo['main']['temp'],
                dados_tempo['main']['pressure'],
                dados_tempo['main']['humidity'],
                dados_tempo['wind']['speed']
            ]
        }
        gerar_grafico(dados_grafico, opcao)

# -------------------------------------------- APLICAÇÃO ----------------------------------------------------#
def mostrar_aplicacao_principal(usuario):
    global app_screen
    app_screen = tk.Toplevel(iniciar)
    app_screen.title("SpacEyes | Admin | Versão 0.1 | SpacEco")
    app_screen.geometry("800x500")
    app_screen.configure(bg="#333333")  # Cor de fundo
    app_screen.resizable(False, False)

    # Label de boas-vindas
    label_welcome = tk.Label(app_screen, text=f"SpacEyes", fg="white", bg="#333333", font=("Arial", 14))
    label_welcome.pack(pady=10)

    # Frame para entrada de cidade e botão de busca
    frame_cidade = tk.Frame(app_screen, bg="#333333")
    frame_cidade.pack(pady=10)

    label_cidade = tk.Label(frame_cidade, text="Cidade:", fg="white", bg="#333333")
    label_cidade.grid(row=0, column=0)

    global entrada_cidade
    entrada_cidade = tk.Entry(frame_cidade, width=30)
    entrada_cidade.grid(row=0, column=1)

    botao_buscar = tk.Button(frame_cidade, text="Buscar", command=buscar_dados_tempo, bg="gray", fg="white")
    botao_buscar.grid(row=0, column=2, padx=10)

    # Frame para opções de gráfico
    frame_opcoes = tk.Frame(app_screen, bg="#333333")
    frame_opcoes.pack(pady=10)

    botao_opcoes = tk.Button(frame_opcoes, text="Opções de Gráfico", command=mostrar_opcoes_grafico_popup, bg="gray", fg="white")
    botao_opcoes.grid(row=0, column=0, padx=5)

    botao_barra = tk.Button(frame_opcoes, text="1 - Gráfico de Barras", command=lambda: gerar_grafico_selecionado(1), bg="gray", fg="white")
    botao_barra.grid(row=0, column=1, padx=5)

    botao_linha = tk.Button(frame_opcoes, text="2 - Gráfico de Linha", command=lambda: gerar_grafico_selecionado(2), bg="gray", fg="white")
    botao_linha.grid(row=0, column=2, padx=5)

    botao_dispersao = tk.Button(frame_opcoes, text="3 - Gráfico de Dispersão", command=lambda: gerar_grafico_selecionado(3), bg="gray", fg="white")
    botao_dispersao.grid(row=0, column=3, padx=5)

    botao_area = tk.Button(frame_opcoes, text="4 - Gráfico de Área", command=lambda: gerar_grafico_selecionado(4), bg="gray", fg="white")
    botao_area.grid(row=0, column=4, padx=5)

    botao_pizza = tk.Button(frame_opcoes, text="5 - Gráfico de Pizza", command=lambda: gerar_grafico_selecionado(5), bg="gray", fg="white")
    botao_pizza.grid(row=0, column=5, padx=5)

    # Frame para exibir resultados
    frame_resultado = tk.Frame(app_screen, bg="#333333")
    frame_resultado.pack(pady=10)

    global resultado
    resultado = tk.Text(frame_resultado, width=50, height=10, bg="gray", fg="white")
    resultado.pack()

    app_screen.mainloop()

# ----------------------------------------------------------- LOGIN ----------------------------------------------------#
# A PRINCIPIO ESTÁ ADMIN / ADMIN

def verificar_login():
    usuario = entry_usuario.get()
    senha = entry_senha.get()

    if usuario == "admin" or usuario == "ADMIN" and senha == "admin" or senha == "ADMIN":
        login_sucesso(usuario)
    else:
        messagebox.showerror("SpacEyes Diz", "Usuário ou senha incorretos.")


def login_sucesso(usuario):
    global iniciar
    iniciar.withdraw()
    mostrar_aplicacao_principal(usuario)


# Configuração da janela principal
iniciar = tk.Tk()
iniciar.title("SpacEyes - Login")
iniciar.geometry("800x500")
iniciar.configure(bg="#333333")  # Cor de fundo
iniciar.resizable(False, False)

login_screen = tk.Frame(iniciar, bg="#333333")
login_screen.pack(pady=50)

label_usuario = tk.Label(login_screen, text="Usuário:", fg="white", bg="#333333")
label_usuario.pack()
entry_usuario = tk.Entry(login_screen)
entry_usuario.insert(0, "")  # Usuário padrão
entry_usuario.pack()

label_senha = tk.Label(login_screen, text="Senha:", fg="white", bg="#333333")
label_senha.pack()
entry_senha = tk.Entry(login_screen, show="*")
entry_senha.insert(0, "")  # Senha padrão
entry_senha.pack()

button_login = tk.Button(login_screen, text="Login", command=verificar_login, bg="gray", fg="white")
button_login.pack()

iniciar.mainloop()
