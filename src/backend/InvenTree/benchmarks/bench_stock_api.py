"""Benchmark tests for Stock API endpoints."""

import pytest

from InvenTree.unit_test import InvenTreeAPITestCase
from stock.models import StockItem, StockLocation


@pytest.mark.django_db
class TestStockAPIBenchmarks(InvenTreeAPITestCase):
    """Benchmark tests for Stock API operations."""

    fixtures = ['category', 'part', 'location', 'stock']

    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Set up test data."""
        super().setUp()
        self.assignRole('stock.view')
        self.assignRole('stock.change')

    def bench_list_stock_items(self, benchmark):
        """Benchmark listing all stock items."""
        url = '/api/stock/'

        def run_test():
            response = self.client.get(url, format='json')
            return response

        result = benchmark(run_test)
        assert result.status_code == 200

    def bench_get_stock_detail(self, benchmark):
        """Benchmark retrieving a single stock item detail."""
        stock = StockItem.objects.first()
        url = f'/api/stock/{stock.pk}/'

        def run_test():
            response = self.client.get(url, format='json')
            return response

        result = benchmark(run_test)
        assert result.status_code == 200

    def bench_filter_stock_by_location(self, benchmark):
        """Benchmark filtering stock by location."""
        location = StockLocation.objects.first()
        url = f'/api/stock/?location={location.pk}'

        def run_test():
            response = self.client.get(url, format='json')
            return response

        result = benchmark(run_test)
        assert result.status_code == 200

    def bench_stock_statistics(self, benchmark):
        """Benchmark stock statistics calculation."""
        url = '/api/stock/statistics/'

        def run_test():
            response = self.client.get(url, format='json')
            return response

        result = benchmark(run_test)
        assert result.status_code == 200
