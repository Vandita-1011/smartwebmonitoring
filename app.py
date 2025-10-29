import os
import requests
from bs4 import BeautifulSoup
import hashlib
import json
from datetime import datetime
from flask import Flask, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

class SmartWebSentinel:
    def _init_(self):
        # Initialize previous_state FIRST before any other operations
        self.previous_state = {}
        self.storage_file = "storage/last_state.json"
        os.makedirs("storage", exist_ok=True)
        # Then load from file
        self.load_previous_state()
        print("✅ SmartWeb Sentinel initialized successfully!")
    
    def load_previous_state(self):
        """Load previous state from JSON file"""
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r') as f:
                    loaded_data = json.load(f)
                    self.previous_state = loaded_data
                print(f"📁 Loaded previous state with {len(self.previous_state)} URLs")
            else:
                self.previous_state = {}
                print("📁 No previous state found - starting fresh")
        except Exception as e:
            print(f"❌ Error loading previous state: {e}")
            self.previous_state = {}
    
    def save_current_state(self, url, content_hash):
        """Save current state to JSON file"""
        try:
            # Ensure previous_state exists
            if not hasattr(self, 'previous_state'):
                self.previous_state = {}
                
            self.previous_state[url] = {
                'hash': content_hash,
                'last_checked': datetime.now().isoformat()
            }
            with open(self.storage_file, 'w') as f:
                json.dump(self.previous_state, f, indent=2)
            print(f"💾 Saved state for {url}")
        except Exception as e:
            print(f"❌ Error saving state: {e}")
    
    def get_content_hash(self, url):
        """Get hash of website content"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            print(f"🔍 Scanning VIT website...")
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(["script", "style"]):
                element.decompose()
            
            # Get clean text
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            clean_text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Create hash
            content_hash = hashlib.md5(clean_text[:2000].encode()).hexdigest()
            print(f"✅ VIT website scanned successfully")
            return content_hash
            
        except Exception as e:
            print(f"❌ Error scanning VIT: {str(e)}")
            return None
    
    def send_sms_alert(self, message):
        """Send SMS using free APIs"""
        try:
            sms_enabled = os.getenv('SMS_ENABLED', 'false').lower() == 'true'
            if not sms_enabled:
                print("📱 SMS alerts disabled")
                return False
            
            phone_number = os.getenv('PHONE_NUMBER')
            sms_api = os.getenv('SMS_API', 'textbelt')
            
            if not phone_number:
                print("❌ Phone number not configured")
                return False
            
            sms_message = f"VIT Alert: {message}"
            print(f"📱 Attempting SMS to {phone_number} via {sms_api}")
            
            if sms_api == 'textbelt':
                return self._send_via_textbelt(phone_number, sms_message)
            elif sms_api == 'callmebot':
                return self._send_via_callmebot(phone_number, sms_message)
            else:
                return False
                
        except Exception as e:
            print(f"❌ SMS failed: {str(e)}")
            return False
    
    def _send_via_textbelt(self, phone_number, message):
        """Send SMS via TextBelt API"""
        try:
            resp = requests.post('https://textbelt.com/text', {
                'phone': phone_number,
                'message': message,
                'key': 'textbelt'
            })
            
            result = resp.json()
            if result.get('success'):
                print("✅ SMS sent via TextBelt!")
                return True
            else:
                error_msg = result.get('error', 'Unknown error')
                print(f"❌ TextBelt error: {error_msg}")
                return False
        except Exception as e:
            print(f"❌ TextBelt failed: {str(e)}")
            return False
    
    def _send_via_callmebot(self, phone_number, message):
        """Send SMS via CallMeBot API"""
        try:
            intl_number = f"+91{phone_number}"
            url = f"https://api.callmebot.com/sms/send.php"
            params = {
                'phone': intl_number,
                'text': message,
                'apikey': '123456'
            }
            
            resp = requests.get(url, params=params, timeout=10)
            
            if resp.status_code == 200:
                print("✅ SMS sent via CallMeBot!")
                return True
            else:
                print(f"❌ CallMeBot error: {resp.text}")
                return False
        except Exception as e:
            print(f"❌ CallMeBot failed: {str(e)}")
            return False
    
    def check_vit_website(self):
        """Check if VIT website has changed"""
        url = "https://vit.ac.in"
        print(f"🔄 Checking VIT main website...")
        
        # Ensure previous_state exists
        if not hasattr(self, 'previous_state'):
            self.previous_state = {}
            print("⚠ previous_state was missing - created new")
        
        current_hash = self.get_content_hash(url)
        
        if not current_hash:
            return False, "Scan failed - could not access VIT website"
        
        previous_data = self.previous_state.get(url, {})
        previous_hash = previous_data.get('hash')
        
        if not previous_hash:
            print(f"📝 First scan completed")
            self.save_current_state(url, current_hash)
            return False, "First scan completed - monitoring started"
        
        if previous_hash != current_hash:
            print(f"🚨 CHANGE DETECTED on VIT website!")
            self.save_current_state(url, current_hash)
            
            alert_message = "VIT website content changed! Check for updates."
            sms_sent = self.send_sms_alert(alert_message)
            
            if sms_sent:
                return True, "CHANGE DETECTED! SMS sent to your mobile 📱"
            else:
                return True, "CHANGE DETECTED! (SMS failed to send)"
        else:
            print(f"✅ No changes on VIT website")
            self.save_current_state(url, current_hash)
            return False, "No changes detected"

# Initialize the monitor - THIS MUST HAPPEN AFTER CLASS DEFINITION
print("🛡 Initializing SmartWeb Sentinel...")
sentinel = SmartWebSentinel()

@app.route('/')
def home():
    return jsonify({
        "service": "SmartWeb Sentinel",
        "status": "🟢 Running",
        "monitoring": "VIT University Website",
        "website": "https://vit.ac.in",
        "phone_number": "9392871897",
        "endpoints": {
            "scan": "/scan-now",
            "status": "/status"
        }
    })

@app.route('/scan-now')
def scan_now():
    """Manually trigger website scanning"""
    try:
        has_changed, message = sentinel.check_vit_website()
        
        return jsonify({
            "website": "https://vit.ac.in",
            "changed": has_changed,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "Scan failed due to error"
        }), 500

@app.route('/status')
def status():
    """System status endpoint"""
    try:
        # Ensure sentinel has previous_state
        if hasattr(sentinel, 'previous_state'):
            storage_count = len(sentinel.previous_state)
        else:
            storage_count = 0
            
        return jsonify({
            "status": "operational",
            "monitoring": "VIT University",
            "last_scan": datetime.now().isoformat(),
            "storage_entries": storage_count,
            "sms_enabled": os.getenv('SMS_ENABLED', 'false')
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

if __name__ == "__main__":
    print("=" * 50)
    print("🛡  SMARTWEB SENTINEL - FIXED VERSION")
    print("🎯 Monitoring: VIT University Website")
    print("📱 SMS Alerts: 9392871897")
    print("=" * 50)
    print(f"🌐 Dashboard: http://localhost:5000")
    print(f"🔍 Manual Scan: http://localhost:5000/scan-now")
    print("=" * 50)
    
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)