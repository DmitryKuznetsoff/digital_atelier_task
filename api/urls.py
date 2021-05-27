from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import BudgetViewSet, GlavBudgetClasstViewSet

router = DefaultRouter()
router.register('budget', BudgetViewSet, 'budget')
router.register('glavbudgetclass', GlavBudgetClasstViewSet, 'glavbudgetclass')

urlpatterns = [
    path('', include(router.urls))
]
