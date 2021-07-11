import prnt
import game as eg
from http.server import BaseHTTPRequestHandler, HTTPServer
import time

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        validURL = True
        try:
            splittetString = self.path.split('/')
            moveorder = []
            for i in range(len(splittetString)):
                if splittetString[i] != '':
                    moveorder.append(int(splittetString[i]))
        except (SyntaxError,ValueError):
            print("Invalid move in path")
            validURL = False

        if(validURL):
            eg.newGame()
            eg.executeGame(moveorder)
            prnt.board(eg.field)


        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>4 wins</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
