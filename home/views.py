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
            messages.success(request, "Categoria adicionada com sucesso!")
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
        # Caso o registro não seja encontrado, exibe a mensagem de erro
        messages.error(request, 'Registro não encontrado')
        return redirect('categoria')  # Redireciona para a listagem

    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Operação realizada com Sucesso')
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
    try:
        categoria = Categoria.objects.get(pk=id)
    except Categoria.DoesNotExist:
        messages.error(request, "Registro não encontrado.")
        return redirect('categoria')  # Redireciona para a listagem
    
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, "Categoria removida com sucesso!")
        return redirect('categoria')  # Redireciona para a listagem
    
    # Se for um GET, renderiza a página de confirmação
    return render(request, 'categoria/confirmar_exclusao.html', {'categoria': categoria})


def detalhes_categoria(request, id):
    try:
        categoria = Categoria.objects.get(pk=id)
    except Categoria.DoesNotExist:
        messages.error(request, "Registro não encontrado.")
        return redirect('categoria')  # Redireciona para a listagem
    return render(request, 'categoria/detalhes.html', {'categoria': categoria})

def clientes(request):
    contexto = {
        'lista': Cliente.objects.all().order_by('id'),
    }
    return render(request, 'clientes/lista.html',contexto)

def form_cliente(request):
    if request.method == 'POST':
       form = ClienteForm(request.POST) # instancia o modelo com os dados do form
       if form.is_valid():# faz a validação do formulário
            form.save() # salva a instancia do modelo no banco de dados
            messages.success(request, "Cliente adicionado com sucesso!")
            return redirect('clientes') # redireciona para a listagem
    else:# método é get, novo registro
        form = ClienteForm() # formulário vazio
    contexto = {
        'form':form,
    }
    return render(request, 'clientes/formulario.html', contexto)

def editar_cliente(request, id):
    try:
        cliente = Cliente.objects.get(pk=id)
    except Cliente.DoesNotExist:
        # Caso o registro não seja encontrado, exibe a mensagem de erro
        messages.error(request, 'Registro não encontrado')
        return redirect('clientes')  # Redireciona para a listagem

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Operação realizada com Sucesso')
            return redirect('clientes')
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'clientes/formulario.html', {'form': form})

def remover_cliente(request, id):
    try:
        cliente = Cliente.objects.get(pk=id)
    except Cliente.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('clientes')  # Redireciona para a listagem
    
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, "Cliente removido com sucesso!")
        return redirect('clientes')  # Redireciona para a listagem
    
    # Se for um GET, renderiza a página de confirmação
    return render(request, 'clientes/confirmar_exclusao.html', {'cliente': cliente})

def produto(request):
    contexto = {
        'lista': Produto.objects.all().order_by('id'),
    }
    return render(request, 'produto/lista.html',contexto)

def form_produto(request):
    if request.method == 'POST':
       form = ProdutoForm(request.POST) # instancia o modelo com os dados do form
       if form.is_valid():# faz a validação do formulário
            form.save() # salva a instancia do modelo no banco de dados
            messages.success(request, "Produto adicionado com sucesso!")
            return redirect('produto') # redireciona para a listagem
    else:# método é get, novo registro
        form = ProdutoForm() # formulário vazio
    contexto = {
        'form':form,
    }
    return render(request, 'produto/form.html', contexto)

def editar_produto(request, id):
    try:
        produto = Produto.objects.get(pk=id)
    except Produto.DoesNotExist:
        # Caso o registro não seja encontrado, exibe a mensagem de erro
        messages.error(request, 'Registro não encontrado')
        return redirect('produto')  # Redireciona para a listagem

    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Operação realizada com Sucesso')
            return redirect('produto')
    else:
        form = ProdutoForm(instance=produto)

    return render(request, 'produto/form.html', {'form': form})

def remover_produto(request, id):
    try:
        produto = Produto.objects.get(pk=id)
    except Produto.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('produto')  # Redireciona para a listagem
    
    if request.method == 'POST':
        produto.delete()
        messages.success(request, 'Operação realizada com Sucesso')
        return redirect('produto')  # Redireciona para a listagem
    
    # Se for um GET, renderiza a página de confirmação
    return render(request, 'produto/confirmar_exclusao.html', {'produto': produto})

def detalhes_produto(request, id):
    try:
        produto = Produto.objects.get(pk=id)
    except Produto.DoesNotExist:
        messages.error(request, "Registro não encontrado.")
        return redirect('produto')  # Redireciona para a listagem
    return render(request, 'produto/detalhes.html', {'produto': produto})

def ajustar_estoque(request, id):
    try:
        produto = Produto.objects.get(pk=id)
        estoque = produto.estoque  # pega o objeto estoque relacionado ao produto
    except Produto.DoesNotExist:
        messages.error(request, "Registro não encontrado.")
        return redirect('produto')
    
    if request.method == 'POST':
        form = EstoqueForm(request.POST, instance=estoque)
        if form.is_valid():
            estoque = form.save()
            lista = [estoque.produto]
            messages.success(request, "Operação realizada com sucesso.")
            return render(request, 'produto/lista.html', {'lista': lista})
    else:
        form = EstoqueForm(instance=estoque)

    return render(request, 'produto/estoque.html', {'form': form})
