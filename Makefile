# install the python in the current environment
.PHONY: install
install: | 
	python3 setup.py install


# build the python package
.PHONY: build
build: |
	python3 setup.py build


# remove already built package
.PHONY: clean
clean: |
	rm -rf build dist cqa.egg-info


# clear pycache directories
.PHONY: clear-cache
clear-cache: |
	rm -rf ./**/__pycache__


# clear python cache, remove built package, and install again
.PHONY: all
all: clear-cache clean install

# run all the tests specified in the tests/ directory
.PHONY: test
test: | 
	pytest tests