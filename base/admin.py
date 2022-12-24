from django.contrib import admin
from base.views import *

admin.site.register(User)
admin.site.register(TransactionType)
admin.site.register(TransactionCategory)
admin.site.register(TransactionModel)