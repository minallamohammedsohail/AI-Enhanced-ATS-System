# Python 3.12+ Compatibility Fix

## Issue
Python 3.12+ removed the deprecated `imp` module, including `ImpImporter`, which was used by older versions of `setuptools` and `pkg_resources`.

## Solution
Updated all dependencies to versions compatible with Python 3.12+:

1. **setuptools >= 69.0.0**: Latest version that doesn't use `ImpImporter`
2. **Updated all packages**: All dependencies have been updated to their latest compatible versions

## Installation
When installing dependencies, make sure to upgrade setuptools first:

```bash
pip install --upgrade pip setuptools>=69.0.0
pip install -r requirements.txt
```

The setup script and batch files have been updated to automatically handle this.

## Verification
After installation, verify that there are no `ImpImporter` errors by running:

```bash
python -c "import pkg_resources; print('OK')"
```

If this runs without errors, the fix is successful.

