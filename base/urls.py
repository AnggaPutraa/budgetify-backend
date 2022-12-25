from django.urls import path, re_path
from base.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/register/', RegisterUserView.as_view(), name="register"),
    path('api/login/', LoginUserView.as_view(), name='login'),
    path('api/logout/', LogoutUserView.as_view(), name='logout'),
    path('api/token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('api/transactions/', UserTransactionsView.as_view(), name='user-transaction'),
    path('api/transactions/transaction-detail/', UserTransactionDetailView.as_view(), 
        name='user-transaction-detail'),
    re_path('getSubcategory/', UserSubCategoryView.as_view()),
]