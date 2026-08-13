from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Usuario)
admin.site.register(models.Orientador)
admin.site.register(models.Orientando)

admin.site.register(models.Projeto)
admin.site.register(models.Categoria)
admin.site.register(models.Tecnologia)

# admin.site.register(models.Favoritar)
admin.site.register(models.Avaliar)

admin.site.register(models.Participacao)
admin.site.register(models.OrientadorProjeto)
