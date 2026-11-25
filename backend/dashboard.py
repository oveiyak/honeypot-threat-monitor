# dashboard.py
import matplotlib.pyplot as plt
import numpy as np
from log_analyzer import decrypt_and_read_logs, analyze_attack_patterns
from flask import Flask, render_template, jsonify
import json
import logging
from cryptography.fernet import Fernet
import io
import base64
from datetime import datetime
import pandas as pd

# Load the encryption key from file
try:
    with open('fernet.key', 'rb') as key_file:
        key = key_file.read()
    cipher_suite = Fernet(key)
except FileNotFoundError:
    print("Fernet key file not found! Please generate a valid key using generate_key.py.")
    exit(1)

def generate_dashboard():
    logs = decrypt_and_read_logs()
    analysis = analyze_attack_patterns()
    
    # Create a simple visualization
    plt.figure(figsize=(12, 8))
    
    # Plot 1: Top IPs
    plt.subplot(2, 2, 1)
    ips = [ip for ip, count in analysis['top_ips']]
    counts = [count for ip, count in analysis['top_ips']]
    plt.bar(ips, counts)
    plt.title('Top IPs')
    plt.xticks(rotation=45)
    
    # Plot 2: Top Endpoints
    plt.subplot(2, 2, 2)
    endpoints = [endpoint for endpoint, count in analysis['top_endpoints']]
    counts = [count for endpoint, count in analysis['top_endpoints']]
    plt.bar(endpoints, counts)
    plt.title('Top Endpoints')
    plt.xticks(rotation=45)
    
    # Plot 3: Interactions over time
    plt.subplot(2, 1, 2)
    timestamps = [log['timestamp'] for log in logs]
    plt.hist(timestamps, bins=20)
    plt.title('Interactions Over Time')
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig('honeypot_dashboard.png')
    print("Dashboard saved as honeypot_dashboard.png")

if __name__ == "__main__":
    generate_dashboard()
