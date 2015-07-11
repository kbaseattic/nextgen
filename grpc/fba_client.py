import gapfill_model_pb2

import shared, time

_TIMEOUT_SECONDS = 10

def run():
    with gapfill_model_pb2.early_adopter_create_fba_model_stub('localhost', 50051) as stub:
        params = gapfill_model_pb2.GapfillModelParams()
        params.model_id = "my model identifier"
        params.formulation.fba.media_id = "formulation media id"
        for i in range(100):
            bound = params.formulation.fba.bounds.add()
            bound.min, bound.max, bound.varType, bound.variable=0, 100, 'int', 'santy_claws'
        print('[Client] Params: {{\n{}\n}}'.format(params))
        result = stub.gapfill_model(params, _TIMEOUT_SECONDS)
        print('[Client] Result: {{\n{}\n}}'.format(result))
        t0, N = time.time(), 1000
        for i in xrange(N):
            result = stub.gapfill_model(params, _TIMEOUT_SECONDS)
        t1 = time.time()
        dt = t1 - t0
        n = N * 1.0
        print('Ran {:d} iterations in {:.2f} seconds =~ {:d} iter/sec, or {:.3f} ms/iter'
            .format(N, dt, int(round(n / dt)), dt * 1e3 / n))
if __name__ == '__main__':
    run()