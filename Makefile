.PHONY: install install-app install-dev app qa-index qa-check qa-benchmark test audit build serve clean

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

qa-check: qa-index
	$(PYTHON) scripts/generate_handbook_qa_knowledge.py --check

qa-benchmark: qa-index
	node scripts/evaluate_handbook_qa_benchmark.js --output-dir artifacts

test: qa-index
	$(PYTHON) -m unittest discover -s tests -p "test_*.py"
	node tests/js/test_handbook_qa_engine.js
	node tests/js/test_handbook_qa_health_method_regression.js
	node tests/js/test_handbook_qa_quality_gate.js
	node tests/js/test_handbook_qa_benchmark.js
	$(PYTHON) scripts/generate_handbook_qa_knowledge.py --check

audit:
	$(PYTHON) scripts/audit_docs.py

build: qa-index
	$(PYTHON) -m mkdocs build --strict

serve: qa-index
	$(PYTHON) -m mkdocs serve

clean:
	rm -rf site
