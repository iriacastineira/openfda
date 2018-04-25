import http.server
import socketserver

# -- IP and the port of the server
IP = "localhost"  # Localhost means "I": your local machine
PORT = 8002


# HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Send message back to client

        # Write content as utf-8 data

        path = self.path
        if path == "/":
            with open ("search.html", "r") as f:
                code = f.read()
                self.wfile.write(bytes(message, "utf8"))
        if "search" in path:
            header = "Content-Type: text/html\n"
            conn = http.client.HTTPSConnection("api.fda.gov")
            



    header += "Content-Length: {}\n".format(len(str.encode(content)))
    response_msg = str.encode(status_line + header + "\n" + content)
    clientsocket.send(response_msg)


return

# Handler = http.server.SimpleHTTPRequestHandler
Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer((IP, PORT), Handler)
print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass

httpd.server_close()
print("")
print("Server stopped!")


# https://github.com/joshmaker/simple-python-webserver/blob/master/server.py
