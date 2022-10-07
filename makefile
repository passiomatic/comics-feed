all: run 

run: 
	python3 scrape.py -i sources.txt

cli: 
	python3 -i cli.py