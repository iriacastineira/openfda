import http.server
import socketserver
import json
import http.client


# -- IP and the port of the server
IP = "localhost"  # Localhost means "I": your local machine
PORT = 8002


# HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Send message back to client

        # Write content as utf-8 data

        path = self.path
        if path == "/":
            with open ("search.html", "r") as f:
                code = f.read()
                self.wfile.write(bytes(code, "utf8"))
        if "search" in path:
            header = "Content-Type: text/html\n"
            conn = http.client.HTTPSConnection("api.fda.gov")
            information = path.split("?")[1]
            drug = information.split("=")[1].split("&")[0]
            limit = information.split("&")[1].split("=")[1]
            url = "/drug/label.json?search=active_ingredient:" + drug + "&" + "limit=" + limit
            conn.request("GET", url, None, header)
            r1 = conn.getresponse()
            drugs_raw = r1.read().decode("utf-8")
            conn.close()
            drugs = json.loads(drugs_raw)
            drugsfinal = str(drugs)
            self.wfile.write(bytes(drugsfinal, "utf8"))
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
