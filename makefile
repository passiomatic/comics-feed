all: run 

run: 
	python3 scrape.py -i sources.txt

repl: 
	python3 -i repl.py