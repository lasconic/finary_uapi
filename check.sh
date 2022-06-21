#!/bin/sh
#
# Small script to ensure quality checks pass before submitting a commit/PR.
#
python -m black finary_api
python -m flake8 finary_api
python -m mypy finary_api