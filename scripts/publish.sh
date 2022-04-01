#!/bin/bash

python3 setup.py build sdist bdist_wheel

if [[ -z "$PYPI_USERNAME" ]]; then
    echo "Publishing test package: expect to be prompted for username and password"
    python -m twine upload --repository testpypi dist/*
else
    if grep -q latest app.version; then
        python -m twine upload --repository testpypi --verbose dist/*  -u "$PYPI_USERNAME" -p "$PYPI_PASSWORD"
    else
        python -m twine upload dist/* --verbose -u "$PYPI_USERNAME" -p "$PYPI_PASSWORD"
    fi
fi

