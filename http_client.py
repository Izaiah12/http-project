import socket  # BSD socket interface
import sys  # access system arguments with sys.argv and use sys.exit() to provide Unix exit codes


def http_get(address):
    # ensure that the argument is an HTTP address
    # if not, exit with a non-zero exit code
    if not address.startswith('http://'):
        sys.exit('Invalid HTTP address')
    # remove the 'http://' portion of the address
    address = address[7:]
    # if the address ends in '/' then remove it
    if address.endswith('/'):
        address = address[:-1]
    # check if a specific page is requested
    # if so, remove it from the address and store it
    # if not, use '/'
    if '/' in address:
        index = address.find('/')
        page = address[index:]
        address = address[:index]
    else:
        page = '/'
    # check if a specific port number is provided
    # if so, remove it from the address and store it
    # if not, use the default port for HTTP (80)
    if ':' in address:
        index = address.find(':')
        port = int(address[index+1:])
        address = address[:index]
    else:
        port = 80

    # create a socket and connect to the address using the given port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((address, port))
    # enable non-blocking behavior by setting a timeout limit for the socket
    # can also be implemented by checking the response content-length and only receiving up to that amount to print
    s.settimeout(5)
    # generate and send an HTTP GET request
    request = 'GET ' + page + ' HTTP/1.1\r\nHost: ' + address + '\r\n\r\n'
    s.send(request)

    # act accordingly given the response code from the server
    # 200 OK: check if the response content-type is 'text/html'
    #         if so, print the provided HTML code then close the socket and exit with exit code 0
    #         if not, exit with a non-zero exit code
    # 301 Moved Permanently: print the provided redirect address then use it to attempt another HTTP GET request
    #                        after closing the socket
    # 302 Moved Temporarily: print the provided redirect address then use it to attempt another HTTP GET request
    #                        after closing the socket
    # 400+: check if the response content-type is 'text/html'
    #       if so, print the response body
    #       then, close the socket and exit with a non-zero exit code
    # else: close the socket and exit with a non-zero exit code
    response = s.recv(1024)
    print(response)
    response_code = int(response[9:12])
    if response_code == 200:
        index = response.find('Content-Type: ')
        content_type = response[index+14:index+23]
        if content_type == 'text/html':
            response = response[response.find('<'):]
            while len(response) > 0:
                print(response)
                try:
                    response = s.recv(1024)
                except (socket.error, socket.timeout):
                    break
            s.close()
            sys.exit(0)
        else:
            s.close()
            sys.exit('Response content is not of type \'text/html\'')
    elif response_code == 301:
        redirect_address = response[response.find('Location: ')+10:].split('\n')[0][:-1]
        print('Redirected to ' + redirect_address)
        s.close()
        http_get(redirect_address)
    elif response_code == 302:
        redirect_address = response[response.find('Location: ')+10:].split('\n')[0][:-1]
        print('Redirected to ' + redirect_address)
        s.close()
        http_get(redirect_address)
    elif response_code >= 400:
        index = response.find('Content-Type: ')
        content_type = response[index + 14:index + 23]
        if content_type == 'text/html':
            response = response[response.find('<'):]
            while len(response) > 0:
                print(response)
                try:
                    response = s.recv(1024)
                except (socket.error, socket.timeout):
                    break
        s.close()
        sys.exit('Failure with response code ' + str(response_code))
    else:
        s.close()
        sys.exit('Failure with response code ' + str(response_code))


def main():
    # check that 1 argument is given in addition to the .py file name
    # if so, attempt an HTTP GET request using the argument as the address
    # if not, exit with a non-zero exit code
    if len(sys.argv) == 2:
        http_get(sys.argv[1])
    else:
        sys.exit('Must provide 1 address argument')


if __name__ == '__main__':
    main()
