mkdir -p src/ppv/v1

python3 -m grpc_tools.protoc \
  --proto_path=proto \
  --python_out=src \
  --grpc_python_out=src \
  proto/ppv/v1/ppv.proto
