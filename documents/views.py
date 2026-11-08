
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone

from vehicles.models import Vehicle
from .models import Document


@login_required
def document_list(request):

    documents = Document.objects.select_related(
        'vehicle',
        'uploaded_by'
    ).all()

    search = request.GET.get('search', '').strip()
    document_type = request.GET.get('type', '').strip()
    status = request.GET.get('status', '').strip()

    # Search documents
    if search:
        documents = documents.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(vehicle__vehicle_number__icontains=search) |
            Q(vehicle__vehicle_name__icontains=search)
        )

    # Filter by document type
    if document_type:
        documents = documents.filter(
            document_type=document_type
        )

    today = timezone.localdate()

    # Filter by expiry status
    if status == 'expired':
        documents = documents.filter(
            expiry_date__lt=today
        )

    elif status == 'active':
        documents = documents.filter(
            Q(expiry_date__gte=today) |
            Q(expiry_date__isnull=True)
        )

    elif status == 'expiring':
        documents = documents.filter(
            expiry_date__gte=today,
            expiry_date__lte=today + timezone.timedelta(days=30)
        )

    context = {
        'documents': documents,
        'search': search,
        'selected_type': document_type,
        'selected_status': status,
        'document_types': Document.DOCUMENT_TYPES,

        'total_documents': Document.objects.count(),

        'expired_documents': Document.objects.filter(
            expiry_date__lt=today
        ).count(),

        'expiring_documents': Document.objects.filter(
            expiry_date__gte=today,
            expiry_date__lte=today + timezone.timedelta(days=30)
        ).count(),
    }

    return render(
        request,
        'documents/document_list.html',
        context
    )


@login_required
def document_detail(request, pk):

    document = get_object_or_404(
        Document.objects.select_related(
            'vehicle',
            'uploaded_by'
        ),
        pk=pk
    )

    return render(
        request,
        'documents/document_detail.html',
        {'document': document}
    )


@login_required
def document_create(request):

    if request.method == 'POST':

        vehicle_id = request.POST.get('vehicle')
        title = request.POST.get('title', '').strip()
        document_type = request.POST.get('document_type')
        uploaded_file = request.FILES.get('file')

        if not vehicle_id or not title or not document_type or not uploaded_file:

            messages.error(
                request,
                'Please fill in all required fields.'
            )

        else:

            vehicle = get_object_or_404(
                Vehicle,
                pk=vehicle_id
            )

            document = Document.objects.create(
                vehicle=vehicle,
                title=title,
                document_type=document_type,
                file=uploaded_file,
                issue_date=request.POST.get('issue_date') or None,
                expiry_date=request.POST.get('expiry_date') or None,
                description=request.POST.get('description', ''),
                uploaded_by=request.user
            )

            messages.success(
                request,
                'Document uploaded successfully.'
            )

            return redirect(
                'documents:document_detail',
                pk=document.pk
            )

    context = {
        'vehicles': Vehicle.objects.all(),
        'document_types': Document.DOCUMENT_TYPES,
        'page_title': 'Upload Document',
    }

    return render(
        request,
        'documents/document_form.html',
        context
    )


@login_required
def document_update(request, pk):

    document = get_object_or_404(
        Document,
        pk=pk
    )

    if request.method == 'POST':

        vehicle_id = request.POST.get('vehicle')
        title = request.POST.get('title', '').strip()
        document_type = request.POST.get('document_type')

        if not vehicle_id or not title or not document_type:

            messages.error(
                request,
                'Please fill in all required fields.'
            )

        else:

            vehicle = get_object_or_404(
                Vehicle,
                pk=vehicle_id
            )

            document.vehicle = vehicle
            document.title = title
            document.document_type = document_type

            document.issue_date = (
                request.POST.get('issue_date') or None
            )

            document.expiry_date = (
                request.POST.get('expiry_date') or None
            )

            document.description = request.POST.get(
                'description',
                ''
            )

            if request.FILES.get('file'):
                document.file = request.FILES['file']

            document.save()

            messages.success(
                request,
                'Document updated successfully.'
            )

            return redirect(
                'documents:document_detail',
                pk=document.pk
            )

    context = {
        'document': document,
        'vehicles': Vehicle.objects.all(),
        'document_types': Document.DOCUMENT_TYPES,
        'page_title': 'Update Document',
    }

    return render(
        request,
        'documents/document_form.html',
        context
    )


@login_required
def document_delete(request, pk):

    document = get_object_or_404(
        Document,
        pk=pk
    )

    if request.method == 'POST':

        document.delete()

        messages.success(
            request,
            'Document deleted successfully.'
        )

        return redirect(
            'documents:document_list'
        )

    return render(
        request,
        'documents/document_confirm_delete.html',
        {'document': document}
    )
