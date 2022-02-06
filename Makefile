GIT_COMMIT = $(shell git rev-parse --short HEAD)

.DEFAULT_GOAL = help

.PHONY = archive
archive: clean  ## Archive the project using git archive.
	git archive --format=zip --output=gol.zip "$(GIT_COMMIT)"

.PHONY = build
build: clean  ## Build a python wheel for the project.
	python setup.py sdist bdist_wheel

.PHONY = build-all
build-all: clean  ## Build all wheels, and executables for the project.
	python setup.py sdist bdist_wheel
	pyinstaller gol.py

.PHONY = build-exe
build-exe: clean  ## Build an executable for the project using pyinstaller.
	pyinstaller gol.py

.PHONY = clean
clean:  ## Clean up the project directory's build and cache files.
	rm -rf __pycache__ build dist *.egg-info ; \
	rm -f *.spec

.PHONY = format
format:  ## Format the source code with black and isort.
	black gol.py gol_test.py ; \
	isort gol.py gol_test.py

.PHONY = help
help:  ## Print this message and exit.
	@IFS=$$'\n' ; \
	help_lines=(`fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##/:/'`); \
	printf "%-30s %s\n" "target" "help" ; \
	printf "%-30s %s\n" "------" "----" ; \
	for help_line in $${help_lines[@]}; do \
		IFS=$$':' ; \
		help_split=($$help_line) ; \
		help_command=`echo $${help_split[0]} | sed -e 's/^ *//' -e 's/ *$$//'` ; \
		help_info=`echo $${help_split[2]} | sed -e 's/^ *//' -e 's/ *$$//'` ; \
		printf '\033[36m'; \
		printf "%-30s %s" $$help_command ; \
		printf '\033[0m'; \
		printf "%s\n" $$help_info; \
	done

.PHONY = install
install:  ## Install the gol library.
	python -m pip install .

.PHONY = test
test:  ## Test the library.
	pytest
