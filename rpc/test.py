import grpc

def test_connection():
    channel = grpc.insecure_channel('[::]:50051')
    try:
        grpc.channel_ready_future(channel).result(timeout=10)
        print("Connected to gRPC server")
    except grpc.FutureTimeoutError:
        print("Failed to connect to gRPC server")
    finally:
        channel.close()

if __name__ == '__main__':
    test_connection()