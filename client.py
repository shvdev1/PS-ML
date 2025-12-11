import grpc
from grpc_protos import text_processor_pb2
from grpc_protos import text_processor_pb2_grpc
import logging


def run_client():
    """Test the TextProcessor gRPC service."""
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = text_processor_pb2_grpc.TextProcessorStub(channel)
        
        # Test cases
        test_inputs = [
            "hello world",
            "grpc is awesome",
            "python text processing"
        ]
        
        logging.info("TextProcessor gRPC Client")
        logging.info("=" * 50)
        
        for text_input in test_inputs:
            request = text_processor_pb2.ProcessRequest(text=text_input)
            response = stub.ProcessText(request)
            logging.info(f"Input:  {text_input}")
            logging.info(f"Output: {response.result}")
            logging.info(f"Status: {response.status}")
            logging.info("-" * 50)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run_client()
