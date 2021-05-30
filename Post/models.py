from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

from Post.validators.post_image_validators import post_image_validate
from Tag.models import Tag


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False)
    title = models.CharField(max_length=settings.POST_TITLE_LENGTH_MAX, unique=True, db_index=True)
    slug = models.CharField(max_length=settings.POST_TITLE_LENGTH_MAX, unique=True, editable=False)
    image = models.ImageField(upload_to='post/%m', validators=[post_image_validate], )
    body = RichTextUploadingField()
    added_datetime = models.DateTimeField(auto_now_add=True, blank=True, null=True, )
    modify_datetime = models.DateTimeField(auto_now=True, blank=True, null=True, )
    tags = models.ManyToManyField(Tag, blank=True, )

    class Meta:
        permissions = [
            ('is_author', 'Can create, edit and delete own post using API.'),
        ]

    def clean(self, *args, **kwargs):
        self.title = self.title.strip()
        self.slug = slugify(self.title, allow_unicode=True, )
        if not self.author.has_perm('Post.is_author'):
            raise ValidationError(settings.ERROR_MESSAGES['NON_AUTHOR_USER'])
        super(Post, self).clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.slug
