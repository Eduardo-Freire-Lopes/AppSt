import streamlit as st
import pandas as pd

st.set_page_config(page_title="Comparação Planilhas",layout="wide")

# st.markdown('<title>Meu Aplicativo Streamlit</title>', unsafe_allow_html=True)
st.markdown("""
    <style>
        .st-emotion-cache-1jicfl2 {
            padding-left: 5rem;
            padding-right: 5rem;
            padding-top: 1.2rem;
        }
    </style>)
""", unsafe_allow_html=True)

# st.markdown("""
#     <div style="text-align: center;">
#         <h1>Comparação de Planilhas</h1>
#     </div>
# """, unsafe_allow_html=True)

def excluir_linhas_do_df_maior(file1, file2, df_interseccao):
    # Ler os arquivos diretamente dentro da função
    df = pd.read_excel(file1)
    df_empregados_sem_deb = pd.read_excel(file2)

    # Obter o dataframe maior
    if len(df) > len(df_empregados_sem_deb):
        df_maior = df
    else:
        df_maior = df_empregados_sem_deb

    # Filtrar o df_maior removendo as linhas que estão no df_interseccao
    df_maior_sem_interseccao = df_maior[~df_maior['Unnamed: 2'].isin(df_interseccao['PIS'])]

    return df_maior_sem_interseccao


def processar_arquivos(file1, file2):

    df = pd.read_excel(file1)
    df_empregados_sem_deb = pd.read_excel(file2)

    df_interseccao = pd.merge(df, df_empregados_sem_deb, on='Unnamed: 1', how='inner')

    df_interseccao = df_interseccao.rename(columns={
        "Unnamed: 1": "Nome",
        'Unnamed: 2_x': "PIS"
    })

    # Limpeza (remover NaN e ajustar o índice)
    df_interseccao = df_interseccao[['Nome', "PIS"]].drop_duplicates(['PIS'])

    return df_interseccao[1:-1]
#----------------------------------------------------------------------------------------------------------------------

colunas0, colunas1,colunas3, colunas2,colunas4 = st.columns([0.12,1.003,0.03,1,0.12])

with colunas1:
    uploaded_file_1 = st.file_uploader("Insira o arquivo Original", type=["xlsx"])

with colunas2:
    uploaded_file_2 = st.file_uploader("Insira Arquivo Novo", type=["xlsx"])

# colshow1, colshow2 = st.columns([1, 1])

with colunas2:
    if uploaded_file_1 and uploaded_file_2:
        df_interseccao2 = processar_arquivos(uploaded_file_1, uploaded_file_2)

        # with colshow1:
        st.subheader("Quem está em ambas:")
        st.dataframe(df_interseccao2)

with colunas1:
    if uploaded_file_1 and uploaded_file_2:
        df_maior_sem_interseccao = excluir_linhas_do_df_maior(uploaded_file_1, uploaded_file_2, df_interseccao2)

        # with colshow2:
        st.subheader("Original sem quem está em ambas:")
        st.dataframe(df_maior_sem_interseccao)
