from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from .models import Categoria

def index(request):
    return render(request,'index.html')

def categoria(request):
    contexto = {
        'lista': Categoria.objects.all().order_by('id'),
    }
    return render(request, 'categoria/lista.html',contexto)

def form_categoria(request):
    if request.method == 'POST':
       form = CategoriaForm(request.POST) # instancia o modelo com os dados do form
       if form.is_valid():# faz a validação do formulário
            form.save() # salva a instancia do modelo no banco de dados
            return redirect('categoria') # redireciona para a listagem
    else:# método é get, novo registro
        form = CategoriaForm() # formulário vazio
    contexto = {
        'form':form,
    }
    return render(request, 'categoria/formulario.html', contexto)

## redireciona para a view de listagem ####

def editar_categoria(request, id):
    try:
        categoria = Categoria.objects.get(pk=id)
    except Categoria.DoesNotExist:
        return redirect('categoria')  # Redireciona para a listagem se o ID não existir

    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('categoria')
    else:
        form = CategoriaForm(instance=categoria)

    return render(request, 'categoria/formulario.html', {'form': form})


##LISTA APENAS O OBJETO EDITADO ####

#def editar_categoria(request, id):
#    categoria = Categoria.objects.get(pk=id)
#    if request.method == 'POST':
        # combina os dados do formulário submetido com a instância do objeto existente, permitindo editar seus valores.
#        form = CategoriaForm(request.POST, instance=categoria)
 #       if form.is_valid():
 #           categoria = form.save() # save retorna o objeto salvo
 #           lista = []
 #           lista.append(categoria) 
  #          return render(request, 'categoria/lista.html', {'lista': lista})
 #   else:
 #        form = CategoriaForm(instance=categoria)
 #   return render(request, 'categoria/formulario.html', {'form': form,})


def remover_categoria(request, id):
    categoria = get_object_or_404(Categoria, pk=id)
    
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, "Categoria removida com sucesso!")
        return redirect('categoria')  # Redireciona para a listagem
    
    # Se for um GET, renderiza a página de confirmação
    return render(request, 'categoria/confirmar_exclusao.html', {'categoria': categoria})

def detalhes_categoria(request, id):
    categoria = get_object_or_404(Categoria, pk=id)
    return render(request, 'categoria/detalhes.html', {'categoria': categoria})
