import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import multi_email_field.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('nome', models.CharField(blank=True, max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('matricula', models.CharField(blank=True, max_length=14, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Usuário',
                'verbose_name_plural': 'Usuários',
                'db_table': 'usuarios',
            },
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
                'db_table': 'categorias',
            },
        ),
        migrations.CreateModel(
            name='Tecnologia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('icone', models.ImageField(upload_to='tecnologias/')),
            ],
            options={
                'verbose_name': 'Tecnologia',
                'verbose_name_plural': 'Tecnologias',
                'db_table': 'tecnologias',
            },
        ),
        migrations.CreateModel(
            name='Orientador',
            fields=[
                ('usuario_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Orientador',
                'verbose_name_plural': 'Orientadores',
                'db_table': 'orientadores',
            },
            bases=('app.usuario',),
        ),
        migrations.CreateModel(
            name='Orientando',
            fields=[
                ('usuario_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Orientando',
                'verbose_name_plural': 'Orientandos',
                'db_table': 'orientandos',
            },
            bases=('app.usuario',),
        ),
        migrations.CreateModel(
            name='Projeto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
                ('descricao', models.TextField(max_length=500)),
                ('avaliacao', models.FloatField(blank=True, default=0.0, null=True)),
                ('data_criacao', models.DateTimeField()),
                ('data_finalizacao', models.DateTimeField(blank=True, null=True)),
                ('data_publicacao', models.DateTimeField()),
                ('status', models.CharField(choices=[('andamento', 'Em Andamento'), ('finalizado', 'Finalizado'), ('abandonado', 'Abandonado')], default='andamento', max_length=20)),
                ('fase', models.CharField(choices=[('web', 'Web'), ('distribuido', 'Distribuído'), ('corporativo', 'Corporativo')], max_length=20)),
                ('plataforma', models.CharField(choices=[('web', 'Web'), ('mobile', 'Mobile'), ('vr', 'VR'), ('desktop', 'Desktop'), ('console', 'Console')], max_length=20)),
                ('resumo', models.TextField(max_length=2000)),
                ('imagem', models.ImageField(upload_to='projetos/')),
                ('repositorio', models.URLField(max_length=500)),
                ('contato', multi_email_field.fields.MultiEmailField(blank=True, default=[], max_length=500, null=True)),
                ('ano_semestre', models.CharField(max_length=20)),
                ('colaboradores', models.TextField()),
                ('contatos', multi_email_field.fields.MultiEmailField(blank=True, default=[], max_length=500, null=True)),
                ('orientador', models.CharField(max_length=255)),
                ('categoria_principal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projetos_principais', to='app.categoria')),
                ('categorias_secundarias', models.ManyToManyField(blank=True, related_name='projetos_secundarios', to='app.categoria')),
                ('projetos_favoritos', models.ManyToManyField(blank=True, related_name='favoritos', to=settings.AUTH_USER_MODEL)),
                ('tecnologias', models.ManyToManyField(blank=True, related_name='projetos', to='app.tecnologia')),
            ],
            options={
                'verbose_name': 'Projeto',
                'verbose_name_plural': 'Projetos',
                'db_table': 'projetos',
            },
        ),
        migrations.CreateModel(
            name='OrientadorProjeto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('participacao', models.BooleanField()),
                ('projeto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.projeto')),
                ('orientador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.orientador')),
            ],
            options={
                'verbose_name': 'Orientadores do Projeto',
                'verbose_name_plural': 'Orientadores dos Projetos',
                'db_table': 'orientadorprojeto',
            },
        ),
        migrations.CreateModel(
            name='Participacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('participacao', models.BooleanField()),
                ('projeto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.projeto')),
                ('orientando', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.orientando')),
            ],
            options={
                'verbose_name': 'Participação',
                'verbose_name_plural': 'Participações',
                'db_table': 'participacoes',
            },
        ),
        migrations.CreateModel(
            name='Avaliar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nota', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('comentario', models.TextField(blank=True, max_length=255, null=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('projeto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.projeto')),
            ],
            options={
                'verbose_name': 'Avaliação',
                'verbose_name_plural': 'Avaliações',
                'db_table': 'avaliacoes',
                'constraints': [models.UniqueConstraint(fields=('usuario', 'projeto'), name='unique_avaliacao')],
            },
        ),
    ]
