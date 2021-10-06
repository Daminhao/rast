# Estre programa é um CRUD para geração de qrcode com informações imporntantes sobre a origem dos peixes.
import streamlit as st # modulo para frond-end
import numpy as np # modulo para operações matematicoas (nem ta sendo usado)
import pandas as pd # modlulo para manipulação de listas e dicionarios
import pyqrcode #modulo para geração do QR-code
import cairosvg #modulo para transformar svg em png

from tinydb import TinyDB, Query # iblioteca para utilizar o tinyDB
from st_aggrid import AgGrid #Modulo para criação de tabelas dinamicas  editaveis
db = TinyDB('DADOS.json')  # criando banco de dados(chama o banco caso já foi criado)
User = Query()#??????

st.title("Rastreador de peixes") # Titulo do webapp

#Devemos lembrar que este é um CRUD para armazenar informações sobre
#lotes de peixes, começaremos pelo 'C' do C.R.U.D que represneta CREAT(criar)

#'''Creat (criar)'''
col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12, col13 = st.columns(13) #criamos colunas para que os inputes do usuario fiquem um ao lado do outro

with col1:
    lote = st.number_input(label = " Lote ", value=0)
with col2:
    cnpj = st.text_input(label = " CNPJ ")
with col3:
    local = st.text_input(label = " Local ")
with col4:
    cooperativa = st.text_input(label = " Cooperativa ")
with col5:
    especie = st.text_input(label = " Espécie ")
with col6:
    tempo_cultivo = st.text_input(label = " Tempo de Cultivo ")
with col7:
    despesca = st.text_input(label = " Despesca ")
with col8:
    metodo_reproducao = st.text_input(label = "Metodo de Reprodução")
with col9:
    dna = st.text_input(label = " DNA ")
with col10:
    tipo_cultivo = st.text_input(label = " Tipo de cultivo ")
with col11:
    tipo_racao = st.text_input(label= " Ração utilizada ")
with col12:
    quantidade_individuos = st.text_input(label = "Estocagem")
with col13:
    TEST13 = st.text_input(label = "insira o nome do TEST13")


botão_salvar = st.button("Salvar") #Bottão para salvar os dados digitados nos inputs

if botão_salvar: #V# Quando o botão salvar for precionado fassa:
    st.write(f'lote: {lote}')
    # escreve no front qual especie que foi armazenado
    db.insert({ #V# # pega os valoes e armazena no banco de dados(tinyDB)
            'lote': lote,
            'cnpj': cnpj,
            'local': local,
            'cooperativa': cooperativa,
            'especie': especie,
            'tempo_cultivo': tempo_cultivo,
            'despesca': despesca,
            'metodo_reproducao': metodo_reproducao,
            'dna': dna,
            'tipo_cultivo': tipo_cultivo,
            'tipo_racao': tipo_racao,
            'quantidade_individuos': quantidade_individuos,
            'TEST13': TEST13
            })

#'''Read(Ler)'''
#valor = db.search(User.lote == 1)# PODE SAIR?
#print('Valor:', valor)# PODE SAIR?

#V# pega as informações contidas no banco de dados e armazena na variavel df
df = pd.DataFrame(data={
                    'Lote':                [a['lote'] for a in db],
                    'CNPJ':                [b['cnpj'] for b in db],
                    'Local':               [c['local'] for c in db],
                    'Cooperativa':         [d['cooperativa'] for d in db],
                    'Especie':             [e['especie'] for e in db],
                    'Tempo de cultivo':    [f['tempo_cultivo'] for f in db],
                    'Despesca':            [g['despesca'] for g in db],
                    'Metodo de Reproducao':[h['metodo_reproducao'] for h in db],
                    'DNA':                 [i['dna'] for i in db],
                    'Tipo de cultivo':     [j['tipo_cultivo'] for j in db],
                    'Tipo de racao':       [k['tipo_racao'] for k in db],
                    'Estocagem':           [l['quantidade_individuos'] for l in db],
                    'TEST13':              [l['TEST13'] for l in db]
                    })
#print ('df',df)
#st.header('Rastreio do pescado') #
#tabela aggrid com as informações do bnaco de dados(read)

#O Aggrid nos permite editar os campos da tabela
#ou sejá ja resolveo nosso "D"(Delete) do C.R.U.D

response = AgGrid(df, editable=True, fit_columns_on_grid_load=True)

col1, col2, = st.columns(2) #criamos novamente colunas para divisão do front end

# função para add um nova linha na tabela e um novo dicionario vazio no db.
add_linha = col1.button("adicionar uma linha") #na coluna 1 ficara o botão para dicioanr um linha vazia
if add_linha: # Caso o botão for precionado, faça: #V#
    lote  = ('')
    cnpj  = ('')
    local  = ('')
    cooperativa  = ('')
    especie  = ('')
    tempo_cultivo  = ('')
    despesca  = ('')
    metodo_reproducao  = ('')
    dna  = ('')
    tipo_cultivo = ('')
    tipo_racao = ('')
    quantidade_individuos = ('')
    TEST13 = ('')


    db.insert({#V# Inclui o dicionario vazio no banco de dados
            'lote': lote,
            'cnpj': cnpj,
            'local': local,
            'cooperativa': cooperativa,
            'especie': especie,
            'tempo_cultivo': tempo_cultivo,
            'despesca': despesca,
            'metodo_reproducao': metodo_reproducao,
            'dna': dna,
            'tipo_cultivo': tipo_cultivo,
            'tipo_racao': tipo_racao,
            'quantidade_individuos': quantidade_individuos,
            'TEST13': TEST13
                }) 

#'''Update (Alterar)'''
df =(response['data']) # chamada das informações contindas na tabela aggrid e armazenamento em uma lista

atualizar_dados_no_bd = col2.button("Salvar no banco de dados")
if atualizar_dados_no_bd: # se o  botão salvar no banco de dados for precionado faça:
    products_list = df.values.tolist() #trasforma a tabela "aggrid" em lista

    #Antes de salvar, é precisa apagar os itens vazios(['']) dos dicionarios
    #do banco de daos isso é feito para evitar que exitam dicionarios com informações
    #vazios atrapalhando a identificação dos lotes por id e o plot na tabela.

    products_list = [s for s in products_list
                    if  s  != ['', '']
                    and s != ['']
                    ]

    print('RESULTADO:',products_list)
    # truncate remove (remove as listas(dicionarios) vazios ['', ''] e ['']
    db.truncate()

    for a in products_list: #adiciona ao banco de dados as informações tratadas
        lote = a[0]
        cnpj = a[1]
        local = a[2]
        cooperativa = a[3]
        especie = a[4]
        tempo_cultivo = a[5]
        despesca = a[6]
        metodo_reproducao = a[7]
        dna = a[8]
        tipo_cultivo = a[9]
        tipo_racao = a[10]
        quantidade_individuos = a[11]
        TEST13 = a[12]

        db.insert({

        'lote' : lote,
        'cnpj' : cnpj,
        'local' : local,
        'cooperativa' : cooperativa,
        'especie' : especie,
        'tempo_cultivo' : tempo_cultivo,
        'despesca' : despesca,
        'metodo_reproducao' : metodo_reproducao,
        'dna' : dna,
        'tipo_cultivo': tipo_cultivo,
        'tipo_racao': tipo_racao,
        'quantidade_individuos': quantidade_individuos,
        'TEST13': TEST13
        })


#Gerador de QRcode
col3,col4 = st.columns(2)# Duas colunas para dividir os inputse plots
with col3:#
    st.header('Gerador de Qrcode')

    info_id = st.number_input('Escolha o numero do lote:', value=1)

    qr_button = st.button("Gerar QRcode")

    if qr_button:
        st.write(f'lote: {info_id}')#V#
        input_id =(info_id)
        print('AAAAAAAAAAA',input_id)
        item = db.get(doc_id=input_id)

        #Select data of db.get
        select_info =   ("lote: {} \n cnpj: {} \n local: {} \n cooperativa: {} \n especie: {} \n tempo_cultivo: {} \n despesca: {} \n metodo_reproducao: {} \n dna: {} \n tipo_cultivo: {} \n tipo_racao: {} \n quantidade_individuos: {} \n TEST13: {} \n ".format
                    (#V#
                    item["lote"],
                    item["cnpj"],
                    item["local"],
                    item["cooperativa"],
                    item["especie"],
                    item["tempo_cultivo"],
                    item["despesca"],
                    item["metodo_reproducao"],
                    item["dna"],
                    item["tipo_cultivo"],
                    item["tipo_racao"],
                    item["quantidade_individuos"],
                    item["TEST13"]
                    ))

        # Using pyqrcode.create() to create a qr code of the input data
        qr = pyqrcode.create(select_info)

        # Using .svg method to save the qr code as SVG file of provided name & scale
        qr.svg('qr_code.svg', scale = 8)

        svg_url = "qr_code.svg"
        my_png = cairosvg.svg2png(url=svg_url, output_width=426, output_height=240)
        with col4:
            st.image(my_png)

            #Plotar informações do QR code
            #Plotar informações do QR code