from django.conf import settings
from django.db import models


class Ticket(models.Model):
    PRIORITY_LOW = 'low'
    PRIORITY_MEDIUM = 'medium'
    PRIORITY_HIGH = 'high'

    STATUS_OPEN = 'open'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_CLOSED = 'closed'

    CATEGORY_IT = 'it'
    CATEGORY_HR = 'hr'
    CATEGORY_FINANCE = 'finance'
    CATEGORY_GENERAL = 'general'

    PRIORITY_CHOICES = [
        (PRIORITY_LOW, 'Baixa'),
        (PRIORITY_MEDIUM, 'Média'),
        (PRIORITY_HIGH, 'Alta'),
    ]

    STATUS_CHOICES = [
        (STATUS_OPEN, 'Aberto'),
        (STATUS_IN_PROGRESS, 'Em andamento'),
        (STATUS_CLOSED, 'Fechado'),
    ]

    CATEGORY_CHOICES = [
        (CATEGORY_IT, 'TI'),
        (CATEGORY_HR, 'RH'),
        (CATEGORY_FINANCE, 'Financeiro'),
        (CATEGORY_GENERAL, 'Geral'),
    ]

    title = models.CharField(max_length=120)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default=CATEGORY_GENERAL)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default=PRIORITY_MEDIUM)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=STATUS_OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tickets')

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'#{self.id} - {self.title}'


class TicketResponse(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='responses')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ticket_responses')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self) -> str:
        return f'Resposta #{self.id} - Ticket {self.ticket_id}'
