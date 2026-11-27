# Desafio Técnico LEDS — Pesquisa e Análise de Dados

Projeto desenvolvido como parte do desafio técnico do Laboratório de Estudos e Desenvolvimento de Sistemas (LEDS), vinculado ao Instituto de Ciências Exatas e Aplicadas (ICEA) da Universidade Federal de Ouro Preto (UFOP).

O projeto consiste na criação de um formulário de pesquisa utilizando LimeSurvey, geração e inserção automatizada de respostas por meio de Python e desenvolvimento de um dashboard interativo para visualização e análise dos dados coletados.

## Objetivos

- Desenvolver um formulário de pesquisa no LimeSurvey.
- Implementar perguntas de diferentes tipos, incluindo perguntas condicionais.
- Automatizar a geração de respostas fictícias utilizando Python.
- Integrar Python ao LimeSurvey por meio da API RemoteControl 2.
- Exportar e processar os dados coletados.
- Desenvolver um dashboard interativo para apresentação dos resultados.

## Tecnologias utilizadas

| Tecnologia | Aplicação |
|---|---|
| Python | Automação e processamento de dados |
| LimeSurvey | Criação e gerenciamento da pesquisa |
| LimeSurvey RemoteControl 2 | Comunicação com a API |
| Pandas | Manipulação e análise dos dados |
| Faker | Geração de dados fictícios |
| Streamlit | Desenvolvimento do dashboard |
| Plotly | Criação de gráficos interativos |
| Git e GitHub | Versionamento e hospedagem do projeto |

## Estrutura do projeto

```text
desafio-leds/
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── respostas.csv
│   └── respostas_exportadas.csv
│
├── limesurvey/
│   └── pesquisa.lss
│
├── scripts/
│   ├── testar_api.py
│   ├── gerar_respostas.py
│   ├── inserir_respostas.py
│   └── exportar_respostas.py
│
├── .env
├── .gitignore
├── requirements.txt
├── README.md
└── USO_DE_IA.md
```

## Configuração do ambiente

### 1. Clonar o repositório

```bash
git clone URL_DO_REPOSITORIO
cd desafio-leds
```

### 2. Criar um ambiente virtual

```bash
python -m venv .venv
```

Ativação no Linux/macOS:

```bash
source .venv/bin/activate
```

Ativação no Windows:

```bash
.venv\Scripts\activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
LIMESURVEY_URL=https://SEU_SERVIDOR_LIMESURVEY
LIMESURVEY_USERNAME=SEU_USUARIO
LIMESURVEY_PASSWORD=SUA_SENHA
LIMESURVEY_SURVEY_ID=467649
```

As informações de acesso devem ser substituídas pelas credenciais correspondentes ao ambiente utilizado.

## Execução do projeto

### 1. Testar a comunicação com o LimeSurvey

```bash
python scripts/teste_api.py
```

O script verifica a autenticação e a comunicação com a API RemoteControl 2.

### 2. Gerar respostas fictícias

```bash
python scripts/gerar_respostas.py
```

As respostas são geradas utilizando a biblioteca Faker e armazenadas em:

```text
data/respostas.csv
```

### 3. Inserir respostas no LimeSurvey

```bash
python scripts/inserir_respostas.py
```

O script realiza a leitura do CSV e utiliza o método `add_response` da API para registrar as respostas na pesquisa.

**Atenção:** execute a inserção somente para registros que ainda não tenham sido enviados. A execução repetida pode gerar respostas duplicadas.

### 4. Exportar respostas

```bash
python scripts/exportar_respostas.py
```

Os dados registrados no LimeSurvey são exportados por meio da API e armazenados em:

```text
data/respostas_exportadas.csv
```

### 5. Executar o dashboard

```bash
streamlit run dashboard/app.py
```

Após a execução, acesse o endereço local apresentado pelo Streamlit, normalmente:

```text
http://localhost:8501
```

No GitHub Codespaces, utilize a porta 8501 disponibilizada na aba Ports.

## Dashboard

O dashboard utiliza os dados exportados do LimeSurvey para apresentar indicadores e visualizações interativas.

Entre as análises implementadas estão:

- Total de participantes.
- Idade média e menor idade.
- Percentual de participantes que trabalham.
- Distribuição por escolaridade.
- Linguagens de programação conhecidas.
- Distribuição da faixa etária.
- Áreas profissionais dos participantes.

Também são disponibilizados filtros para exploração dos dados por faixa etária, escolaridade e situação profissional.

## Fluxo de funcionamento

1. Criação e configuração da pesquisa no LimeSurvey.
2. Geração de respostas fictícias com Python.
3. Inserção das respostas por meio da API RemoteControl 2.
4. Exportação dos dados da pesquisa.
5. Processamento dos dados com Pandas.
6. Apresentação dos resultados por meio do Streamlit e Plotly.

## Arquivos importantes

- `cadastro_aluno.lss`: arquivo de exportação da estrutura da pesquisa LimeSurvey.
- `requirements.txt`: dependências Python necessárias.
- `.env`: configurações de acesso à API.
- `USO_DE_IA.md`: documentação sobre a utilização de inteligência artificial durante o desenvolvimento.

## Considerações finais

O projeto demonstra a integração entre ferramentas de coleta de dados, automação com Python e visualização interativa de informações.

A solução foi desenvolvida com foco na organização dos dados, automatização de tarefas e apresentação dos resultados de maneira acessível.

---

**Projeto desenvolvido para o desafio técnico do LEDS — UFOP.**