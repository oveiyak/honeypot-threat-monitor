# honeypot_tester.py
import requests
import socket
import time

def test_http_honeypot(host, port=8989):
    print(f"Testing HTTP honeypot at {host}:{port}")
    
    # Test admin login
    try:
        response = requests.post(f"http://{host}:{port}/api/v1/admin/login", 
                                json={"username": "admin", "password": "password123"})
        print(f"Admin login response: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error testing admin login: {e}")
    
    # Test user data endpoint
    try:
        response = requests.get(f"http://{host}:{port}/api/v1/users/data")
        print(f"User data response: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error testing user data: {e}")
    
    # Test config endpoint
    try:
        response = requests.get(f"http://{host}:{port}/api/v1/config")
        print(f"Config response: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error testing config: {e}")

def test_tcp_honeypot(host, port=8080):
    print(f"Testing TCP honeypot at {host}:{port}")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        sock.send(b"GET / HTTP/1.1\r\nHost: example.com\r\n\r\n")
        response = sock.recv(1024)
        print(f"TCP response: {response}")
        sock.close()
    except Exception as e:
        print(f"Error testing TCP honeypot: {e}")

if __name__ == "__main__":
    # Use the IP address of your Android device/emulator
    test_http_honeypot("192.168.1.100")
    test_tcp_honeypot("192.168.1.100")
    
    # Wait a moment for logs to be written
    time.sleep(2)
    
    # Test log analysis
    from log_analyzer import analyze_attack_patterns
    print("\nAnalysis results:")
    print(analyze_attack_patterns())
