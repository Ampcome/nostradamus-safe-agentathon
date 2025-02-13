PYTHON_EXEC ?= poetry run
RUFF_CMD ?= ruff

help: ## Show all Makefile targets
	@echo "Usage: make [target]"
	@echo "Available targets:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

format: ## Running code formatter: ruff
	@echo "(ruff) Formatting..."
	@if [ "$(filter-out $@,$(MAKECMDGOALS))" ]; then \
		$(PYTHON_EXEC) $(RUFF_CMD) check --select I --fix $(filter-out $@,$(MAKECMDGOALS)); \
		$(PYTHON_EXEC) $(RUFF_CMD) format $(filter-out $@,$(MAKECMDGOALS)); \
	else \
		$(PYTHON_EXEC) $(RUFF_CMD) check --select I --fix .; \
		$(PYTHON_EXEC) $(RUFF_CMD) format .; \
	fi

lint: ## Running the linter: ruff
	@echo "(ruff) Linting..."
	@if [ "$(filter-out $@,$(MAKECMDGOALS))" ]; then \
		$(PYTHON_EXEC) $(RUFF_CMD) check $(filter-out $@,$(MAKECMDGOALS)); \
	else \
		$(PYTHON_EXEC) $(RUFF_CMD) check common_lib server_app celery_app telegram_app; \
	fi

%:
	@: