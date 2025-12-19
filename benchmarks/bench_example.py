"""
Example benchmarks for InvenTree.

This file demonstrates how to write performance benchmarks using pytest-codspeed.
You can add more benchmarks by creating additional test functions prefixed with 'bench_'.
"""

from codspeed_pytest import Benchmark


def bench_list_comprehension(benchmark: Benchmark):
    """Benchmark list comprehension performance."""

    def run():
        return [i * 2 for i in range(1000)]

    result = benchmark(run)
    assert len(result) == 1000


def bench_string_concatenation(benchmark: Benchmark):
    """Benchmark string concatenation."""

    def run():
        result = ""
        for i in range(100):
            result += str(i)
        return result

    result = benchmark(run)
    assert len(result) > 0


def bench_dict_operations(benchmark: Benchmark):
    """Benchmark dictionary operations."""

    def run():
        data = {}
        for i in range(500):
            data[f"key_{i}"] = i * 2
        return data

    result = benchmark(run)
    assert len(result) == 500
