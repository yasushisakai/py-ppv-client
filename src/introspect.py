#!/usr/bin/env python3

import grpc
from grpc_reflection.v1alpha import reflection_pb2, reflection_pb2_grpc
from ppv.v1 import ppv_pb2_grpc

def introspect_server():
    """Introspect the gRPC server to see available services and methods"""
    
    try:
        # Try to connect
        channel = grpc.insecure_channel('localhost:50051')
        
        # First, let's try gRPC reflection if available
        try:
            reflection_stub = reflection_pb2_grpc.ServerReflectionStub(channel)
            request = reflection_pb2.ServerReflectionRequest()
            request.list_services = ""
            
            responses = reflection_stub.ServerReflectionInfo(iter([request]))
            
            print("=== Available Services (via reflection) ===")
            for response in responses:
                if response.HasField('list_services_response'):
                    for service in response.list_services_response.service:
                        print(f"Service: {service.name}")
                break
                
        except grpc.RpcError as e:
            print(f"Reflection not available: {e.code()}")
            
        # Try our known service
        print("\n=== Testing PPVService methods ===")
        stub = ppv_pb2_grpc.PPVServiceStub(channel)
        
        # Get service descriptor
        service_desc = ppv_pb2_grpc.PPVService
        
        print("Available methods in PPVService:")
        for method_name in dir(stub):
            if not method_name.startswith('_'):
                print(f"  - {method_name}")
                
        channel.close()
        
    except grpc.RpcError as e:
        print(f"Failed to connect to server: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    introspect_server()