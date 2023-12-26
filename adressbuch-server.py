from http.server import BaseHTTPRequestHandler, HTTPServer
import DatabaseHandler

hostName = "localhost"
serverPort = 2323
database_cur = DatabaseHandler.connect_or_create()


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(DatabaseHandler.get_adresses(database_cur), "utf-8"))


if __name__ == '__main__':
    print(DatabaseHandler.get_adresses(database_cur))
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(f"Server started at http://{hostName}:{serverPort}")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
