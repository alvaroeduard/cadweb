from decimal import Decimal, ROUND_HALF_UP
import locale
from django.db import models
from datetime import date
from django.db.models.signals import post_save
from django.dispatch import receiver
import hashlib

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    ordem = models.IntegerField()
    
    def __str__(self):
        return self.nome
    
class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=15,verbose_name="C.P.F")
    datanasc = models.DateField(verbose_name="Data de Nascimento")


    def __str__(self):
        return self.nome
    
    @property
    def datanascimento(self):
        """Retorna a data de nascimento no formato DD/MM/AAAA"""
        if self.datanasc:
            return self.datanasc.strftime("%d/%m/%Y")
        return None  

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    img_base64 = models.TextField(blank=True)

    def __str__(self):
        return self.nome
    
    @property
    def estoque(self):
        estoque_item, flag_created = Estoque.objects.get_or_create(produto=self, defaults={'qtde': 0})
        return estoque_item
    
    @receiver(post_save, sender='home.Produto')  # Substitua 'suaapp' pelo nome do seu app
    def atualizar_preco_pedidos(sender, instance, **kwargs):
        if instance.pk:  # Verifica se é uma atualização, não uma criação
            try:
                produto_antigo = Produto.objects.get(pk=instance.pk)
                if produto_antigo.preco != instance.preco:
                    # Atualiza todos os itens de pedido vinculados a este produto
                    ItemPedido.objects.filter(produto=instance).update(preco=instance.preco)
            except Produto.DoesNotExist:
                pass

class Estoque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    qtde = models.IntegerField()

    def __str__(self):
        return f'{self.produto.nome} - Quantidade: {self.qtde}'
    
class Pedido(models.Model):


    NOVO = 1
    EM_ANDAMENTO = 2
    CONCLUIDO = 3
    CANCELADO = 4


    STATUS_CHOICES = [
        (NOVO, 'Novo'),
        (EM_ANDAMENTO, 'Em Andamento'),
        (CONCLUIDO, 'Concluído'),
        (CANCELADO, 'Cancelado'),
    ]


    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    produtos = models.ManyToManyField(Produto, through='ItemPedido')
    data_pedido = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=NOVO)


    def __str__(self):
            return f"Pedido {self.id} - Cliente: {self.cliente.nome} - Status: {self.get_status_display()}"

    @property
    def chave_acesso(self):
        """Gera uma chave de acesso única baseada no ID do pedido, data do pedido e CPF do cliente."""
        if self.id is None or self.data_pedido is None or not hasattr(self.cliente, 'cpf'):
            return None  # Retorna None se o pedido ainda não foi salvo ou não houver CPF

        # Formatação do CPF garantindo 11 dígitos
        cpf_cliente = str(self.cliente.cpf).zfill(11).replace('.', '').replace('-', '')

        # Ano e mês do pedido
        ano = self.data_pedido.strftime('%Y')
        mes = self.data_pedido.strftime('%m')

        # Parâmetros fixos da chave
        modelo_nf = "55"  # Modelo 55 para NF-e
        numero_nf = str(self.id).zfill(9)  # Número da nota com 9 dígitos
        serie_nf = "001"  # Série da NF-e
        tipo_emissao = "1"  # Emissão normal

        # Geração da chave sem DV
        chave_sem_dv = f"{ano}{mes}{cpf_cliente}{modelo_nf}{serie_nf}{numero_nf}{tipo_emissao}"

        # Retornar a chave formatada
        return chave_sem_dv

    @property
    def data_pedidof(self):
        """Retorna a data de nascimento no formato DD/MM/AAAA"""
        if self.data_pedido:
            return self.data_pedido.strftime("%d/%m/%Y")
        return None
    
    @property
    def total(self):
        """Calcula o total de todos os itens no pedido, formatado como moeda local"""
        total = sum(item.qtde * item.preco for item in self.itempedido_set.all())
        return total

    @property
    def qtdeItens(self):
        """Conta a qtde de itens no pedido, """
        return self.itempedido_set.count()
    
    # lista de todos os pagamentos realiados
    @property
    def pagamentos(self):
        return Pagamento.objects.filter(pedido=self) 
    
    #Calcula o total de todos os pagamentos do pedido
    @property
    def total_pago(self):
        return sum(pagamento.valor for pagamento in self.pagamentos.all())
           
    @property
    def debito(self):
        """Retorna o valor restante a ser pago no pedido."""
        return self.total - self.total_pago

    # === Cálculo dos impostos ===
    def formatar_decimal(self, valor):
        """Formata um valor Decimal para ter apenas duas casas decimais."""
        return valor.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    @property
    def icms(self):
        """Calcula o ICMS (18% sobre o total do pedido)."""
        return self.formatar_decimal(self.total * Decimal('0.18'))

    @property
    def ipi(self):
        """Calcula o IPI (5% sobre o total do pedido)."""
        return self.formatar_decimal(self.total * Decimal('0.05'))

    @property
    def pis(self):
        """Calcula o PIS (1.65% sobre o total do pedido)."""
        return self.formatar_decimal(self.total * Decimal('0.0165'))

    @property
    def cofins(self):
        """Calcula o COFINS (7.6% sobre o total do pedido)."""
        return self.formatar_decimal(self.total * Decimal('0.076'))

    @property
    def total_impostos(self):
        """Calcula o total de impostos somando ICMS, IPI, PIS e COFINS."""
        return self.formatar_decimal(self.icms + self.ipi + self.pis + self.cofins)

    @property
    def valorfinal(self):
        """Calcula o total de impostos + valor total dos itens."""
        return self.formatar_decimal(self.total_impostos + self.total)

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    qtde = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return f"{self.produto.nome} (Qtd: {self.qtde}) - Preço Unitário: {self.preco}" 
    
    @property
    def totalItem(self):
        return self.qtde * self.preco # Calcula o total de cada item
    
    
    
class Pagamento(models.Model):
    DINHEIRO = 1
    CARTAO = 2
    PIX = 3
    OUTRA = 4


    FORMA_CHOICES = [
        (DINHEIRO, 'Dinheiro'),
        (CARTAO, 'Cartão'),
        (PIX, 'Pix'),
        (OUTRA, 'Outra'),
    ]


    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    forma = models.IntegerField(choices=FORMA_CHOICES)
    valor = models.DecimalField(max_digits=10, decimal_places=2,blank=False)
    data_pgto = models.DateTimeField(auto_now_add=True)
    
    @property
    def data_pgtof(self):
        """Retorna a data no formato DD/MM/AAAA HH:MM"""
        if self.data_pgto:
            return self.data_pgto.strftime('%d/%m/%Y %H:%M')
        return None
