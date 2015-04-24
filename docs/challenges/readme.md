# KBase Challenges

This directory contains documents describing current challenges within KBase.
The top-level document, `challenges.asciidoc`, includes all the other documents.

## About AsciiDoc

Due to its flexilibility and ability to render nicely as a real document, we are using (or at least trying) [AsciiDoc](http://www.methods.co.nz/asciidoc/) as the text format for these documents. Note that GitHub also natively understands AsciiDoc and therefore should be able to render the pages for browsing (even the file inclusion functionality is supported in a basic form).

To _locally_ generate documentation in any format supported by AsciiDoc, first [install AsciiDoc](http://www.methods.co.nz/asciidoc/INSTALL.html), change to the directory with the `challenges.asciidoc` file, and run the  `asciidoc` command. For example, to generate HTML with a table of contents, run:

    asciidoc -a toc challenges.asciidoc

This will create a file named `challenges.html` that you can load into your browser.