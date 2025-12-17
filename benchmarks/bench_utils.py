"""
Benchmarks for utility functions.

This benchmark suite measures performance of common utility
functions used throughout the InvenTree application.
"""

import pytest

from InvenTree.helpers import str2bool, normalize, decimal2string


def test_bench_str2bool_conversion(benchmark):
    """Benchmark string to boolean conversion."""
    test_values = ['true', 'false', 'yes', 'no', '1', '0', 'True', 'False']
    
    def convert_strings():
        return [str2bool(val) for val in test_values]
    
    result = benchmark(convert_strings)
    assert len(result) == len(test_values)


def test_bench_normalize_string(benchmark):
    """Benchmark string normalization."""
    test_string = '  Test String With   Multiple   Spaces  '
    
    def normalize_text():
        return normalize(test_string)
    
    result = benchmark(normalize_text)
    assert isinstance(result, str)


def test_bench_decimal_to_string(benchmark):
    """Benchmark decimal to string conversion."""
    from decimal import Decimal
    
    test_decimals = [Decimal(str(i / 10.0)) for i in range(100)]
    
    def convert_decimals():
        return [decimal2string(d) for d in test_decimals]
    
    result = benchmark(convert_decimals)
    assert len(result) == len(test_decimals)


def test_bench_multiple_normalize_operations(benchmark):
    """Benchmark multiple string normalization operations."""
    test_strings = [f'  String {i}  with   spaces  ' for i in range(50)]
    
    def normalize_multiple():
        return [normalize(s) for s in test_strings]
    
    result = benchmark(normalize_multiple)
    assert len(result) == 50
