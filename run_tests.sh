#!/bin/bash
set -e

echo "🧪 Running RepoViz Test Suite..."
echo ""

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "Installing test dependencies..."
    pip install -r requirements-test.txt
fi

# Run tests with coverage
echo "Running tests..."
pytest tests/ -v --cov=. --cov-report=term-missing --cov-report=html

echo ""
echo "✅ Tests complete!"
echo "📊 Coverage report: htmlcov/index.html"
