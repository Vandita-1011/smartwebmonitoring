# Deployment Guide for Render

This guide will help you deploy the SmartWeb Sentinel website monitoring system to Render.

## Prerequisites
- A Render account (free tier works fine)
- Your code pushed to a GitHub repository
- Basic understanding of environment variables

## Step-by-Step Deployment Instructions

### Step 1: Push Code to GitHub

1. Create a new repository on GitHub
2. Push your code to the repository:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

### Step 2: Connect GitHub to Render

1. Log in to [Render](https://render.com)
2. Click **"New +"** in the top navigation
3. Select **"Blueprint"** from the dropdown
4. Click **"Connect a repository"**
5. Authorize Render to access your GitHub account
6. Select your repository from the list

### Step 3: Configure Services

Render will automatically detect the `render.yaml` file, which defines two services:

#### Service 1: Web Service (Flask API)
- **Name:** smartweb-sentinel
- **Type:** Web Service
- **Environment:** Python 3.11
- **Plan:** Free
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`

#### Service 2: Worker Service (Background Monitor)
- **Name:** sentinel-scanner
- **Type:** Worker
- **Environment:** Python 3.11
- **Plan:** Free
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `python worker.py`

### Step 4: Set Environment Variables

For **both services**, add these environment variables in the Render dashboard:

#### Required Variables
None! The app works with defaults.

#### Optional Variables (for SMS alerts)
1. Go to each service's dashboard
2. Navigate to **"Environment"** tab
3. Add these variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `SMS_ENABLED` | Enable SMS alerts | `true` or `false` |
| `PHONE_NUMBER` | Your phone number | `9392871897` |
| `SMS_API` | SMS service to use | `textbelt` or `callmebot` |
| `SCAN_INTERVAL` | Seconds between scans | `600` (10 minutes) |

### Step 5: Deploy

1. Click **"Apply"** to start deployment
2. Render will:
   - Build both services
   - Install dependencies
   - Start the web service and worker
3. Wait for deployment to complete (usually 2-3 minutes)

### Step 6: Verify Deployment

1. Once deployed, Render will provide a URL like: `https://smartweb-sentinel.onrender.com`
2. Open the URL in your browser
3. You should see JSON with service information
4. Test the scan endpoint: `https://smartweb-sentinel.onrender.com/scan-now`
5. Check the status: `https://smartweb-sentinel.onrender.com/status`

## How It Works on Render

### Web Service
- Runs the Flask API using Gunicorn (production server)
- Handles HTTP requests to scan websites and check status
- Accessible via the public URL

### Worker Service
- Runs in the background continuously
- Checks the monitored website every 10 minutes (configurable)
- Sends SMS alerts when changes are detected

## Customizing the Monitored Website

To monitor a different website instead of VIT:

1. Edit `app.py`
2. Find the `check_vit_website()` function (line 161)
3. Change the URL from `"https://vit.ac.in"` to your desired website
4. Update the function names and messages to match your use case
5. Commit and push changes
6. Render will auto-deploy the updates

## SMS Alert Setup

### Using TextBelt (Free - 1 SMS per day)
1. Set `SMS_API=textbelt`
2. Set `SMS_ENABLED=true`
3. Set your `PHONE_NUMBER`
4. You get 1 free SMS per day

### Using CallMeBot (Free - requires registration)
1. Register your WhatsApp number at [CallMeBot](https://www.callmebot.com/)
2. Set `SMS_API=callmebot`
3. Set `SMS_ENABLED=true`
4. Set your `PHONE_NUMBER`

## Monitoring Multiple Websites

Currently, the system monitors one website (VIT). To monitor multiple websites:

### Option 1: Multiple Deployments
- Deploy separate instances for each website
- Each instance monitors one website

### Option 2: Code Modification (Advanced)
- Modify `app.py` to accept URL parameters
- Update the storage system to handle multiple URLs
- Modify the worker to check multiple websites

## Troubleshooting

### Service won't start
- Check the logs in Render dashboard
- Verify `requirements.txt` is present
- Ensure Python version is 3.11

### SMS not working
- Verify `SMS_ENABLED=true`
- Check phone number format
- Ensure you haven't exceeded free tier limits
- Try switching between `textbelt` and `callmebot`

### Worker not checking website
- Check worker logs in Render dashboard
- Verify `SCAN_INTERVAL` is set correctly
- Ensure the target website is accessible

### Website changes not detected
- The first scan establishes a baseline
- Changes are only detected after the second scan
- Check if the website content actually changed
- Verify storage is persisting between checks

## Cost Information

### Free Tier Limits (Render)
- **Web Service:** 750 hours/month (enough for 24/7)
- **Worker Service:** 750 hours/month (enough for 24/7)
- **Limitation:** Services sleep after 15 minutes of inactivity (web only)
- **Note:** Worker service runs continuously on free tier

### Keeping Web Service Awake
To prevent the web service from sleeping:

1. Use a free uptime monitoring service like:
   - UptimeRobot (https://uptimerobot.com/)
   - Cronitor (https://cronitor.io/)
   - Better Uptime (https://betteruptime.com/)

2. Configure it to ping your Render URL every 10 minutes

## Production Recommendations

1. **Use Paid Tier** - For critical monitoring, upgrade to paid tier ($7/month)
2. **Add Email Alerts** - Implement email notifications in addition to SMS
3. **Database Storage** - Use PostgreSQL for better persistence
4. **Add Authentication** - Protect endpoints with API keys
5. **Implement Logging** - Use a logging service like LogDNA or Papertrail
6. **Set up Monitoring** - Use Render's built-in metrics

## Support

For issues specific to this project:
- Check the logs in Render dashboard
- Review the code in `app.py` and `worker.py`
- Test locally on Replit first

For Render platform issues:
- Visit [Render Documentation](https://render.com/docs)
- Contact Render Support

## Next Steps After Deployment

1. ✅ Verify both services are running
2. ✅ Test the `/scan-now` endpoint
3. ✅ Configure SMS alerts (optional)
4. ✅ Set up uptime monitoring
5. ✅ Customize the monitored website
6. ✅ Share your monitoring URL with others

---

**Your SmartWeb Sentinel is now live on Render! 🎉**
