from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Produto, ItemPedido

@receiver(post_save, sender=Produto)
def atualizar_precos_itens_pedido(sender, instance, **kwargs):
    """ Atualiza os preços dos itens do pedido quando o produto for atualizado. """
    itens_pedido = ItemPedido.objects.filter(produto=instance)

    for item in itens_pedido:
        item.preco = instance.preco  # Atualiza o preço para o novo preço do produto
        item.save()
