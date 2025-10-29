# SmartWeb Sentinel - Website Change Monitor

## Overview
SmartWeb Sentinel is a website monitoring system that automatically detects when content changes on specific websites and sends notifications. Perfect for tracking exam results, hostel allotments, admission updates, or any website that updates infrequently.

**Current Status:** ✅ Fully functional on Replit
**Last Updated:** October 29, 2025

## What This Project Does
- **Monitors websites** for content changes using intelligent hashing
- **Stores tracking data** persistently to detect changes across restarts
- **Sends SMS alerts** (optional) when changes are detected
- **Provides web API** for manual scans and status checks
- **Background worker** for automated periodic monitoring

## Project Architecture

### Files
- `app.py` - Main Flask web application with monitoring logic
- `worker.py` - Background worker for periodic website checks
- `requirements.txt` - Python dependencies
- `render.yaml` - Deployment configuration for Render
- `storage/` - Persistent storage for website state tracking

### Technology Stack
- **Backend:** Python 3.11 with Flask
- **Web Scraping:** BeautifulSoup4, Requests
- **Deployment:** Configured for both Replit and Render
- **Alerts:** SMS via TextBelt/CallMeBot APIs (optional)

### Key Features
1. **Content Hashing** - Uses MD5 hashing to detect content changes
2. **Persistent State** - Stores last known state in JSON files
3. **Smart Scanning** - Removes scripts/styles for accurate comparison
4. **API Endpoints:**
   - `/` - Service status and information
   - `/scan-now` - Manual website scan trigger
   - `/status` - System health check

## Configuration

### Environment Variables
The application supports these optional environment variables:

- `PORT` - Server port (default: 5000)
- `SMS_ENABLED` - Enable SMS alerts (default: false)
- `PHONE_NUMBER` - Phone number for SMS alerts
- `SMS_API` - SMS service to use: textbelt or callmebot (default: textbelt)
- `SCAN_INTERVAL` - Time between scans in seconds (default: 600)

### Current Monitoring Target
- **Website:** VIT University (https://vit.ac.in)
- **Can be customized** in `app.py` to monitor any website

## How to Use on Replit

1. **View the Dashboard**
   - The web interface shows current monitoring status
   - Displays available endpoints and configuration

2. **Trigger Manual Scan**
   - Visit `/scan-now` endpoint
   - Or use curl: `curl http://localhost:5000/scan-now`
   - Returns JSON with scan results

3. **Check System Status**
   - Visit `/status` endpoint
   - Shows operational status and storage info

## Recent Changes

### October 29, 2025
- Fixed critical bug: Changed `_init_` to `__init__` in SmartWebSentinel class
- Set up Python 3.11 environment
- Installed all required dependencies
- Configured Flask workflow on port 5000
- Created .gitignore for Python project
- Verified application runs without errors
- Created comprehensive documentation

## Deployment to Render

The project is pre-configured for Render deployment with `render.yaml`:

### Render Services
1. **Web Service** (smartweb-sentinel)
   - Runs Flask API using Gunicorn
   - Free tier compatible
   
2. **Worker Service** (sentinel-scanner)
   - Runs background monitoring
   - Checks website periodically

### Deployment Steps for Render
1. Push code to GitHub repository
2. Connect GitHub repo to Render
3. Render will auto-detect `render.yaml`
4. Configure environment variables in Render dashboard:
   - Set `SMS_ENABLED=true` (if you want SMS alerts)
   - Set `PHONE_NUMBER` (your phone number)
   - Set `SCAN_INTERVAL` (time between scans)
5. Deploy both services

## Future Enhancement Ideas
- Add support for multiple websites simultaneously
- Email notifications in addition to SMS
- Web dashboard with scan history
- User authentication for multi-user support
- Webhook integrations (Discord, Slack, etc.)
- AI-powered content analysis to detect specific changes
- Custom monitoring rules per website
- Browser screenshot comparison

## Notes
- SMS alerts are disabled by default to avoid API costs
- Storage directory is created automatically
- First scan establishes baseline - changes detected on subsequent scans
- The monitoring is currently focused on VIT University but can easily be adapted to any website
