from django.http import HttpResponse
from django.core import serializers as django_core_serializers

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from base.models import *
from base.serializers import *

class RegisterUserView(APIView):
    serializer_class = RegisterSerializer
    def post(self, request):
        user=request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        return Response(user_data, status=status.HTTP_201_CREATED)

class LoginUserView(APIView):
    serializer_class = LoginSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class LogoutUserView(APIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

class UserTransactionsView(APIView):
    serializer_class = TransactionModelSeriliazser
    permission_classes = [IsAuthenticated]

class UserSubCategoryView(APIView):        
    def get(self, request):
        user_id = request.GET.get('user_id', '')
        type_id = request.GET.get('type_id', '')
        result = TransactionCategory.objects.filter(
            type=type_id,
            user = User.objects.get(pk=user_id)
        )
        return HttpResponse(django_core_serializers.serialize('json', result),
            content_type='application/json'
        )