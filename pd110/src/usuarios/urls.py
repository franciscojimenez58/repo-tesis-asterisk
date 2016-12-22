from django.conf.urls import url
from .views import *
from usuarios import views
from django.contrib.auth.decorators import login_required


"""Usuarios URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

urlpatterns = [
    url(r'^registrar', login_required(UsuarioCreador.as_view()), name="registrar"),

    # URLs basadas en clases
    # url(r'^$', login_required(UsuarioLista.as_view()), name="listarUsuarios"),
    # url(r'^editar/(?P<pk>\d+)$', login_required(UsuarioActualizar.as_view()), name="actualizarUsuarios"),
    # url(r'^borrar/(?P<pk>\d+)$', login_required(UsuarioEliminar.as_view()), name="eliminarUsuarios"),
    # url(r'^registro', login_required(views.registro), name="registro"),

    # URLs basadas en funciones
    url(r'^$', views.listar, name='listarUsuarios'),
    url(r'^registro$', views.registro, name='registroUsuarios'),
    url(r'^editar/(?P<pk>\d+)$', views.actualizar, name='actualizarUsuarios'),
    url(r'^borrar/(?P<pk>\d+)$', views.eliminar, name='eliminarUsuarios'),


]