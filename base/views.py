from django.http import HttpResponse
from django.core import serializers as django_core_serializers
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.exceptions import ParseError
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

class UserTransactionCategoryView(APIView):
    serializer_class = TransactionCategorySeriliazer
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            category = TransactionCategory.objects.get(user=request.user)
            serializer = self.serializer_class(data=category, many=True)
            return Response(serializer, status=status.HTTP_200_OK)
        except Exception as e:
            raise ParseError(e)
    def post(self, request):
        try:
            pass
        except Exception as e:
            raise ParseError(e)
    def patch(self, request):
        try:
            id = request.GET.get('id')
        except Exception as e:
            raise ParseError(e)

class UserTransactionsView(APIView):
    serializer_class = TransactionModelSeriliazser
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            transactions = TransactionModel.objects.filter(user=request.user)
            serializer = self.serializer_class(data=transactions, many=True)
            serializer.is_valid()
            return Response(serializer.data)
        except Exception as e:
            raise ParseError(e)
    def post(self, request):
        try:
            data = request.data
            transaction_type = TransactionType.objects.get(
                type=data['type']
            )
            transaction_category = TransactionCategory.objects.filter(
                user=request.user,
                name=data['category']
            )
            transaction = TransactionModel.objects.create(
                user = request.user,
                type = transaction_type,
                category = transaction_category.first(),
                amount = data['amount'],
                note = data['note'],
                date = data['date']
            )
            serializer = self.serializer_class(transaction, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            raise ParseError(e)
    def delete(self, request):
        try:
            id = request.GET.get('id')
            transaction = TransactionModel.objects.get(id=id)
            transaction.delete()
            return Response({
                "detail": "successfuly deleted a transaction"
            }, status=status.HTTP_200_OK)
        except Exception as e:
            raise ParseError(e)

class UserTransactionDetailView(APIView):
    serializer_class = TransactionModelSeriliazser
    permission_classes = [IsAuthenticated]
    def get_object(self, id):
        return get_object_or_404(TransactionModel, pk=id)
    def get(self, request):
        try:
            id = request.GET.get('id')
            transaction = self.get_object(id)
            serializer = self.serializer_class(transaction, many=False)
            return Response(serializer.data)
        except Exception as e:
            raise ParseError(e)
    def patch(self, request):
        try:
            data = request.data
            id = request.GET.get('id')
            transaction = TransactionModel.objects.get(id=id)
            if data.get("type") is not None:
                transaction_type = TransactionType.objects.get(
                    type=data['type']
                )
                transaction.type = transaction_type
            if data.get("category") is not None:
                transaction_category = TransactionCategory.objects.filter(
                    user=request.user,
                    name=data['category']
                )
                transaction.category = transaction_category
            transaction.amount = data.get("amount", transaction.amount)
            transaction.note = data.get("note", transaction.note)
            transaction.date = data.get("date", transaction.date)
            transaction.save()
            serializer = self.serializer_class(transaction, many=False)
            return Response({
                'detail': 'successfuly updated a transaction',
                'transaction': serializer.data
            })
        except Exception as e:
            raise ParseError(e)

class UserSubCategoryView(APIView):        
    def get(self, request):
        user_id = request.GET.get('user_id', '')
        type_id = request.GET.get('type_id', '')
        result = TransactionCategory.objects.filter(
            type=type_id,
            user = User.objects.get(pk=user_id)
        )
        return HttpResponse(
            django_core_serializers.serialize('json', result),
            content_type='application/json'
        )