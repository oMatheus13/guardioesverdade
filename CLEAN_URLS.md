# Guia de Implementação de URLs Limpas

Este documento explica como usar URLs limpas neste projeto, por que implementamos essa abordagem e fornece diretrizes para manter uma estrutura de URL consistente.

## Estrutura do Projeto

Para entender o contexto destas instruções, é importante estar familiarizado com a estrutura de diretórios do projeto:

```
/ (diretório raiz) 
├── index.html # Página principal 
│   ├── api/ 
│   └── router/ 
│ 
└── index.js # Função serverless para roteamento 
├── css/ # Arquivos CSS globais 
│ ├── reset.css 
│ 
├── fonts.css 
│ ├── variables.css
│ ├── main.css
│ └── components/
│   ├── header.css
│   └── footer.css
├── js/ # Arquivos JavaScript globais
│ └── main.js
├── includes/ # Componentes HTML reutilizáveis
│ ├── header.html
│ └── footer.html
├── pages/ # Páginas HTML estáticas
│ ├── about.html
│ ├── contact.html
│ ├── 404.html
│ └── ...
└── fragments/ # Páginas específicas de cada projeto
    ├── projeto-1/
    │   ├── index.html # Página principal do projeto
    │   └── ...
    ├── projeto-2/
    │   ├── index.html
    │   └── ...
    └── ...
```

## O Que São URLs Limpas?

URLs limpas são endereços web legíveis para humanos e amigáveis para mecanismos de busca. Elas evitam expor a estrutura de arquivos subjacente e as extensões de arquivo. Por exemplo, em vez de:

*   `https://seusite.com/pages/sobre.html`
*   `https://seusite.com/fragments/projeto-x/index.html`

Queremos usar:

*   `https://seusite.com/sobre`
*   `https://seusite.com/projeto-x`

## Por Que Usar URLs Limpas?

*   **Melhor Experiência do Usuário:** Mais fáceis de ler e lembrar, tornando mais simples para os usuários compartilhar e navegar no site.
*   **Melhor SEO:** Mecanismos de busca preferem URLs limpas, o que pode melhorar o ranking do seu site.
*   **Segurança Aprimorada:** Oculta a estrutura de arquivos interna, reduzindo o risco de expor informações confidenciais.
*   **Manutenção Facilitada:** Simplifica o gerenciamento do site e reduz o impacto da reorganização de arquivos.

## Detalhes da Implementação

Para alcançar URLs limpas, usamos uma combinação dos recursos de roteamento da Vercel e uma função serverless:

1.  **Função Serverless (`api/router/index.js`):**
    *   Esta função atua como um roteador central, interceptando todas as solicitações de entrada e servindo o arquivo HTML apropriado.
    *   Ela verifica se a URL solicitada corresponde a um arquivo no diretório `pages/` ou a um projeto no diretório `fragments/`.
    *   Se uma correspondência for encontrada, a função lê o arquivo e o envia ao navegador.
    *   Se nenhuma correspondência for encontrada, ela serve a página `404.html`.

2.  **Configuração da Vercel (`vercel.json`):**
    *   O arquivo `vercel.json` contém uma regra de reescrita que direciona todas as solicitações de entrada para a função `api/router/index.js`.
    *   Isso permite que a função serverless lide com a lógica de roteamento.

## Como Usar URLs Limpas

Para usar URLs limpas de forma eficaz, siga estas diretrizes:

### 1. Links Entre Páginas

Ao criar links entre páginas dentro do seu site, **sempre use as URLs limpas**:

```html
<a href="/sobre">Sobre Nós</a>
<a href="/contato">Contato</a>
<a href="/projeto-x">Ver Projeto X</a>
```
Não use as URLs antigas:
```html
<!-- Incorreto -->
<a href="pages/sobre.html">Sobre Nós</a>
<a href="fragments/projeto-x/index.html">Ver Projeto X</a>
```
### 2. Convenções de Nomenclatura
*   **Páginas:** Para páginas em `pages/` (ex: `sobre.html`, `contato.html`), a URL limpa é o nome do arquivo sem a extensão `.html`: `/sobre`, `/contato`.
*   **Projetos (Fragments):** Para projetos em `fragments/`, a URL limpa é o nome do diretório do projeto: `/projeto-x`, `/projeto-y`. Cada projeto deve ter um arquivo `index.html` como ponto de entrada principal.
*   **Raiz:** Para a página principal, a URL limpa é `/`.
### 3. Assets (CSS, JavaScript, Imagens)
Os caminhos para os assets (CSS, JavaScript, imagens, fontes, etc.) devem ser relativos à raiz do seu projeto `/`.

*   O CSS local do fragmento deve ser vinculado assim:

```html
<link rel="stylesheet" href="/fragments/o-que-o-mundo-deveria-saber/f-fonts.css" />
```
*   O CSS global deve ser vinculado assim:

```html
<link rel="stylesheet" href="/css/reset.css" />
```
*   As imagens dos fragmentos devem ser vinculadas assim:

```html
<img src="/fragments/o-que-o-mundo-deveria-saber/assets/img/mockups-e-aplicacoes/iphone-14-case-mockup.png" alt="Mockups em quadros, capinha de celular, fita cassete" />
```
### 4. Adicionando Novas Páginas/Projetos
*   **Nova Página:** Crie um novo arquivo HTML no diretório `pages/` (ex: `pages/nova-pagina.html`). A URL limpa será `/nova-pagina`.
*   **Novo Projeto:** Crie um novo diretório no diretório `fragments/` (ex: `fragments/novo-projeto/`). Adicione um arquivo `index.html` a este diretório. A URL limpa será `/novo-projeto`.
*   Não é necessário atualizar `vercel.json`: A função serverless lidará automaticamente com o roteamento para novas páginas e projetos.

### 5. Considerações Importantes
*   **Sensibilidade a Maiúsculas e Minúsculas:** URLs geralmente não diferenciam maiúsculas de minúsculas. No entanto, é uma boa prática usar URLs em letras minúsculas para consistência.
*   **Barras Iniciais:** Evite usar barras finais (ex: `/sobre/`) a menos que seja necessário.
