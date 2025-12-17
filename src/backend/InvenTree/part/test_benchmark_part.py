"""Performance benchmarks for the Part model.

These benchmarks measure the performance of critical Part operations
using pytest-codspeed for continuous performance tracking.
"""

import pytest

from part.models import Part, PartCategory


@pytest.fixture
def sample_category(db):
    """Create a sample category for testing."""
    return PartCategory.objects.create(
        name='Test Category', description='Category for benchmark testing'
    )


@pytest.fixture
def sample_parts(db, sample_category):
    """Create sample parts for testing."""
    parts = []
    for i in range(100):
        part = Part.objects.create(
            category=sample_category,
            name=f'Test Part {i}',
            description=f'Description for test part {i}',
            IPN=f'IPN-{i:04d}',
            revision='A',
        )
        parts.append(part)
    return parts


@pytest.mark.benchmark
def test_part_creation(sample_category):
    """Benchmark: Creating a new Part instance."""
    part = Part.objects.create(
        category=sample_category,
        name='Benchmark Part',
        description='A part for benchmarking',
        IPN='BENCH-001',
        revision='A',
    )
    assert part.pk is not None


@pytest.mark.benchmark
def test_part_query_by_name(sample_parts):
    """Benchmark: Querying parts by name."""
    results = list(Part.objects.filter(name__icontains='Test Part'))
    assert len(results) > 0


@pytest.mark.benchmark
def test_part_query_by_category(sample_parts, sample_category):
    """Benchmark: Querying parts by category."""
    results = list(Part.objects.filter(category=sample_category))
    assert len(results) == 100


@pytest.mark.benchmark
def test_part_with_related_data(sample_parts):
    """Benchmark: Querying parts with select_related optimization."""
    results = list(Part.objects.select_related('category').all())
    assert len(results) >= 100


@pytest.mark.benchmark
def test_part_bulk_create(sample_category):
    """Benchmark: Bulk creating multiple parts."""
    parts = [
        Part(
            category=sample_category,
            name=f'Bulk Part {i}',
            description=f'Bulk description {i}',
            IPN=f'BULK-{i:04d}',
            revision='A',
        )
        for i in range(50)
    ]
    created = Part.objects.bulk_create(parts)
    assert len(created) == 50


@pytest.mark.benchmark
def test_part_update(sample_parts):
    """Benchmark: Updating a part instance."""
    part = sample_parts[0]
    part.description = 'Updated description for benchmarking'
    part.save()
    assert 'Updated' in part.description


@pytest.mark.benchmark
def test_part_validation(sample_category):
    """Benchmark: Part validation logic."""
    part = Part(
        category=sample_category,
        name='Validation Test Part',
        description='Testing validation performance',
        IPN='VAL-001',
        revision='A',
    )
    part.clean()
    assert part is not None
