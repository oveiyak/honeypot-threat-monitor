# honeypot_core.py
from flask import Flask, request, jsonify
import datetime
import json
import socket
import threading
import logging
from cryptography.fernet import Fernet

# Load the encryption key from file
with open('fernet.key', 'rb') as key_file:
    key = key_file.read()
cipher_suite = Fernet(key)
logging.basicConfig(filename='honeypot.log', level=logging.INFO)

class MobileHoneypot:
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_routes()
        
    def setup_routes(self):
        # Fake API endpoints that look valuable to attackers
        @self.app.route('/api/v1/admin/login', methods=['POST'])
        def fake_admin_login():
            self.log_interaction('admin_login', request)
            return jsonify({"status": "error", "message": "Invalid credentials"}), 401
            
        @self.app.route('/api/v1/users/data', methods=['GET'])
        def fake_user_data():
            self.log_interaction('user_data', request)
            return jsonify({"users": self.generate_fake_users()}), 200
            
        @self.app.route('/api/v1/config', methods=['GET'])
        def fake_config():
            self.log_interaction('config', request)
            return jsonify({
                "db_host": "10.0.2.15",
                "db_user": "app_user",
                "debug_mode": "true"
            }), 200
    
    def log_interaction(self, endpoint, request):
        data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "ip": request.remote_addr,
            "endpoint": endpoint,
            "method": request.method,
            "headers": dict(request.headers),
            "data": request.get_json(silent=True) or request.form.to_dict() or request.args.to_dict()
        }
        encrypted_data = cipher_suite.encrypt(json.dumps(data).encode())
        logging.info(encrypted_data.decode())
        
    def generate_fake_users(self):
        return [
            {"id": 1, "username": "admin", "email": "admin@example.com"},
            {"id": 2, "username": "user1", "email": "user1@example.com"},
            {"id": 3, "username": "test_user", "email": "test@example.com"}
        ]
        
    def start_flask(self, host='0.0.0.0', port=5000):
        threading.Thread(target=self.app.run, kwargs={'host': host, 'port': port}).start()
        
    def start_tcp_honeypot(self, port=8080):
        def tcp_listener():
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind(('0.0.0.0', port))
            server.listen(5)
            while True:
                client, addr = server.accept()
                data = client.recv(1024)
                self.log_tcp_interaction(addr[0], port, data)
                client.send(b"HTTP/1.1 200 OK\r\nServer: Apache/2.4.41\r\n\r\n")
                client.close()
                
        threading.Thread(target=tcp_listener).start()
        
    def log_tcp_interaction(self, ip, port, data):
        log_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "ip": ip,
            "port": port,
            "data": data.decode('utf-8', errors='ignore')
        }
        encrypted_data = cipher_suite.encrypt(json.dumps(log_data).encode())
        logging.info(encrypted_data.decode())

if __name__ == "__main__":
    print("Starting honeypot...")
    honeypot = MobileHoneypot()
    honeypot.start_flask()
    honeypot.start_tcp_honeypot()
    print("Honeypot is running!")
    print("HTTP server listening on port 5000")
    print("TCP honeypot listening on port 8080")
    print("Press Ctrl+C to stop")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nStopping honeypot...")

