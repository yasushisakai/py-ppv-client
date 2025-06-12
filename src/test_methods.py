#!/usr/bin/env python3

import grpc
from google.protobuf.empty_pb2 import Empty
from ppv.v1 import ppv_pb2_grpc
from ppv.v1 import ppv_pb2 as ppv


def test_individual_methods():
    """Test each RPC method individually to see which ones are implemented"""

    try:
        channel = grpc.insecure_channel('localhost:50051')
        stub = ppv_pb2_grpc.PPVServiceStub(channel)

        # Test 1: ListJobs
        print("=== Testing ListJobs ===")
        try:
            result = stub.ListJobs(Empty())
            print(f"✓ ListJobs: Success - {len(result.ids)} jobs")
        except grpc.RpcError as e:
            print(f"✗ ListJobs: Failed - {e.code()}: {e.details()}")

        # Test 2: RequestCompute
        print("\n=== Testing RequestCompute ===")
        try:
            req = ppv.ComputeRequest(
                n_delegate=2,
                n_policy=2,
                n_interm=0,
                # row first
                matrix=[0.0, 0.1, 0.0, 0.0,
                        0.2, 0.0, 0.0, 0.0,
                        0.8, 0.0, 1.0, 0.0,
                        0.0, 0.9, 0.0, 1.0]
            )

            result = stub.RequestCompute(req)
            print(f"✓ RequestCompute: Success - Job ID: {result.job_id}")
        except grpc.RpcError as e:
            print(f"✗ RequestCompute: Failed - {e.code()}: {e.details()}")

        # Test 3: RequestDot
        print("\n=== Testing RequestDot ===")
        try:
            req = ppv.DotRequest(
                size=2,
                a=[1.0, 2.0, 3.0, 4.0],
                b=[1.0, 2.0, 3.0, 4.0]
            )
            result = stub.RequestDot(req)
            print(f"✓ RequestDot: Success - Job ID: {result.job_id}")
        except grpc.RpcError as e:
            print(f"✗ RequestDot: Failed - {e.code()}: {e.details()}")

        channel.close()

    except Exception as e:
        print(f"Connection error: {e}")


if __name__ == "__main__":
    test_individual_methods()
