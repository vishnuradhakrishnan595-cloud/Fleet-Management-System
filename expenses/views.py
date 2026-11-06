from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Expense
from vehicles.models import Vehicle


@login_required
def expense_list(request):
    expenses = Expense.objects.select_related('vehicle', 'recorded_by').order_by('-expense_date')
    return render(request, 'expenses/expense_list.html', {'expenses': expenses})


@login_required
def expense_detail(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    return render(request, 'expenses/expense_detail.html', {'expense': expense})


@login_required
def expense_create(request):
    if request.method == 'POST':
        try:
            Expense.objects.create(
                vehicle_id=request.POST.get('vehicle') or None,
                category=request.POST.get('category'),
                title=request.POST.get('title'),
                amount=request.POST.get('amount'),
                expense_date=request.POST.get('expense_date'),
                description=request.POST.get('description', ''),
                receipt=request.FILES.get('receipt'),
                recorded_by=request.user
            )
            messages.success(request, 'Expense recorded successfully.')
            return redirect('expense_list')
        except Exception as e:
            messages.error(request, f'Unable to record expense: {e}')

    return render(request, 'expenses/expense_create.html', {
        'vehicles': Vehicle.objects.all()
    })


@login_required
def expense_update(request, pk):
    expense = get_object_or_404(Expense, pk=pk)

    if request.method == 'POST':
        try:
            expense.vehicle_id = request.POST.get('vehicle') or None
            expense.category = request.POST.get('category')
            expense.title = request.POST.get('title')
            expense.amount = request.POST.get('amount')
            expense.expense_date = request.POST.get('expense_date')
            expense.description = request.POST.get('description', '')

            if request.FILES.get('receipt'):
                expense.receipt = request.FILES['receipt']

            expense.save()
            messages.success(request, 'Expense updated successfully.')
            return redirect('expense_list')
        except Exception as e:
            messages.error(request, f'Unable to update expense: {e}')

    return render(request, 'expenses/expense_update.html', {
        'expense': expense,
        'vehicles': Vehicle.objects.all()
    })
