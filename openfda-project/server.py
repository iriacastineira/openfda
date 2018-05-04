import http.server
import socketserver
import json
import http.client

IP = "localhost"
PORT = 8000

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        path = self.path
        list = []

        if path == "/":
            with open ("search_list.html", "r") as f:
                code = f.read()
                self.wfile.write(bytes(code, "utf8"))
        elif "searchDrug" in path:
            header = {'User-Agent': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            information = path.split("?")[1]
            drug = information.split("=")[1].split("&")[0]
            if "limit" in path:
                limit = information.split("&")[1].split("=")[1]
            else:
                limit = "10"
            url = "/drug/label.json?search=active_ingredient:" + drug + "&" + "limit=" + limit
            conn.request("GET", url, None, header)
            r1 = conn.getresponse()
            drugs_raw = r1.read().decode("utf-8")
            conn.close()
            drug = json.loads(drugs_raw)
            drug_list = []
            for i in range(len(drug["results"])):
                    drug_name = drug["results"][i]["openfda"]["brand_name"][0]
                    drug_list.append(drug_name)
            self.wfile.write(bytes("<ul>","utf8"))
            for d in drug_list:
                print(d)
                message="<li>"+d+"</li>"
                self.wfile.write(bytes(message,"utf8"))

            self.wfile.write(bytes("</ul>","utf8"))

        elif "searchCompany" in path:
            header = {'User-Agent': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            information = path.split("?")[1]
            company = information.split("=")[1].split("&")[0]
            if "limit" in path:
                limit = information.split("&")[1].split("=")[1]
            else:
                limit = "10"

            url = "/drug/label.json?search=manufacturer_name:" + company + "&" + "limit=" + limit
            conn.request("GET", url, None, header)
            r1 = conn.getresponse()
            company_raw = r1.read().decode("utf-8")
            conn.close()
            company = json.loads(company_raw)
            company_list = []
            for i in range(len(company["results"])):
                for a in range(len(company["results"][i]["openfda"]["brand_name"])):
                    company_name = company["results"][i]["openfda"]["brand_name"][a]
                    company_list.append(company_name)
            self.wfile.write(bytes("<ul>", "utf8"))
            for d in company_list:
                message="<li>"+ d+ "</li>"
                self.wfile.write(bytes(message, "utf8"))
            self.wfile.write(bytes("</ul>", "utf8"))
        elif "listDrug" in path:
            header = {'User-Agent': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")

            drug = self.path.split("?")[1]

            url = "/drug/label.json?" + drug
            information = path.split("?")[1]
            limit = information.split("=")[1]
            conn.request("GET", url, None, header)
            r1 = conn.getresponse()
            drugs_raw = r1.read().decode("utf-8")
            conn.close()
            drugs = json.loads(drugs_raw)
            drugs_list = []
            for i in range(len(drugs["results"])):
                try:
                    drugs_name = drugs["results"][i]["openfda"]["brand_name"][0]
                    drugs_list.append(drugs_name)
                except KeyError:
                    drugs_list.append("Unknown")
            self.wfile.write(bytes("<ul>", "utf8"))
            for d in drugs_list:
                message="<li>"+ d+ "</li>"
                self.wfile.write(bytes(message, "utf8"))
            self.wfile.write(bytes("</ul>", "utf8"))
        elif "listCompanies" in path:
            header = {'User-Agent': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            company = self.path.split("?")[1]

            url = "/drug/label.json?" + company
            information = path.split("?")[1]
            limit = information.split("=")[1]
            conn.request("GET", url, None, header)
            r1 = conn.getresponse()
            company_raw = r1.read().decode("utf-8")
            conn.close()
            companies = json.loads(company_raw)
            companies_list = []
            for i in range(len(companies["results"])):
                try:
                    companies_name = companies["results"][i]["openfda"]["manufacturer_name"][0]
                    companies_list.append(companies_name)
                except KeyError:
                    companies_list.append('Unknown')
            self.wfile.write(bytes("<ul>", "utf8"))
            for d in companies_list:
                message="<li>"+ d+ "</li>"
                self.wfile.write(bytes(message, "utf8"))
            self.wfile.write(bytes("</ul>", "utf8"))




        return




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

