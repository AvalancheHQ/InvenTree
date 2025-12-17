"""Benchmark tests for Part API endpoints."""

import pytest
from django.contrib.auth import get_user_model

from InvenTree.unit_test import InvenTreeAPITestCase
from part.models import Part, PartCategory


@pytest.mark.django_db
class TestPartAPIBenchmarks(InvenTreeAPITestCase):
    """Benchmark tests for Part API operations."""

    fixtures = ['category', 'part', 'location']

    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Set up test data."""
        super().setUp()
        self.assignRole('part.view')
        self.assignRole('part.change')

    def bench_list_parts(self, benchmark):
        """Benchmark listing all parts."""
        url = '/api/part/'

        def run_test():
            response = self.client.get(url, format='json')
            return response

        result = benchmark(run_test)
        assert result.status_code == 200

    def bench_get_part_detail(self, benchmark):
        """Benchmark retrieving a single part detail."""
        part = Part.objects.first()
        url = f'/api/part/{part.pk}/'

        def run_test():
            response = self.client.get(url, format='json')
            return response

        result = benchmark(run_test)
        assert result.status_code == 200

    def bench_filter_parts_by_category(self, benchmark):
        """Benchmark filtering parts by category."""
        category = PartCategory.objects.first()
        url = f'/api/part/?category={category.pk}'

        def run_test():
            response = self.client.get(url, format='json')
            return response

        result = benchmark(run_test)
        assert result.status_code == 200

    def bench_search_parts(self, benchmark):
        """Benchmark searching parts by name."""
        url = '/api/part/?search=widget'

        def run_test():
            response = self.client.get(url, format='json')
            return response

        result = benchmark(run_test)
        assert result.status_code == 200
