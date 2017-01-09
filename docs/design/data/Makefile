outputs=$(patsubst %.asciidoc,%.html,$(wildcard *.asciidoc))

all: ghpages

ghpages: asciidoc
	mv *.html ../../../../docs-ghpages/docs

asciidoc: $(outputs)

$(outputs): %.html:%.asciidoc
	asciidoctor -a toc $<

clean:
	/bin/rm -f $(outputs)
