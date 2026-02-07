import io
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
from .models import EquipmentDataset, Equipment


class AuthenticationTest(TestCase):
    """Test authentication endpoints."""
    
    def setUp(self):
        self.client = APIClient()
    
    def test_register_user(self):
        """Test user registration."""
        response = self.client.post('/api/auth/register/', {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
    
    def test_login_user(self):
        """Test user login."""
        User.objects.create_user('testuser', 'test@example.com', 'testpass123')
        response = self.client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)


class CSVUploadTest(TestCase):
    """Test CSV upload functionality."""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('testuser', 'test@example.com', 'testpass123')
        self.client.force_authenticate(user=self.user)
    
    def test_upload_valid_csv(self):
        """Test uploading a valid CSV file."""
        csv_content = b"Equipment Name,Type,Flowrate,Pressure,Temperature\nPump-001,Pump,150.5,25.3,45.2\nReactor-001,Reactor,0,15.8,180.5"
        csv_file = SimpleUploadedFile("test.csv", csv_content, content_type="text/csv")
        
        response = self.client.post('/api/upload/', {'file': csv_file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['total_count'], 2)
    
    def test_upload_invalid_format(self):
        """Test uploading non-CSV file."""
        txt_file = SimpleUploadedFile("test.txt", b"some text", content_type="text/plain")
        response = self.client.post('/api/upload/', {'file': txt_file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_dataset_limit(self):
        """Test that only 5 datasets are kept."""
        csv_content = b"Equipment Name,Type,Flowrate,Pressure,Temperature\nPump-001,Pump,150.5,25.3,45.2"
        
        for i in range(7):
            csv_file = SimpleUploadedFile(f"test{i}.csv", csv_content, content_type="text/csv")
            self.client.post('/api/upload/', {'file': csv_file}, format='multipart')
        
        self.assertEqual(EquipmentDataset.objects.filter(user=self.user).count(), 5)


class DatasetAPITest(TestCase):
    """Test dataset API endpoints."""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('testuser', 'test@example.com', 'testpass123')
        self.client.force_authenticate(user=self.user)
        
        # Create a test dataset
        self.dataset = EquipmentDataset.objects.create(
            user=self.user,
            filename='test.csv',
            total_count=2,
            avg_flowrate=75.25,
            avg_pressure=20.55,
            avg_temperature=112.85
        )
        Equipment.objects.create(
            dataset=self.dataset,
            name='Pump-001',
            equipment_type='Pump',
            flowrate=150.5,
            pressure=25.3,
            temperature=45.2
        )
        Equipment.objects.create(
            dataset=self.dataset,
            name='Reactor-001',
            equipment_type='Reactor',
            flowrate=0,
            pressure=15.8,
            temperature=180.5
        )
    
    def test_list_datasets(self):
        """Test listing datasets."""
        response = self.client.get('/api/datasets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_get_dataset_detail(self):
        """Test getting dataset details."""
        response = self.client.get(f'/api/datasets/{self.dataset.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['equipment_items']), 2)
    
    def test_get_dataset_summary(self):
        """Test getting dataset summary."""
        response = self.client.get(f'/api/datasets/{self.dataset.id}/summary/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('type_distribution', response.data)
        self.assertEqual(response.data['type_distribution']['Pump'], 1)


class PDFReportTest(TestCase):
    """Test PDF report generation."""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('testuser', 'test@example.com', 'testpass123')
        self.client.force_authenticate(user=self.user)
        
        self.dataset = EquipmentDataset.objects.create(
            user=self.user,
            filename='test.csv',
            total_count=1,
            avg_flowrate=150.5,
            avg_pressure=25.3,
            avg_temperature=45.2
        )
        Equipment.objects.create(
            dataset=self.dataset,
            name='Pump-001',
            equipment_type='Pump',
            flowrate=150.5,
            pressure=25.3,
            temperature=45.2
        )
    
    def test_generate_pdf_report(self):
        """Test PDF report generation."""
        response = self.client.get(f'/api/datasets/{self.dataset.id}/report/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'application/pdf')
