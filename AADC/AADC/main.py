import pandas as pd 
import matplotlib.pyplot as plt
from IPython.display import display
from cep_df import cep_df

dados = pd.read_csv('D:\heloh\Documents\Faculdade\Covid_DF.csv', sep = ';')

# Colunas Selecionadas
colunas_selecionadas =  ['paciente_idade', 'paciente_enumsexobiologico', 'paciente_racacor_valor', 'paciente_endereco_nmmunicipio', 'paciente_endereco_nmpais', 'paciente_endereco_uf', 'estalecimento_nofantasia', 'vacina_grupoatendimento_nome', 'vacina_categoria_nome', 'vacina_descricao_dose', 'vacina_nome', 'paciente_endereco_cep']

# Novo Dataframe com as colunas selecionadas
dados_vacina = dados.filter(items = colunas_selecionadas)

# Idades inconsistentes foram substituidas pela média aritmética da coluna 'paciente_idade'
dados_vacina.loc[dados_vacina['paciente_idade'].isnull()] = dados_vacina['paciente_idade'].mean()

# Dados nulos das outras colunas foram substituidos por 'Não informado'
dados_vacina.fillna("Não informado", inplace = True)

# Soma de valores nulos em cada coluna
#print(dados_vacina.isnull().sum())

# Drop paciente_racacor_valor = 50.59404737212269]
#print((dados_vacina['paciente_racacor_valor']).value_counts())
#print(dados_vacina.loc[dados_vacina['paciente_racacor_valor'] == 50.59404737212269] )
dados_vacina.drop(dados_vacina.loc[dados_vacina['paciente_racacor_valor'] == 50.59404737212269].index, inplace=True)

#Alteração na UF do paciente
dados_vacina.loc[dados_vacina['paciente_endereco_uf'] == 'XX'] = 'Não informado'
#print(dados_vacina)

# Exportando dados
#dados_vacina['paciente_idade'].to_csv('paciente_idade.csv')

####################### Quantidade de pessoas que tomaram a 1°, 2° e 3° dose #######################

def graf_quant_dose123():

    # Filtrando dados do DataFrame
    colunas = ['vacina_descricao_dose']
    doses = dados_vacina.filter(items=colunas)
 
    graf = doses.value_counts()

    labels = ['1° Dose', '2° Dose', 'Dose única']
    plt.style.use("ggplot")
    explode = (0.1, 0.0, 0.0)
    
    graf.plot.pie(autopct='%1.1f%%', explode = explode, shadow=True, startangle = 90, ylabel='', title = 'Porcentagem de pessoas que tomaram a 1° dose, 2° dose e a dose única.\n', subplots=True, labels = ['', '', '']) 

    L = plt.legend( bbox_to_anchor=(1, 0, 0.5, 1), loc='center left', labels = labels)
    plt.show() 

#######################Classificação por região geográfica.(estados do Brasil)#######################

def graf_regiao_geografica_estados():

    # Filtrando dados do DataFrame
    colunas = ['paciente_endereco_uf']
    dados_regiao_geografica = dados_vacina.filter(items=colunas)

    # Gráfico UF do paciente 
    graf = (dados_regiao_geografica['paciente_endereco_uf'].value_counts())

    graf.plot.bar(title = 'Localização geográfica das pessoas que se vacinaram no DF\n', xlabel= 'Estados', ylabel = 'Quantidade de pessoas')
    plt.show() 

####################### Classificação por região geográfica. (paises) #######################

def graf_regiao_geografica_paises():

    label = 'Ruanda', 'Venezuela', 'Bolívia' ,  'Congo', 'Japão', 'Andorra','Colômbia', 'Gibraltar', 'Portugal', 'São Tomé e Príncipe'

    # Filtrando dados do DataFrame
    colunas = ['paciente_endereco_nmpais']
    regiao_geografica_paises = dados_vacina.filter(items=colunas)

    # Gráfico país do paciente 
    graf_paises = (regiao_geografica_paises['paciente_endereco_nmpais'].value_counts())

    # Países estrangeiros 
    graf_paises_estrangeiros = regiao_geografica_paises[(regiao_geografica_paises['paciente_endereco_nmpais'] != 'BRASIL') & (regiao_geografica_paises['paciente_endereco_nmpais'] != 'Não informado')].value_counts()

    # Criação do gráfico
    fig, axs = plt.subplots(1,2)
    axs[0].set_title('Países')
    axs[0].pie(graf_paises, shadow=True, startangle=90)
    axs[1].set_title('Países estrangeiros')
    axs[1].pie(graf_paises_estrangeiros, labels=label, shadow=True, startangle=90)
    plt.show() 

# Faixa etária das pessoas que tomaram a vacina.
# Arrumar label
def faixa_etaria():

  # Filtrando dados do DataFrame
    colunas = ['paciente_idade']
    idade = dados_vacina.filter(items=colunas)
    
    #print(graf)
    
    # Criação do gráfico
    import re

    fig, ax = plt.subplots() 
    graf = idade.value_counts()

    graf.plot.bar(ax=ax)
   
    ax.set_title('Blá blá blá')

    handles, labels = ax.get_legend_handles_labels()
    new_labels = [re.search('\((.+?)', label) for label in labels]

    #tt = ax.get_xlabel()
    tt = ax.xaxis.get_label()
    print(tt)
    new_labels_2 = [re.search('\((.+?)', label) for label in tt]
    ax.set_xlabel(new_labels_2)

    plt.show()
    





###########################################################################################

# Testes
def graf_regiao_geografica_df ():
    # Filtrando dados do DataFrame
    colunas = ['paciente_endereco_cep', 'paciente_endereco_nmmunicipio', 'paciente_endereco_uf']
    dados_regiao_geografica_df = dados_vacina.filter(items=colunas)

    dados_regiao_geografica_df = dados_regiao_geografica_df[dados_regiao_geografica_df.paciente_endereco_uf == 'DF']

    #chamando a função cep_df para obter a RA
    dados_regiao_geografica_df['RA'] = [cep_df(cep) for cep in dados_regiao_geografica_df.paciente_endereco_cep]

    print(dados_regiao_geografica_df)

# Conexão com o banco de dados 
def exportar_dados():
    from pymongo import MongoClient

    mongodb = MongoClient("mongodb+srv://Heloise:AmorDaMinhaVida@cluster0.kvg8p.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
 
    # Banco de dados
    db = mongodb.Cluster0
    print(db.list_collection_names())

    #collection
    collection = db['dados_aadc']

    dados_vacina.reset_index(inplace=True)
    data_dict = dados_vacina.to_dict("records")
    collection.insert_one({"index":"Sensex","data":data_dict})



# Chamando as funções 
#graf_quant_dose123()
#graf_regiao_geografica_estados()
#graf_regiao_geografica_df()
#graf_regiao_geografica_paises()
#exportar_dados()
faixa_etaria()
