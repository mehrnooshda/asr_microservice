from concurrent import futures

import grpc
import translate_pb2
import translate_pb2_grpc
import os
# from rpc.translate_textate_pb2 import TranslateTextRequest
import time
# RouteGuideServicer provides an implementation of the methods of the RouteGuide service.
def translate_text(text):
    # if os.environ.get('https_proxy'):
    #     del os.environ['https_proxy']
    # if os.environ.get('http_proxy'):
    #     del os.environ['http_proxy']
    print("befterer")
    # server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # route_guide_pb2_grpc.add_RouteGuideServicer_to_server(RouteGuideServicer(), server)
    channel = grpc.insecure_channel('[::]:50051', options=(('grpc.enable_http_proxy', 0),))
    time.sleep(10)
    print("efterer")
    stub = translate_pb2_grpc.TranslationServiceStub(channel)
    print(1)
    response = stub.TranslateText(translate_pb2.TranslateTextRequest(text=text))
    print(2)

    return response.text