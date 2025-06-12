from google.protobuf.empty_pb2 import Empty
from ppv.v1 import ppv_pb2_grpc
from ppv.v1 import ppv_pb2 as ppv

import grpc
import os
import sys


def main():
    # Create a channel and stub
    channel = grpc.insecure_channel('localhost:50051')
    stub = ppv_pb2_grpc.PPVServiceStub(channel)

    # Example 1: List existing jobs
    print("=== Listing Jobs ===")
    try:
        jobs = stub.ListJobs(Empty())
        print(f"Current job IDs: {jobs.ids}")
    except grpc.RpcError as e:
        print(f"Failed to list jobs: {e}")

    # Example 2: Request and wait for compute
    print("\n=== Compute Request ===")
    comp = ppv.ComputeRequest(
        n_delegate=2,
        n_policy=2,
        n_interm=0,
        matrix=[0.0, 0.1, 0.0, 0.0, 0.2, 0.0, 0.0, 0.0,
                0.8, 0.0, 1.0, 0.0, 0.0, 0.9, 0.0, 1.0]
    )

    try:
        res = stub.RequestCompute(comp)
        compute_job_id = res.job_id
        print(f"Compute job submitted with ID: {compute_job_id}")

        # Wait for compute results
        wait = ppv.WaitRequest(job_id=compute_job_id)

        for status in stub.WaitCompute(wait):
            if status.status == ppv.ComputeStatus.FINISHED:
                print("Compute completed successfully")
                print(f"Consensus: {list(status.consensus)}")
                print(f"Influence: {list(status.influence)}")
                print(f"Iteration: {status.iteration}")
                print(f"Did Converge: {status.did_converge}")
                break
            elif status.status == ppv.ComputeStatus.QUEUED:
                print("Compute job is queued...")
            elif status.status == ppv.ComputeStatus.PROCESSING:
                print("Compute job is being processed...")
    except grpc.RpcError as e:
        print(f"Compute request failed: {e}")

    # Example 3: Request and wait for dot product
    print("\n=== Dot Product Request ===")
    dot_req = ppv.DotRequest(
        size=3,
        a=[1.0, 2.0, 3.0],
        b=[4.0, 5.0, 6.0]
    )

    try:
        dot_res = stub.RequestDot(dot_req)
        dot_job_id = dot_res.job_id
        print(f"Dot product job submitted with ID: {dot_job_id}")

        # Wait for dot product results
        wait_dot = ppv.WaitRequest(job_id=dot_job_id)

        for status in stub.WaitDot(wait_dot):
            if status.status == ppv.DotStatus.FINISHED:
                print("Dot product completed successfully")
                print(f"Output matrix: {list(status.output)}")
                break
            elif status.status == ppv.DotStatus.QUEUED:
                print("Dot product job is queued...")
            elif status.status == ppv.DotStatus.PROCESSING:
                print("Dot product job is being processed...")
    except grpc.RpcError as e:
        print(f"Dot product request failed: {e}")

    channel.close()


if __name__ == "__main__":
    main()
