
from datetime import date

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from vehicles.models import Vehicle
from .models import Document


User = get_user_model()


class DocumentModelTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )

        self.vehicle = Vehicle.objects.create(
            vehicle_number='KL07AB1234',
            vehicle_name='Test Truck',
            vehicle_type='truck',
            brand='Tata',
            model='407',
            year=2024,
            fuel_type='diesel',
            capacity=5000,
            registration_date=date(2024, 1, 1),
            insurance_expiry=date(2027, 1, 1),
            status='available'
        )

        self.document = Document.objects.create(
            vehicle=self.vehicle,
            title='Vehicle Insurance',
            document_type='insurance',
            file=SimpleUploadedFile(
                'insurance.pdf',
                b'Test PDF content',
                content_type='application/pdf'
            ),
            uploaded_by=self.user
        )

    def test_document_creation(self):

        self.assertEqual(
            self.document.title,
            'Vehicle Insurance'
        )

    def test_document_string_representation(self):

        self.assertEqual(
            str(self.document),
            'Vehicle Insurance'
        )

    def test_document_vehicle_relationship(self):

        self.assertEqual(
            self.document.vehicle,
            self.vehicle
        )

    def test_document_uploaded_by_relationship(self):

        self.assertEqual(
            self.document.uploaded_by,
            self.user
        )


class DocumentViewTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )

        self.vehicle = Vehicle.objects.create(
            vehicle_number='KL07AB1234',
            vehicle_name='Test Truck',
            vehicle_type='truck',
            brand='Tata',
            model='407',
            year=2024,
            fuel_type='diesel',
            capacity=5000,
            registration_date=date(2024, 1, 1),
            insurance_expiry=date(2027, 1, 1),
            status='available'
        )

        self.document = Document.objects.create(
            vehicle=self.vehicle,
            title='Vehicle Insurance',
            document_type='insurance',
            file=SimpleUploadedFile(
                'insurance.pdf',
                b'Test PDF content',
                content_type='application/pdf'
            ),
            uploaded_by=self.user
        )

        self.client.login(
            username='testuser',
            password='testpassword123'
        )

    def test_document_list_page(self):

        response = self.client.get(
            reverse('documents:document_list')
        )

        self.assertEqual(response.status_code, 200)

    def test_document_detail_page(self):

        response = self.client.get(
            reverse(
                'documents:document_detail',
                args=[self.document.pk]
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_document_create_page(self):

        response = self.client.get(
            reverse('documents:document_create')
        )

        self.assertEqual(response.status_code, 200)

    def test_document_update_page(self):

        response = self.client.get(
            reverse(
                'documents:document_update',
                args=[self.document.pk]
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_document_delete_confirmation_page(self):

        response = self.client.get(
            reverse(
                'documents:document_delete',
                args=[self.document.pk]
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_document_delete(self):

        response = self.client.post(
            reverse(
                'documents:document_delete',
                args=[self.document.pk]
            )
        )

        self.assertRedirects(
            response,
            reverse('documents:document_list')
        )

        self.assertFalse(
            Document.objects.filter(
                pk=self.document.pk
            ).exists()
        )

    def test_document_list_requires_login(self):

        self.client.logout()

        response = self.client.get(
            reverse('documents:document_list')
        )

        self.assertEqual(response.status_code, 302)
