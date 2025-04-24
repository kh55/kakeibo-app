from django.contrib import admin
from .models import Expense, Card, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('date', 'category', 'amount', 'card', 'memo')
    list_filter = ('date', 'category', 'card')
    search_fields = ('category__name', 'memo')

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'created_at', 'updated_at')
    search_fields = ('name', 'number') 