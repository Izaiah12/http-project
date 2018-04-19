from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import os
import socket  # BSD socket interface
import sys  # access system arguments with sys.argv and use sys.exit() to provide Unix exit codes


def create_response(file, file_name, response_code, s):
    response_type = 'HTTP/1.1 ' + response_code + '\n'

    response_headers = ''
    headers = ['Date', 'Server', 'Content-Type', 'Connection']
    now = datetime.now()
    timestamp = mktime(now.timetuple())
    date = format_date_time(timestamp)
    server = s.gethostname()
    content_type = file_name.split('.')[1]
    header_values = [date, server, content_type, 'Closed']
    response_code = int(response_code[:3])
    if response_code == 200:
        headers.insert(2, 'Last-Modified')
        headers.insert(4, 'Content-Length')
        modified-timestamp = os.path.getmtime(file_name)
        modified-date = format_date_time(modified-timestamp)
        content_length = str(os.path.getsize(file_name))
        header_values.insert(2, modified-date)
        header_values.insert(4, content_length)
        header_values[3] = 'text/html'
    for i in range(0, len(headers)-1):
        response_headers += headers[i] + ': ' + header_values[i] + '\n'
    response_headers += '\n'

    if response_code == 200:
        response_body = file.read() + '\n'
    else:
        response_body = ''

    response = response_type + response_headers + response_body
    return response


def http_server(port):
    # ensure that the argument is a port number >= 1024
    if not port >= 1024:
        sys.exit('Can not use reserved ports')

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('murphy.wot.eecs.northwestern.edu', port))
    s.listen(1)

    while True:
        accept_socket, address = s.accept()
        file_name = parse(accept_socket)
        file, response_code = retrieve(file_name)

        response = create_response(file, file_name, response_code, s)
        accept_socket.sendall(response)

        accept_socket.close()


def parse(accept_socket):
    request = accept_socket.recv(8192)
    file_name = request[5:].split(' ')[0]
    if file_name == '':
        file_name = 'index.html'
    elif '.' not in file_name:
        file_name += '.html'
    return file_name


def retrieve(file_name):
    file_type = file_name.split('.')[1]
    if file_type == 'html' or file_type == 'htm':
        if os.path.isfile(file_name):
            file = open(file_name, 'r')
            return file, '200 OK'
        else:
            return None, '404 Not Found'
    else:
        return None, '415 Unsupported Media Type'


def main():
    # check that 1 argument is given in addition to the .py file name
    # if so, attempt to host an HTTP server using the argument as the port number
    # if not, exit with a non-zero exit code
    if len(sys.argv) == 2:
        http_server(int(sys.argv[1]))
    else:
        sys.exit('Must provide 1 port number argument')


if __name__ == '__main__':
    main()
