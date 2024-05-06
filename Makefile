USE_CONDA ?= 1
INSTALL_SCRIPT = install_with_conda.sh
ifeq (false,$(USE_CONDA))
	INSTALL_SCRIPT = install_with_venv.sh
endif

CONDA_ACTIVATE=source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate ; conda activate
CONDA_ENV=nestle-mroi

.DEFAULT_GOAL = help

# help: help					- Display this makefile's help information
.PHONY: help
help:
	@grep "^# help\:" Makefile | grep -v grep | sed 's/\# help\: //' | sed 's/\# help\://'

# help: install					- Create a virtual environment and install dependencies
.PHONY: install
install:
	@bash bin/$(INSTALL_SCRIPT)

# help: install_precommit			- Install pre-commit hooks
.PHONY: install_precommit
install_precommit:
	@pre-commit install -t pre-commit
	@pre-commit install -t pre-push

# help: serve_docs_locally			- Serve docs locally on port 8001
.PHONY: serve_docs_locally
serve_docs_locally:
	@mkdocs serve --livereload -a localhost:8001

# help: deploy_docs				- Deploy documentation to GitHub Pages
.PHONY: deploy_docs
deploy_docs:
	@mkdocs build
	@mkdocs gh-deploy

.PHONY: upload_wheel
upload_wheel:
	@$(CONDA_ACTIVATE) $(CONDA_ENV) && python setup.py sdist bdist_wheel
	@$(CONDA_ACTIVATE) $(CONDA_ENV) && databricks fs cp  dist/24_finance-$$(cat VERSION)-py3-none-any.whl dbfs:/FileStore/jars/ --overwrite
