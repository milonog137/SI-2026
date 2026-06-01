PYTHON ?= python3
CASE_ID ?= c1_supported_quiz_scope
LABEL ?= before_intervention

.PHONY: doctor test ask check run-all snapshot

doctor:
	$(PYTHON) run.py doctor

test:
	$(PYTHON) -m unittest discover -s tests

ask:
	$(PYTHON) run.py ask --case $(CASE_ID)

check:
	$(PYTHON) run.py check --case $(CASE_ID)

run-all:
	$(PYTHON) run.py run-all

snapshot:
	$(PYTHON) run.py snapshot --case $(CASE_ID) --label $(LABEL)
