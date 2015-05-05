outputs=$(patsubst %.asciidoc,%.html,$(wildcard *.asciidoc))

all: ghpages sharing

ghpages: asciidoc
	mv *.html ../../../../docs-ghpages/docs

asciidoc: $(outputs)

$(outputs): %.html:%.asciidoc
	asciidoctor -a toc $<

sharing:
	cd sharing && make

clean:
	/bin/rm -f $(outputs)
