
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpRequest, request
from django.contrib.auth.models import User, Group
from django.views.generic import TemplateView, ListView
from django.views.generic.detail import DetailView
from .forms import RegistroForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
# Create your views here.


# View para Crear usuarios
class UsuarioCreador(CreateView):
    model = User
    form_class = RegistroForm
    template_name = "usuarios/registrar.html"
    success_url = reverse_lazy('registrar')


# View para ver la lista de usuarios
class UsuarioLista(ListView):
    model = User
    template_name = "usuarios/lista.html"


# View para modificar los usurios
class UsuarioActualizar(UpdateView):
    model = User
    template_name = "usuarios/actualizar.html"
    success_url = reverse_lazy('listarUsuarios')
    fields = [            
            'first_name',
            'last_name',
            'email',
            'groups',
            'is_superuser',
            
        ]


# View para eliminar usuarios
class UsuarioEliminar(DeleteView):
    model = User
    template_name = "usuarios/eliminar.html"
    success_url = reverse_lazy('listarUsuarios')


def registro(request):
    form = RegistroForm(request.POST or None)
    if form.is_valid():
        # Extrae todos los datos enviados por el formulario
        form_data = form.cleaned_data
        # Guarda los datos del usuario sin incluir el grupo
        form.save()
        # Extraer del formulario el grupo y cambiamos el tipo de dato de grupo
        grupos = form_data.get("groups")
        grupos = str(grupos.get())

        # Extraer del formulario el nombre de usuario y cambiamos el tipo de dato de usuarios
        usuarios = form_data.get("username")
        usuarios = unicode(usuarios)

        # Encuentra el usuario creado y recupera el id
        for usuario in User.objects.all():
            if usuarios == usuario.username:
                myuser = usuario

        # Compara los grupos el escogido y los existentes
        for grupo in Group.objects.all():
            if grupos == grupo.name:
                myuser.groups.clear()
                myuser.groups.add(grupo)

        return redirect('listarUsuarios')

    context = {
        "form": form,

    }
    return render(request, "usuarios/registrar.html", context)
    

def listar(request):
    if request.user.is_superuser:
        usuario = User.objects.all()
    else:
        usuario = User.objects.filter(is_superuser=False)
    data = {}
    data['object_list'] = usuario
    return render(request, "usuarios/lista.html", data)


def actualizar(request, pk):
    if request.user.is_superuser:
        usuario = get_object_or_404(User, pk=pk)
    else:
        usuario = get_object_or_404(User, pk=pk, is_superuser=False)
    
    form = RegistroForm(request.POST or None, instance=usuario)    

    if form.is_valid():
        form_data = form.cleaned_data
        # Guarda los datos del usuario sin incluir el grupo
        form.save()

        # Extraer del formulario el grupo y cambiamos el tipo de dato de grupo
        grupos = form_data.get("groups")
        grupos = str(grupos.get())

        # Extraer del formulario el nombre de usuario y cambiamos el tipo de dato de usuarios
        usuarios = form_data.get("username")
        usuarios = unicode(usuarios)

        # Encuentra el usuario elegido y recupera el id
        for usuario in User.objects.all():
            if usuarios == usuario.username:
                myuser = usuario

        # Compara los grupos el escogido y los existentes
        for grupo in Group.objects.all():
            if grupos == grupo.name:
                myuser.groups.clear()
                myuser.groups.add(grupo)

        return redirect('listarUsuarios')

    return render(request, "usuarios/actualizar.html", {'form': form})


def eliminar(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        return redirect('listarUsuarios')
    return render(request, "usuarios/eliminar.html", {'object': usuario})
