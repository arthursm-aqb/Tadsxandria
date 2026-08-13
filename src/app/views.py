from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from .models import Usuario, Projeto
from .forms import EditarProjetoPasso1Form, EditarProjetoPasso2Form
from app.services import (
    CadastrarProjetoService,
    CadastrarUsuarioService,
    CategoriaService,
    ListarProjetosMaisAvaliadosService,
    LoginUsuarioService,
    OrientandoService,
    PesquisarProjetosService,
    PlataformaService,
    ProjetoService,
    StatusService,
    TecnologiaService,
)

class ListarProjetosMaisAvaliadosView(View):
    def get(self, request):  # metodo get pq o django negou o acesso da aplicação
        avaliacoes = ListarProjetosMaisAvaliadosService.executar(3)  # top 3 projetos mais avaliados

        return render(request, "app/index.html", {
            "avaliacoes": avaliacoes,
        })

class CadastrarProjetoView(View):

    def get_contexto_base(self):
        # Um método auxiliar para não repetir chamadas ao banco quando houver erro
        return {
            "categorias": CategoriaService.listarcategorias(),
            "orientandos": OrientandoService.listarorientandos(),
            "plataformas": PlataformaService.listarplataformas(),
        }

    def get(self, request):
        contexto = self.get_contexto_base()
        return render(request, "app/cadastrar_projeto.html", contexto)

    def post(self, request):

        dados = {
            "titulo": request.POST.get("titulo_proj"),
            "plataforma": request.POST.get("plataforma_proj"),
            "data_criacao": request.POST.get("data_criacao_proj"),
            "colaboradores": request.POST.get("colaboradores_proj"),
            "orientador": request.POST.get("orientador_proj"),
            "categoria": request.POST.get("categoria_proj"),
        }

        return self.validarCampos(request, dados)

    def enviarDados(self, dados):
        projeto = CadastrarProjetoService(
            dados["titulo"], dados["plataforma"], dados["data_criacao"],
            dados["colaboradores"], dados["orientador"], dados["categoria"]
        )
        proj = projeto.criarProjeto()
        return proj

    def validarCampos(self, request, dados):
        erros = {}

        if not dados["titulo"]:
            erros['erro_titulo'] = 'Preencha o campo do título'

        if not dados["plataforma"]:
            erros['erro_plataforma'] = 'Preencha o campo da plataforma'

        if not dados["data_criacao"]:
            erros['erro_data_criacao'] = 'Preencha o campo da data de criação'

        if not dados["colaboradores"]:
            erros['erro_colaboradores'] = 'Preencha o campo dos colaboradores'

        if not dados["orientador"]:
            erros['erro_orientador'] = 'Preencha o campo do orientador'

        if not dados["categoria"]:
            erros['erro_categoria'] = 'Preencha o campo da categoria'

        if erros:
            contexto = self.get_contexto_base()
            contexto["erros"] = erros
            contexto["dados_preenchidos"] = dados  # Para repopular os inputs e o usuário não perder o que já digitou

            return render(request, "app/cadastrar_projeto.html", contexto)

        try:
            projeto = self.enviarDados(dados)

            return redirect('editar_projeto_passo1', projeto_id=projeto.id)   # Redireciona para a página inicial após o cadastro bem-sucedido

        except ValueError as erro_service:
            contexto = self.get_contexto_base()
            detalhes_do_erro = erro_service.args[0]
            contexto["erros"] = detalhes_do_erro
            contexto["dados_preenchidos"] = dados
            return render(request, "app/cadastrar_projeto.html", contexto)


class LoginUsuarioView(View):
    campos = [
        {
            "label": "Email",
            "name": "email",
            "type": "email",
        },
        {
            "label": "Senha",
            "name": "senha",
            "type": "password",
        },
    ]

    entrada_formulario = {"campos": campos}

    def erro(self, request, mensagem):
        resposta = self.entrada_formulario.copy()
        resposta["erro"] = mensagem

        return render(request, "app/login.html", resposta)

    def get(self, request):
        return render(request, "app/login.html", self.entrada_formulario)

    def post(self, request):
        self.email = request.POST.get("email")
        self.senha = request.POST.get("senha")

        return self.enviar_dados(request)

    def enviar_dados(self, request):
        if not self.email:
            return self.erro(request, "Não pode estar vazio o email")
        if not self.senha:
            return self.erro(request, "Não pode estar vazia a senha")
        try:
            service = LoginUsuarioService(
                request, self.email, self.senha
            )
            usuario = service.getSenha()
            login(request, usuario)

        except ValueError as erro:
            resposta = self.entrada_formulario.copy()
            resposta["erro"] = str(erro)

            return render(request, "app/login.html", resposta)
        return redirect("index")


class VisualizarProjetoView(View):
    def get(self, request, pk):
        return self.visualizar_projeto(request, pk)

    def visualizar_projeto(self, request, pk):
        contexto = ProjetoService.buscarProjeto(pk)
        return render(request, "app/projeto.html", contexto)


class CadastrarUsuarioView(View):
    campos = [
        {"label": "Nome", "name": "nome", "type": "text", "observacao": None},
        {
            "label": "Email",
            "name": "email",
            "type": "email",
            "observacao": "Digite seu email completo. Ex: fulano01@email.com",
        },
        {
            "label": "Senha",
            "name": "senha",
            "type": "password",
            "observacao": "Senha de 8 caracteres, use números e símbolos. Ex: @, #, %",
        },
    ]

    tipos = [{"name": "Aluno"}, {"name": "Professor"}, {"name": "Comunidade Externa"}]

    entrada_formulario = {"campos": campos, "tipos": tipos}

    def erro(self, request, mensagem):
        resposta = self.entrada_formulario.copy()
        resposta["erro"] = mensagem

        return render(request, "app/cadastrar_conta.html", resposta)

    def get(self, request):  # exibo enquanto não recebo os dados enviado
        return render(request, "app/cadastrar_conta.html", self.entrada_formulario)

    def post(self, request):
        self.nome = request.POST.get("nome")
        self.email = request.POST.get("email")
        self.senha = request.POST.get("senha")
        self.tipoPessoa = request.POST.get("tipoPessoa")

        return self.validarDados(request)

    def validarDados(self, request):
        if not self.nome:
            return self.erro(request, "Não pode estar vazio o nome")

        if not self.email:
            return self.erro(request, "Não pode estar vazio o email")

        if not self.senha:
            return self.erro(request, "Não pode estar vazia a senha")

        if not self.tipoPessoa:
            return self.erro(request, "Tem que ter pelo menos uma categoria marcada")

        try:
            service = CadastrarUsuarioService(
                self.nome, self.email, self.senha, self.tipoPessoa
            )
            service.ultimaValidacao()

        except ValueError as erro:
            resposta = self.entrada_formulario.copy()
            resposta["erro"] = str(erro)

            return render(request, "app/cadastrar_conta.html", resposta)

        nomeUsuario = {"nome": self.nome}
        return render(request, "app/cadastrou.html", nomeUsuario)

class PesquisarProjetosView(View):
    def get(self, request):
        termos = request.GET.get("q", "")
        indice = request.GET.get("indice", "todos")
        sort = request.GET.get("sort", "recentes")

        categorias = request.GET.getlist("categoria")
        plataformas = request.GET.getlist("plataforma")
        status = request.GET.getlist("status")
        tecnologias = request.GET.getlist("tecnologia")

        projetos = PesquisarProjetosService.pesquisarProjeto(
            termos=termos,
            indice=indice,
            categorias_selecionadas=categorias,
            plataformas_selecionadas=plataformas,
            status_selecionados=status,
            tecnologias_selecionadas=tecnologias,
            sort=sort,
        )

        return render(
            request,
            "app/pesquisar_projetos.html",
            {
                "projetos": projetos,
                "categorias": CategoriaService.listar_categorias(),
                "plataformas": PlataformaService.listar_plataformas(),
                "status": StatusService.listar_status(),
                "tecnologias": TecnologiaService.listar_tecnologias(),

                # importante para manter os filtros marcados
                "categorias_selecionadas": categorias,
                "plataformas_selecionadas": plataformas,
                "status_selecionados": status,
                "tecnologias_selecionadas": tecnologias,
            },
        )

class EditarProjetoPasso1View(View):
    def get(self, request, projeto_id):
        dados_projeto = ProjetoService.obter_dados_iniciais(projeto_id, request.session)
        form = EditarProjetoPasso1Form(initial=dados_projeto)
        
        if request.user.is_authenticated and request.user.groups.filter(name='Orientadores').exists():
            template_nome = 'app/editar_projeto_orientador_um.html'
        else:
            template_nome = 'app/editar_projeto_orientado_um.html'
            
        return render(request, template_nome, {'form': form, 'projeto_id': projeto_id})

    def post(self, request, projeto_id):
        if 'cancelar' in request.POST:
            ProjetoService.limpar_sessao(projeto_id, request.session)
            return redirect('projeto', pk=projeto_id)
            
        form = EditarProjetoPasso1Form(request.POST)
        if form.is_valid():
            ProjetoService.salvar_passo_sessao(projeto_id, request.session, form.cleaned_data)
            
            if 'salvar' in request.POST:
                ProjetoService.salvar_no_banco(projeto_id, request.session)
                return redirect('projeto', pk=projeto_id)
                
            elif 'avancar' in request.POST:
                return redirect('editar_projeto_passo2', projeto_id=projeto_id)
                
        if request.user.is_authenticated and request.user.groups.filter(name='Orientadores').exists():
            template_nome = 'app/editar_projeto_orientador_um.html'
        else:
            template_nome = 'app/editar_projeto_orientado_um.html'
        return render(request, template_nome, {'form': form, 'projeto_id': projeto_id})


class EditarProjetoPasso2View(View):
    def get(self, request, projeto_id):
        dados_projeto = ProjetoService.obter_dados_iniciais(projeto_id, request.session)
        form = EditarProjetoPasso2Form(initial=dados_projeto)
        
        if request.user.is_authenticated and request.user.groups.filter(name='Orientadores').exists():
            template_nome = 'app/editar_projeto_orientador_dois.html'
        else:
            template_nome = 'app/editar_projeto_orientado_dois.html'
            
        return render(request, template_nome, {'form': form, 'projeto_id': projeto_id})

    def post(self, request, projeto_id):
        if 'cancelar' in request.POST:
            ProjetoService.limpar_sessao(projeto_id, request.session)
            return redirect('projeto', pk=projeto_id)
            
        form = EditarProjetoPasso2Form(request.POST)
        if form.is_valid():
            ProjetoService.salvar_passo_sessao(projeto_id, request.session, form.cleaned_data)
            
            if 'voltar' in request.POST:
                return redirect('editar_projeto_passo1', projeto_id=projeto_id)
                
            elif 'salvar' in request.POST:
                ProjetoService.salvar_no_banco(projeto_id, request.session)
                return redirect('projeto', pk=projeto_id)
                
        if request.user.is_authenticated and request.user.groups.filter(name='Orientadores').exists():
            template_nome = 'app/editar_projeto_orientador_dois.html'
        else:
            template_nome = 'app/editar_projeto_orientado_dois.html'
        return render(request, template_nome, {'form': form, 'projeto_id': projeto_id})