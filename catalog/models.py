from django.contrib.auth.models import User
from django.db import models

import uuid


class Term(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, related_name='term_created_by')
    modified_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, related_name='term_modified_by')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1)

    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000, blank=True, null=True)
    slug = models.CharField(max_length=200)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return f"[Term {self.name}]"


class Collection(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, related_name='collection_created_by')
    modified_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, related_name='collection_modified_by')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1)

    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000, blank=True, null=True)
    slug = models.CharField(max_length=200)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self) -> str:
        return f"[Collection {self.name}]"


class Document(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, related_name='document_created_by')
    modified_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, related_name='document_modified_by')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1)

    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)

    collections = models.ManyToManyField(Collection)
    terms = models.ManyToManyField(Term, blank=True)
    related = models.ManyToManyField('self', blank=True)


class DocumentXMPMeta(models.Model):
    document_id = models.ForeignKey(Document, on_delete=models.CASCADE)
    xmp = models.TextField(verbose_name="XMP Metadata")


class DataFile(models.Model):
    id = models.UUIDField(primary_key=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, related_name='file_created_by')
    modified_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, related_name='file_modified_by')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1)

    document_id = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True)
    file_name = models.CharField(max_length=255)
    file_mime_type = models.CharField(max_length=127)
    file_size = models.IntegerField()
    file_last_modified_date = models.DateTimeField()
    file_last_modified_nano = models.IntegerField()

    FORMAT_TYPES = (
        ('n', 'native'),  # Native files are documents that were "born" digital
        ('s', 'scanned'), # Scanned documents are usually a collection of images
        ('w', 'working'), # Working documents are in editable formats for word processors or editors
    )
    file_format_type = models.CharField(max_length=1, choices=FORMAT_TYPES)

    source_url = models.CharField(max_length=255, blank=True, null=True)
    source_retrieved = models.DateTimeField(blank=True, null=True)
    source_retrieve_log = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_date', 'id']

    def __str__(self) -> str:
        return f"[File { self.id } {self.file_name}]"
