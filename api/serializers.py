from rest_framework import serializers

from api.models import Budget, GlavBudgetClass


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'


class GlavBudgetClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlavBudgetClass
        fields = '__all__'
