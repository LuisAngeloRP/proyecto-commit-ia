SHELL=/bin/sh

init:
	sudo apt-get install python3
	sudo apt-get make

install:
	pip install -r requirements.txt

.PHONY: run

run:
	python main.py --mode $(MODE) $(if $(USE_AI),--use-ai)