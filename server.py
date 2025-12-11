import grpc
import logging
from concurrent import futures
from grpc_protos import text_processor_pb2
from grpc_protos import text_processor_pb2_grpc


def process(text):
    """Mocked process function that transforms text."""
    return text.upper() + " [PROCESSED]"


class TextProcessorServicer(text_processor_pb2_grpc.TextProcessorServicer):
    """Implementation of the TextProcessor service."""

    def ProcessText(self, request, context):
        """Process the input text."""
        try:
            result = process(request.text)
            return text_processor_pb2.ProcessResponse(
                result=result,
                status="success"
            )
        except Exception as e:
            return text_processor_pb2.ProcessResponse(
                result="",
                status=f"error: {str(e)}"
            )


def serve():
    """Start the gRPC server."""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    text_processor_pb2_grpc.add_TextProcessorServicer_to_server(
        TextProcessorServicer(), server
    )
    server.add_insecure_port('[::]:50051')
    logging.info("Starting TextProcessor gRPC server on port 50051...")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve()
