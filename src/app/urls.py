from django.urls import path
from app import views

urlpatterns = [
    path('projeto/<int:projeto_id>/editar/passo-1/', views.EditarProjetoPasso1.as_view(), name='editar_projeto_passo1'),
    path('projeto/<int:projeto_id>/editar/passo-2/', views.EditarProjetoPasso2.as_view(), name='editar_projeto_passo2'),
    path('projeto/<int:projeto_id>/', views.Projeto.as_view(), name='projeto'),
]
