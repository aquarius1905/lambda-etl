#!/bin/bash

set -e

echo "Running flake8..."
poetry run flake8 app tests --count --show-source --statistics

echo "Running black..."
poetry run black app tests --check --diff

echo "Running isort..."
poetry run isort app tests