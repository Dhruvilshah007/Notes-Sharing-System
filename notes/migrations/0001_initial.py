# Generated by Django 3.1 on 2020-10-10 10:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Signup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', models.CharField(max_length=10, null=True)),
                ('branch', models.CharField(max_length=10)),
                ('role', models.CharField(max_length=10)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploadingdate', models.CharField(max_length=30)),
                ('branch', models.CharField(max_length=30)),
                ('subject', models.CharField(max_length=30)),
                ('notesfile', models.FileField(null=True, upload_to='')),
                ('filetype', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=200, null=True)),
                ('status', models.CharField(max_length=15, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]