# 📄 iLoveMD - Conversor PDF para Markdown

Um simples aplicativo web construído com Django para converter arquivos PDF para o formato Markdown.

## ✨ Funcionalidades

* Upload de arquivos PDF através de uma interface web.
* Conversão do conteúdo do PDF para Markdown utilizando a biblioteca `docling`.
* Exibição do resultado Markdown diretamente no navegador.
* Botão para download do arquivo `.md` gerado.
* (Desenvolvimento) Limpeza automática da pasta de uploads (`media/`) ao reiniciar o servidor de desenvolvimento.

## 🚀 Tecnologias Utilizadas

* **Backend:** Python, Django
* **Conversão PDF:** Biblioteca `docling` (`docling-lib`)
* **Frontend:** HTML, CSS, JavaScript (básico)
* **Banco de Dados (Dev):** SQLite
* **Controle de Versão:** Git, GitHub

## ⚙️ Configuração e Instalação Local

Siga os passos abaixo para rodar o projeto localmente:

1.  **Clone o Repositório:**
    ```bash
    git clone [https://github.com/marcelofirmino29/ILOVEMD.git](https://github.com/marcelofirmino29/ILOVEMD.git)
    cd ILOVEMD
    ```
    *(Substitua a URL se o nome do repositório for diferente)*

2.  **Crie e Ative um Ambiente Virtual:**
    *No Linux/macOS:*
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
    *No Windows:*
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Instale as Dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute as Migrações do Django:** (Necessário para o banco de dados inicial)
    ```bash
    python manage.py migrate
    ```

5.  **Inicie o Servidor de Desenvolvimento:**
    ```bash
    python manage.py runserver
    ```

6.  **Acesse a Aplicação:** Abra seu navegador e vá para `http://127.0.0.1:8000/`.

##  MODO DE USO 

1.  Acesse a página principal (`http://127.0.0.1:8000/`).
2.  Clique em "Escolher arquivo" para selecionar um documento PDF do seu computador.
3.  Clique no botão "Converter para Markdown".
4.  Aguarde o processamento (um indicador de "Convertendo..." será exibido).
5.  O resultado em Markdown será exibido na caixa de texto.
6.  Se a conversão for bem-sucedida, um botão "Baixar [nome_arquivo].md" aparecerá para fazer o download do arquivo convertido.

## 📝 Observações

* A pasta `media/` é limpa automaticamente toda vez que o servidor de desenvolvimento (`runserver`) é iniciado, se a configuração em `interface/apps.py` estiver ativa e `DEBUG=True`.
* Este projeto utiliza SQLite para o banco de dados de desenvolvimento. Para produção, considere usar um banco de dados mais robusto como PostgreSQL ou MySQL.
* Lembre-se de configurar corretamente as variáveis de ambiente e `DEBUG=False` para um ambiente de produção.
