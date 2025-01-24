build:
	hatch build
install:
	pip install --force-reinstall dist/resumaker*.whl
build-install:
	make build
	make install
format:
	black src/
	black tests/
lint:
	python -m flake8 src/
test:
	pytest