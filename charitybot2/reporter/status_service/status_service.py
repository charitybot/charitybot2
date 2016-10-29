from flask import Flask, request, json

app = Flask(__name__)

service_address = '127.0.0.1'
service_port = 9000
service_url = 'http://' + service_address
service_full_url = service_url + ':' + str(service_port) + '/'
service_debug_mode = False


def parse_request(req):
    return json.loads(req.data.decode('utf-8'))


@app.route('/')
def index():
    return 'Status Service'


@app.route('/event/<event_name>')
def event(event_name):
    return event_name


@app.route('/destroy')
def destroy():
    shutdown_service()
    return 'Shutting down service'


def start_service():
    app.run(host=service_address, port=service_port, debug=True)


def shutdown_service():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


if __name__ == '__main__':
    start_service()
