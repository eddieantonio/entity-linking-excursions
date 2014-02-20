DOTFLAGS = 
DOT = dot

all: sample.pdf
	open $<

sample.dot: entity_graph.py 
	./$< > $@

%.pdf: %.dot
	$(DOT) $(DOTFLAGS) -Tpdf $< > $*.pdf

.PHONY: all
