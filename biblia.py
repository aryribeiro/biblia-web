import streamlit as st
import requests
import math
import time
from cachetools import TTLCache
from ratelimit import limits, sleep_and_retry
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Configuração de cache
cache = TTLCache(maxsize=500, ttl=3600)

# Limite de requisições por minuto
REQUESTS_PER_MINUTE = 20
MAX_REQUESTS_PER_SEARCH = 50  # Máximo de requisições por busca

# Função para configurar sessão com retries
def create_session():
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    return session

session = create_session()

@sleep_and_retry
@limits(calls=REQUESTS_PER_MINUTE, period=60)
def fetch_with_rate_limit(url):
    """Faz uma requisição respeitando o limite de taxa."""
    return session.get(url, timeout=10)

def fetch_verses(book, chapter, retries=5):
    cache_key = f"{book}-{chapter}"
    if cache_key in cache:
        return cache[cache_key]

    url = f"https://bible-api.com/{book}%20{chapter}?translation=almeida"
    for attempt in range(retries):
        try:
            response = fetch_with_rate_limit(url)
            if response.status_code == 429:
                time.sleep(2 ** attempt)
                continue
            response.raise_for_status()
            data = response.json()
            verses = data.get("verses", [])
            cache[cache_key] = verses
            return verses
        except requests.exceptions.RequestException as e:
            if attempt == retries - 1:
                st.error(f"Erro ao buscar versículos: {e}")
                break
    return []

def search_word_in_book(book, word):
    if not word or len(word) < 3:
        st.warning("Digite uma palavra c/ pelo menos 3 letras.")
        return []

    results = []
    request_count = 0
    try:
        for chapter in range(1, 151 if book == "Salmos" else 23 if book == "Apocalipse" else 31):
            if request_count >= MAX_REQUESTS_PER_SEARCH:
                st.warning("Limite de requisições atingido para esta busca. Por favor, tente novamente mais tarde.")
                break
            verses = fetch_verses(book, chapter)
            request_count += 1
            if verses:
                for verse in verses:
                    if word.lower() in verse["text"].lower():
                        results.append({
                            "chapter": verse["chapter"],
                            "verse": verse["verse"],
                            "text": verse["text"]
                        })
            else:
                break
        return results
    except Exception as e:
        st.error(f"Erro na busca: {e}")
        return []

# Configuração inicial do Streamlit
st.set_page_config(page_title="Bíblia Web App", layout="wide", page_icon="📖")

# URL do logo
logo_url = "https://i.imgur.com/HfH3YQ1.jpeg"

# Exibindo o logo pela URL
st.markdown(
    f"""
    <style>
        .centered-logo {{
            display: flex;
            justify-content: center;
        }}
    </style>
    <div class="centered-logo">
        <img src="{logo_url}" width="400">
    </div>
    """,
    unsafe_allow_html=True
)

# Estilização global para textos
st.markdown(
    """
    <style>
    /* Ajuste global do tamanho da fonte */
    html, body, [class*="css"] {
        font-size: 1.2rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Bíblia Web App")

books = [
    "Gênesis", "Êxodo", "Levítico", "Números", "Deuteronômio", "Josué", "Juízes", "Rute",
    "1 Samuel", "2 Samuel", "1 Reis", "2 Reis", "1 Crônicas", "2 Crônicas", "Esdras",
    "Neemias", "Ester", "Jó", "Salmos", "Provérbios", "Eclesiastes", "Cantares de Salomão",
    "Isaías", "Jeremias", "Lamentações", "Ezequiel", "Daniel", "Oséias", "Joel", "Amós",
    "Obadias", "Jonas", "Miquéias", "Naum", "Habacuque", "Sofonias", "Ageu", "Zacarias", "Malaquias",
    "Mateus", "Marcos", "Lucas", "João", "Atos", "Romanos", "1 Coríntios", "2 Coríntios",
    "Gálatas", "Efésios", "Filipenses", "Colossenses", "1 Tessalonicenses", "2 Tessalonicenses",
    "1 Timóteo", "2 Timóteo", "Tito", "Filemom", "Hebreus", "Tiago", "1 Pedro", "2 Pedro",
    "1 João", "2 João", "3 João", "Judas", "Apocalipse"
]

# Menu lateral
st.sidebar.header("📖 Escolha o Livro")

# Campo para selecionar o livro
selected_book = st.sidebar.selectbox("Almeida Corrigida Fiel", books)

# Menu lateral para busca
st.sidebar.header("🔍 Busca por Palavra")

# Campo para buscar palavra
search_term = st.sidebar.text_input("Digite uma palavra com pelo menos 3 letras")

# Botão para iniciar a busca
if st.sidebar.button("Buscar"):
    if selected_book and search_term:
        with st.spinner("Por favor aguarde..."):
            results = search_word_in_book(selected_book, search_term)
            if results:
                st.sidebar.success(f"Foram encontrados {len(results)} resultados.")
                for result in results:
                    st.sidebar.markdown(
                        f"**{selected_book} {result['chapter']}:{result['verse']}**: {result['text']}"
                    )
            else:
                st.sidebar.error("Nenhum resultado encontrado.")
    else:
        st.sidebar.warning("Escolha um livro e digite uma palavra válida para buscar.")

# Menu principal para selecionar capítulos e exibir versículos
if selected_book:
    chapters = list(range(1, 151 if selected_book == "Salmos" else 23 if selected_book == "Apocalipse" else 31))
    selected_chapter = st.selectbox("Após escolher o **Livro** no menu lateral esquerdo, escolha o **Capítulo** abaixo", chapters)

    if selected_chapter:
        verses = fetch_verses(selected_book, selected_chapter)
        if verses:
            items_per_page = 10
            total_pages = math.ceil(len(verses) / items_per_page)
            page = st.number_input("Escolha a **Página**, para ver demais versículos, clicando no sinal de **MAIS** ou **MENOS**, ao lado ⮕", min_value=1, max_value=total_pages, value=1)

            start_idx = (page - 1) * items_per_page
            end_idx = start_idx + items_per_page

            for verse in verses[start_idx:end_idx]:
                st.markdown(f"**{verse['verse']}**: {verse['text']}")

            st.markdown("---")
        else:
            st.error("Nenhum versículo encontrado para este capítulo.")

# informações de contato
st.markdown("""

#### Bíblia Web App | ACF
💬 Por Ary Ribeiro. Contato, através do email: aryribeiro@gmail.com
\n Obs.: esse aplicativo web construído com API pública, de terceiros. Caso a busca esteja lenta, favor aguardar.
""")