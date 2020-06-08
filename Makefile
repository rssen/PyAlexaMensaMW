VERBOSE ?=@

python-packages := handler

.PHONY: check check_black check_mypy check_pylint package

check: check_black check_pylint check_mypy

check_black:
	black -l 100 --check $(python-packages)

check_pylint:
	pylint $(python-packages)

check_mypy:
	mypy $(python-packages)

format:
	black -l 100 $(python-packages)

package:
	cp ./dependencies/dependencies.zip .
	zip -gr dependencies.zip handler
	mv dependencies.zip skill.zip
