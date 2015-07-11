import gapfill_model_pb2

import time

class FBAServicer(gapfill_model_pb2.EarlyAdopterfba_modelServicer):
	def gapfill_model(self, request, context):
		#print("[Server] Got request: {{\n{}\n}}".format(request))
		# xxx: invoke gapfill, collect result
		meta = gapfill_model_pb2.ModelMetadata()
		# xxx: fill in meta
		return meta

def serve():
	server = gapfill_model_pb2.early_adopter_create_fba_model_server(
		        FBAServicer(), 50051, None, None)
	server.start()
	try:
		while True:
			time.sleep(60*60)
	except KeyboardInterrupt:
		server.stop()

if __name__ == '__main__':
	serve()