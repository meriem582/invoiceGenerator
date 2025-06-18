from django.db import models

# C'est la table qui contient les produits
# Chaque produit a un nom, un prix et une date d'expiration
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    expiration_date = models.DateField()
    
class Meta:
    db_table="product"

# C'est la table qui contient les factures
# Chaque facture a une date de création et une liste d'items ( items c'est les produits achetés )
class Invoice(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    
    def get_total(self):
        return sum(item.get_prix_total() for item in self.items.all())
    
class Meta:
    db_table="invoice"

# C'est la table qui contient les items de la facture
# Chaque item est lié à une facture et à un produit (relation many-to-many qu'a causer la création de cette table)
class InvoiceItem (models.Model):
    invoice  = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_prix_total(self):
        return self.quantity * self.product.price
    
class Meta:
    db_table="InvoiceItem"
