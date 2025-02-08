from django.urls import path
from . import views
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.index, name="index"),
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('categoria', views.categoria, name="categoria"),
    path('form_categoria', views.form_categoria, name="form_categoria"),
    path('editar_categoria/<int:id>', views.editar_categoria, name="editar_categoria"),
    path('remover_categoria/<int:id>', views.remover_categoria, name='remover_categoria'),
    path('detalhes_categoria/<int:id>', views.detalhes_categoria, name='detalhes_categoria'),
    path('clientes', views.clientes, name="clientes"),
    path('form_cliente', views.form_cliente, name="form_cliente"),
    path('editar_cliente/<int:id>', views.editar_cliente, name="editar_cliente"),
    path('remover_cliente/<int:id>', views.remover_cliente, name='remover_cliente'),
    path('produto', views.produto, name="produto"),
    path('form_produto', views.form_produto, name="form_produto"),
    path('editar_produto/<int:id>', views.editar_produto, name="editar_produto"),
    path('remover_produto/<int:id>', views.remover_produto, name='remover_produto'),
    path('detalhes_produto/<int:id>', views.detalhes_produto, name='detalhes_produto'),
    path('ajustar_estoque/<int:id>', views.ajustar_estoque, name='ajustar_estoque'),
    path('teste1/', views.teste1, name='teste1'),
    path('teste2/', views.teste2, name='teste2'),
    path('teste3/', views.teste3, name='teste3'),
    path('buscar_dados/<str:app_modelo>/', views.buscar_dados, name='buscar_dados'),
    path('pedido', views.pedido, name="pedido"),
    path('novo_pedido/<int:id>', views.novo_pedido, name='novo_pedido'),
    path('remover_pedido/<int:id>', views.remover_pedido, name='remover_pedido'),
    path('detalhes_pedido/<int:id>', views.detalhes_pedido, name='detalhes_pedido'),
    path('detalhes_pedido/<int:id>/editar', views.editar_item_pedido, name='editar_item_pedido'),
    path('detalhes_pedido/remover_item/<int:id>/', views.remover_item_pedido, name='remover_item_pedido'),
    path('form_pagamento/<int:id>/', views.form_pagamento, name='form_pagamento'),
    path('pagamento/editar/<int:id>/', views.editar_pagamento, name='editar_pagamento'),
    path('pagamento/remover/<int:id>/', views.remover_pagamento, name='remover_pagamento'),
]
