import pytest
from unittest.mock import MagicMock, patch
from grpc_protos import text_processor_pb2
from grpc_protos import text_processor_pb2_grpc
from client import run_client


def test_run_client():
    """Test the run_client function."""
    with patch('grpc.insecure_channel') as mock_channel:
        # Mock the gRPC channel and stub
        mock_stub = MagicMock()
        mock_channel.return_value.__enter__.return_value = mock_stub
        
        # Mock the ProcessText method
        mock_response = MagicMock()
        mock_response.result = "processed text"
        mock_response.status = "success"
        mock_stub.ProcessText.return_value = mock_response
        
        # Mock the stub class
        with patch('grpc_protos.text_processor_pb2_grpc.TextProcessorStub', return_value=mock_stub):
            run_client()

        # Verify the ProcessText method was called with expected inputs
        expected_calls = [
            text_processor_pb2.ProcessRequest(text="hello world"),
            text_processor_pb2.ProcessRequest(text="grpc is awesome"),
            text_processor_pb2.ProcessRequest(text="python text processing")
        ]
        
        actual_calls = [call[0][0] for call in mock_stub.ProcessText.call_args_list]
        
        for expected, actual in zip(expected_calls, actual_calls):
            assert expected.text == actual.text
