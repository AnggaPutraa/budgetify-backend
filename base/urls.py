from django.urls import path, re_path
from base.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/register/', RegisterUser.as_view(), name="register"),
    path('api/login/', LoginUser.as_view(), name='login'),
    path('api/logout/', LogoutUser.as_view(), name='logout'),
    path('api/token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    re_path('getSubcategory/', TransactionSubCategory.as_view()),
]