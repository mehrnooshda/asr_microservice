from concurrent import futures
from urllib import request

from flask import Flask, request, jsonify
from vosk import Model, KaldiRecognizer
import json
import os
from threading import Thread
import logging
from rpc.client import translate_text
import grpc
import translate_pb2_grpc

app = Flask(__name__)

model = Model("model")
logging.basicConfig(level=logging.INFO)

# In-memory task management
tasks = {}


def process_file(task_id, file_path):
    wf = open(file_path, "rb")
    rec = KaldiRecognizer(model, 16000)
    rec.AcceptWaveform(wf.read())
    result = json.loads(rec.FinalResult())
    text = result["text"]
    tasks[task_id]['status'] = 'completed'
    tasks[task_id]['result'] = text


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400


    file_path = os.path.join('files', file.filename)

    if not os.path.exists('files'):
        os.mkdir(os.path.dirname(file_path))
    file.save(file_path)

    task_id = len(tasks) + 1
    tasks[task_id] = {"status": "processing", "result": None}
    thread = Thread(target=process_file, args=(task_id, file_path))
    thread.start()
    return jsonify({"task_id": task_id}), 202


@app.route('/result/<int:task_id>', methods=['GET'])
def get_result(task_id):
    task = tasks.get(task_id)
    if not task:
        return jsonify({"status": "error", "message": "Task not found"}), 404
    translated_text = translate_text(task['status'])

    return jsonify(translated_text)

class TranslationServicer(translate_pb2_grpc.TranslationServiceServicer):
    """Provides methods that implement functionality of route guide server."""

    def __init__(self):
        self.db = translate_pb2_grpc.read_translation_database()
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    translate_pb2_grpc.add_TranslationServiceServicer_to_server(
        TranslationServicer(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    app.run(port=8001, debug=True)
    print("Server")
    serve()
