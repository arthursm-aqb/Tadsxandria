# CDU008. Editar projeto

- **Ator principal**: Usuário orientado
- **Atores secundários**: Usuário orientador	 
- **Resumo**: Esse caso de uso descreve as ações realizadas por usuários que querem editar informações sobre o projeto
- **Pré-condição**: Usuário precisa estar já inserido em um projeto
- **Pós-Condição**: Notificação do sistema dizendo que as mudanças foram salvas

## Fluxo Principal - Usuário do tipo orientado editando o projeto
| Ações do ator | Ações do sistema |
| :-----------------: | :-----------------: | 
| 1 - Usuário abre a página "editar projeto" | |  
| | 2 - O sistema abre a página, onde tem a primeira parte formulário com informações que já foram preenchidas durande a criação do projeto. As informações são: título, plataforma, ano/semestre, colaboradores, contato, orientador, categoria e subcategoria  | 
| 3 - O usuário realiza alterações e depois seleciona a opção avançar para editar outras informações | |
| | 4- O sistema passa para a página seguinte, onde tem as informações: resumo, descrição, ferramentas utilizadas, repositório, status e a imagem, que será a capa do projeto |
| 5 - O usuário realiza alterações e salva as mudanças | |
| | 6 - O sistema envia uma mensagem dizendo "alterações salvas" |

## Fluxo Alternativo I - Usuário do tipo orientador editando o projeto
| Ações do ator | Ações do sistema |
| :-----------------: |:-----------------: | 
| 1.1 - Usuário abre a página "editar projeto" | |  
| | 1.2 - O sistema abre a página, onde tem a primeira parte formulário com informações que já foram preenchidas durande a criação do projeto. As informações são: título, plataforma, colaboradores, contato, orientador, categoria e subcategoria |
| 1.3 - O usuário realiza alterações e depois seleciona a opção avançar para editar outras informações | |
| | 1.4- O sistema passa para a página seguinte, onde tem as informações: resumo, descrição, ferramentas utilizadas, repositório, status e a imagem, que será a capa do projeto |
| 1.5 - O usuário realiza alterações e salva as mudanças | |
| | 1.6 - O sistema envia uma mensagem dizendo "alterações salvas" |

## Fluxo Alternativo II - Colaborador não encontrado
| Ações do ator | Ações do sistema |
| :-----------------: | :-----------------: | 
| 2.1 - Usuário abre a página "editar projeto" | |  
| | 2.2 - O sistema abre a página, onde tem a primeira parte formulário com informações que já foram preenchidas durande a criação do projeto. As informações são: título, plataforma, colaboradores, contato, orientador, categoria e subcategoria |
| 2.3 - O usuário realiza alterações na parte de colaborador mas insere um id não reconhecido pelo sistema e depois seleciona a opção avançar para editar outras informações | |
| | 2.4- O sistema não passa para a página seguinte e envia uma notificação dizendo "Colaborador não encontrado" |

> Obs. as seções a seguir apenas serão utilizadas na segunda unidade do PDSWeb (segundo orientações do gerente do projeto).

## Diagrama de Interação (Sequência ou Comunicação)

```mermaid
sequenceDiagram
    autonumber
    actor U as Usuário
    participant V1 as EditarProjetoPasso1View
    participant F1 as EditarProjetoPasso1Form
    participant V2 as EditarProjetoPasso2View
    participant F2 as EditarProjetoPasso2Form
    participant S as ProjetoService
    participant SES as HttpRequest.session
    participant M as Projeto (Model/ORM)

    note over U, V1: Usuário já se encontra visualizando o formulário do Passo 1
    
    %% SUBMISSÃO DO PASSO 1
    U->>V1: HTTP POST (dados do formulário 1 inseridos no corpo da requisição)
    activate V1
    V1->>F1: Instancia formulário passando dicionário (request.POST)
    V1->>F1: Invoca método de validação .is_valid()
    activate F1
    F1-->>V1: Retorna True (Validação de tipos e restrições bem-sucedida)
    deactivate F1
    
    V1->>S: Invoca salvar_passo_sessao(projeto_id, request.session, form.cleaned_data)
    activate S
    S->>SES: Grava o dicionário estruturado: session['dados_edicao_1'] = cleaned_data
    SES-->>S: Confirmação de armazenamento na tabela hash em memória/banco
    S-->>V1: Retorno de execução bem-sucedida do método de serviço
    deactivate S
    
    V1-->>U: Retorna HTTP 302 Redirect para a URL 'editar_projeto_passo2'
    deactivate V1

    %% TRANSIÇÃO E GET DO PASSO 2
    U->>V2: HTTP GET automático disparado pelo redirecionamento do navegador
    activate V2
    V2->>S: Invoca obter_dados_iniciais(projeto_id, request.session)
    activate S
    S->>SES: Realiza leitura das chaves 'dados_edicao_1' para verificar estado
    SES-->>S: Retorna dicionário contendo os dados salvos no passo anterior
    S-->>V2: Retorna o dicionário de dados consolidados combinados
    deactivate S
    
    V2->>F2: Instancia formulário injetando os dados recuperados no argumento (initial=dados)
    F2-->>V2: Retorna objeto do formulário populado dinamicamente
    V2-->>U: Retorna HTTP 200 contendo o documento HTML renderizado do Passo 2
    deactivate V2

    %% SUBMISSÃO E PERSISTÊNCIA FINAL DO PASSO 2
    U->>V2: HTTP POST (dados do formulário 2 inseridos no corpo da requisição)
    activate V2
    V2->>F2: Instancia formulário passando o dicionário atual (request.POST)
    V2->>F2: Invoca método de validação .is_valid()
    activate F2
    F2-->>V2: Retorna True (Campos adicionais validados)
    deactivate F2
    
    V2->>S: Invoca salvar_passo_sessao(projeto_id, request.session, form.cleaned_data)
    activate S
    S->>SES: Grava dicionário estruturado: session['dados_edicao_2'] = cleaned_data
    SES-->>S: Confirmação de armazenamento
    S-->>V2: Retorno de execução bem-sucedida do método
    deactivate S

    V2->>S: Invoca salvar_no_banco(projeto_id, request.session)
    activate S
    S->>SES: Solicita a leitura das chaves 'dados_edicao_1' e 'dados_edicao_2'
    SES-->>S: Retorna os dicionários com todo o payload coletado nas duas telas
    S->>M: Executa consulta via API do Django ORM: Projeto.objects.get(id=projeto_id)
    M-->>S: Retorna a instância em memória do modelo de Projeto existente
    S->>S: Mescla e sobrescreve as propriedades do objeto com os valores extraídos da sessão
    S->>M: Dispara operação de escrita final: objeto_projeto.save()
    M-->>S: Confirmação de persistência no Banco de Dados (Execução do comando SQL UPDATE)
    S-->>V2: Retorno de sucesso da persistência em banco
    deactivate S

    V2->>S: Invoca limpar_sessao(projeto_id, request.session)
    activate S
    S->>SES: Executa o comando del para remover as chaves temporárias do escopo da sessão
    SES-->>S: Estrutura de dados limpa com sucesso
    S-->>V2: Retorno de encerramento do ciclo
    deactivate S
    
    V2-->>U: Retorna HTTP 302 Redirect para a URL 'projeto' (VisualizarProjetoView)
    deactivate V2
```

## Diagrama de Classes de Projeto

```mermaid
classDiagram
    class EditarProjetoPasso1View {
        +get(request: HttpRequest, projeto_id: int) HttpResponse
        +post(request: HttpRequest, projeto_id: int) HttpResponse
    }

    class EditarProjetoPasso2View {
        +get(request: HttpRequest, projeto_id: int) HttpResponse
        +post(request: HttpRequest, projeto_id: int) HttpResponse
    }

    class EditarProjetoPasso1Form {
        +cleaned_data: dict
        +is_valid() bool
    }

    class EditarProjetoPasso2Form {
        +cleaned_data: dict
        +is_valid() bool
    }

    class ProjetoService {
        +obter_dados_iniciais(projeto_id: int, session: HttpSession) dict
        +salvar_passo_sessao(projeto_id: int, session: HttpSession, cleaned_data: dict) void
        +salvar_no_banco(projeto_id: int, session: HttpSession) void
        +limpar_sessao(projeto_id: int, session: HttpSession) void
    }

    class Projeto {
        +id: int
        +titulo: str
        +descricao: str
        +plataforma: str
        +ano/semestre: str
        +colaboradores: int
        +contatos: str
        +orientador: str
        +categoria: str
        +categoria_secundaria: str
        +resumo: str
        +ferramentas_utilizadas: str
        +repositorio: str
        +status: enum
        +imagem: str
        +save() void
    }

    %% Relacionamentos de Dependência e Uso
    EditarProjetoPasso1View ..> EditarProjetoPasso1Form : "Instancia e Valida"
    EditarProjetoPasso2View ..> EditarProjetoPasso2Form : "Instancia e Valida"
    
    EditarProjetoPasso1View --> ProjetoService : "Invoca Lógica"
    EditarProjetoPasso2View --> ProjetoService : "Invoca Lógica"
    
    ProjetoService --> Projeto : "Consulta e Modifica (ORM)"
