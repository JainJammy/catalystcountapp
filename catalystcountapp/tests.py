from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user_model
from django.urls import reverse
"""created unit test cases for file upload and query builder and add users display records and delete users """


from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from catalystcountapp.models import Company  # Assuming Company is your model

class FileUploadTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.upload_url = reverse('upload_file')  # Update with your URL name

    def test_file_upload(self):
        # Create a small sample CSV file for testing
        sample_csv_content = """name,industry,year_founded,city,state,country,employees
        Company1,ITTechnology,2005,CityA,StateA,CountryA,50
        Company2,Finance,2010,CityB,StateB,CountryB,100
        """
        sample_csv = SimpleUploadedFile(
            "sample_data.csv",
            sample_csv_content.encode(),
            content_type="text/csv"
        )
        
        response = self.client.post(self.upload_url, {'file': sample_csv})
        self.assertEqual(response.status_code, 302)  # Assuming redirect on success
        self.assertEqual(Company.objects.count(), 2)

class QueryBuilderTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.query_url = reverse('query_companies')
        # Create sample data
        Company.objects.create(
            name="Test Company 1",
            industry="Technology",
            year_founded=2000,
            city="CityA",
            state="StateA",
            country="CountryA",
            employees=50
        )
        Company.objects.create(
            name="Test Company 2",
            industry="Finance",
            year_founded=2010,
            city="CityB",
            state="StateB",
            country="CountryB",
            employees=100
        )

    def test_query_no_filters(self):
        response = self.client.get(self.query_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)

    def test_query_with_industry_filter(self):
        response = self.client.get(self.query_url, {'industry': 'Technology'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)

    def test_query_with_year_founded_filter(self):
        response = self.client.get(self.query_url, {'year_founded': 2000})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)

    def test_query_with_employees_range_filter(self):
        response = self.client.get(self.query_url, {'employees_from': 50, 'employees_to': 150})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)

class AddUserTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.add_user_url = reverse('add_user')  # Update with your URL name
        self.User = get_user_model()
        self.test_user_data = {
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'password12345',
            'password2': 'password12345'
        }

    def test_add_user(self):
        response = self.client.post(self.add_user_url, self.test_user_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.User.objects.filter(email='testuser@example.com').exists())
        user = self.User.objects.get(email='testuser@example.com')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
class DeleteUserTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.User = get_user_model()
        self.test_user = self.User.objects.create_user(
            email='deleteuser@example.com',
            first_name='Delete',
            last_name='User',
            password='password12345'
        )
        self.delete_user_url = reverse('delete_user', args=[self.test_user.id])  # Update with your URL name and args

    def test_delete_user(self):
        response = self.client.delete(self.delete_user_url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.User.objects.filter(email='deleteuser@example.com').exists())
