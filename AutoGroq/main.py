Aqui está a tradução do código com comentários em português explicando as funções para leigos que nunca viram o código:

```python
import streamlit as st

# Importa os limites de tokens para cada modelo
from config import LIMITES_TOKENS_MODELO

# Importa funções relacionadas ao gerenciamento de agentes
from agent_management import exibir_agentes

# Importa funções relacionadas à interface do usuário
from ui_utils import obter_chave_api, exibir_entrada_chave_api, exibir_discussao_e_whiteboard, exibir_botao_download, exibir_entrada_usuario, exibir_solicitacao_reformulada, exibir_botoes_resetar_e_enviar, exibir_entrada_solicitacao_usuario, reformular_prompt, obter_agentes_de_texto, extrair_codigo_da_resposta, obter_workflow_de_agentes


def main():
    # Adiciona estilos CSS personalizados à página
    st.markdown("""
        <style>
        /* Estilos gerais */
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
        }

        /* Estilos da barra lateral */
        .sidebar .sidebar-content {
            background-color: #ffffff !important;
            padding: 20px !important;
            border-radius: 5px !important;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
        }

        .sidebar .st-emotion-cache-k7vsyb h1 {
            font-size: 12px !important;
            font-weight: bold !important;
            color: #007bff !important;
        }

        .sidebar h2 {
            font-size: 16px !important;
            color: #666666 !important;
        }

        .sidebar .stButton button {
            display: block !important;
            width: 100% !important;
            padding: 10px !important;
            background-color: #007bff !important;
            color: #ffffff !important;
            text-align: center !important;
            text-decoration: none !important;
            border-radius: 5px !important;
            transition: background-color 0.3s !important;
        }

        .sidebar .stButton button:hover {
            background-color: #0056b3 !important;
        }

        .sidebar a {
            display: block !important;
            color: #007bff !important;
            text-decoration: none !important;
        }

        .sidebar a:hover {
            text-decoration: underline !important;
        }

        /* Estilos do conteúdo principal */
        .main .stTextInput input {
            width: 100% !important;
            padding: 10px !important;
            border: 1px solid #cccccc !important;
            border-radius: 5px !important;
        }

        .main .stTextArea textarea {
            width: 100% !important;
            padding: 10px !important;
            border: 1px solid #cccccc !important;
            border-radius: 5px !important;
            resize: none !important;
        }

        .main .stButton button {
            padding: 10px 20px !important;
            background-color: #dc3545 !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 5px !important;
            cursor: pointer !important;
            transition: background-color 0.3s !important;
        }

        .main .stButton button:hover {
            background-color: #c82333 !important;
        }

        .main h1 {
            font-size: 32px !important;
            font-weight: bold !important;
            color: #007bff !important;
        }

        /* Estilos de seleção de modelo */
        .main .stSelectbox select {
            width: 100% !important;
            padding: 10px !important;
            border: 1px solid #cccccc !important;
            border-radius: 5px !important;
        }

        /* Estilos de mensagem de erro */
        .main .stAlert {
            color: #dc3545 !important;
        }
        </style>
        """, unsafe_allow_html=True)
    
    # Dicionário com os limites de tokens para cada modelo
    limites_tokens_modelo = {
        'llama3-70b-8192': 8192,
        'llama3-8b-8192': 8192,
        'mixtral-8x7b-32768': 32768,
        'gemma-7b-it': 8192
    }

    # Obtém a chave de API do usuário
    chave_api = obter_chave_api()
    if chave_api is None:
        # Se a chave de API não foi encontrada, exibe um campo de entrada para o usuário inserir
        chave_api = exibir_entrada_chave_api()
        if chave_api is None:
            st.warning("Por favor, insira sua GROQ_API_KEY para usar o aplicativo.")
            return

    
    col1, col2 = st.columns([1, 1])  # Cria duas colunas na página
    with col1:
        # Exibe uma caixa de seleção para escolher o modelo
        modelo_selecionado = st.selectbox(
            'Selecionar Modelo',
            options=list(LIMITES_TOKENS_MODELO.keys()),
            index=0,
            key='selecao_modelo'
        )
        st.session_state.modelo = modelo_selecionado
        st.session_state.max_tokens = LIMITES_TOKENS_MODELO[modelo_selecionado]

    with col2:
        # Exibe um controle deslizante para ajustar a temperatura (criatividade) do modelo
        temperatura = st.slider(
            "Definir Temperatura",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.get('temperatura', 0.3),
            step=0.01,
            key='temperatura'
        )
            
    st.title("AutoGroq")  # Exibe o título da página
        
    # Garante que os valores padrão para a discussão e o whiteboard estejam definidos
    if "discussao" not in st.session_state:
        st.session_state.discussao = ""
    if "whiteboard" not in st.session_state:
        st.session_state.whiteboard = ""

    with st.sidebar:
        # Adiciona um elemento sidebar à página
        st.markdown('<div class="sidebar">', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    exibir_agentes()  # Exibe os agentes disponíveis
    
    with st.container():
        # Cria um contêiner para o conteúdo principal
        st.markdown('<div class="main">', unsafe_allow_html=True)
        exibir_entrada_solicitacao_usuario()  # Exibe um campo de entrada para o usuário digitar sua solicitação
        exibir_solicitacao_reformulada()  # Exibe a solicitação do usuário reformulada
        st.markdown('<div class="discussao-whiteboard">', unsafe_allow_html=True)
        exibir_discussao_e_whiteboard()  # Exibe a discussão e o whiteboard
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="entrada-usuario">', unsafe_allow_html=True)
        exibir_entrada_usuario()  # Exibe um campo de entrada para o usuário inserir mais informações
        st.markdown('</div>', unsafe_allow_html=True)
        exibir_botoes_resetar_e_enviar()  # Exibe botões para resetar
