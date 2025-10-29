# SmartWeb Sentinel - Website Change Monitor

## Overview
SmartWeb Sentinel is a beautiful, modern website monitoring system that automatically detects when content changes on specific websites and sends notifications. Perfect for tracking exam results, hostel allotments, admission updates, or any website that updates infrequently.

**Current Status:** ✅ Fully functional with modern web interface
**Last Updated:** October 29, 2025

## What This Project Does
- **Beautiful Dashboard** - Modern, responsive web interface
- **Monitor Multiple Websites** - Add unlimited websites to track
- **Smart Change Detection** - Uses content hashing to detect changes
- **Instant Notifications** - SMS and email alerts when changes detected
- **Real-time Scanning** - Manual or automated scanning
- **Persistent Storage** - Tracks history across restarts

## Project Architecture

### Files & Directories
- `app.py` - Main Flask application with web interface and API
- `worker.py` - Background worker for periodic automated checks
- `templates/` - HTML templates for web interface
  - `index.html` - Main dashboard
- `static/` - Static assets
  - `css/style.css` - Modern styling
- `storage/` - Persistent data storage
  - `websites.json` - Tracked websites data
  - `settings.json` - Notification settings
- `requirements.txt` - Python dependencies
- `render.yaml` - Render deployment configuration
- `.gitignore` - Git ignore rules

### Technology Stack
- **Backend:** Python 3.11 with Flask
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Web Scraping:** BeautifulSoup4, Requests
- **Notifications:** SMS (TextBelt), Email (via integrations)
- **Deployment:** Replit & Render ready

## Features

### Dashboard
- **Statistics Cards** - Monitor sites, scans, changes at a glance
- **Add Websites** - Simple form to add new sites to monitor
- **Website List** - View all monitored sites with status
- **Manual Scanning** - Scan individual sites or all at once
- **Notification Settings** - Configure email and SMS alerts

### Website Tracking
1. **Content Hashing** - MD5 hash comparison for change detection
2. **Baseline Establishment** - First scan sets the baseline
3. **Change Detection** - Subsequent scans detect any changes
4. **Scan History** - Track scan count and last checked time
5. **Status Badges** - Visual indicators for changed/monitored status

### Notification System
- **Email Notifications** - Get email alerts (requires integration)
- **SMS Alerts** - Receive text messages via TextBelt API
- **Toggle Controls** - Easy on/off switches for each method
- **Customizable** - Set your email and phone number

## How to Use

### On Replit

1. **Access the Dashboard**
   - Open the web preview to see the beautiful interface
   - The dashboard shows your monitoring statistics

2. **Add a Website**
   - Enter the website URL (e.g., https://vit.ac.in)
   - Give it a display name (e.g., "VIT University")
   - Set scan interval in minutes (default: 10)
   - Click "Add Website"

3. **Scan Websites**
   - Click the refresh icon on any website to scan it
   - Or use "Scan All Now" to check all websites
   - First scan establishes baseline
   - Changes detected on subsequent scans

4. **Configure Notifications**
   - Toggle email/SMS notifications on or off
   - Enter your email address for email alerts
   - Enter phone number for SMS alerts (format: +1234567890)
   - Click "Save Settings"

5. **View Results**
   - Websites with changes show "Changed!" badge
   - See scan count and last checked time
   - Recent alerts appear in the dashboard

## Recent Changes

### October 29, 2025 - Major Update
- **Complete UI Overhaul** - Built modern, beautiful web interface
- **Dashboard Design** - Created responsive dashboard with statistics
- **Multi-Website Support** - Can now monitor unlimited websites
- **Add/Delete Functionality** - Manage websites through web interface
- **Scan Controls** - Manual scanning for individual or all websites
- **Notification UI** - Toggle and configure notifications easily
- **Enhanced Storage** - Improved JSON-based storage system
- **Beautiful Styling** - Gradient backgrounds, cards, animations
- **Status Indicators** - Visual badges for changed/monitored status
- **Error Handling** - Better error messages and user feedback

### Initial Setup (Same Day)
- Fixed critical bug: `_init_` → `__init__` in SmartWebSentinel class
- Set up Python 3.11 environment
- Installed all required dependencies
- Configured Flask workflow on port 5000
- Created .gitignore for Python project

## API Endpoints

### Web Interface
- `GET /` - Main dashboard
- `POST /add-website` - Add new website to monitor
- `POST /delete-website` - Remove website from monitoring
- `POST /scan-website` - Scan specific website
- `POST /scan-all` - Scan all websites
- `POST /update-notifications` - Update notification settings

### JSON API
- `GET /status` - System status (JSON)
- `GET /api/scan-now` - Quick scan endpoint (JSON)

## Notification Integrations

### Available on Replit

The project supports multiple notification methods through Replit integrations:

1. **Twilio** - Professional SMS service
   - Use `search_integrations` to find "Twilio"
   - Set up connector for reliable SMS delivery
   - Better than free APIs for production use

2. **Email Services**
   - **SendGrid** - Transactional email service
   - **Resend** - Modern email API
   - **Gmail** - Use your Gmail account
   - **Outlook** - Use your Outlook account
   - **AgentMail** - Built-in email service

3. **Current SMS** - Uses TextBelt free API
   - 1 free SMS per day per phone number
   - Good for testing and light use
   - Upgrade to Twilio for production

### Setting Up Notifications

**For Email (Recommended):**
1. Search for email integration (SendGrid/Resend recommended)
2. Connect your account
3. Enable email notifications in dashboard
4. Enter your email address

**For SMS (Current - TextBelt):**
1. Just enter your phone number in dashboard
2. Enable SMS notifications
3. Limited to 1 free SMS per day

**For SMS (Production - Twilio):**
1. Search for Twilio integration
2. Connect your Twilio account
3. Update app.py to use Twilio credentials
4. Unlimited SMS based on your plan

## Deployment to Render

### Automatic Deployment

The project includes `render.yaml` for easy deployment:

1. **Push to GitHub**
   ```bash
   git push origin main
   ```

2. **Connect to Render**
   - Go to https://render.com
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Render auto-detects `render.yaml`

3. **Deploy Services**
   - Web Service: Runs Flask app (Gunicorn)
   - Worker Service: Runs background monitor
   - Both deploy automatically

4. **Configure Environment Variables** (Optional)
   - `SCAN_INTERVAL` - Time between scans (default: 600 seconds)
   - Add Twilio/SendGrid API keys if using those services

5. **Access Your App**
   - Render provides a public URL
   - Dashboard accessible immediately
   - Start adding websites to monitor

### Free Tier Notes
- Web service sleeps after 15 min inactivity
- Worker service runs continuously
- Use UptimeRobot to keep web service awake
- Sufficient for monitoring 10-20 websites

## Customization Guide

### Change Colors
Edit `static/css/style.css`:
- Main gradient: Lines 7-8
- Stat card gradients: Lines 78, 82, 86, 90 (in index.html)
- Button colors: Lines 138-156 (style.css)

### Add More Websites
Just use the "Add Website" form in the dashboard!

### Modify Scan Logic
Edit `app.py` → `get_content_hash()` method (lines 74-93)
- Change content extraction logic
- Modify hash generation
- Add custom filtering

### Change Scan Interval
- Per website: Set when adding website
- Global: Set `SCAN_INTERVAL` environment variable
- Worker: Modify `worker.py` (line 27)

## Future Enhancement Ideas
- Historical change tracking with diff viewer
- Webhook integrations (Discord, Slack, Teams)
- Scheduled scans with cron-like expressions
- Multi-user support with authentication
- Browser automation for JavaScript-heavy sites
- AI-powered content analysis
- Email digest of daily changes
- Mobile app for notifications
- API for third-party integrations
- Export data to CSV/JSON

## Security Notes
- No authentication currently (add for production)
- API endpoints are open (protect with API keys)
- Notification settings stored in JSON (use encrypted database for production)
- SMS/Email can be spoofed (validate user input)
- Rate limiting recommended for public deployment

## Troubleshooting

### Website not loading
- Check if Flask server is running on port 5000
- Check browser console for errors
- Ensure static files are being served

### Scans failing
- Verify website URL is correct and accessible
- Check if site blocks automated requests
- Increase timeout in `get_content_hash()` method

### Notifications not sending
- Verify email/phone number is correct
- Check that notifications are enabled (toggled on)
- TextBelt limited to 1 free SMS per day
- Consider using Twilio for reliable delivery

### Changes not detected
- First scan establishes baseline (no change detected)
- Very small changes might not affect hash
- JavaScript-rendered content might not be captured
- Try increasing hash sample size in code

## Tech Stack Details

- **Python 3.11** - Modern Python with type hints
- **Flask 2.3.3** - Lightweight web framework
- **BeautifulSoup4** - HTML parsing and scraping
- **Requests** - HTTP library for fetching pages
- **Gunicorn** - Production WSGI server
- **JSON Storage** - Simple, file-based persistence

## Project Status

✅ **Completed Features**
- Beautiful web interface
- Multi-website monitoring
- Add/delete websites
- Manual scanning
- Notification settings UI
- SMS alerts (TextBelt)
- Persistent storage
- Responsive design
- Real-time updates

🚧 **In Progress**
- Email notification integration
- Historical change tracking
- User authentication

💡 **Planned**
- Webhook support
- Advanced scheduling
- Mobile responsiveness improvements
- API documentation

## Notes
- Designed for ease of use by non-technical users
- Modern, clean interface inspired by popular SaaS products
- Production-ready for small-scale deployments
- Easily extensible for custom requirements
- Free tier friendly (Replit, Render, TextBelt)
