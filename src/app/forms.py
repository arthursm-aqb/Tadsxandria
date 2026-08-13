from django import forms

class EditarProjetoPasso1Form(forms.Form):
    titulo = forms.CharField(
        max_length=255,
        min_length=2, 
        label="Título",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    plataforma = forms.CharField(
        max_length=100, 
        label="Plataforma",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    ano_semestre = forms.CharField(
        max_length=20, 
        label="Ano/semestre",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    colaboradores = forms.CharField(
        label="Colaboradores",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), 
        required=True
    )
    contatos = forms.CharField(
        max_length=255, 
        label="Contatos",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    orientador = forms.CharField(
        max_length=255, 
        label="Orientador",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
    categoria = forms.CharField(
        max_length=100, 
        min_length=5,
        label="Categoria",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    categoria_secundaria = forms.CharField(
        max_length=100, 
        label="Categoria secundária",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

class EditarProjetoPasso2Form(forms.Form):
    resumo = forms.CharField(
        label="Resumo",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    descricao = forms.CharField(
        label="Descrição",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )
    ferramentas_utilizadas = forms.CharField(
        max_length=255, 
        label="Ferramentas utilizadas",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    repositorio = forms.URLField(
        label="Repositório",
        widget=forms.URLInput(attrs={'class': 'form-control'})
    )
    status = forms.ChoiceField(
        label="Status",
        choices=[('em_andamento', 'Em andamento'), ('concluido', 'Concluído')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    imagem = forms.ImageField(label="Imagem", required=False)