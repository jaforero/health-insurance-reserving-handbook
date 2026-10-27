.PHONY: install install-app install-dev app qa-index test audit build serve clean

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

qa-index:
	$(PYTHON) scripts/generate_handbook_qa_knowledge.py

test: qa-index
	$(PYTHON) -m unittest discover -s tests -p "test_*.py"

audit:
	$(PYTHON) scripts/audit_docs.py

build: qa-index
	$(PYTHON) -m mkdocs build --strict

serve: qa-index
	$(PYTHON) -m mkdocs serve

clean:
	rm -rf site
