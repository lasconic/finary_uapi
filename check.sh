#!/bin/sh
#
# Small script to ensure quality checks pass before submitting a commit/PR.
#
python -m black finary_uapi tests
python -m flake8 finary_uapi tests
python -m mypy finary_uapi tests