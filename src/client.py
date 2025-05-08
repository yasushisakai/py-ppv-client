# from google.protobuf.empty_pb2 import Empty
from ppv.v1 import ppv_pb2_grpc
from ppv.v1 import ppv_pb2 as ppv

import grpc
import os
import sys

HERE = os.path.dirname(__file__)              # …/src
sys.path.insert(0, HERE)                      # for "import gen…"
sys.path.insert(0, os.path.join(HERE, 'gen'))  # for "import ppv.v1…"

channel = grpc.insecure_channel('localhost:50051')
stub = ppv_pb2_grpc.PPVServiceStub(channel)

# if you want to list the jobs:
# jobs = stub.ListJobs(Empty())

comp = ppv.ComputeRequest(
    n_delegate=2,
    n_policy=2,
    n_interm=0,
    matrix=[0.0, 0.1, 0.0, 0.0, 0.2, 0.0, 0.0, 0.0,
            0.8, 0.0, 1.0, 0.0, 0.0, 0.9, 0.0, 1.0]
)

res = stub.RequestCompute(comp)

job_id = res.job_id

wait = ppv.WaitRequest(
    job_id=job_id
)

for res in stub.WaitCompute(wait):
    if res.status == ppv.ComputeStatus.FINISHED:
        print("Compute completed successfully")
        print(f"Consensus: {res.consensus}")
        print(f"Influence: {res.influence}")
        print(f"Iteration: {res.iteration}")
        print(f"Did Converge: {res.did_converge}")
