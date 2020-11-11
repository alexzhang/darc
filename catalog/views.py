from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import render

from catalog.models import Collection, DataFile, Document, DocumentXMPMeta, Term


def collection_detail(request, pk=None, slug=None):
    try:
        c = Collection.objects.get(slug=slug) if pk is None else Collection.objects.get(pk=pk)
    except Collection.DoesNotExist:
        raise Http404(f"Collection does not exist in database: {slug if pk is None else pk}")
    parent = "None" if (c.parent is None) else f"{c.parent.pk} - {c.parent}"
    child_collections = [item.name for item in Collection.objects.all() if item.parent == c]
    child_documents = [item.title for item in Document.objects.all() if c in item.collections.all()]
    return HttpResponse(f"Collection Detail: {c.pk}\n\n" +
                            f"Name: {c.name}\n" +
                            f"Slug: {c.slug}\n\n" +
                            f"Description: {c.description}\n\n" +
                            f"Owner: {c.owner}\n" +
                            f"Created by: {c.created_by}\n" +
                            f"Modified by: {c.modified_by}\n" +
                            f"Created: {c.created_date}\n" +
                            f"Modified: {c.modified_date}\n\n" +
                            f"Parent: {parent}\n\n" +
                            f"Child collections: {child_collections}\n\n"
                            f"Child Documents: {child_documents}\n", content_type='text/plain')

def collection_root(request):
    def recursive_render(node):
        children = Collection.objects.filter(parent=node)
        ret_string = node.name
        for child in children:
            child_string = recursive_render(child)
            for line in child_string.splitlines(False):
                ret_string += "\n\t" + line
        return ret_string
    content = "\n".join([recursive_render(root_item) for root_item in Collection.objects.filter(parent=None)])
    return HttpResponse(f"Collections:\n\n{content}\n", content_type='text/plain')

def datafile_detail(request, uuid):
    try:
        f = DataFile.objects.get(pk=uuid)
    except DataFile.DoesNotExist:
        raise Http404(f"DataFile does not exist in database: {uuid}")
    return HttpResponse(f"DataFile Detail: {f.pk}\n\n" +
                            f"Document: {f.document_id.pk} - {f.document_id.title}\n\n" +
                            f"Owner: {f.owner}\n" +
                            f"Created by: {f.created_by}\n" +
                            f"Modified by: {f.modified_by}\n" +
                            f"Created: {f.created_date}\n" +
                            f"Modified: {f.modified_date}\n\n" +
                            f"File name: {f.file_name}\n" +
                            f"File MIME type: {f.file_mime_type}\n" +
                            f"Format: {f.get_file_format_type_display()}\n\n" +
                            f"Source URL: {f.source_url}\n" +
                            f"Retrieved: {f.source_retrieved}\n\n" +
                            f"===== Log =====\n{f.source_retrieve_log}\n", content_type='text/plain')

@login_required
def document_detail(request, pk):
    try:
        d = Document.objects.get(pk=pk)
    except Document.DoesNotExist:
        raise Http404(f"Document does not exist in database: {pk}")
    collections = [item.name for item in d.collections.all()]
    terms = [item.name for item in d.terms.all()]
    related = [item.title for item in d.related.all()]
    xmp = DocumentXMPMeta.objects.filter(document_id=d).first()
    if xmp is not None:
        xmp = f"\n{xmp.xmp}"
    return HttpResponse(f"Document Detail: {d.pk}\n\n" +
                            f"Title: {d.title}\n" +
                            f"Slug: {d.slug}\n\n" +
                            f"Owner: {d.owner}\n" +
                            f"Created by: {d.created_by}\n" +
                            f"Modified by: {d.modified_by}\n" +
                            f"Created: {d.created_date}\n" +
                            f"Modified: {d.modified_date}\n\n" +
                            f"Collections: {collections}\n" +
                            f"Terms: {terms}\n" +
                            f"Related: {related}\n\n" +
                            f"XMP Metadata: {xmp}\n", content_type='text/plain')

def documentxmpmeta_detail(request, pk):
    try:
        x = DocumentXMPMeta.objects.get(pk=pk)
    except DocumentXMPMeta.DoesNotExist:
        raise Http404(f"DocumentXMPMeta does not exist in database: {pk}")
    return HttpResponse(f"DocumentXMPMeta Detail: {x.pk}\n\n" +
                            f"Document: {x.document_id.pk} - {x.document_id.title}\n\n" +
                            f"===== XMP =====\n{x.xmp}\n", content_type='text/plain')

def term_detail(request, pk=None, slug=None):
    try:
        t = Term.objects.get(slug=slug) if pk is None else Term.objects.get(pk=pk)
    except Term.DoesNotExist:
        raise Http404(f"Term does not exist in database: {slug if pk is None else pk}")
    parent = "None" if (t.parent is None) else f"{t.parent.pk} - {t.parent}"
    documents = [item.title for item in Document.objects.all() if t in item.terms.all()]
    return HttpResponse(f"Term Detail: {t.pk}\n\n" +
                            f"Name: {t.name}\n" +
                            f"Slug: {t.slug}\n\n" +
                            f"Description: {t.description}\n\n" +
                            f"Owner: {t.owner}\n" +
                            f"Created by: {t.created_by}\n" +
                            f"Modified by: {t.modified_by}\n" +
                            f"Created: {t.created_date}\n" +
                            f"Modified: {t.modified_date}\n\n" +
                            f"Parent: {parent}\n\n" +
                            f"Tagged: {documents}\n", content_type='text/plain')

def document_list(request): # useful to list all docs and for search
    documents = "\n".join([f"{d.pk} - {d.title}" for d in Document.objects.all()])
    return HttpResponse(f"{documents}\n", content_type='text/plain')
