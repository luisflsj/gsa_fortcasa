import streamlit as st
import pandas as pd
import plotly.express as px
from database import df_fortcasa
from funcoes import format_number

st.set_page_config(page_title="Análise Estatística Jurídica - FortCasa", layout="wide")

st.markdown("<h1 style='text-align: center;'>Análise Estatística Jurídica - FortCasa</h1>", unsafe_allow_html=True)
st.markdown("---")

st.sidebar.image('logo_gsa.png', width=300)

with st.sidebar:
    razao_social = df_fortcasa['Nome/Razão Social'].unique().tolist()
    filtro_razao_social = st.multiselect('Razão Social', razao_social)

    empreendimento = df_fortcasa['Empreendimento'].unique().tolist()
    filtro_empreendimento = st.multiselect('Empreendimento', empreendimento)

    polo = df_fortcasa['Autor/Réu'].unique().tolist()
    filtro_polo = st.multiselect('Polo', polo)

    comarca = df_fortcasa['Comarca'].unique().tolist()
    filtro_comarca = st.multiselect('Comarca', comarca)

    fase = df_fortcasa['Fase'].unique().tolist()
    filtro_fase = st.multiselect('Fase', fase)

    df_fortcasa_filtrado = df_fortcasa

    if filtro_razao_social:
        df_fortcasa_filtrado = df_fortcasa_filtrado[df_fortcasa_filtrado['Nome/Razão Social'].isin(filtro_razao_social)]

    if filtro_empreendimento:
        df_fortcasa_filtrado = df_fortcasa_filtrado[df_fortcasa_filtrado['Empreendimento'].isin(filtro_empreendimento)]

    if filtro_polo:
        df_fortcasa_filtrado = df_fortcasa_filtrado[df_fortcasa_filtrado['Autor/Réu'].isin(filtro_polo)]

    if filtro_comarca:
        df_fortcasa_filtrado = df_fortcasa_filtrado[df_fortcasa_filtrado['Comarca'].isin(filtro_comarca)]

    if filtro_fase:
        df_fortcasa_filtrado = df_fortcasa_filtrado[df_fortcasa_filtrado['Fase'].isin(filtro_fase)]

######################
##     MÉTRICAS     ##
######################

aba1, aba2 = st.tabs(['Quadro Geral', 'Análises e Gráficos'])

with aba1:
    qtd_processos = df_fortcasa_filtrado['Número do Processo'].count()
    df_fortcasa_filtrado['Valor Causa'] = df_fortcasa_filtrado['Valor Causa'].astype(str).str.replace(',', '.', regex=False).astype(float)
    valor_causa = df_fortcasa_filtrado['Valor Causa'].sum()
    contagem_demandado = df_fortcasa_filtrado['Autor/Réu'].value_counts().get('DEMANDADO', 0)
    contagem_demandante = df_fortcasa_filtrado['Autor/Réu'].value_counts().get('DEMANDANTE', 0)
    qtd_loteamento = len(df_fortcasa_filtrado['Empreendimento'].unique())
    qtd_empresas = len(df_fortcasa_filtrado['Nome/Razão Social'].unique())


    st.subheader('Métricas dos Processos')
    coluna1, coluna2, coluna3 = st.columns(3)
    with coluna1:
        st.metric('Total Valor de Causa', format_number(valor_causa, 'R$'))
        st.metric('Quantidade de Processos', qtd_processos)
    with coluna2:
        st.metric('Polo Passivo', contagem_demandado)
        st.metric('Polo Ativo', contagem_demandante)
    with coluna3:
        st.metric('Quantidade de empresas', qtd_empresas)
        st.metric('Quantidade de Loteamentos', qtd_loteamento)

    st.markdown('---')

    st.dataframe(df_fortcasa_filtrado)
    st.write('Quantidade de Registros', df_fortcasa_filtrado['Comarca'].count())

with aba2:
    st.subheader('Gráfico e Análises')

    contagem_fases = df_fortcasa_filtrado['Fase'].value_counts().reset_index()
    contagem_fases.columns = ['Fase', 'Quantidade']
    contagem_fases = contagem_fases.sort_values(by='Quantidade', ascending=False)

    grafico_qtd_fase = px.bar(
        contagem_fases, 
        x='Fase', 
        y='Quantidade', 
        color_discrete_sequence=[px.colors.qualitative.Vivid[5]],
        text_auto = True,
        title='Contagem de Processos por Fases'
    )
    st.plotly_chart(grafico_qtd_fase, use_container_width=True)

    df_vlr_fases = df_fortcasa_filtrado.groupby('Fase')['Valor Causa'].sum().reset_index()
    df_vlr_fases = df_vlr_fases.sort_values(by = 'Valor Causa', ascending=False)
    df_vlr_fases['Valor Causa Formatado'] = df_vlr_fases['Valor Causa'].apply(format_number)

    grafico_vlr_fase = px.bar(
        df_vlr_fases, 
        x='Fase', 
        y='Valor Causa', 
        color_discrete_sequence=[px.colors.qualitative.Vivid[5]],
        text = 'Valor Causa Formatado',
        title='Valor de Causa de Processos por Fases'
    )
    st.plotly_chart(grafico_vlr_fase, use_container_width=True)

    contagem_empreendimento = df_fortcasa_filtrado['Empreendimento'].value_counts().reset_index()
    contagem_empreendimento.columns = ['Empreendimento', 'Quantidade']
    contagem_empreendimento = contagem_empreendimento.sort_values(by='Quantidade', ascending=False)

    grafico_qtd_empreendimento = px.bar(
        contagem_empreendimento.head(10), 
        x='Empreendimento', 
        y='Quantidade', 
        color_discrete_sequence=[px.colors.qualitative.Vivid[5]],
        text_auto = True,
        title='Contagem de Processos por Loteamento'
    )
    st.plotly_chart(grafico_qtd_empreendimento, use_container_width=True)

    df_vlr_lote = df_fortcasa_filtrado.groupby('Empreendimento')['Valor Causa'].sum().reset_index()
    df_vlr_lote = df_vlr_lote.sort_values(by = 'Valor Causa', ascending=False)
    df_vlr_lote['Valor Causa Formatado'] = df_vlr_lote['Valor Causa'].apply(format_number)

    grafico_vlr_lote = px.bar(
        df_vlr_lote.head(10), 
        x='Empreendimento', 
        y='Valor Causa', 
        color_discrete_sequence=[px.colors.qualitative.Vivid[5]],
        text = 'Valor Causa Formatado',
        title='Valor de Causa de Processos por Loteamento'
    )
    st.plotly_chart(grafico_vlr_lote, use_container_width=True)

    contagem_empresa = df_fortcasa_filtrado['Nome/Razão Social'].value_counts().reset_index()
    contagem_empresa.columns = ['Nome/Razão Social', 'Quantidade']
    contagem_empresa = contagem_empresa.sort_values(by='Quantidade', ascending=False)

    grafico_qtd_contagem_empresa = px.bar(
        contagem_empresa.head(10), 
        x='Nome/Razão Social', 
        y='Quantidade', 
        color_discrete_sequence=[px.colors.qualitative.Vivid[5]],
        text_auto = True,
        title='Contagem de Processos por Empresa'
    )
    st.plotly_chart(grafico_qtd_contagem_empresa, use_container_width=True)

    df_vlr_empresa = df_fortcasa_filtrado.groupby('Nome/Razão Social')['Valor Causa'].sum().reset_index()
    df_vlr_empresa = df_vlr_empresa.sort_values(by = 'Valor Causa', ascending=False)
    df_vlr_empresa['Valor Causa Formatado'] = df_vlr_empresa['Valor Causa'].apply(format_number)

    grafico_vlr_empresa = px.bar(
        df_vlr_empresa.head(10), 
        x='Nome/Razão Social', 
        y='Valor Causa', 
        color_discrete_sequence=[px.colors.qualitative.Vivid[5]],
        text = 'Valor Causa Formatado',
        title='Valor de Causa de Processos por Empresa'
    )
    st.plotly_chart(grafico_vlr_empresa, use_container_width=True)