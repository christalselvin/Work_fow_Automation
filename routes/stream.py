from flask import Response
import json
import time
from flask import current_app as app

log_path = 'C:\\windows\\temp\\test.log'


@app.route('/api/log_stream', methods=['GET'])
def log_stream():
    def generate_logs():
        with open(log_path, 'r') as file:
            where = file.tell()
            yield "data: " + json.dumps({"data": file.read()}) + "\n\n"
            while True:
                line = file.readline()
                if not line:
                    time.sleep(0.5)
                    file.seek(where)
                else:
                    where = file.tell()
                    yield "data: " + json.dumps({"data": line}) + "\n\n"
    return Response(generate_logs(), content_type='text/event-stream')
