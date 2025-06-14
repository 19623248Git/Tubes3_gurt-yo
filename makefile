# Python commands
PYTHON = python
VENV = .\env\Scripts\activate.ps1

# Default target
.PHONY: all
all: check-venv test-extract test-seeder test-search

# Check if running in virtual environment
.PHONY: check-venv
check-venv:
	$(PYTHON) check_venv.py

# Test PDF extraction
.PHONY: test-extract
test-extract: check-venv
	$(PYTHON) test/ExtractCVTest.py data/ACCOUNTANT/10554236.pdf

# Test database seeder
.PHONY: test-seeder
test-seeder: check-venv
	$(PYTHON) test/SeedingTest.py

# Test search strategies
.PHONY: test-search
test-search: check-venv
	$(PYTHON) test/SearchTest.py

# Run the main application
.PHONY: run
run: check-venv
	cd src && $(PYTHON) main.py

# Clean Python cache files
.PHONY: clean
clean:
	powershell "Get-ChildItem -Path . -Filter __pycache__ -Recurse | Remove-Item -Recurse -Force"
	powershell "Get-ChildItem -Path . -Filter *.pyc -Recurse | Remove-Item -Force"
