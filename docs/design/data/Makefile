outputs=$(patsubst %.asciidoc,%.html,$(wildcard *.asciidoc))

all: asciidoc

asciidoc: $(outputs)

$(outputs): %.html:%.asciidoc
	asciidoctor -a toc $<

clean:
	/bin/rm -f $(outputs)
