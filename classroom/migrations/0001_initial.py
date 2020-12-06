# Generated by Django 3.1.3 on 2020-12-05 18:58

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='eUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('student_num', models.CharField(max_length=10, unique=True, validators=[django.core.validators.RegexValidator('^\\d{1,10}$')])),
                ('name', models.CharField(max_length=32)),
                ('dept', models.CharField(default='None', max_length=32)),
                ('create_date', models.DateField(auto_now_add=True)),
                ('is_professor', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='none', max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, unique=True)),
                ('season', models.CharField(max_length=32)),
                ('start_time', models.DateTimeField(blank=True)),
                ('end_time', models.DateTimeField(blank=True)),
                ('students_num', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ('-title',),
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32)),
                ('desc', models.TextField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('text', models.TextField(max_length=20000)),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('updated_date', models.DateTimeField(auto_now=True, null=True)),
                ('views', models.IntegerField(default=0, editable=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classroom.category')),
            ],
            options={
                'ordering': ('-created_date',),
            },
        ),
        migrations.CreateModel(
            name='files',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.GenericIPAddressField(auto_created=True)),
                ('file', models.FileField(upload_to='')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(blank=True, max_length=255)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classroom.post')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classroom.post')),
            ],
        ),
        migrations.CreateModel(
            name='ClassList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classroom.class')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='class',
            name='professor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classroom.professor'),
        ),
        migrations.AddField(
            model_name='class',
            name='students',
            field=models.ManyToManyField(through='classroom.ClassList', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='category',
            name='class_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classroom.class'),
        ),
    ]