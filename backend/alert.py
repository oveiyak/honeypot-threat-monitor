# alert_system.py
import requests
import json
import threading
import time

class HoneypotAlert:
    def __init__(self, webhook_url=None, email=None):
        self.webhook_url = webhook_url
        self.email = email
        self.alert_threshold = 5  # Number of interactions before alerting
        self.cooldown_period = 300  # 5 minutes between alerts
        self.last_alert_time = 0
        self.interaction_count = 0
        
    def check_logs_and_alert(self):
        from log_analyzer import decrypt_and_read_logs
        
        while True:
            logs = decrypt_and_read_logs()
            recent_logs = [log for log in logs if self._is_recent(log)]
            
            if len(recent_logs) >= self.alert_threshold:
                current_time = time.time()
                if current_time - self.last_alert_time > self.cooldown_period:
                    self._send_alert(recent_logs)
                    self.last_alert_time = current_time
            
            time.sleep(60)  # Check every minute
    
    def _is_recent(self, log):
        import datetime
        log_time = datetime.datetime.fromisoformat(log['timestamp'])
        now = datetime.datetime.now()
        return (now - log_time).total_seconds() < 300  # Within last 5 minutes
    
    def _send_alert(self, logs):
        if self.webhook_url:
            alert_data = {
                "text": f"⚠️ Honeypot Alert: {len(logs)} suspicious interactions detected",
                "attachments": [
                    {
                        "title": "Recent Interactions",
                        "text": json.dumps(logs[:3], indent=2)
                    }
                ]
            }
            requests.post(self.webhook_url, json=alert_data)
            
    def start_monitoring(self):
        threading.Thread(target=self.check_logs_and_alert, daemon=True).start()
