from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from app import views
from django.conf import settings
from django.conf.urls.static import static
from app.views import ListarProjetosMaisAvaliadosView #importei

urlpatterns = [
    path("", ListarProjetosMaisAvaliadosView.as_view(), name="index"),
    path(
        "login/", 
         views.LoginUsuarioView.as_view(), 
         name="login",
    ),
    path(
        "cadastrar_conta/",
        views.CadastrarUsuarioView.as_view(),
        name="cadastrar_conta",
    ),
    path(
        "cadastrar_projeto/",
        views.CadastrarProjetoView.as_view(),
        name="cadastrar_projeto",
    ),
    path(
        "pesquisar_projetos/",
        views.PesquisarProjetosView.as_view(),
        name="pesquisar_projetos",
    ),
    path(
        "projeto/<int:projeto_id>/editar/passo1/",
        views.EditarProjetoPasso1View.as_view(),
        name="editar_projeto_passo1",
    ),
    path(
        "projeto/<int:projeto_id>/editar/passo2/",
        views.EditarProjetoPasso2View.as_view(),
        name="editar_projeto_passo2",
    ),
    path(
        "projeto/<int:pk>/",
        views.VisualizarProjetoView.as_view(),
        name="projeto",
    ),
    path("admin/", admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
