from operator import itemgetter
import pandas as pd

baseDados2022 = 'base_Dados_Vale_Paraiba_2022.csv'
baseDados2018 = 'base_Dados_Vale_Paraiba_2018.csv'

def pesquisaEscolaridade(cidade, genero, estadoCivil, graph, ano):
    print(cidade, genero, estadoCivil, graph, ano)
    df = anoEleicao(ano)

    tituloGraph = ""



    print("--- DIAGNÓSTICO DO DATAFRAME ---")
    print("Tipo da coluna NM_MUNICIPIO:", df['NM_MUNICIPIO'].dtype)
    print("Exemplos brutos na base:", repr(df['NM_MUNICIPIO'].iloc[0:5].values))
    print("Buscando por:", repr(cidade))
    
    # Testa se a cidade existe de forma parcial (ignorando maiúsculas e espaços extras)
    teste_cidade = df[df['NM_MUNICIPIO'].astype(str).str.contains("SÃO JOSÉ DOS CAMPOS", case=False, na=False)]
    print("Linhas encontradas com 'SÃO JOSÉ DOS CAMPOS' (parcial):", len(teste_cidade))
    
    if len(teste_cidade) > 0:
        print("Valores únicos de estado civil para essa cidade:", teste_cidade['DS_ESTADO_CIVIL'].unique())
    print("---------------------------------")


    if genero != "":
        dfCidade = df.loc[df['DS_GENERO'] == genero]
        tituloGraph += f'GÊNERO {genero}'
    else:
        dfCidade = df
        tituloGraph = 'DIVISÃO POR ESCOLARIDADE'

    print("Filtro Genero: ", dfCidade['DS_ESTADO_CIVIL'])

    if estadoCivil != "":
        dfCidade = dfCidade.loc[dfCidade['DS_ESTADO_CIVIL'].str.strip().str.upper() == estadoCivil]
        tituloGraph += f', {estadoCivil}(A)'
    else:
        pass

    print("Filtro Estado Civil: ", dfCidade)
    print("Cidade: ", cidade)

    if cidade != "":
        dfCidade = dfCidade.loc[dfCidade['NM_MUNICIPIO'] == cidade]
        tituloGraph += f' DA CIDADE {cidade}'
    else:
        pass


    dicEscolaridade = dict(dfCidade['DS_GRAU_ESCOLARIDADE'].value_counts())


    listEscolaridade = []
    listQTDEscolaridade = []

    for k, v in dicEscolaridade.items():
        listEscolaridade.append(k)
        listQTDEscolaridade.append(int(v))

    totalPessoas = 0
    for valor in listQTDEscolaridade:
        totalPessoas += valor

    dic = {
        "eixoX": listEscolaridade,
        "eixoY": listQTDEscolaridade,
        "totalPessoas": totalPessoas,
        "tituloGraph": tituloGraph,
        "tipoGrafico": graph,
    }

    return dic

def divisaoGenero():

    df = anoEleicao(2024)

    totalPessoas = len(df)

    # Definindo as informações do eixo X, passando os Gêneros
    labels = ['Masculino', 'Feminino']
    print(df['DS_GENERO'])

    # Definindo as informações do eixo Y, passando a quantidade de cada gênero
    masc = len(df.loc[df['DS_GENERO'] == 'MASCULINO'])
    fem = len(df.loc[df['DS_GENERO'] == 'FEMININO'])
    ni = len(df.loc[df['DS_GENERO'] == 'NÃO INFORMADO'])
    pessoas = []

    # Armazenando os dados na ordem do eixo X (labels), na ordem do eixo Y "Labels" ('Não Informado', 'Masculino', 'Feminino')
    pessoas.append(masc)
    pessoas.append(fem)

    dic = {
        "labelsGenero": labels,
        "qtdGenero": pessoas,
        "qtdGenNaoInfo": ni,
        "totalPessoas": totalPessoas,
    }

    return dic

def divisaoGeneroCidade(cidade, genero, estadoCivil, graph, ano):

    df = anoEleicao(ano)

    tituloGraph = ""

    if genero != "":
        dfCidade = df.loc[df['DS_GENERO'] == genero]
        tituloGraph += f'GÊNERO {genero}'
    else:
        dfCidade = df
        tituloGraph = 'DIVISÃO POR GÊNERO'

    if estadoCivil != "":
        dfCidade = dfCidade.loc[dfCidade['DS_ESTADO_CIVIL'] == estadoCivil]
        tituloGraph += f', {estadoCivil}(A)'
    else:
        pass

    if cidade != "":
        dfCidade = dfCidade.loc[dfCidade['NM_MUNICIPIO'] == cidade]
        tituloGraph += f' DA CIDADE {cidade}'
    else:
        pass

    totalPessoas = len(dfCidade)

    labels = ['Masculino', 'Feminino']

    masc = len(dfCidade.loc[dfCidade['DS_GENERO'] == 'MASCULINO'])
    fem = len(dfCidade.loc[dfCidade['DS_GENERO'] == 'FEMININO'])
    ni = len(dfCidade.loc[dfCidade['DS_GENERO'] == 'NÃO INFORMADO'])
    pessoas = []

    pessoas.append(masc)
    pessoas.append(fem)

    dic = {
        "eixoX": labels,
        "eixoY": pessoas,
        "qtdGenNaoInfo": ni,
        "totalPessoas": totalPessoas,
        "tituloGraph": tituloGraph,
        "tipoGrafico": graph,
    }

    return dic

def anoEleicao(ano):
    try:
        ano = int(ano)
    except (TypeError, ValueError):
        ano = 2022  

    if ano == 2022:
        # Mudamos de 'latin1' para 'utf-8' com tratamento de erros de bytes inválidos
        df = pd.read_csv(baseDados2022, encoding='utf-8', encoding_errors='ignore')
    else:
        df = pd.read_csv(baseDados2018, encoding='utf-8', encoding_errors='ignore')
        
    # Padroniza os nomes das colunas
    df.columns = df.columns.str.strip().str.upper()
    
    # Padroniza também a coluna de municípios para remover espaços ocultos na base inteira
    if 'NM_MUNICIPIO' in df.columns:
        df['NM_MUNICIPIO'] = df['NM_MUNICIPIO'].astype(str).str.strip().str.upper()
    
    if 'DS_ESTADO_CIVIL' in df.columns:
        df['DS_ESTADO_CIVIL'] = df['DS_ESTADO_CIVIL'].astype(str).str.strip().str.upper()
        
    if 'DS_GENERO' in df.columns:
        df['DS_GENERO'] = df['DS_GENERO'].astype(str).str.strip().str.upper()

    return df