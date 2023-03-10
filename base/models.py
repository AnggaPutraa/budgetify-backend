from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken

class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    image_url = models.ImageField(
        upload_to='images/%Y/%m/%d/', max_length=255, null=True, blank=True)
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return{
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }
    def __str__(self):
        return self.username

class TransactionType(models.Model):
    type = models.CharField(max_length=20)
    class Meta:
        verbose_name_plural = 'Transaction Type'
    def __str__(self):
        return self.type

class TransactionCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    type = models.ForeignKey(
        TransactionType, 
        related_name='transaction_sub_category', 
        on_delete=models.CASCADE
    )
    class Meta:
        verbose_name_plural = 'Transaction Categories'
    def __str__(self):
        return f'{self.user.username} - {self.name}'

class TransactionModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.ForeignKey(
        TransactionType, 
        related_name='transaction', 
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        TransactionCategory, 
        related_name='transaction', 
        on_delete=models.CASCADE
    )
    amount = models.BigIntegerField()
    note = models.TextField(max_length=200, blank=True)
    date = models.DateField(auto_now=False, auto_now_add=False)
    class Meta:
        verbose_name_plural = 'Transactions'
    def __str__(self):
        return f'{self.user.username} - {self.type.type}'
