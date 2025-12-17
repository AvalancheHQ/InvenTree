"""
Benchmarks for database query performance.

This benchmark suite measures database query optimization,
which is critical for overall application performance.
"""

import pytest
from django.contrib.auth.models import User

from part.models import Part, PartCategory
from stock.models import StockItem, StockLocation


@pytest.fixture
def setup_inventory_data(django_db_setup, django_db_blocker):
    """Create inventory test data for benchmarks."""
    with django_db_blocker.unblock():
        user = User.objects.get_or_create(username='bench_inventory_user')[0]
        
        # Create categories and parts
        categories = []
        for i in range(10):
            cat, _ = PartCategory.objects.get_or_create(
                name=f'Bench Category {i}',
                defaults={'description': f'Category {i}'}
            )
            categories.append(cat)
        
        # Create parts
        parts = []
        for i in range(50):
            part, _ = Part.objects.get_or_create(
                name=f'Inventory Part {i}',
                defaults={
                    'description': f'Part for inventory benchmarking {i}',
                    'category': categories[i % 10],
                    'active': True,
                }
            )
            parts.append(part)
        
        # Create stock locations
        locations = []
        for i in range(10):
            loc, _ = StockLocation.objects.get_or_create(
                name=f'Bench Location {i}',
                defaults={'description': f'Location {i}'}
            )
            locations.append(loc)
        
        # Create stock items
        stock_items = []
        for i, part in enumerate(parts):
            item, _ = StockItem.objects.get_or_create(
                part=part,
                location=locations[i % 10],
                defaults={'quantity': 100}
            )
            stock_items.append(item)
        
        return {
            'user': user,
            'categories': categories,
            'parts': parts,
            'locations': locations,
            'stock_items': stock_items
        }


@pytest.mark.django_db
def test_bench_part_query_with_category(benchmark, setup_inventory_data):
    """Benchmark querying parts with select_related for category."""
    def query_parts():
        return list(Part.objects.select_related('category').all()[:50])
    
    result = benchmark(query_parts)
    assert len(result) > 0


@pytest.mark.django_db
def test_bench_stock_items_with_prefetch(benchmark, setup_inventory_data):
    """Benchmark querying stock items with prefetch_related."""
    def query_stock_items():
        return list(
            StockItem.objects
            .select_related('part', 'location')
            .prefetch_related('part__category')
            .all()[:50]
        )
    
    result = benchmark(query_stock_items)
    assert len(result) > 0


@pytest.mark.django_db
def test_bench_part_filtering(benchmark, setup_inventory_data):
    """Benchmark filtering parts by active status."""
    def filter_active_parts():
        return list(Part.objects.filter(active=True).all()[:50])
    
    result = benchmark(filter_active_parts)
    assert len(result) > 0


@pytest.mark.django_db
def test_bench_aggregate_stock_quantity(benchmark, setup_inventory_data):
    """Benchmark aggregating stock quantities."""
    from django.db.models import Sum
    
    def aggregate_stock():
        return StockItem.objects.aggregate(total=Sum('quantity'))
    
    result = benchmark(aggregate_stock)
    assert 'total' in result
