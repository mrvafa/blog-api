from django.conf import settings
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify

from Tag.validators.tag_image_validators import tag_image_validate


class Tag(models.Model):
    title = models.CharField(max_length=settings.TAG_TITLE_LENGTH_MAX, unique=True, )
    slug = models.CharField(max_length=settings.TAG_TITLE_LENGTH_MAX, unique=True, editable=False)
    image = models.ImageField(upload_to='tag/%d', validators=[tag_image_validate,], blank=True, null=True, )
    body = RichTextUploadingField(blank=True, null=True)
    added_datetime = models.DateTimeField(auto_created=True, blank=True, null=True, )
    modify_datetime = models.DateTimeField(auto_now_add=True, blank=True, null=True, )

    def clean(self, *args, **kwargs):
        self.title = self.title.strip()
        self.slug = slugify(self.title, allow_unicode=True,)
        super(Tag, self).clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.slug
