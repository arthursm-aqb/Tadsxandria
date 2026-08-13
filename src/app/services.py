from app.models import(
    Projeto, Categoria, Tecnologia, Usuario,
    Orientando, Orientador, Participacao,
    OrientadorProjeto, PLATAFORMA, STATUS
)
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from datetime import datetime
from django.db import transaction
from django.db.models import Count, Q
from django.contrib.auth import authenticate

class ListarProjetosMaisAvaliadosService:

    @staticmethod
    def executar(limit):  # 3 projetos pros cards
        return (
            Projeto.objects
            .annotate(
                total_avaliacoes=Count("avaliacao")  # Conta a quantidade de avaliações de cada projeto
            )
            .order_by("-total_avaliacoes")  # Ordena do que tem MAIS avaliações para o que tem MENOS
        )[:limit]  # Top 3


class CategoriaService:

    @staticmethod
    def listarcategorias():
        """Nomes das categorias (usado no formulário de cadastro de projeto)."""
        return list(Categoria.objects.values_list('nome', flat=True))

    @staticmethod
    def listar_categorias():
        """Objetos Categoria completos (usado nos filtros de pesquisa)."""
        return Categoria.objects.all()


class OrientandoService:

    @staticmethod
    def listarorientandos():
        return list(Orientando.objects.values_list('email', flat=True))


class PlataformaService:

    @staticmethod
    def listarplataformas():
        return [{"valor": valor, "rotulo": rotulo} for valor, rotulo in PLATAFORMA]

    @staticmethod
    def listar_plataformas():
        return PlataformaService.listarplataformas()


class StatusService:
    @staticmethod
    def listar_status():
        return [{"valor": valor, "rotulo": rotulo} for valor, rotulo in STATUS]


class TecnologiaService:
    @staticmethod
    def listar_tecnologias():
        return Tecnologia.objects.all()


class CadastrarProjetoService:
    def __init__(self, titulo, plataforma, data_criacao, colaboradores, orientador, categoria):
        self.titulo = titulo
        self.plataforma = plataforma
        self.data_criacao = data_criacao
        self.colaboradores = list(colaboradores.split(", "))
        self.orientador = orientador
        self.categoria = categoria

    def colocarOrientadores(self, projeto, erros):
        if Orientador.objects.filter(email=self.orientador).exists():
            try:
                orientadorproj = OrientadorProjeto(
                    orientador=Orientador.objects.get(email=self.orientador),
                    projeto=projeto,
                    participacao=True,
                )
                orientadorproj.save()
            except Exception:
                erros["erro_orientador"] = "Houve um erro ao cadastrar o orientador"
        else:
            erros["erro_orientador"] = "O projeto precisa de um orientador!"

    def criarParticipacoes(self, projeto, erros):
        if self.colaboradores:
            try:
                for orientando in self.colaboradores:
                    if Orientando.objects.filter(email=orientando).exists():
                        participacao = Participacao(
                            orientando=Orientando.objects.get(email=orientando),
                            projeto=projeto,
                            participacao=True,
                        )
                        participacao.save()
            except Exception:
                erros["erro_colaboradores"] = "Houve um erro ao cadastrar os orientandos"
        else:
            erros["erro_colaboradores"] = "O projeto precisa no mínimo de um colaborador!!"

    def criarProjeto(self):
        erros = {}

        if Projeto.objects.filter(titulo=self.titulo).exists():
            erros["erro_titulo"] = "Projeto já cadastrado."

        if len(self.titulo) <= 1:
            erros["erro_titulo"] = "Um projeto deve ter mais de uma letra."

        try:
            self.data_criacao = datetime.strptime(self.data_criacao, "%d/%m/%Y")
        except Exception:
            erros["erro_data_criacao"] = "A data informada é inválida ou não existe."

        if isinstance(self.data_criacao, datetime) and self.data_criacao > datetime.now():
            erros["erro_data_criacao"] = "A data informada é inválida ou não existe."

        if Categoria.objects.filter(nome=self.categoria).exists():
            self.categoria = Categoria.objects.get(nome=self.categoria)
        else:
            if len(self.categoria) <= 3:
                erros["erro_categoria"] = "Escreva o nome de uma categoria com no mínimo 4 letras."
            nova_categoria = Categoria(nome=self.categoria)
            nova_categoria.save()
            self.categoria = nova_categoria

        projeto = Projeto(
            titulo=self.titulo,
            plataforma=self.plataforma,
            data_criacao=self.data_criacao,
            data_publicacao=datetime.now(),
            categoria_principal=self.categoria,
        )

        with transaction.atomic():
            projeto.save()

            self.criarParticipacoes(projeto, erros)
            self.colocarOrientadores(projeto, erros)

            if erros:
                raise ValueError(erros)

        return projeto


class ProjetoService:
    @staticmethod
    def buscarProjeto(pk):

        projeto = get_object_or_404(Projeto, pk=pk)

        categorias = list(projeto.categorias_secundarias.all()) + [projeto.categoria_principal]

        projetoSimilares = (
            Projeto.objects.filter(
                Q(categoria_principal__in=categorias)
                | Q(categorias_secundarias__in=categorias)
            )
            .exclude(pk=pk)
            .distinct()
        )

        orientador = get_object_or_404(
            OrientadorProjeto, projeto=projeto, participacao=True
        )

        orientandos = Participacao.objects.filter(projeto=projeto)

        return {
            "projeto": projeto,
            "projetos_similares": projetoSimilares,
            "orientador": orientador,
            "orientandos": orientandos,
        }

    @staticmethod
    def obter_dados_iniciais(projeto_id, session):
        projeto = get_object_or_404(Projeto, id=projeto_id)
        
        if f'editar_projeto_{projeto_id}' not in session:
            session[f'editar_projeto_{projeto_id}'] = {
                'titulo': projeto.titulo,
                'plataforma': projeto.plataforma,
                'ano_semestre': projeto.ano_semestre,
                'colaboradores': projeto.colaboradores,
                'contatos': projeto.contatos,
                'orientador': projeto.orientador,
                'categoria': projeto.categoria_principal.nome if projeto.categoria_principal else None,
                'categorias_secundarias': list(projeto.categorias_secundarias.values_list('nome', flat=True)),
                'resumo': projeto.resumo,
                'descricao': projeto.descricao,
                'tecnologias': list(projeto.tecnologias.values_list('nome', flat=True)),
                'repositorio': projeto.repositorio,
                'status': projeto.status,
            }
        return session[f'editar_projeto_{projeto_id}']

    @staticmethod
    def salvar_passo_sessao(projeto_id, session, dados_passo):
        dados_atuais = ProjetoService.obter_dados_iniciais(projeto_id, session)
        dados_atuais.update(dados_passo)
        session[f'editar_projeto_{projeto_id}'] = dados_atuais
        session.modified = True

    @staticmethod
    def salvar_no_banco(projeto_id, session):
        from .models import Categoria, Tecnologia
        projeto = get_object_or_404(Projeto, id=projeto_id)
        dados_sessao = session.get(f'editar_projeto_{projeto_id}')
        
        if dados_sessao:
            nome_cat = dados_sessao.pop('categoria', None)
            nome_sec = dados_sessao.pop('categorias_secundarias', None)
            lista_tecnologias = dados_sessao.pop('tecnologias', None)
            if nome_cat:
                categoria_obj, _ = Categoria.objects.get_or_create(nome=nome_cat)
                projeto.categoria_principal = categoria_obj
            for campo, valor in dados_sessao.items():
                if hasattr(projeto, campo):
                    setattr(projeto, campo, valor)
            projeto.save()
            if nome_sec:
                cat_sec_objs, _ = Categoria.objects.get_or_create(nome__in=nome_sec)
                projeto.categorias_secundarias.set(cat_sec_objs)
            if lista_tecnologias:
                if isinstance(lista_tecnologias, str):
                    lista_tecnologias = [t.strip() for t in lista_tecnologias.split()]
                tecnologias_objs = [Tecnologia.objects.get_or_create(nome=nome)[0] for nome in lista_tecnologias]
                projeto.tecnologias.set(tecnologias_objs)
            del session[f'editar_projeto_{projeto_id}']

    @staticmethod
    def limpar_sessao(projeto_id, session):
        if f'editar_projeto_{projeto_id}' in session:
            del session[f'editar_projeto_{projeto_id}']

    @staticmethod
    def validar_titulo_unico(projeto_id, titulo_novo):
        if Projeto.objects.filter(titulo=titulo_novo).exclude(id=projeto_id).exists():
            raise ValidationError("Já existe um projeto com este título. Por favor, escolha outro título.")

class CadastrarUsuarioService:
    def __init__(self, nome, email, senha, tipoPessoa):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.tipoPessoa = tipoPessoa

    def ultimaValidacao(self):
        if Usuario.objects.filter(email=self.email).exists():
            raise ValueError("Email já cadastrado")

        return self.criarUsuario()

    def criarUsuario(self):
        if self.tipoPessoa == "Professor":
            usuario = Orientador(nome=self.nome, email=self.email)
        elif self.tipoPessoa == "Aluno":
            usuario = Orientando(nome=self.nome, email=self.email)
        else:
            usuario = Usuario(nome=self.nome, email=self.email)

        usuario.set_password(self.senha)
        usuario.save()

        return usuario


class PesquisarProjetosService:
    def __init__(self, titulo):
        self.titulo = titulo

    def pesquisarProjeto(
        termos="",
        indice="todos",
        categorias_selecionadas=None,
        plataformas_selecionadas=None,
        status_selecionados=None,
        tecnologias_selecionadas=None,
        sort="recentes",
    ):

        categorias_selecionadas = categorias_selecionadas or []
        plataformas_selecionadas = plataformas_selecionadas or []
        status_selecionados = status_selecionados or []
        tecnologias_selecionadas = tecnologias_selecionadas or []

        projetos = Projeto.objects.all()

        termos = (termos or "").strip()
        if termos:
            if indice == "titulo":
                projetos = projetos.filter(titulo__icontains=termos)
            elif indice == "descricao":
                projetos = projetos.filter(descricao__icontains=termos)
            else:  # "todos" -> título OU descricao
                projetos = projetos.filter(
                    Q(titulo__icontains=termos) | Q(descricao__icontains=termos)
                )

        if categorias_selecionadas:
            projetos = projetos.filter(
                Q(categoria_principal_id__in=categorias_selecionadas)
                | Q(categorias_secundarias__id__in=categorias_selecionadas)
            )

        if plataformas_selecionadas:
            projetos = projetos.filter(plataforma__in=plataformas_selecionadas)

        if status_selecionados:
            projetos = projetos.filter(status__in=status_selecionados)

        if tecnologias_selecionadas:
            projetos = projetos.filter(tecnologias__id__in=tecnologias_selecionadas)

        projetos = projetos.distinct()

        projetos = PesquisarProjetosService._ordenar(projetos, sort)

        return projetos

    @staticmethod
    def _ordenar(projetos, sort):
        if sort == "antigos":
            return projetos.order_by("data_publicacao")
        if sort == "relevancia":
            return projetos.order_by("-avaliacao", "-data_publicacao")
        return projetos.order_by("-data_publicacao")  # "recentes" (padrão)


class LoginUsuarioService:
    def __init__(self, request, email, senha):
        self.request = request
        self.email = email
        self.senha = senha

    def getSenha(self):
        usuario = authenticate(
            request=self.request,
            email=self.email,
            password=self.senha,
        )
        if usuario is None:
            raise ValueError("Email ou senha inválidos")
        return usuario
