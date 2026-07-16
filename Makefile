.PHONY: install install-app install-dev app test audit build serve clean

PYTHON ?= python
PIP ?= $(PYTHON) -m pip

install:
	$(PIP) install -r requirements.txt

install-app:
	$(PIP) install -e . -r requirements-app.txt

install-dev:
	$(PIP) install -e . -r requirements-dev.txt

app:
	$(PYTHON) scripts/iniciar_asistente_triangulos.py

test:
	$(PYTHON) -m unittest discover -s tests -p "test_*.py"

audit:
	$(PYTHON) scripts/audit_docs.py

build:
	$(PYTHON) -m mkdocs build --strict

serve:
	$(PYTHON) -m mkdocs serve

clean:
	rm -rf site
