from django.contrib import admin
from .models import Ticket, TicketResponse


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'priority', 'status', 'created_by', 'created_at')
    list_filter = ('category', 'priority', 'status')
    search_fields = ('title', 'description', 'created_by__username')


@admin.register(TicketResponse)
class TicketResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'ticket', 'author', 'created_at')
    search_fields = ('message', 'author__username', 'ticket__title')
