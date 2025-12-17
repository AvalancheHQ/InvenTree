"""
Benchmarks for API serialization performance.

This benchmark suite measures the performance of Django REST Framework
serialization, which is critical for API response times.
"""

import pytest
from django.contrib.auth.models import User
from django.test import RequestFactory

from part.models import Part, PartCategory
from part.serializers import PartSerializer


@pytest.fixture
def setup_data(django_db_setup, django_db_blocker):
    """Create test data for benchmarks."""
    with django_db_blocker.unblock():
        # Create a user
        user = User.objects.get_or_create(username='benchmark_user')[0]
        
        # Create a category
        category = PartCategory.objects.get_or_create(
            name='Benchmark Category',
            defaults={'description': 'Category for benchmarking'}
        )[0]
        
        # Create parts for benchmarking
        parts = []
        for i in range(100):
            part, _ = Part.objects.get_or_create(
                name=f'Benchmark Part {i}',
                defaults={
                    'description': f'Part for benchmarking {i}',
                    'category': category,
                    'active': True,
                    'IPN': f'BM-PART-{i:04d}',
                }
            )
            parts.append(part)
        
        return {'user': user, 'category': category, 'parts': parts}


@pytest.mark.django_db
def test_bench_single_part_serialization(benchmark, setup_data):
    """Benchmark serializing a single Part object."""
    part = setup_data['parts'][0]
    factory = RequestFactory()
    request = factory.get('/')
    request.user = setup_data['user']
    
    def serialize_part():
        serializer = PartSerializer(part, context={'request': request})
        return serializer.data
    
    result = benchmark(serialize_part)
    assert 'pk' in result
    assert result['name'] == part.name


@pytest.mark.django_db
def test_bench_multiple_parts_serialization(benchmark, setup_data):
    """Benchmark serializing multiple Part objects."""
    parts = setup_data['parts'][:50]
    factory = RequestFactory()
    request = factory.get('/')
    request.user = setup_data['user']
    
    def serialize_parts():
        serializer = PartSerializer(parts, many=True, context={'request': request})
        return serializer.data
    
    result = benchmark(serialize_parts)
    assert len(result) == 50
    assert all('pk' in item for item in result)


@pytest.mark.django_db
def test_bench_part_category_serialization(benchmark, setup_data):
    """Benchmark serializing a PartCategory with related parts."""
    from part.serializers import CategorySerializer
    
    category = setup_data['category']
    factory = RequestFactory()
    request = factory.get('/')
    request.user = setup_data['user']
    
    def serialize_category():
        serializer = CategorySerializer(category, context={'request': request})
        return serializer.data
    
    result = benchmark(serialize_category)
    assert 'pk' in result
    assert result['name'] == category.name
