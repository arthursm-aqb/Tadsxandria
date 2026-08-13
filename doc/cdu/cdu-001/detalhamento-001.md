# CDU - Cadastro de Usuários

- **Ator principal**: Visitante
- **Resumo**: Permite ao visitante criar uma conta para acessar ao sistema.
- **Pré-condição**: Não ter conta no sistema e estar na página de criação de conta.
- **Pós-condição**: Visitante é redirecionado para a dashboard principal.

## Fluxo Principal

| Ações do ator | Ações do sistema |
| :-----------: | :--------------: |
| 1 - O visitante preenche os campos de nome, utilizador, e-mail, CPF e senha. | |
| | 2 - O sistema valida as informações e redireciona o visitante para a dashboard principal. |

## Fluxo de Exceção I - Dados Inválidos

| Ações do ator | Ações do sistema |
| :-----------: | :--------------: |
| 1.1 - O visitante preenche os campos de nome, utilizador, e-mail, CPF e senha. | |
| | 1.2 - O sistema identifica erros nos dados e exibe uma mensagem de erro, impedindo o registo. |

## Fluxo de Exceção II - Login com Google

| Ações do ator | Ações do sistema |
| :-----------: | :--------------: |
| 2.1 - O visitante clica no botão "Entrar com Google". | |
| | 2.2 - O sistema redireciona para o login do Google, valida e credencia o acesso. |
| 2.3 - O visitante é redirecionado para a página inicial, tornando-se um utilizador logado. | |

## Fluxo de Exceção III - Login com GitHub

| Ações do ator | Ações do sistema |
| :-----------: | :--------------: |
| 3.1 - O visitante clica no botão "Entrar com GitHub". | |
| | 3.2 - O sistema redireciona para o login do GitHub, valida e credencia o acesso. |
| 3.3 - O visitante é redirecionado para a página inicial, tornando-se um utilizador logado. | |

## Fluxo de Exceção IV - Login com SUAP

| Ações do ator | Ações do sistema |
| :-----------: | :--------------: |
| 4.1 - O visitante clica no botão "Entrar com SUAP". | |
| | 4.2 - O sistema redireciona para o login do SUAP, valida e credencia o acesso. |
| 4.3 - O visitante é redirecionado para a página inicial, tornando-se um utilizador logado.  | |
