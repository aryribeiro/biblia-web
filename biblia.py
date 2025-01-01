import streamlit as st
import requests
import math

# Funções auxiliares
def fetch_verses(book, chapter):
    url = f"https://bible-api.com/{book}%20{chapter}?translation=almeida"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("verses", [])
    return []

def search_word(word):
    results = []
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
    
    for book in books:
        for chapter in range(1, 151 if book == "Salmos" else 23 if book == "Apocalipse" else 31):
            url = f"https://bible-api.com/{book}%20{chapter}?translation=almeida"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json().get("verses", [])
                for verse in data:
                    if word.lower() in verse["text"].lower():
                        results.append({
                            "book": book,
                            "chapter": verse["chapter"],
                            "verse": verse["verse"],
                            "text": verse["text"]
                        })
            else:
                break
    return results

# Configuração do Streamlit
st.set_page_config(page_title="Bíblia Online", layout="wide")
st.title("📖 Bíblia Online - Almeida")

# Menu de seleção
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
selected_book = st.selectbox("Escolha o Livro", books)

if selected_book:
    # Determinar o número de capítulos dinamicamente
    chapters = list(range(1, 151 if selected_book == "Salmos" else 23 if selected_book == "Apocalipse" else 31))
    selected_chapter = st.selectbox("Escolha o Capítulo", chapters)

    # Exibir os versículos do capítulo escolhido
    if selected_chapter:
        verses = fetch_verses(selected_book, selected_chapter)
        if verses:
            # Paginação
            items_per_page = 10
            total_pages = math.ceil(len(verses) / items_per_page)
            page = st.number_input("Página", min_value=1, max_value=total_pages, value=1)

            start_idx = (page - 1) * items_per_page
            end_idx = start_idx + items_per_page

            for verse in verses[start_idx:end_idx]:
                st.markdown(f"**{verse['verse']}**: {verse['text']}")

            st.markdown("---")
        else:
            st.error("Nenhum versículo encontrado para este capítulo.")

# Campo de busca por palavra
st.sidebar.header("🔍 Busca por Palavra")
search_term = st.sidebar.text_input("Digite uma palavra")
if st.sidebar.button("Buscar"):
    results = search_word(search_term)
    if results:
        for result in results:
            st.sidebar.markdown(f"**{result['book']} {result['chapter']}:{result['verse']}**: {result['text']}")
    else:
        st.sidebar.error("Nenhum resultado encontrado.")
