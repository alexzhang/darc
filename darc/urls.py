from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from catalog.views import collection_detail, collection_root, datafile_detail, document_detail, documentxmpmeta_detail, term_detail, document_list


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('c/', collection_root),
    path('collections/', collection_root),

    path('c/<int:pk>', collection_detail),
    path('collection/<int:pk>', collection_detail),
    path('c/<slug:slug>', collection_detail),
    path('collection/<slug:slug>', collection_detail),

    path('f/<uuid:uuid>', datafile_detail),
    path('file/<uuid:uuid>', datafile_detail),

    path('d/', document_list),
    path('documents/', document_list),
    path('d/<int:pk>', document_detail),
    path('document/<int:pk>', document_detail),

    path('x/<int:pk>', documentxmpmeta_detail),
    path('xmp/<int:pk>', documentxmpmeta_detail),

    path('t/<int:pk>', term_detail),
    path('term/<int:pk>', term_detail),
    path('t/<slug:slug>', term_detail),
    path('term/<slug:slug>', term_detail),
]
