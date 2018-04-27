import http.server
import socketserver
import json
import http.client


# -- IP and the port of the server
IP = "localhost"  # Localhost means "I": your local machine
PORT = 8000


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
        list = []
        if path == "/":
            with open ("search.html", "r") as f:
                code = f.read()
                self.wfile.write(bytes(code, "utf8"))
        elif "searchDrug" in path:
            header = {'User-Agent': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            information = path.split("?")[1]
            drug = information.split("=")[1].split("&")[0]
            limit = information.split("&")[1].split("=")[1]
            url = "/drug/label.json?search=active_ingredient:" + drug + "&" + "limit=" + limit
            conn.request("GET", url, None, header)
            r1 = conn.getresponse()
            drugs_raw = r1.read().decode("utf-8")
            conn.close()
            drug = json.loads(drugs_raw)
            drug_list = []
            for i in range(len("results")):
                drug_name = drug["results"][i]["openfda"]["brand_name"][0]
                drug_list.append(drug_name)
            self.wfile.write(bytes("<ul>"), "utf8")
            for d in drug_list:
                self.wfile.write(bytes("<li>", d, "<li>"), "utf8")
            self.wfile.write(bytes("</ul>"), "utf8")

        elif "searchCompany" in path:
            header = {'User-Agent': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            information = path.split("?")[1]
            company = information.split("=")[1].split("&")[0]
            limit = information.split("&")[1].split("=")[1]
            url = "/drug/label.json?search=manufacturer_name:" + company + "&" + "limit=" + limit
            conn.request("GET", url, None, header)
            r1 = conn.getresponse()
            companies_raw = r1.read().decode("utf-8")
            conn.close()
            companies = json.loads(drugs_raw)
            self.wfile.write(bytes(json.dumps(companies), "utf8"))
        elif "listDrug" in path:


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