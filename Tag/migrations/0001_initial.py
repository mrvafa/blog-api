# Generated by Django 3.2.3 on 2021-05-18 11:35

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_datetime', models.DateTimeField(auto_created=True, blank=True, null=True)),
                ('title', models.CharField(max_length=100, unique=True)),
                ('slug', models.CharField(max_length=100, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='tag/%d')),
                ('body', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('modify_datetime', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]
