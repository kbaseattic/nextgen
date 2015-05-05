outputs=$(patsubst %.asciidoc,%.html,$(wildcard *.asciidoc))

default: local
	
all: local ghpages

ghpages: asciidoc
	mv *.html ../../../../../docs-ghpages/docs

local: asciidoc
	@printf "Results in *.html\n"

asciidoc: $(outputs)

$(outputs): %.html:%.asciidoc
	asciidoctor -a toc $<

clean:
	/bin/rm -f $(outputs)
