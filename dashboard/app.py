
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ==========================================
# CONFIGURAÇÕES
# ==========================================

st.set_page_config(
    page_title="Dashboard - Pesquisa LEDS",
    page_icon="📊",
    layout="wide"
)

ARQUIVO = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "respostas_exportadas.csv"
)

ESCOLARIDADE = {
    "A001": "Ensino médio incompleto",
    "A002": "Ensino médio completo",
    "A003": "Ensino superior incompleto",
    "A004": "Ensino superior completo",
    "A005": "Pós-graduação"
}

LINGUAGENS = {
    "Q004[SQ001]": "Python",
    "Q004[SQ002]": "Java",
    "Q004[SQ003]": "JavaScript",
    "Q004[SQ004]": "C/C++",
    "Q004[SQ005]": "PHP",
    "Q004[SQ006]": "Nenhuma"
}

# ==========================================
# CARREGAMENTO DOS DADOS
# ==========================================

@st.cache_data
def carregar_dados():
    if not ARQUIVO.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {ARQUIVO}"
        )

    df = pd.read_csv(
        ARQUIVO,
        sep=None,
        engine="python",
        encoding="utf-8-sig"
    )

    # Limpeza dos nomes das colunas
    df.columns = (
        df.columns
        .str.replace("\ufeff", "", regex=False)
        .str.replace('"', "", regex=False)
        .str.strip()
    )

    # Conversão dos campos numéricos
    if "Q002" in df.columns:
        df["Q002"] = pd.to_numeric(
            df["Q002"],
            errors="coerce"
        )

    return df


try:
    df = carregar_dados()

except Exception as erro:
    st.error(f"Erro ao carregar os dados: {erro}")
    st.stop()


# Verificação das colunas necessárias
colunas_obrigatorias = [
    "Q001",
    "Q002",
    "Q003",
    "Q005",
    "Q006"
]

colunas_ausentes = [
    coluna
    for coluna in colunas_obrigatorias
    if coluna not in df.columns
]

if colunas_ausentes:
    st.error(
        f"Colunas não encontradas no CSV: {colunas_ausentes}"
    )

    st.write("Colunas disponíveis:", df.columns.tolist())
    st.stop()


# ==========================================
# CABEÇALHO
# ==========================================

st.title("📊 Dashboard - Pesquisa LEDS")

st.markdown(
    """
    Painel de análise dos dados coletados por meio do
    LimeSurvey, desenvolvido com Python, Pandas,
    Streamlit e Plotly.
    """
)

st.divider()


# ==========================================
# FILTROS
# ==========================================

st.sidebar.header("Filtros")

df_filtrado = df.copy()

idades_validas = df["Q002"].dropna()

if not idades_validas.empty:
    idade_min = int(idades_validas.min())
    idade_max = int(idades_validas.max())

    faixa_etaria = st.sidebar.slider(
        "Faixa etária",
        min_value=idade_min,
        max_value=idade_max,
        value=(idade_min, idade_max)
    )

    df_filtrado = df_filtrado[
        df_filtrado["Q002"].between(
            faixa_etaria[0],
            faixa_etaria[1]
        )
    ]

opcoes_escolaridade = [
    codigo
    for codigo in ESCOLARIDADE
    if codigo in df["Q003"].dropna().unique()
]

escolaridades_selecionadas = st.sidebar.multiselect(
    "Escolaridade",
    options=opcoes_escolaridade,
    default=opcoes_escolaridade,
    format_func=lambda codigo: ESCOLARIDADE[codigo]
)

df_filtrado = df_filtrado[
    df_filtrado["Q003"].isin(escolaridades_selecionadas)
]

situacoes = {
    "A001": "Trabalha",
    "A002": "Não trabalha"
}

situacoes_selecionadas = st.sidebar.multiselect(
    "Situação profissional",
    options=["A001", "A002"],
    default=["A001", "A002"],
    format_func=lambda codigo: situacoes[codigo]
)

df_filtrado = df_filtrado[
    df_filtrado["Q005"].isin(situacoes_selecionadas)
]


# ==========================================
# INDICADORES
# ==========================================

total = len(df_filtrado)

idade_media = df_filtrado["Q002"].mean()

idade_minima = df_filtrado["Q002"].min()

idade_maxima = df_filtrado["Q002"].max()

trabalhando = (
    df_filtrado["Q005"] == "A001"
).sum()

percentual_trabalhando = (
    trabalhando / total * 100 if total else 0
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Participantes",
    total
)

col2.metric(
    "Idade média",
    f"{idade_media:.1f} anos" if pd.notna(idade_media) else "—"
)

col3.metric(
    "Menor idade",
    f"{idade_minima:.0f} anos" if pd.notna(idade_minima) else "—"
)

col4.metric(
    "Participantes que trabalham",
    f"{percentual_trabalhando:.1f}%"
)

st.divider()


# ==========================================
# GRÁFICO 1 - ESCOLARIDADE
# ==========================================

st.subheader("1. Escolaridade dos participantes")

df_filtrado["Escolaridade"] = (
    df_filtrado["Q003"]
    .map(ESCOLARIDADE)
    .fillna("Não informado")
)

dados_escolaridade = (
    df_filtrado["Escolaridade"]
    .value_counts()
    .reset_index()
)

dados_escolaridade.columns = [
    "Escolaridade",
    "Quantidade"
]

if not dados_escolaridade.empty:

    fig1 = px.bar(
        dados_escolaridade,
        x="Escolaridade",
        y="Quantidade",
        text="Quantidade",
        color="Escolaridade",
        title="Distribuição por nível de escolaridade"
    )

    fig1.update_layout(
        showlegend=False,
        xaxis_title="Escolaridade",
        yaxis_title="Número de participantes"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

else:
    st.info("Não existem dados de escolaridade para os filtros selecionados.")


# ==========================================
# GRÁFICO 2 - LINGUAGENS
# ==========================================

st.subheader("2. Linguagens de programação")

dados_linguagens = []

for coluna, nome in LINGUAGENS.items():

    if coluna in df_filtrado.columns:

        quantidade = (
            df_filtrado[coluna]
            .astype(str)
            .str.strip()
            .str.upper()
            .eq("Y")
            .sum()
        )

        dados_linguagens.append({
            "Linguagem": nome,
            "Quantidade": quantidade
        })

linguagens_df = pd.DataFrame(dados_linguagens)

if not linguagens_df.empty:

    linguagens_df = linguagens_df.sort_values(
        "Quantidade",
        ascending=False
    )

    fig2 = px.bar(
        linguagens_df,
        x="Linguagem",
        y="Quantidade",
        text="Quantidade",
        color="Linguagem",
        title="Linguagens conhecidas pelos participantes"
    )

    fig2.update_layout(
        showlegend=False,
        xaxis_title="Linguagem",
        yaxis_title="Número de participantes"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )


# ==========================================
# GRÁFICO 3 - SITUAÇÃO PROFISSIONAL
# ==========================================

st.subheader("3. Situação profissional")

dados_trabalho = (
    df_filtrado["Q005"]
    .map(situacoes)
    .fillna("Não informado")
    .value_counts()
    .reset_index()
)

dados_trabalho.columns = [
    "Situação",
    "Quantidade"
]

if not dados_trabalho.empty:

    fig3 = px.pie(
        dados_trabalho,
        names="Situação",
        values="Quantidade",
        title="Participantes que trabalham",
        hole=0.4
    )

    fig3.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )


# ==========================================
# GRÁFICO 4 - FAIXA ETÁRIA
# ==========================================

st.subheader("4. Distribuição das idades")

idades = df_filtrado.dropna(
    subset=["Q002"]
)

if not idades.empty:

    fig4 = px.histogram(
        idades,
        x="Q002",
        nbins=10,
        title="Distribuição da faixa etária",
        labels={
            "Q002": "Idade",
            "count": "Participantes"
        }
    )

    fig4.update_layout(
        xaxis_title="Idade",
        yaxis_title="Número de participantes"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )


# ==========================================
# GRÁFICO 5 - ÁREAS PROFISSIONAIS
# ==========================================

st.subheader("5. Áreas profissionais")

df_trabalhadores = df_filtrado[
    (df_filtrado["Q005"] == "A001") &
    (df_filtrado["Q006"].notna()) &
    (df_filtrado["Q006"].astype(str).str.strip() != "")
]

if not df_trabalhadores.empty:

    dados_area = (
        df_trabalhadores["Q006"]
        .value_counts()
        .reset_index()
    )

    dados_area.columns = [
        "Área profissional",
        "Quantidade"
    ]

    fig5 = px.bar(
        dados_area,
        x="Quantidade",
        y="Área profissional",
        orientation="h",
        text="Quantidade",
        title="Distribuição por área profissional"
    )

    fig5.update_layout(
        xaxis_title="Número de participantes",
        yaxis_title="Área profissional"
    )

    st.plotly_chart(
        fig5,
        use_container_width=True
    )

else:
    st.info(
        "Não existem respostas de área profissional para os filtros selecionados."
    )


# ==========================================
# TABELA DE DADOS
# ==========================================

st.divider()

st.subheader("Dados coletados")

st.write(
    f"Exibindo {len(df_filtrado)} de {len(df)} respostas."
)

with st.expander("Visualizar respostas completas"):

    st.dataframe(
        df_filtrado,
        use_container_width=True,
        hide_index=True
    )


# ==========================================
# RODAPÉ
# ==========================================

st.divider()

st.caption(
    "Projeto desenvolvido para o desafio técnico do LEDS / UFOP."
)
