
.PHONY: create-venv venv install-uv install-deps


create-venv:
	uv venv

venv: create-venv
	. .venv/bin/activate

install-uv:
	curl -fsSL https://astral.sh/uv/install.sh | sh

install-deps: venv
	uv pip install -r requirements.txt


