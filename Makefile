DEFAULT_PYTHON_VERSION=3.12.2
PYENV_VIRTUALENV_NAME=splitwise

.PHONY: clean
clean:
	pyenv uninstall -f $(PYENV_VIRTUALENV_NAME) || true
	rm .python-version || true

.PHONY: setup_pyenv
setup_pyenv:
	brew list -q pyenv || brew install pyenv

.PHONY: setup_pyenv_virtualenv
setup_pyenv_virtualenv: setup_pyenv
	brew list -q pyenv-virtualenv || brew install pyenv-virtualenv

.PHONY: install_pyenv_python
install_python: setup_pyenv_virtualenv
	pyenv install -s $(DEFAULT_PYTHON_VERSION);

.PHONY: setup_venv
setup_venv: install_python
	pyenv virtualenv -f $(DEFAULT_PYTHON_VERSION) $(PYENV_VIRTUALENV_NAME) && \
	pyenv local $(PYENV_VIRTUALENV_NAME)

.PHONY: setup_poetry
setup_poetry: setup_venv
	pip install poetry

.PHONY: install
install: setup_poetry
	poetry install