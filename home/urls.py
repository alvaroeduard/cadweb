from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('categoria', views.categoria, name="categoria"),
    path('form_categoria', views.form_categoria, name="form_categoria"),
    path('editar_categoria/<int:id>', views.editar_categoria, name="editar_categoria"),
    path('remover_categoria/<int:id>', views.remover_categoria, name='remover_categoria'),
    path('detalhes_categoria/<int:id>', views.detalhes_categoria, name='detalhes_categoria'),

]
