from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db import models
from django.db.models import Count
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import TicketForm, TicketResponseForm, TicketStatusForm, RegisterForm
from .models import Ticket


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
def dashboard(request):
    if request.user.is_staff:
        tickets = Ticket.objects.all()
    else:
        tickets = Ticket.objects.filter(created_by=request.user)

    counts = tickets.aggregate(
        total=Count('id'),
        open=Count('id', filter=models.Q(status=Ticket.STATUS_OPEN)),
        closed=Count('id', filter=models.Q(status=Ticket.STATUS_CLOSED)),
    )

    latest = tickets.select_related('created_by')[:5]

    context = {
        'counts': counts,
        'latest_tickets': latest,
    }
    return render(request, 'tickets/dashboard.html', context)


@login_required
def ticket_list(request):
    if request.user.is_staff:
        tickets = Ticket.objects.select_related('created_by').all()
    else:
        tickets = Ticket.objects.select_related('created_by').filter(created_by=request.user)

    status_filter = request.GET.get('status')
    priority_filter = request.GET.get('priority')

    if status_filter:
        tickets = tickets.filter(status=status_filter)
    if priority_filter:
        tickets = tickets.filter(priority=priority_filter)

    context = {
        'tickets': tickets,
        'status_filter': status_filter or '',
        'priority_filter': priority_filter or '',
        'status_choices': Ticket.STATUS_CHOICES,
        'priority_choices': Ticket.PRIORITY_CHOICES,
    }
    return render(request, 'tickets/ticket_list.html', context)


@login_required
def ticket_create(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            return redirect('ticket_detail', ticket_id=ticket.id)
    else:
        form = TicketForm()

    return render(request, 'tickets/ticket_form.html', {'form': form})


@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket.objects.select_related('created_by'), id=ticket_id)

    if not request.user.is_staff and ticket.created_by != request.user:
        return HttpResponseForbidden('Você não tem permissão para ver este chamado.')

    response_form = TicketResponseForm()
    status_form = TicketStatusForm(instance=ticket)

    if request.method == 'POST':
        if 'response_submit' in request.POST:
            if ticket.status == Ticket.STATUS_CLOSED and not request.user.is_staff:
                return HttpResponseForbidden('Chamado fechado não pode receber resposta de usuário comum.')

            response_form = TicketResponseForm(request.POST)
            if response_form.is_valid():
                response = response_form.save(commit=False)
                response.ticket = ticket
                response.author = request.user
                response.save()
                return redirect('ticket_detail', ticket_id=ticket.id)

        if 'status_submit' in request.POST and request.user.is_staff:
            status_form = TicketStatusForm(request.POST, instance=ticket)
            if status_form.is_valid():
                status_form.save()
                return redirect('ticket_detail', ticket_id=ticket.id)

    context = {
        'ticket': ticket,
        'response_form': response_form,
        'status_form': status_form,
    }
    return render(request, 'tickets/ticket_detail.html', context)


@login_required
def ticket_updates(request, ticket_id):
    ticket = get_object_or_404(Ticket.objects.select_related('created_by'), id=ticket_id)

    if not request.user.is_staff and ticket.created_by != request.user:
        return HttpResponseForbidden('Você não tem permissão para ver este chamado.')

    responses = []
    for response in ticket.responses.select_related('author').all():
        role = 'Atendente' if response.author.is_staff else 'Solicitante'
        created_at = timezone.localtime(response.created_at).strftime('%d/%m/%Y %H:%M')
        responses.append({
            'author': response.author.username,
            'role': role,
            'created_at': created_at,
            'message': response.message,
        })

    return JsonResponse({
        'status': ticket.status,
        'status_label': ticket.get_status_display(),
        'responses': responses,
    })
