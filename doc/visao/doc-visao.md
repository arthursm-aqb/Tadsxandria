# Documento de Visão

## Histórico de Revisões

| Data | Versão | Descrição | Autores |
| :--: | :----: | :-------: | ------- |
| 07/04/2026 | 1.0 | Versão inicial |  Ana Barbosa, Gustavo Dias, Miguel Rodrigues, Raquel Martiniano |
| 25/04/2026 | 1.1 | Versão com correções no documento de visão nos tópicos 2, 3, 7 e 8 |  Ana Barbosa, Gustavo Dias, Miguel Rodrigues, Raquel Martiniano, Arthur da Silva Mariz, Erick Job e Beatriz Barbosa |
| 06/05/2026 | 1.2 | Versão com correções no documento de visão no tópico 8 |  Ana Barbosa, Gustavo Dias, Miguel Rodrigues, Raquel Martiniano, Arthur da Silva Mariz, Arthur Fontenele, Erick Job e Beatriz Barbosa |
| 04/06/2026 | 1.3 | Versão com correções no documento de visão no tópico 8 |  Ana Barbosa, Gustavo Dias, Miguel Rodrigues, Raquel Martiniano, Arthur da Silva Mariz, Arthur Fontenele, Erick Job e Beatriz Barbosa |



## 1. Visão Geral do Sistema Proposto

A nossa proposta é criar um sistema web que funcione como um repositório público dos trabalhos e projetos desenvolvidos pelos discentes do curso de TADS da DIATINF, beneficiando a comunidade acadêmica ao permitir guardar e pesquisar sobre os PDS's e TCC's já produzidos pelos alunos do curso.

## 2. Descrição do Problema
| | |
| :-: | --- |
| **Problema** | Na atualidade, no curso de TADS da DIATINF IFRN-CNAT, nota-se que não existe algum meio de preservar os PDS e TCC's dos discentes. |
| **Afeta** | Afeta a comunidade de TADS DIATINF IFRN ao não permitir revisitar esses trabalhos e fadá-los ao esquecimento. |  
| **Impacta** | Impacta os alunos de TADS ao superar o imbróglio existente ao oferecer modos para depositar, salvar, compartilhar e visualizar os projetos PDS e TCC. |
| **Solução** | A implementação de um sistema web que funcione como repositório público para trabalhos e projetos desenvolvidos pelos discentes do curso de TADS da DIATINF solucionaria esse problema e proporcionaria o acesso ao conhecimento e a perpetuação desses projetos. |

## 3. Descrição dos Usuários 

| Usuário | Descrição | Responsabilidades |
| :----- | :------- | :-------------- |
| Visitante | Usuário não autenticado que explora os conteúdos públicos do sistema de forma restrita | <br>- Pesquisar por projetos <br>- Visualizar informações superficiais na tela de detalhamento dos projetos <br>- Compartilhar projetos <br> - Navegar pelo sistema com acesso restrito às funcionalidades |
| Comum | Usuário autenticado que possui acesso total às funcionalidades de navegação da plataforma | <br>- Visualizar informações superficiais na tela de detalhamento dos projetos  <br>- Baixar a documentação dos projetos em PDF <br>- Ler a documentação dos projetos pelo navegador <br>- Comentar na página de um projeto e avaliá-lo <br>- Contribuir em projetos <br>- Compartilhar projetos via link <br>- Acessar e gerenciar seu perfil de usuário |
| Orientando | Usuário autenticado que possui acesso total às funconalidades de navegação e restrito das de gerência de projetos | <br>- Visualizar informações superficiais na tela de detalhamento dos projetos <br>- Baixar a documentação dos projetos em PDF <br>- Ler a documentação dos projetos pelo navegador <br>- Comentar na página de um projeto e avaliá-lo <br>- Contribuir em projetos <br>- Compartilhar projetos via link <br>- Acessar e gerenciar seu perfil de usuário <br>- Acessar o painel de gerenciamento de projetos <br>- Editar, de forma limitada, os dados dos projetos dos quais participa |
| Orientador | Usuário autenticado que possui acesso total às funconalidades de navegação e de gerência de projetos | <br>- Visualizar informações superficiais na tela de detalhamento dos projetos <br>- Baixar a documentação dos projetos em PDF <br>- Ler a documentação dos projetos pelo navegador <br>- Comentar na página de um projeto e avaliá-lo <br>- Compartilhar projetos via link <br>- Acessar e gerenciar seu perfil de usuário <br>- Acessar o painel de gerenciamento de projetos <br>- Submeter projetos à plataforma <br>- Atribuir usuários comuns/Orientandos aos seus projetos <br>- Editar integralmente os dados dos projetos dos quais participa |
| Administrador | Usuário responsável pela organização, moderação e manutenção da plataforma. | <br>- Ter acesso integral a todos os projetos <br>- Gerenciar usuários cadastrados <br>- Gerenciar projetos (editar, excluir, moderar)|

## 4. Descrição do Ambiente dos Usuários

O ambiente pode ser acessado publicamente pelos usuários, necessitando apenas de um dispositivo móvel ou computador com acesso à internet e um navegador web (_browser_). Os usuários podem acessar certas funcionalidades de acordo com seu perfil. Muitas ações demandam poucos minutos para serem executadas, como avaliar projetos, publicar ideias, visualizar participações de projetos, entre outros.

## 5. Principais Necessidades dos Usuários

<!--  Apresentadas no formato de tópicos -->

1. **Dificuldade em encontrar projetos anteriores**
   - Muitos professores e alunos têm dificuldade em localizar projetos já desenvolvidos, como PDS, TCC e projetos integradores
   - Falta de um local centralizado para busca desses projetos

2. **Perda de projetos ao longo do tempo**
   - Projetos acabam se perdendo por falta de armazenamento adequado
   - Dificuldade em manter um histórico acessível dos trabalhos desenvolvidos

3. **Dificuldade em saber se uma ideia já foi desenvolvida**
   - Alunos podem desenvolver projetos semelhantes sem saber que já existem
   - Falta de informação sobre projetos anteriores e seus autores

## 6. Alternativas Concorrentes

1. **Memória IFRN**
   - Manter: Ferramenta que possibilita aumentar e diminuir o tamanho das letras.
   - Distanciar: Ineficiência da aba de “ajuda”.

2. **GitHub**
   - Manter: Sistema de colaboração: comentários, likes, seguir.
   - Distanciar: Interface complexa para iniciantes.

3. **Google Acadêmico**
   - Manter: Opção de salvar um conteúdo para visualizar depois.
   - Distanciar: Sem opção para temas do fundo.

4. **Repositório UFRN**
   - Manter: Opção de trocar o tema da página.
   - Distanciar: Disponibilização de arquivos apenas em PDF.

## 7. Regras de Negócio

| ID  | Regra | Descrição |
| :-: | ----- | --------- |
| RN01 | Critério de Recomendações | O sistema deve recomendar projetos aos usuários com base na quantidade de estrelas e nas categorias e subcategorias dos conteúdos. |
| RN02 | Permissões de Administrador | Os usuários com perfil de administrador devem ter acesso a todas as funcionalidades do sistema. |
| RN03 | Publicação de Projetos | Os projetos, antes de serem disponibilizados publicamente no sistema, devem ser aprovados por um administrador. |
| RN04 | Status de Progresso | Os projetos devem possuir um status indicando seu progresso (ex: Em andamento, Descontinuado, Finalizado). |
| RN05 | Validação de arquivos | Apenas documentos e imagens vinculados ao projeto que possuam formato e tamanho permitidos podem ser enviados (ex: .PNG e .JPG de até 10MB). |
| RN06 | Orientação Obrigatória | Todo projeto deve ter pelo menos um Orientador vinculado. |
| RN07 | Permissões de Orientando | Os usuários com perfil de Orientando devem ter acesso restrito às funcionalidades de gerenciamento de projetos. |
| RN08 | Autenticação | Certas funcionalidades do sistema devem exigir a autenticação do usuário. |
| RN09 | Equipe Obrigatória | Todo projeto deve ter pelo menos um Orientando vinculado para ser publicado. |
| RN10 | Histórico do Projeto | O histórico de versões do projeto deve estar disponível para visualização. |
| RN11 | Fases do Projeto | Um projeto pode ter diferentes fases, como `Dev. Web` e `Dev. Distríbuido` |
| RN12 | Criterio de Avaliação Pública | A avaliação pública é uma nota de 0 até 5. A avaliação pública geral considera a seguinte média ponderada: $\frac{\sum (\text{Nota} \times \text{Quantidade de Avaliações})}{\text{Total de Avaliações}}$ |
| RN13 | Tecnologias Obrigatórias | Projetos de desenvolvimento de sistemas devem ter pelo menos uma tecnologia vinculada, como Python, TypeScript, PostgreSQL, entre outras. |
| RN14 | Disponibilidade de Filtros | A ferramenta de pesquisa deve possuir múltiplos filtros. |

## 8. Requisitos Funcionais

| Código | Nome | Usuário | Descrição | Prioridade |
| :----: | ---- | ------- | ---------- | ---------- |
| RF01 | Cadastrar conta | Visitante | Usuário poderá cadastrar uma conta no site. | Alta |
| RF02 | Login | Visitante | O usuário pode acessar o formulário de _login_ e preencher as informações, email e senha, para entrar no sistema. | Alta |
| RF03 | Compartilhar projeto | TODOS | Usuário poderá compartilhar projetos via link. | Baixa |
| RF04 | Editar projeto | Orientado, Orientador | O usuário pode editar e adicionar novas informações ao projeto. | Alta |
| RF05 | Filtro de pesquisas | TODOS | O usuário vai poder listar projetos por diversos critérios por meio de filtros. | Médio |
| RF06 | Comentar | Comum, Orientado e Orientador | O usuário é capaz de comentar na aba de comentários de uma página de projeto. | Baixa |
| RF07 | Dar avaliação | Comum, Orientado, Orientador | O usuário é capaz de avaliar os projetos em até 5 estrelas. Quanto maior o número de estrelar, mais satisfatório foi o projeto para o usuário. | Médio |
| RF08 | Acessar Projetos Recentes | TODOS | O usuário é capaz de acessar a aba recentes e listar os projetos mais recentes lançados no sistema. | Baixa |
| RF09 | Modo escuro | TODOS | O usuário é capaz de alterar a interface para o modo escuro para ajustar melhor na visão. | Baixa |
| RF10 | Recuperar senha | Comum, Orientado, Orientador | O usuário é capaz de recuperar a senha, inserindo e confirmando uma nova senha. | Alto |
| RF11 | Favoritar projetos | Comum, Orientando, Orientador | O usuário poderá favoritar os seus projetos já cadastrados no site, o que mais se interessou ou gostou, mantendo os projetos favoritos salvo na conta do usuário. | Média |
| RF12 | Baixar documentação do projeto | Comum, Orientado e Orientador | O usuário poderá baixar a documentação do projeto específico em PDF no site. | Média |
| RF13 | Ler documentação do projeto | Comum, Orientado e Orientador | O usuário poderá acessar a documentação de um projeto específico pelo navegador. | Média |
| RF14 | Mudar o contraste  | TODOS | O usuário poderá selecionar a opção da mudança da cor de fundo do site de modo contraste para a cor mais escura. | Baixa |
| RF15 | Mudar tamanho da fonte  | TODOS | O usuário poderá selecionar a mudança do tamanho da letra, para facilitar a leitura, caso esteja muito grande ou pequena. | Baixa |
| RF16 | Acessar meu perfil | Comum, Orientado e Orientador | O usuário poderá acessar seu perfil de usuário, editar informações e estética. | Baixa |
| RF17 | Acessar perfis de usuários | TODOS | O usuário poderá acessar o perfil de outros usuários e ver quais projetos tal colaborou. | Baixa |
| RF18 | Pesquisar projetos | TODOS | O usuário pode acessar a página de busca e procurar projetos com a barra de pesquisa e filtros cadastrados no sistema. | Alta |
| RF19 | Listar projetos mais avaliados | TODOS | O usuário pode acessar na página inicial uma lista com os projetos mais avaliados no sistema | Alta |
| RF20 | Visualizar Projeto | TODOS | O usuário pode abrir a página de um projeto específico para visualizar metadados e sintese dele. | Alta |
| RF21 | Configurações de conta | Comum, Orientado e Orientador  | O usuário pode acessar a página de configurações de conta e alterar seus dados. | Baixa |
| RF22 | Alterar nome público | Comum, Orientado e Orientador  | O usuário pode acessar a página de configurações de conta e alterar seu nome público. | Baixa |
| RF23 | Alterar senha | Comum, Orientado e Orientador  | O usuário pode acessar a página de configurações de conta e alterar sua senha atual. | Baixa |
| RF24 | Alterar e-mail | Comum, Orientado e Orientador  | O usuário pode acessar a página de configurações de conta e alterar seu e-mail atual. | Baixa |
| RF25 | Acessar página de ajuda | TODOS | O usuário pode acessar a página de Ajuda e visualizar as dúvidas mais comuns sobre o sistema. | Baixa |
| RF26 | Acessar página de contato | TODOS | O usuário pode acessar a página de Contato e ter acesso aos dados de contato da equipe do sistema. | Baixa |
| RF27 | Enviar Mensagem de Contato | TODOS | O usuário pode acessar a página de Contato e enviar mensagens, dúvidas ou sugestões preenchendo um formulário. | Baixa |
| RF28 | Alterar orientação | Orientador | O usuário pode transferir seu papel de orientador em um projeto para outro orientador | Alta |


<!--  **Prioridade**: alta, média ou baixa -->

## 9. Requisitos Não-funcionais

| Código | Nome | Descrição | Categoria | Classificação |
| :----: | ---- | --------- | --------- | ------------- |
| RNF01 | Framework Django | Para desenvolvimento do projeto, deve ser utilizado o framework de desenvolvimento web Django, que utiliza a linguagem de programação Python | Implementação | Obrigatória |
| RNF02 | Arquitetura MTV | O código deve seguir os padrão da [arquitetura MTV](https://docs.djangoproject.com/en/6.0/faq/general/#django-appears-to-be-a-mvc-framework-but-you-call-the-controller-the-view-and-the-view-the-template-how-come-you-don-t-use-the-standard-names) do Django, baseada na [arquitetura MVC](https://pt.wikipedia.org/wiki/MVC) | Implementação | Obrigatório |
| RNF03 | Autenticação Necessária | O sistema deve exigir autenticação do usuário para determinadas ações | Segurança | Obrigatório |
| RNF04 | Disponibilidade | O sistema deve estar disponível durante todo o dia, com disponibilidade mensal de 99% do tempo. | Confiabilidade | Obrigatório |
| RNF05 | Fidelidade da Interface | A interface do sistema deve se manter consistente nos navegadores mais utilizados, como Google Chrome, Firefox, Microsoft Edge. | Usabilidade | Desejável | 
| RNF06 | Identificação do estado de desenvolvimento do projeto | Cada projeto deve informar o estado em que se encontra | Implementação | Obrigatório |
| RNF07 | Textos diretos | Por ter muita informação, o sistema deve dar clareza nas informações, não sendo poluído demais ao ponto do usuário não consiga processar bem as informações que precisava | interface | Desejável |

<!--
> **Categoria**: usabilidade, confiabilidade, performance, suportabilidade, restrição de projeto, implementação, interface e requisito físico - segundo classificação [FURP+](https://pt.wikipedia.org/wiki/FURPS).

> **Classificação**: desejável ou obrigatório.
-->
