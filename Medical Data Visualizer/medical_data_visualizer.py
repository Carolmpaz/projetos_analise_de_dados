import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


# Importa a base de dados, salvando os seus valores na variável df
df = pd.read_csv('medical_examination.csv')

# Define função que calcula overweight, definindo-o como 1 ou 0 
def calculate_overweight(df):
    imc = df['weight']/((df['height']/100)**2)
    if imc > 25:
        return 1
    else:
        return 0; 


# Cria uma nova coluna (overweight) na base de dados 
df['overweight'] = df.apply(calculate_overweight, axis=1)

# Define função que normaliza os dados de uma determinada coluna, definindo-os como 1 ou 0 
def normalize_database(column):
    if column == 1:
        return 0
    else:
        return 1
 
# Aplica a função de normalização na coluna 'gluc'
df['gluc'] = df['gluc'].apply(normalize_database)

# Aplica a função de normalização na coluna 'cholesterol'
df['cholesterol'] = df['cholesterol'].apply(normalize_database)

# Define função que cria gráfico para as variáveis categóricas de acordo com o valor da variável 'cardio'
def draw_cat_plot():

    # Define a variável 'df_cat' como sendo uma varição da base de dados, com apenas três colunas, valor da variável 'cardio', nome da variável análisada e valor dessa variável 
    df_cat = pd.melt(
        df, 
        id_vars=['cardio'], # Variável 'cardio' definida como refereêncial
        value_vars=['cholesterol','gluc','smoke','alco','active','overweight'], # Variáveis a serem análisadas
        var_name= 'variables', # Nome da coluna que guarda o nome nas variáveis Valores dessas variáveis
        value_name='values') # Nome da coluna que guarda os valores dessas variáveis



    # Agrupa as linhas semelhantes da base de dados e faz uma contagem delas, criando uma nova coluna com esse número encontrado 
    df_cat = df_cat.groupby(['variables','values','cardio']).size().reset_index(name='count')

    # Cria um gráfico com as informações organizadas na base de dados 'df_cat'
    fig = sns.catplot(
    data=df_cat, # Define a base de dados a ser utilizada
    x="variables", # Define a coluna de nome das variáveis como eixo x
    y="count", # Define a coluna de número de linhas com os mesmos valores como eixo y
    hue="values", # Define a coluna que será diferenciada (utilizado posteriormente para diferenciação por cor)
    col="cardio", # Define variável que será utilizada como referncial na divosão dos blocos, ou seja, cria-se um bloco de gráficos para cada valor da variável 'cardio'
    kind="bar", # Define o gráfico como sendo um gráfico de barras
    height=6, # Define a altura do gráfigo
    aspect=1.2, # Define a razão entre a largura e altura do gráfico
    palette= {0: 'blue', 1: 'orange'} # Definr as cores que diferenciação os valores da variável definida no comando 'hue'
    )
    
    fig.set_axis_labels("variable", "total") # Define o nome dos eixos x e y 
    fig.set_titles("Cardio = {col_name}") # Define o título do gráfico de acordo com o valor da variável 'cardio'

    # Extrai apenas a figura do FacetGrid
    fig = fig.fig

    # Salva o gráfico gerado com o nome 'catplot.png'
    fig.savefig('catplot.png')
    return fig


# Define função que cria matriz de correlção entre as variáveis da base de dados 
def draw_heat_map():
    # Define função que realiza a limpeza dos dados
    def clean_database(df):
        # Verifica se o valor da variável 'ap_lo' é menor ou igual ao valor da variável 'ap_hi'
        verify_ap = df['ap_lo'] <= df['ap_hi']

        # Verifica se o valor da variável 'height' está dentro do percentil de 97,5 e 2,5
        verify_height = (df['height'] >= df['height'].quantile(0.025)) & (df['height'] <= df['height'].quantile(0.975))
        
        # Verifica se o valor da variável 'weight' está dentro do percentil de 97,5 e 2,5
        verify_weight = (df['weight'] >= df['weight'].quantile(0.025)) & (df['weight'] <= df['weight'].quantile(0.975))

        # Unifica o valor dessas três variáveis de verificação
        verify_final = verify_ap & verify_height & verify_weight

        # Retorna apenas as linhas da base de dados que cumprem essas verificações
        return df[verify_final]

    # Define a variável 'df_heat' como uma base de dados, apenas com os valores retornados na função clean_database 
    df_heat = clean_database(df)
   
    # Calcule a matriz de correlação e armazene-a na variável 'corr'
    corr = df_heat.corr()

    # Cria máscara para o triãnngulo superior da matriz de correlação
    mask = np.triu(corr)
   
    # Define a variável 'fig' como sendo a imagem da matriz de correlação, defininfo o seu tamanho
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(
        corr, # Cálculo da matriz de correlação
        mask=mask, # Mascára para triângulo superior
        fmt=".1f", # Número de casas decimais utilizadas
        annot=True, # Define que o texto será escrito dentro das células da matriz
        cmap="coolwarm", # Coloração da matriz de correlação 
        vmin=-0.10, # Valor mínimo da faixa de cores
        vmax=0.25) # Valor máximo da faixa de cores
    # Gera imagem da matriz de correlação
    plt.show()

    # Salva imagem da matriz de correlação como 'heatmap.png'
    fig.savefig('heatmap.png')
    return fig
