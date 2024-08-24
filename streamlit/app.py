# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import os

# URL do arquivo CSV
url = "https://raw.githubusercontent.com/Harofry/Analises-de-redes-segunda-unidade/main/duolingo_language_report_by_country.csv"

# Carregar o CSV como um DataFrame do pandas
duo_language = pd.read_csv(url)
duo_language = duo_language.dropna()

# Exibir as primeiras linhas do DataFrame
st.write("Dados Carregados")
st.write(duo_language.head())

# Verifique os nomes das colunas para evitar KeyErrors
st.write("Colunas disponíveis:")
st.write(duo_language.columns)

# Ajuste o nome das colunas conforme necessário
source_column = 'pop1_2022'
target_column = 'pop2_2022'
edge_attribute = 'country'

# Criar o grafo
try:
    G = nx.from_pandas_edgelist(duo_language, source_column, target_column, edge_attr=edge_attribute)
except KeyError as e:
    st.error(f"Erro ao criar o grafo: {e}")
    st.stop()

# Configurar o grafo PyVis
nt = Network('800px', '800px', cdn_resources='in_line')

# Adicionar nós e arestas ao grafo
for node, data in G.nodes(data=True):
    nt.add_node(node, label=node, size=data.get('pop1_2022', 10)*0.01, title=f"País: {data.get('country', 'N/A')}")

for source, target, data in G.edges(data=True):
    nt.add_edge(source, target, title=data.get('country', 'No Data'))

# Salvar o grafo interativo como um arquivo HTML
html_file = 'duo_language_Network_Graph.html'
try:
    with open(html_file, 'w', encoding='utf-8') as file:
        file.write(nt.generate_html())
except Exception as e:
    st.error(f"Erro ao salvar o arquivo HTML: {e}")

# Função para exibir o HTML do grafo
def show_graph(file_name, height=1000, width=1000):
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as file:
            source_code = file.read()
        st.components.v1.html(source_code, height=height, width=width)
    else:
        st.error(f"Arquivo {file_name} não encontrado.")

# Exibir o grafo
st.title('Duo Language Network Graph')
show_graph(html_file)
