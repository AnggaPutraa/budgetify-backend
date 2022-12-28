from django.urls import path, re_path, reverse_lazy
from django.views.generic.base import RedirectView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from base.views import *

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('admin:index'))),
    path('api/register/', RegisterUserView.as_view(), name="register"),
    path('api/login/', LoginUserView.as_view(), name='login'),
    path('api/logout/', LogoutUserView.as_view(), name='logout'),
    path('api/token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('api/user/transactions/', UserTransactionsView.as_view(), name='user-transactions'),
    path('api/user/transactions/transaction-detail/', UserTransactionDetailView.as_view(), name='user-transaction-detail'),
    path('api/user/transactions/category/', UserTransactionCategoryView.as_view(), name='user-transaction-category'),
    re_path('get-subcategory/', UserSubCategoryView.as_view()),
]