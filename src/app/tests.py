from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from app.models import Projeto, Categoria, Usuario, Tecnologia
from django.contrib.auth import get_user_model

class EditarProjetoViewsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        UserModelo = get_model = get_user_model()
        self.usuario = UserModelo.objects.create_user(email='testuser@example.com', password='12345')
        from django.contrib.auth.models import Group
        self.grupo_orientadores, _ = Group.objects.get_or_create(name='Orientadores')
        self.usuario.groups.add(self.grupo_orientadores)
        self.client.login(email='testuser@example.com', password='12345')
        
        self.cat = Categoria.objects.create(nome="Desenvolvimento")
        
        self.projeto = Projeto.objects.create(
            titulo="Projeto Inicial",
            plataforma="web",             
            ano_semestre="2026.1",
            colaboradores="João, Maria",
            orientador="Prof. Carlos",
            categoria_principal=self.cat,         
            resumo="Resumo antigo com mais de vinte caracteres...",
            descricao="Descrição antiga",
            repositorio="https://github.com/teste",
            status="andamento",                    
            fase="web",                           
            data_criacao=timezone.now(),         
            data_publicacao=timezone.now()        
        )
        self.url_passo1 = reverse('editar_projeto_passo1', args=[self.projeto.id])
        self.url_passo2 = reverse('editar_projeto_passo2', args=[self.projeto.id])
        self.url_projeto = reverse('projeto', args=[self.projeto.id])

    def test_clique_avancar_pagina_1_salva_na_sessao(self):
        """Testa se preencher a página 1 e clicar em Avançar joga os dados na Session."""
        dados_formulario = {
            'avancar': '',
            'titulo': "Projeto Alterado",
            'plataforma': "web",
            'ano_semestre': "2026.2",
            'colaboradores': "João, Maria, José",
            'orientador': "Prof. Carlos",
            'categoria': "Desenvolvimento",
            'categoria_secundaria': "Qualquer uma",
            'fase': 'web',
            'resumo': 'Resumo novo com mais de vinte caracteres...',
            'data_criacao': timezone.now(),
            'data_publicacao': timezone.now(),
            'contatos': "contato@example.com",
            'tecnologias': "Python, Django"
        }
        
        response = self.client.post(self.url_passo1, data=dados_formulario)

        self.assertRedirects(response, self.url_passo2)
        
        sessao = self.client.session
        chave_projeto = f'editar_projeto_{self.projeto.id}'
        self.assertIn(chave_projeto, sessao)
        self.assertEqual(sessao[chave_projeto]['titulo'], "Projeto Alterado")

    def test_salva_banco(self):
        """Testa se preencher a página 1 e clicar em Salvar já grava direto no Banco."""
        dados_formulario = {
            'salvar': '', 
            'titulo': "Título Definitivo Passo 1",
            'plataforma': "web",
            'ano_semestre': "2026.1",
            'colaboradores': "João",
            'orientador': "Prof. Carlos",
            'categoria': "Desenvolvimento",
            'categoria_secundaria': "Qualquer uma",
            'fase': 'web',
            'resumo': 'Resumo definitivo com tamanho suficiente...',
            'data_criacao': timezone.now(),
            'data_publicacao': timezone.now(),
            'contatos': "contato@exemplo.com",
            'tecnologias': "Python, Django"
        }
        
        response = self.client.post(self.url_passo1, data=dados_formulario)
        
        self.projeto.refresh_from_db()
        
        self.assertEqual(self.projeto.titulo, "Título Definitivo Passo 1")
        
        self.assertNotIn(f'editar_projeto_{self.projeto.id}', self.client.session)

    def test_cancelar_pag_1(self):
        """Testa se o botão Cancelar joga as alterações fora."""
        dados_formulario = {
            'cancelar': '',
            'titulo': "Título Invasor Que Não Deve Ser Salvo"
        }
        
        response = self.client.post(self.url_passo1, data=dados_formulario)
        
        self.projeto.refresh_from_db()
        self.assertEqual(self.projeto.titulo, "Projeto Inicial")
        self.assertNotIn(f'editar_projeto_{self.projeto.id}', self.client.session)
