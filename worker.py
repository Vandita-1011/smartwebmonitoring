import os
import time
from datetime import datetime
from app import sentinel

def check_vit():
    print(f"\n{'='*50}")
    print(f"🔍 Checking VIT - {datetime.now().strftime('%H:%M %d/%m')}")
    print(f"{'='*50}")
    
    has_changed, message = sentinel.check_vit_website()
    
    if has_changed:
        print(f"🚨 CHANGE DETECTED!")
        print(f"📱 SMS sent to 9392871897")
    else:
        print(f"✅ No changes")
    
    print(f"⏰ Next check in 10 minutes...")
    print(f"{'='*50}\n")
    
    return has_changed

if __name__ == "__main__":
    check_vit()
    
    scan_interval = int(os.getenv('SCAN_INTERVAL', '600'))
    
    print(f"🔁 VIT Monitor Active")
    print(f"📱 Checking every {scan_interval} seconds")
    
    try:
        while True:
            time.sleep(scan_interval)
            check_vit()
    except KeyboardInterrupt:
        print(f"\n🛑 VIT Monitor Stopped")