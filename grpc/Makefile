
COMPILE := protoc
COMPILE_OPTS := -I. --grpc_out=. 
PYTHON_PLUGIN := /usr/local/bin/grpc_python_plugin
PYTHON_OPTS := --python_out=. --plugin=protoc-gen-grpc=$(PYTHON_PLUGIN)

default: python

python: *.proto
	$(COMPILE)  $(PYTHON_OPTS) $(COMPILE_OPTS) $<

clean:
	for f in *.proto; do \
		rm -f `basename $$f .proto`_pb2.py*; \
	done
	rm -f *.pyc
