from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.db import models
from django.utils.text import slugify

from Post.validators.post_image_validators import post_image_validate
from Tag.models import Tag


class Post(models.Model):
    title = models.CharField(max_length=settings.POST_TITLE_LENGTH_MAX, unique=True, db_index=True)
    slug = models.CharField(max_length=settings.POST_TITLE_LENGTH_MAX, unique=True, editable=False)
    image = models.ImageField(upload_to='post/%d', validators=[post_image_validate], )
    body = RichTextUploadingField()
    added_datetime = models.DateTimeField(auto_created=True, blank=True, null=True, )
    modify_datetime = models.DateTimeField(auto_now_add=True, blank=True, null=True, )
    tags = models.ManyToManyField(Tag, blank=True, )

    def clean(self, *args, **kwargs):
        self.title = self.title.strip()
        self.slug = slugify(self.title, allow_unicode=True, )
        super(Post, self).clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.slug
