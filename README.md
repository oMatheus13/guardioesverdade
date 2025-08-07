# Guardiões da Verdade

Este repositório contém o código-fonte do site do Clube de Desbravadores Guardiões da Verdade. O projeto visa fornecer uma plataforma online para o clube, incluindo informações sobre eventos, áreas restritas para membros, e um sistema de sócio-guardião para arrecadação de fundos.

## Visão Geral

O projeto `Guardiões da Verdade` é uma aplicação web desenvolvida em Python, utilizando o framework Flask, para dar suporte às atividades e à comunidade do Clube de Desbravadores Guardiões da Verdade. Ele integra funcionalidades como autenticação de usuários, gerenciamento de conteúdo dinâmico, e um sistema de doações via Mercado Pago.




## Funcionalidades

- **Páginas Informativas:** Homepage, Sobre, Álbum, Classes, Contato, Dracmas, Eventos, Unidades.
- **Autenticação de Usuários:** Login, Cadastro e Logout de usuários.
- **Área Restrita:** Conteúdo exclusivo para membros logados.
- **Sócio Guardião:** Página dedicada ao programa de sócio-guardião com links de pagamento via Mercado Pago.
- **Integração com Mercado Pago:** Webhook para processamento de pagamentos e atualização do plano do usuário.
- **Estrutura MVC:** Organização do código seguindo o padrão Model-View-Controller.
- **Gerenciamento de Banco de Dados:** Utilização de SQLAlchemy e Flask-Migrate para manipulação e migração de banco de dados.




## Tecnologias Utilizadas

O projeto é construído com as seguintes tecnologias:

- **Python:** Linguagem de programação principal.
- **Flask:** Microframework web para Python.
- **SQLAlchemy:** ORM (Object Relational Mapper) para interação com o banco de dados.
- **Flask-Migrate:** Extensão para gerenciar migrações de banco de dados com Alembic.
- **Flask-Login:** Gerenciamento de sessões de usuário.
- **Flask-Bcrypt:** Hashing de senhas.
- **Mercado Pago SDK:** Integração com a API do Mercado Pago para pagamentos.
- **Supabase:** Utilizado para autenticação e possivelmente outras funcionalidades de backend (baseado nas variáveis de ambiente `SUPABASE_URL` e `SUPABASE_KEY`).
- **PostgreSQL:** Banco de dados relacional (indicado pelo `psycopg2-binary` no `requirements.txt`).
- **HTML/CSS:** Para a construção das interfaces de usuário.




## Como Rodar o Projeto

Para configurar e executar o projeto localmente, siga os passos abaixo:

### Pré-requisitos

- Python 3.x
- pip (gerenciador de pacotes do Python)
- PostgreSQL (ou outro banco de dados compatível, se preferir)

### Instalação

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/oMatheus13/guardioesverdade.git
    cd guardioesverdade
    ```

2.  **Crie e ative um ambiente virtual (recomendado):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # No Linux/macOS
    # venv\Scripts\activate  # No Windows
    ```

3.  **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as variáveis de ambiente:**

    Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

    ```
    SECRET_KEY='sua_chave_secreta_aqui'
    DATABASE_URL='postgresql://user:password@host:port/database_name'
    SUPABASE_URL='sua_url_supabase_aqui'
    SUPABASE_KEY='sua_chave_supabase_aqui'
    TOKEN_MERCADOPAGO='seu_token_mercadopago_aqui'
    ```

    - `SECRET_KEY`: Uma chave secreta para segurança da aplicação Flask.
    - `DATABASE_URL`: A URL de conexão com o seu banco de dados PostgreSQL.
    - `SUPABASE_URL` e `SUPABASE_KEY`: Credenciais para integração com o Supabase.
    - `TOKEN_MERCADOPAGO`: Seu token de acesso do Mercado Pago para a integração de pagamentos.

5.  **Inicialize e migre o banco de dados:**

    ```bash
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

### Execução

Para iniciar a aplicação, execute:

```bash
python main.py
```

O servidor estará disponível em `http://0.0.0.0:5000` (ou `http://127.0.0.1:5000`).




## Contribuição

Contribuições são bem-vindas! Se você deseja contribuir com este projeto, por favor, siga estas etapas:

1.  Faça um fork do repositório.
2.  Crie uma nova branch para sua feature (`git checkout -b feature/sua-feature`).
3.  Faça suas alterações e commit (`git commit -m 'feat: Adiciona sua feature'`).
4.  Envie para a branch (`git push origin feature/sua-feature`).
5.  Abra um Pull Request.




## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.



