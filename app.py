import os
import requests
from bs4 import BeautifulSoup
import hashlib
import json
from datetime import datetime
from flask import Flask, jsonify, render_template, request, redirect, url_for
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

class SmartWebSentinel:
    def __init__(self):
        self.storage_file = "storage/websites.json"
        self.settings_file = "storage/settings.json"
        os.makedirs("storage", exist_ok=True)
        self.websites = self.load_websites()
        self.settings = self.load_settings()
        print("✅ SmartWeb Sentinel initialized successfully!")
    
    def load_websites(self):
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"❌ Error loading websites: {e}")
            return []
    
    def save_websites(self):
        try:
            with open(self.storage_file, 'w') as f:
                json.dump(self.websites, f, indent=2)
        except Exception as e:
            print(f"❌ Error saving websites: {e}")
    
    def load_settings(self):
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    return json.load(f)
            return {
                'email_enabled': False,
                'sms_enabled': False,
                'notification_email': '',
                'notification_phone': ''
            }
        except Exception as e:
            print(f"❌ Error loading settings: {e}")
            return {}
    
    def save_settings(self):
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"❌ Error saving settings: {e}")
    
    def add_website(self, url, name, scan_interval=10):
        for site in self.websites:
            if site['url'] == url:
                return False, "Website already exists"
        
        website = {
            'url': url,
            'name': name,
            'scan_interval': scan_interval,
            'hash': None,
            'last_checked': None,
            'scan_count': 0,
            'changed': False,
            'added_on': datetime.now().isoformat()
        }
        
        self.websites.append(website)
        self.save_websites()
        return True, "Website added successfully"
    
    def delete_website(self, url):
        self.websites = [site for site in self.websites if site['url'] != url]
        self.save_websites()
        return True, "Website deleted"
    
    def get_content_hash(self, url):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for element in soup(["script", "style"]):
                element.decompose()
            
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            clean_text = ' '.join(chunk for chunk in chunks if chunk)
            
            content_hash = hashlib.md5(clean_text[:5000].encode()).hexdigest()
            return content_hash, None
            
        except Exception as e:
            return None, str(e)
    
    def scan_website(self, url):
        for website in self.websites:
            if website['url'] == url:
                current_hash, error = self.get_content_hash(url)
                
                if error:
                    return False, f"Scan failed: {error}", False
                
                website['scan_count'] = website.get('scan_count', 0) + 1
                website['last_checked'] = datetime.now().strftime('%Y-%m-%d %H:%M')
                
                if website['hash'] is None:
                    website['hash'] = current_hash
                    website['changed'] = False
                    self.save_websites()
                    return True, "First scan completed - baseline established", False
                
                if website['hash'] != current_hash:
                    website['changed'] = True
                    old_hash = website['hash']
                    website['hash'] = current_hash
                    self.save_websites()
                    
                    self.send_notification(website['name'], website['url'])
                    
                    return True, "Change detected!", True
                else:
                    website['changed'] = False
                    self.save_websites()
                    return True, "No changes detected", False
        
        return False, "Website not found", False
    
    def scan_all_websites(self):
        results = []
        changes_found = 0
        
        for website in self.websites:
            success, message, changed = self.scan_website(website['url'])
            if changed:
                changes_found += 1
            results.append({
                'url': website['url'],
                'name': website['name'],
                'success': success,
                'changed': changed
            })
        
        return results, changes_found
    
    def send_notification(self, site_name, site_url):
        try:
            if self.settings.get('email_enabled') and self.settings.get('notification_email'):
                print(f"📧 Would send email to {self.settings['notification_email']}")
            
            if self.settings.get('sms_enabled') and self.settings.get('notification_phone'):
                phone = self.settings['notification_phone']
                message = f"Alert: {site_name} has changed! Check {site_url}"
                self.send_sms(phone, message)
            
            print(f"🔔 Notification sent for {site_name}")
            return True
        except Exception as e:
            print(f"❌ Notification failed: {e}")
            return False
    
    def send_sms(self, phone_number, message):
        try:
            resp = requests.post('https://textbelt.com/text', {
                'phone': phone_number,
                'message': message,
                'key': 'textbelt'
            }, timeout=10)
            
            result = resp.json()
            if result.get('success'):
                print(f"✅ SMS sent to {phone_number}")
                return True
            else:
                print(f"❌ SMS failed: {result.get('error', 'Unknown error')}")
                return False
        except Exception as e:
            print(f"❌ SMS error: {e}")
            return False
    
    def get_stats(self):
        total_scans = sum(site.get('scan_count', 0) for site in self.websites)
        changes = sum(1 for site in self.websites if site.get('changed', False))
        
        notifications_status = "Disabled"
        if self.settings.get('email_enabled') or self.settings.get('sms_enabled'):
            notifications_status = "Enabled"
        
        return {
            'total_scans': total_scans,
            'changes_detected': changes,
            'notifications_status': notifications_status
        }

sentinel = SmartWebSentinel()

@app.route('/')
def home():
    stats = sentinel.get_stats()
    
    return render_template('index.html',
        websites=sentinel.websites,
        total_scans=stats['total_scans'],
        changes_detected=stats['changes_detected'],
        notifications_status=stats['notifications_status'],
        email_enabled=sentinel.settings.get('email_enabled', False),
        sms_enabled=sentinel.settings.get('sms_enabled', False),
        notification_email=sentinel.settings.get('notification_email', ''),
        notification_phone=sentinel.settings.get('notification_phone', ''),
        recent_alerts=[]
    )

@app.route('/add-website', methods=['POST'])
def add_website():
    url = request.form.get('url')
    name = request.form.get('name')
    scan_interval = int(request.form.get('scan_interval', 10))
    
    if not url or not name:
        return jsonify({'success': False, 'message': 'URL and name are required'}), 400
    
    success, message = sentinel.add_website(url, name, scan_interval)
    return jsonify({'success': success, 'message': message})

@app.route('/delete-website', methods=['POST'])
def delete_website():
    data = request.get_json()
    url = data.get('url')
    
    success, message = sentinel.delete_website(url)
    return jsonify({'success': success, 'message': message})

@app.route('/scan-website', methods=['POST'])
def scan_website():
    data = request.get_json()
    url = data.get('url')
    
    success, message, changed = sentinel.scan_website(url)
    return jsonify({
        'success': success,
        'message': message,
        'changed': changed,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/scan-all', methods=['POST'])
def scan_all():
    results, changes_found = sentinel.scan_all_websites()
    
    message = f"Scanned {len(results)} websites. "
    if changes_found > 0:
        message += f"Found {changes_found} change(s)!"
    else:
        message += "No changes detected."
    
    return jsonify({
        'success': True,
        'message': message,
        'results': results,
        'changes_found': changes_found
    })

@app.route('/update-notifications', methods=['POST'])
def update_notifications():
    sentinel.settings['email_enabled'] = 'email_enabled' in request.form
    sentinel.settings['sms_enabled'] = 'sms_enabled' in request.form
    sentinel.settings['notification_email'] = request.form.get('email', '')
    sentinel.settings['notification_phone'] = request.form.get('phone', '')
    
    sentinel.save_settings()
    
    return jsonify({'success': True, 'message': 'Settings updated'})

@app.route('/status')
def status():
    stats = sentinel.get_stats()
    return jsonify({
        'status': 'operational',
        'websites_monitored': len(sentinel.websites),
        'total_scans': stats['total_scans'],
        'changes_detected': stats['changes_detected'],
        'notifications': stats['notifications_status']
    })

@app.route('/api/scan-now')
def api_scan_now():
    if sentinel.websites:
        url = sentinel.websites[0]['url']
        success, message, changed = sentinel.scan_website(url)
        return jsonify({
            'success': success,
            'message': message,
            'changed': changed
        })
    return jsonify({'success': False, 'message': 'No websites configured'})

if __name__ == "__main__":
    print("=" * 60)
    print("🛡  SMARTWEB SENTINEL - Website Change Monitor")
    print(f"📊 Monitoring {len(sentinel.websites)} website(s)")
    print("=" * 60)
    print(f"🌐 Dashboard: http://localhost:5000")
    print("=" * 60)
    
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
