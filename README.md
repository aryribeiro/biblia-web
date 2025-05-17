Obs.: caso o app esteja no modo "sleeping" (dormindo) ao entrar, basta clicar no botão que estará disponível e aguardar, para ativar o mesmo. 
![print biblia web producao](https://github.com/user-attachments/assets/2e845126-48af-4c2e-a78b-1e3fe989edd9)

## README - Bíblia Web App
📖 Bíblia Web App

Este é um aplicativo web desenvolvido com [Streamlit](https://streamlit.io/) que permite aos usuários navegar pelas Escrituras Sagradas em português (versão Almeida Corrigida Fiel) e realizar buscas por palavras dentro de um livro específico.

✨ Funcionalidades
•	Escolha interativa de livros e capítulos da Bíblia
•	Busca por palavra-chave dentro de um livro (mínimo 3 letras)
•	Resultado paginado dos versículos por capítulo
•	Cache com expiração para evitar chamadas excessivas à API
•	Limitação de requisições por minuto respeitando a API pública utilizada
•	Layout limpo, responsivo e com logotipo centralizado

📦 Tecnologias Utilizadas
•	Python 3
•	Streamlit
•	Requests
•	Cachetools
•	Ratellimit

🚀 Como Executar Localmente
1. Clone este repositório
git clone https://github.com/aryribeiro/biblia-web.git
cd biblia-web

2. Crie um ambiente virtual (opcional, mas recomendado)
python -m venv venv
source venv/bin/activate  # No Windows use `venv\Scripts\activate`

3. Instale as dependências
pip install -r requirements.txt

4. Execute a aplicação
streamlit run app.py

📎 Observações
•	O aplicativo utiliza a API pública https://bible-api.com/.
•	Em caso de lentidão ou falha, tente novamente após alguns segundos.

📧 Contato
•	Criado por Ary Ribeiro
•	Email: aryribeiro@gmail.com