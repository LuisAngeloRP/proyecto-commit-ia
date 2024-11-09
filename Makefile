SHELL=/bin/sh

install:
	pip install -r requirements.txt

run-all:
	python main.py --mode all --use-ai

run-per-file:
	python main.py --mode per-file --use-ai