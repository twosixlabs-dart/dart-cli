#!/bin/bash


if [[ -z "$PYPI_USERNAME" ]]; then
    python3 setup.py build sdist bdist_wheel
    echo "Publishing test package: expect to be prompted for username and password"
    python -m twine upload --repository testpypi dist/*
else
    echo "$GITHUB_SHA"
    git_hash=$(git rev-parse --short "$GITHUB_SHA")
    echo "$git_hash"
    python scripts/manage_version.py update-version -- "-$git_hash"
    python3 setup.py build sdist bdist_wheel
    if grep -q latest app.version; then
        python -m twine upload --repository testpypi --verbose dist/*  -u "$PYPI_USERNAME" -p "$PYPI_PASSWORD"
    else
        python -m twine upload dist/* --verbose -u "$PYPI_USERNAME" -p "$PYPI_PASSWORD"
    fi
fi

