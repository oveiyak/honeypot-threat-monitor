import json
from cryptography.fernet import Fernet

# Step 1: Load the Fernet key from a file
def load_fernet_key():
    try:
        with open("fernet.key", "rb") as key_file:
            return key_file.read()  # Read and return the key
    except FileNotFoundError:
        print("Fernet key file not found! Please generate a valid key using Fernet.generate_key().")
        exit(1)

# Step 2: Initialize the Fernet cipher suite with the loaded key
key = load_fernet_key()
cipher_suite = Fernet(key)

# Step 3: Decrypt and read logs from the honeypot log file
def decrypt_and_read_logs():
    logs = []
    try:
        with open('honeypot.log', 'r') as log_file:
            for line in log_file:
                try:
                    # Extract encrypted data from log format
                    encrypted_data = line.strip()
                    decrypted_data = cipher_suite.decrypt(encrypted_data.encode())
                    logs.append(json.loads(decrypted_data))
                except Exception as e:
                    print(f"Error decrypting log entry: {e}")
    except FileNotFoundError:
        print("Log file not found! Ensure that honeypot.log exists.")
    
    return logs

# Step 4: Analyze attack patterns from decrypted logs
def analyze_attack_patterns():
    logs = decrypt_and_read_logs()
    
    # Group by IP and endpoint
    ip_counts = {}
    endpoint_counts = {}
    
    for log in logs:
        ip = log.get('ip', 'unknown')
        ip_counts[ip] = ip_counts.get(ip, 0) + 1
        
        endpoint = log.get('endpoint', 'unknown')
        endpoint_counts[endpoint] = endpoint_counts.get(endpoint, 0) + 1
    
    return {
        "total_interactions": len(logs),
        "unique_ips": len(ip_counts),
        "top_ips": sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)[:5],
        "top_endpoints": sorted(endpoint_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    }

