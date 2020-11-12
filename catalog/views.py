from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import render

from catalog.models import Collection, DataFile, Document, DocumentXMPMeta, Term


def search_results(request):
    query = request.GET.get('q', None)
    if not query:
        return HttpResponse("Error: query cannot be blank", content_type='text/plain')
    collections = "  " + "\n  ".join([c.name for c in Collection.objects.all().filter(name__contains=query)])
    documents = "  " + "\n  ".join([d.title for d in Document.objects.all().filter(title__contains=query)])
    terms = "  " + "\n  ".join([t.name for t in Term.objects.all().filter(name__contains=query)])
    result = "Collections:\n" + collections + "\nDocuments:\n" + documents + "\nTerms:\n" + terms
    return render(request, 'search_results.html', context={'query': query, 'result': result})

def collection_detail(request, pk=None, slug=None):
    try:
        c = Collection.objects.get(slug=slug) if pk is None else Collection.objects.get(pk=pk)
    except Collection.DoesNotExist:
        raise Http404(f"Collection does not exist in database: {slug if pk is None else pk}")
    parent = "None" if (c.parent is None) else f"{c.parent.pk} - {c.parent}"
    child_collections = [item.name for item in Collection.objects.all() if item.parent == c]
    child_documents = [item.title for item in Document.objects.all() if c in item.collections.all()]
    metadata_table = {
            "Collection ID": c.pk,
            "Name": c.name,
            "Slug": c.slug,
            "Created by": c.created_by,
            "Modified by": c.modified_by,
            "Created": c.created_date,
            "Modified": c.modified_date,
            "Parent": parent,
            "Children": child_collections,
            "Contents": child_documents,
        }
    return render(request, 'detail_collection.html', context={'c': c, 'meta': metadata_table})

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
    metadata_table = {
            "DataFile ID": f.pk,
            "Title": f"{f.document_id.pk} - {f.document_id.title}",
            "Owner": f.owner,
            "Created by": f.created_by,
            "Modified by": f.modified_by,
            "Created": f.created_date,
            "Modified": f.modified_date,
            "File name": f.file_name,
            "File MIME type": f.file_mime_type,
            "Format": f.get_file_format_type_display(),
            "Source URL": f.source_url,
            "Retrieved": f.source_retrieved,
            "Log": f.source_retrieve_log,
        }
    return render(request, 'detail_datafile.html', context={'f': f, 'meta': metadata_table})

@login_required
def document_detail(request, pk=None, slug=None):
    try:
        d = Document.objects.get(slug=slug) if pk is None else Document.objects.get(pk=pk)
    except Document.DoesNotExist:
        raise Http404(f"Document does not exist in database: {slug if pk is None else pk}")
    collections = [item.name for item in d.collections.all()]
    terms = [item.name for item in d.terms.all()]
    related = [item.title for item in d.related.all()]
    xmp = DocumentXMPMeta.objects.filter(document_id=d).first()
    metadata_table = {
            "Document ID": d.pk,
            "Title": d.title,
            "Slug": d.slug,
            "Owner": d.owner,
            "Created by": d.created_by,
            "Modified by": d.modified_by,
            "Created": d.created_date,
            "Modified": d.modified_date,
            "Collections": collections,
            "Terms": terms,
            "Related": related,
            "XMP Metadata": xmp.xmp if xmp is not None else '',
        }
    return render(request, 'detail_document.html', context={'d': d, 'meta': metadata_table})

def documentxmpmeta_detail(request, pk):
    try:
        x = DocumentXMPMeta.objects.get(pk=pk)
    except DocumentXMPMeta.DoesNotExist:
        raise Http404(f"DocumentXMPMeta does not exist in database: {pk}")
    return render(request, 'detail_xmp.html', context={'x': x})

def term_detail(request, pk=None, slug=None):
    try:
        t = Term.objects.get(slug=slug) if pk is None else Term.objects.get(pk=pk)
    except Term.DoesNotExist:
        raise Http404(f"Term does not exist in database: {slug if pk is None else pk}")
    parent = "None" if (t.parent is None) else f"{t.parent.pk} - {t.parent}"
    documents = [item.title for item in Document.objects.all() if t in item.terms.all()]
    metadata_table = {
            "Document ID": t.pk,
            "Name": t.name,
            "Slug": t.slug,
            "Owner": t.owner,
            "Created by": t.created_by,
            "Modified by": t.modified_by,
            "Created": t.created_date,
            "Modified": t.modified_date,
            "Parent": parent,
            "Documents": documents,
        }
    return render(request, 'detail_term.html', context={'t': t, 'meta': metadata_table})

def document_list(request): # useful to list all docs and for search
    documents = "\n".join([f"{d.pk} - {d.title}" for d in Document.objects.all()])
    return HttpResponse(f"{documents}\n", content_type='text/plain')
