"""Performance benchmarks for Part API endpoints.

These benchmarks measure the performance of API operations
using pytest-codspeed for continuous performance tracking.
"""

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from part.models import Part, PartCategory

User = get_user_model()


@pytest.fixture
def api_client(db):
    """Create an authenticated API client."""
    user = User.objects.create_user(
        username='benchmark_user', password='testpass123', is_staff=True
    )
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def sample_category(db):
    """Create a sample category for testing."""
    return PartCategory.objects.create(
        name='API Test Category', description='Category for API benchmark testing'
    )


@pytest.fixture
def sample_parts(db, sample_category):
    """Create sample parts for API testing."""
    parts = []
    for i in range(50):
        part = Part.objects.create(
            category=sample_category,
            name=f'API Part {i}',
            description=f'API Description {i}',
            IPN=f'API-{i:04d}',
            revision='A',
        )
        parts.append(part)
    return parts


@pytest.mark.benchmark
def test_api_part_list(api_client, sample_parts):
    """Benchmark: Fetching list of parts via API."""
    response = api_client.get('/api/part/')
    assert response.status_code == 200


@pytest.mark.benchmark
def test_api_part_detail(api_client, sample_parts):
    """Benchmark: Fetching a single part detail via API."""
    part = sample_parts[0]
    response = api_client.get(f'/api/part/{part.pk}/')
    assert response.status_code == 200


@pytest.mark.benchmark
def test_api_part_create(api_client, sample_category):
    """Benchmark: Creating a part via API."""
    data = {
        'category': sample_category.pk,
        'name': 'New API Part',
        'description': 'Created via API benchmark',
        'IPN': 'API-NEW-001',
        'revision': 'A',
    }
    response = api_client.post('/api/part/', data, format='json')
    assert response.status_code in [200, 201]


@pytest.mark.benchmark
def test_api_part_filter_by_category(api_client, sample_parts, sample_category):
    """Benchmark: Filtering parts by category via API."""
    response = api_client.get(f'/api/part/?category={sample_category.pk}')
    assert response.status_code == 200


@pytest.mark.benchmark
def test_api_part_search(api_client, sample_parts):
    """Benchmark: Searching parts via API."""
    response = api_client.get('/api/part/?search=API Part')
    assert response.status_code == 200
