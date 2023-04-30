from django.db import models
from django.contrib.auth.models import User
from product.models import Product
# Create your models here.




class CartItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False,related_name='cartitems')
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=7, decimal_places=2,default=0, blank=False)

    def __str__(self):
        return str(self.product)
