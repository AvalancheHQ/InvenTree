"""Benchmark tests for database operations."""

import pytest
from django.contrib.auth import get_user_model

from part.models import Part, PartCategory
from stock.models import StockItem, StockLocation


@pytest.mark.django_db(transaction=True)
class TestDatabaseBenchmarks:
    """Benchmark tests for common database operations."""

    fixtures = ['category', 'part', 'location', 'stock']

    def bench_part_query_all(self, benchmark):
        """Benchmark querying all parts."""

        def run_query():
            return list(Part.objects.all())

        result = benchmark(run_query)
        assert len(result) > 0

    def bench_part_filter_by_category(self, benchmark):
        """Benchmark filtering parts by category."""
        category = PartCategory.objects.first()

        def run_query():
            return list(Part.objects.filter(category=category))

        result = benchmark(run_query)
        assert isinstance(result, list)

    def bench_part_with_related_data(self, benchmark):
        """Benchmark querying parts with related data."""

        def run_query():
            return list(
                Part.objects.select_related('category').prefetch_related(
                    'stock_items'
                )
            )

        result = benchmark(run_query)
        assert len(result) > 0

    def bench_stock_item_query_all(self, benchmark):
        """Benchmark querying all stock items."""

        def run_query():
            return list(StockItem.objects.all())

        result = benchmark(run_query)
        assert len(result) > 0

    def bench_stock_filter_by_location(self, benchmark):
        """Benchmark filtering stock by location."""
        location = StockLocation.objects.first()

        def run_query():
            return list(StockItem.objects.filter(location=location))

        result = benchmark(run_query)
        assert isinstance(result, list)

    def bench_stock_with_part_data(self, benchmark):
        """Benchmark querying stock items with part data."""

        def run_query():
            return list(
                StockItem.objects.select_related('part', 'location').prefetch_related(
                    'part__category'
                )
            )

        result = benchmark(run_query)
        assert len(result) > 0
