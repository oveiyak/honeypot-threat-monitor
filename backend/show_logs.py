from cryptography.fernet import Fernet
import json
from datetime import datetime

def load_key():
    with open('fernet.key', 'rb') as key_file:
        return key_file.read()

def decrypt_logs():
    key = load_key()
    cipher_suite = Fernet(key)
    
    print("\n=== Honeypot Activity Log ===\n")
    with open('honeypot.log', 'r') as log_file:
        for line in log_file:
            try:
                if line.startswith('INFO:root:'):
                    # Extract encrypted data
                    encrypted_data = line.replace('INFO:root:', '').strip()
                    # Decrypt the data
                    decrypted_data = cipher_suite.decrypt(encrypted_data.encode())
                    # Parse JSON
                    log_entry = json.loads(decrypted_data)
                    
                    # Format and print the log entry
                    timestamp = datetime.fromisoformat(log_entry['timestamp'])
                    print(f"Time: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
                    print(f"IP Address: {log_entry.get('ip', 'N/A')}")
                    print(f"Endpoint: {log_entry.get('endpoint', log_entry.get('port', 'N/A'))}")
                    print(f"Method: {log_entry.get('method', 'N/A')}")
                    
                    # Print headers if they exist
                    if 'headers' in log_entry:
                        print("Headers:")
                        for header, value in log_entry['headers'].items():
                            print(f"  {header}: {value}")
                    
                    # Print data if it exists
                    if 'data' in log_entry and log_entry['data']:
                        print("Data:")
                        print(f"  {json.dumps(log_entry['data'], indent=2)}")
                    
                    print("-" * 50)
            except Exception as e:
                continue  # Skip non-encrypted log entries

if __name__ == "__main__":
    decrypt_logs() 