# A basic web server using sockets


import socket

PORT = 8010
MAX_OPEN_REQUESTS = 5

def process_client(clientsocket):
    print(clientsocket)
    print(clientsocket.recv(1024))

    import http.client
    import json

    headers = {'User-Agent': 'http-client'}

    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET", "/drug/label.json?limit=10", None, headers)
    r1 = conn.getresponse()
    print(r1.status, r1.reason)
    repos_raw = r1.read().decode("utf-8")
    conn.close()
    repos = json.loads(repos_raw)

    list = []
    i = 0
    intro = "<!DOCTYPE html>" + "\n" + "<html>" + "\n" + "<head>" +"\n" + "<body>" + "\n" + "<ol>"
    end = "<ol>" + "\n" + "</body>" + "\n" + "</head>" +"\n" + "</html>"
    while i<10:
        if "active_ingredient" in repos["results"][i]:
            list.append(repos["results"][i]["active_ingredient"][0])
            i +=1
        else:
            list.append("There isn't a drug for this index")
            i +=1
    with open("h.html", "w") as f:
        f.write(intro)
        for word in list:
            word1="<li>" + word + "</li>"
            f.write(word1)
        f.write(end)

    with open("h.html","r") as f:
	    content =f.read()
    web_contents = content
    web_headers = "HTTP/1.1 200"
    web_headers += "\n" + "Content-Type: text/html"
    web_headers += "\n" + "Content-Length: %i" % len(str.encode(web_contents))
    clientsocket.send(str.encode(web_headers + "\n\n" + web_contents))
    clientsocket.close()

# create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind the socket to a public host, and a well-known port
hostname = socket.gethostname()
# Let's use better the local interface name
hostname = "localhost"
try:
    serversocket.bind((hostname, PORT))
    # become a server socket
    # MAX_OPEN_REQUESTS connect requests before refusing outside connections
    serversocket.listen(MAX_OPEN_REQUESTS)

    while True:
        # accept connections from outside
        print ("Waiting for connections at %s %i" % (hostname, PORT))
        (clientsocket, address) = serversocket.accept()
        # now do something with the clientsocket
        # in this case, we'll pretend this is a non threaded server
        process_client(clientsocket)

except socket.error as ex:
	print("Problemas using port %i. Do you have permission?" % PORT)
	print(ex)
