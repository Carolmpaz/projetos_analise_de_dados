import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Importa a base de dados, configura a coluna data como datetime e a configura como indice da base de dados
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date']).set_index('date')

# Define função que realiza a limpeza dos dados
def clean_database(df):

    # Garante que os valores da variável 'value' é numérico
    df['value'] = pd.to_numeric(df['value'], errors='coerce')

    # Verifica se o valor da variável 'date' está dentro do percentil de 97,5 e 2,5
    verify_date = (df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))

    # Retorna apenas as linhas da base de dados que cumprem essas verificações
    return df[verify_date]

# Define a variável 'df' como uma base de dados, apenas com os valores retornados na função clean_database 
df = clean_database(df)



def draw_line_plot():
    
    # Cria a imagem e eixos do gráfico, definindo a variável fig como sendo a imagem e ax como sendo os elemnetos do gráfico
    fig, ax = plt.subplots(figsize=(12,6)) 

    # Define os eixos do gráfico, trçando as linhas do gráfico
    ax.plot(df.index, df['value'])

    # Define o título do gráfico 
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    
    # Define o nome do eixo X
    ax.set_xlabel("Date")

    # Define o nome do eixo y
    ax.set_ylabel("Page Views")


    # Salva a imagem e retorna a variável 'fig' 
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():

    #Cria uma cópia da base de dados 'df'
    df_bar = df.copy()

    # Cria uma nova coluna na base de dados apenas com o ano correspondestes ao index da linha 
    df_bar['year'] = df.index.year

    # Cria uma nova coluna na base de dados apenas com o mês correspondestes ao index da linha 
    df_bar['month'] = df.index.month

    # Lista com os nomes dos meses
    month_names = ['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']


    # Agrupa todas as linhas que possuem os memso valores de mês e ano e faz uma média dos valores da coluna 'value'
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Substitui os números das colunas pelos nomes dos meses
    df_bar.columns = month_names

    # Gera a imagem e os elemnetos do gráfico, guradando-os nas variáveis 'fig' e 'ax', respectiamente
    fig, ax = plt.subplots(figsize=(12, 8))

    # Desenha o gráfico 
    df_bar.plot(kind='bar', ax=ax)

    # Configura o nome do eixo X do gráfico
    ax.set_xlabel("Years")

    # Configura o nome do eixo y do gráfico
    ax.set_ylabel("Average Page Views")

    # Configura o título do gráfico
    ax.legend(title="Months")


    # Salva a imagem e retorna a variável 'fig' 
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepara a base de dados, reseta o indice e cria as colunas de ano e mês
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
   
    # Gera a imagem e os elemnetos do gráfico, guradando-os nas variáveis 'fig' e 'ax', respectiamente
    fig, ax = plt.subplots(1, 2, figsize=(15, 6))

    # Gera o gráfico de relação entre as colunas 'year' e 'value'
    sns.boxplot(x="year", y="value", data=df_box, ax=ax[0])
    ax[0].set_title("Year-wise Box Plot (Trend)") # Define o título do gráfico
    ax[0].set_xlabel("Year") # Define o nome do eixo X
    ax[0].set_ylabel("Page Views") # Define o nome do eixo y
    
    # Define a ordem dos meses para projeção do gráfico
    month_order = ['Jan','Feb','Mar','Apr','May','Jun',
                   'Jul','Aug','Sep','Oct','Nov','Dec']

    # Gera o gráfico de relação entre as colunas 'month' e 'value'
    sns.boxplot(x="month", y="value", data=df_box, order=month_order, ax=ax[1])
    ax[1].set_title("Month-wise Box Plot (Seasonality)") # Define o título do gráfico
    ax[1].set_xlabel("Month") # Define o nome do eixo X
    ax[1].set_ylabel("Page Views") # Define o nome do eixo y 

    # Salva a imagem e retorna a variável 'fig' 
    fig.savefig('box_plot.png')
    return fig
