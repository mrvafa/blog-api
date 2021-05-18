# Generated by Django 3.2.3 on 2021-05-18 18:20

import Post.validators.post_image_validators
import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Tag', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=100, unique=True)),
                ('slug', models.CharField(editable=False, max_length=100, unique=True)),
                ('image', models.ImageField(upload_to='post/%m', validators=[Post.validators.post_image_validators.post_image_validate])),
                ('body', ckeditor_uploader.fields.RichTextUploadingField()),
                ('added_datetime', models.DateTimeField(auto_now_add=True, null=True)),
                ('modify_datetime', models.DateTimeField(auto_now=True, null=True)),
                ('tags', models.ManyToManyField(blank=True, to='Tag.Tag')),
            ],
        ),
    ]
