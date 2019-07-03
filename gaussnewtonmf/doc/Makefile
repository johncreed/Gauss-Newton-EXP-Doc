all: output/gauss_mf.pdf

TEX = $(shell echo *.tex)

output/%.pdf: %.tex $(TEX)
	mkdir -p output
	pdflatex -output-directory=output -shell-escape $<
	bibtex output/$*
	pdflatex -output-directory=output -shell-escape $<
	pdflatex -output-directory=output -shell-escape $<
clean:
	rm -rf output
	find figures -name \*.pdf | xargs rm

bib:
	scp r03944049@linux1.csie.ntu.edu.tw:~cjlin/latex/sdp.bib .
