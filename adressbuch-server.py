import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import DatabaseHandler

hostName = "localhost"
serverPort = 2323
database_con = DatabaseHandler.connect_or_create()
database_cur = database_con.cursor()


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        if self.path == "/":
            self.wfile.write(bytes(DatabaseHandler.get_adresses(database_cur), "utf-8"))
        else:
            self.wfile.write(bytes(DatabaseHandler.get_searched_adresses(database_cur, self.path), "utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Methods', '*')
        self.send_header('Access-Control-Allow-Headers', "*")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def do_POST(self):
        if self.path == "/post":
            data_string = self.rfile.read(int(self.headers['Content-Length']))
            data = json.loads(data_string.decode("utf-8"))
            DatabaseHandler.add_contact(database_con, data)
        elif self.path == "/delete":
            data_string = self.rfile.read(int(self.headers['Content-Length']))
            print(data_string)
            DatabaseHandler.delete_contact(database_con, data_string.decode("utf-8"))
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()


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
