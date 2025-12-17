# InvenTree Performance Benchmarks

This directory contains performance benchmarks for InvenTree using [CodSpeed](https://codspeed.io/).

## Overview

CodSpeed provides continuous performance monitoring by tracking benchmark results over time. The benchmarks in this directory measure critical performance aspects of InvenTree, including:

- **API Serialization**: Django REST Framework serialization performance
- **Database Queries**: ORM query optimization and database access patterns
- **Utility Functions**: Common helper functions used throughout the application

## Running Benchmarks Locally

### Prerequisites

Install the development dependencies including pytest-codspeed:

```bash
pip install -r src/backend/requirements-dev.txt
```

### Run All Benchmarks

```bash
pytest benchmarks/ --codspeed
```

### Run Specific Benchmark Suite

```bash
# API serialization benchmarks
pytest benchmarks/bench_api_serialization.py --codspeed

# Database query benchmarks
pytest benchmarks/bench_database_queries.py --codspeed

# Utility function benchmarks
pytest benchmarks/bench_utils.py --codspeed
```

### Run Without CodSpeed Instrumentation

To run benchmarks as regular tests without CodSpeed instrumentation:

```bash
pytest benchmarks/
```

## Writing New Benchmarks

### Benchmark Function Naming

Benchmark functions should be prefixed with `test_bench_` to distinguish them from regular tests:

```python
def test_bench_my_feature(benchmark):
    # Your benchmark code here
    result = benchmark(my_function, arg1, arg2)
    assert result is not None
```

### Using Django Database

For benchmarks that require database access, use the `django_db` marker and setup fixtures:

```python
@pytest.mark.django_db
def test_bench_database_operation(benchmark, setup_data):
    def operation():
        return MyModel.objects.filter(active=True).count()
    
    result = benchmark(operation)
    assert result >= 0
```

### Best Practices

1. **Isolate what you're measuring**: Each benchmark should measure a single, well-defined operation
2. **Use realistic data**: Create fixtures that represent typical production data
3. **Avoid side effects**: Benchmarks should be repeatable without affecting each other
4. **Document context**: Add docstrings explaining what each benchmark measures and why it matters

## CI Integration

Benchmarks automatically run in GitHub Actions on:
- Push to main branch
- Pull requests
- Manual workflow dispatch

CodSpeed compares PR benchmarks against the base branch to detect performance regressions before merging.

## Viewing Results

Benchmark results are uploaded to [CodSpeed](https://codspeed.io/) where you can:
- Track performance trends over time
- Compare performance between branches
- Identify performance regressions in pull requests
- View detailed flame graphs and execution profiles

## Learn More

- [CodSpeed Documentation](https://codspeed.io/docs)
- [pytest-codspeed Plugin](https://codspeed.io/docs/reference/pytest-codspeed)
- [Writing Python Benchmarks](https://codspeed.io/docs/benchmarks/python)
