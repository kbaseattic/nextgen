outputs=$(patsubst %.asciidoc,%.html,$(wildcard *.asciidoc))
ghdir=../../../../../docs-ghpages/docs

default: local
	
all: local ghpages

ghpages: asciidoc
	mv *.html $(ghdir)
	cp *.png $(ghdir)

local: asciidoc
	@printf "Results in *.html\n"

asciidoc: $(outputs)

$(outputs): %.html:%.asciidoc
	asciidoctor -a toc $<

clean:
	/bin/rm -f $(outputs)
