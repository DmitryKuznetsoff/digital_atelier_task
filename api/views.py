from rest_framework import viewsets
from api.models import Budget, GlavBudgetClass
from api.serializers import BudgetSerializer, GlavBudgetClassSerializer


class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer


class GlavBudgetClasstViewSet(viewsets.ModelViewSet):
    queryset = GlavBudgetClass.objects.all()
    serializer_class = GlavBudgetClassSerializer
