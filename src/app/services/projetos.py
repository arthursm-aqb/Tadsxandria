from models import Projeto, Orientador, Orientando, Participacao, OrientadorProjeto, Categoria

class CadastrarProjetoService:

    @staticmethod
    def criarProjeto():
        
        projeto = Projeto(
            titulo = titulo,
            plataforma = plataforma,
            data_criacao = data_criacao,
            categoria = Categoria.objects.get(id=categoria)
        )
        projeto.save()

        for i in orientandos:
            participacao = Participacao(
                orientando = Orientando.objects.get(i),
                projeto = projeto,
                participacao = True,
            )
            participacao.save()

        for i in orientadores:
            orientadorproj = OrientadorProjetooj(
                orientador = Orientador.objects.get(i),
                projeto = projeto,
                OrientadorProjeto = True,
            )
            orientadorproj.save()

        return projeto
