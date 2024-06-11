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

    polo = df_fortcasa['Status Processual'].unique().tolist()
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
        df_fortcasa_filtrado = df_fortcasa_filtrado[df_fortcasa_filtrado['Status Processual'].isin(filtro_polo)]

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
    # =========== Transformando em Float =========== #
    df_fortcasa_filtrado['Valor da Causa'] = df_fortcasa_filtrado['Valor da Causa'].astype(str).str.replace(',', '.', regex=False).astype(float)
    df_fortcasa_filtrado['Valor do Acordo'] = df_fortcasa_filtrado['Valor do Acordo'].astype(str).str.replace(',', '.', regex=False).astype(float)
    df_fortcasa_filtrado['Valor de Cumprimento de Sentença'] = df_fortcasa_filtrado['Valor de Cumprimento de Sentença'].astype(str).str.replace(',', '.', regex=False).astype(float)

    # =========== Somando Valores =========== #
    valor_causa = df_fortcasa_filtrado['Valor da Causa'].sum()
    valor_cump_sentenca = df_fortcasa_filtrado['Valor de Cumprimento de Sentença'].sum()
    valor_acordo = df_fortcasa_filtrado['Valor do Acordo'].sum()

    # =========== Contando Valores =========== #
    contagem_polo_passivo  = df_fortcasa_filtrado['Status Processual'].value_counts().get('POLO PASSIVO', 0)
    contagem_polo_ativo = df_fortcasa_filtrado['Status Processual'].value_counts().get('POLO ATIVO', 0)
    qtd_loteamento = len(df_fortcasa_filtrado['Empreendimento'].unique())
    qtd_empresas = len(df_fortcasa_filtrado['Nome/Razão Social'].unique())


    st.subheader('Métricas dos Processos')
    coluna1, coluna2, coluna3 = st.columns(3)
    with coluna1:
        st.metric('Total Valor de Causa', format_number(valor_causa, 'R$'))
        st.metric('Total Valor de Cumprimento de Sentença]', format_number(valor_cump_sentenca, 'R$'))
        st.metric('Total Valor do Acordo', format_number(valor_acordo, 'R$'))
        
    with coluna2:
        st.metric('Quantidade de Processos', qtd_processos)
        st.metric('Polo Passivo', contagem_polo_passivo )
        st.metric('Polo Ativo', contagem_polo_ativo)
    with coluna3:
        st.metric('Quantidade de Empresas', qtd_empresas)
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
        y='Fase', 
        x='Quantidade', 
        color_discrete_sequence=[px.colors.qualitative.Vivid[5]],
        text='Quantidade',
        orientation='h',
        title='Contagem de Processos por Fases'
    )
    st.plotly_chart(grafico_qtd_fase, use_container_width=True)

    df_vlr_fases = df_fortcasa_filtrado.groupby('Fase')['Valor da Causa'].sum().reset_index()
    df_vlr_fases = df_vlr_fases.sort_values(by = 'Valor da Causa', ascending=False)
    df_vlr_fases['Valor da Causa Formatado'] = df_vlr_fases['Valor da Causa'].apply(format_number)

    grafico_vlr_fase = px.bar(
        df_vlr_fases, 
        x='Fase', 
        y='Valor da Causa', 
        color_discrete_sequence=[px.colors.qualitative.Vivid[5]],
        text = 'Valor da Causa Formatado',
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
        text = 'Quantidade',
        title='Contagem de Processos por Loteamento'
    )
    st.plotly_chart(grafico_qtd_empreendimento, use_container_width=True)

    df_vlr_lote = df_fortcasa_filtrado.groupby('Empreendimento')['Valor da Causa'].sum().reset_index()
    df_vlr_lote = df_vlr_lote.sort_values(by = 'Valor da Causa', ascending=False)
    df_vlr_lote['Valor da Causa Formatado'] = df_vlr_lote['Valor da Causa'].apply(format_number)

    grafico_vlr_lote = px.bar(
        df_vlr_lote.head(10), 
        x='Empreendimento', 
        y='Valor da Causa', 
        color_discrete_sequence=[px.colors.qualitative.Vivid[5]],
        text = 'Valor da Causa Formatado',
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
        text = 'Quantidade',
        title='Contagem de Processos por Empresa'
    )
    st.plotly_chart(grafico_qtd_contagem_empresa, use_container_width=True)

    df_vlr_empresa = df_fortcasa_filtrado.groupby('Nome/Razão Social')['Valor da Causa'].sum().reset_index()
    df_vlr_empresa = df_vlr_empresa.sort_values(by = 'Valor da Causa', ascending=False)
    df_vlr_empresa['Valor da Causa Formatado'] = df_vlr_empresa['Valor da Causa'].apply(format_number)

    grafico_vlr_empresa = px.bar(
        df_vlr_empresa.head(10), 
        x='Nome/Razão Social', 
        y='Valor da Causa', 
        color_discrete_sequence=[px.colors.qualitative.Vivid[5]],
        text = 'Valor da Causa Formatado',
        title='Valor de Causa de Processos por Empresa'
    )
    st.plotly_chart(grafico_vlr_empresa, use_container_width=True)
