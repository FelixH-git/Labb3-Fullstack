

from http.server import SimpleHTTPRequestHandler, HTTPServer
import json
import random
import pymysql.cursors

INTERFACES = 'localhost'
PORT = 8020

class Databaseinfo():
    def __init__(self):
        self.conn = connection = pymysql.connect(host='dsd400.port0.org',
                             user="pyFHLK",
                             password='passwordlurigt'.encode().decode('latin1'),
                             database='labbgrupp1000',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    def Get_Students(self):
        with self.conn:
            with self.conn.cursor() as cursor:
                # Read records
                cursor.execute("SELECT * FROM student")
                return cursor.fetchall()

    def Post_Student(self, IDstudent, Mejl_student, FullName):
        with self.conn:
            with self.conn.cursor() as cursor:
                print(f'INSERT INTO student (IDstudent, Mejl_student, FullName) VALUES ({IDstudent}, "{Mejl_student}", "{FullName}")')
                cursor.execute(f'INSERT INTO student (IDstudent, Mejl_student, FullName) VALUES ({IDstudent}, "{Mejl_student}", "{FullName}")')
                self.conn.commit()

    def Get_Bookings(self):
        with self.conn:
            with self.conn.cursor() as cursor:
                # Read records
                cursor.execute("SELECT * FROM Book")
                return cursor.fetchall()
    
    def Post_Booking(self, IDStudent, IDRum):
        with self.conn:
            with self.conn.cursor() as cursor:
                # Read records
                cursor.execute(f"INSERT INTO Book (IDstudent, IDRum) VALUES ({IDStudent}, {IDRum})")
                return cursor.fetchall()




class RequestHandler(SimpleHTTPRequestHandler):
    # Override handler for GET requests
    def do_GET(self):
        DatabaseinfoVAR = Databaseinfo()
        if self.path.startswith('/api'):
            self.send_response(200)
            self.send_header('Content-type', 'text/json')
            self.end_headers()
            if self.path.startswith('/api/student'):
                # Generate a random number and send it as JSON response
                response = DatabaseinfoVAR.Get_Students()
                self.wfile.write(json.dumps(response).encode())
            else:
                response = {'error': 'Not implemented'}
                self.wfile.write(json.dumps(response).encode())
            return

        # Call default serving static files if not '/api'
        # from 'html' subdirectory
        self.path = '/html' + self.path
        return super().do_GET()


    def do_POST(self):
        DatabaseinfoVAR = Databaseinfo()
        if self.path.startswith("/api/book"):
            self.send_response(200)
            content_len = int(self.headers['content-length'])
            post_body = self.rfile.read(content_len)
            test_data = json.loads(post_body)
            DatabaseinfoVAR.Post_Student(test_data["IDstudent"], test_data["Mejl_student"], test_data["FullName"])



try:
    # Skapa en webbserver och definiera hanteraren för inkommande förfrågningar
    server = HTTPServer((INTERFACES, PORT), RequestHandler)
    print('Starting HTTP server on http://' + INTERFACES + ":" + str(PORT))
    server.serve_forever()

except KeyboardInterrupt:
    print('Ctrl-C received, shutting down the web server')
    server.socket.close()
