# Notification Setup Guide

This guide will help you set up email and SMS notifications for SmartWeb Sentinel.

## Current Notification Support

### Built-in SMS (TextBelt - Free)
**Status:** ✅ Already working
**Limitations:** 1 free SMS per day per phone number

**How to use:**
1. Open the dashboard
2. Scroll to "Notification Settings"
3. Toggle on "SMS Notifications"
4. Enter your phone number (format: +1234567890)
5. Click "Save Settings"

**Testing:**
- Add a website and scan it twice to trigger a change notification
- You'll receive an SMS when a change is detected

---

## Setting Up Professional Notifications

### Option 1: Email Notifications (Recommended)

#### Using SendGrid (Professional Email Service)

1. **Search for Integration**
   - I can help you set up SendGrid integration
   - Just ask: "Set up SendGrid for email notifications"

2. **Connect Your Account**
   - You'll need a SendGrid account (free tier available)
   - Follow the prompts to connect

3. **Update Code**
   After integration is set up, update `app.py` to use SendGrid:
   ```python
   def send_email(self, to_email, subject, message):
       # SendGrid integration code will be provided
       # during integration setup
       pass
   ```

#### Using Gmail Integration

1. **Search for Integration**
   - Ask me to: "Set up Gmail for notifications"
   
2. **Connect Gmail**
   - Authorize your Gmail account
   - No coding required after setup

3. **Enable in Dashboard**
   - Toggle "Email Notifications" on
   - Enter your email address
   - Save settings

---

### Option 2: Professional SMS (Twilio)

#### Why Twilio?
- Reliable delivery
- No daily limits
- Delivery confirmations
- Global reach
- Pay-as-you-go pricing

#### Setup Steps

1. **Create Twilio Account**
   - Go to https://www.twilio.com/
   - Sign up for free trial ($15 credit)
   - Get your Account SID and Auth Token

2. **Set Up Integration**
   - Ask me: "Set up Twilio for SMS notifications"
   - I'll help you connect your Twilio account

3. **Update Code**
   After integration setup, the SMS sending in `app.py` will automatically use Twilio credentials.

---

## Integration Options on Replit

| Service | Type | Cost | Reliability | Setup Difficulty |
|---------|------|------|-------------|------------------|
| **TextBelt** | SMS | Free (1/day) | Basic | ✅ Already done |
| **Twilio** | SMS | Paid | Excellent | Easy with integration |
| **SendGrid** | Email | Free tier | Excellent | Easy with integration |
| **Resend** | Email | Free tier | Excellent | Easy with integration |
| **Gmail** | Email | Free | Good | Easy with integration |
| **AgentMail** | Email | Free | Good | Very easy |

---

## Quick Setup Commands

### For Email Notifications

**SendGrid:**
```
"Set up SendGrid for email notifications"
```

**Gmail:**
```
"Set up Gmail for email notifications"
```

**Resend:**
```
"Set up Resend for email notifications"
```

### For SMS Notifications

**Twilio:**
```
"Set up Twilio for SMS notifications"
```

---

## Code Integration Examples

### After Email Integration is Set Up

Update the `send_notification` method in `app.py`:

```python
def send_notification(self, site_name, site_url):
    try:
        # Email notification
        if self.settings.get('email_enabled') and self.settings.get('notification_email'):
            subject = f"Alert: {site_name} Changed!"
            message = f"The website {site_name} ({site_url}) has been updated. Check it now!"
            
            # Use the integrated email service
            self.send_email(
                to=self.settings['notification_email'],
                subject=subject,
                body=message
            )
        
        # SMS notification
        if self.settings.get('sms_enabled') and self.settings.get('notification_phone'):
            sms_message = f"Alert: {site_name} has changed! Check {site_url}"
            self.send_sms(self.settings['notification_phone'], sms_message)
        
        return True
    except Exception as e:
        print(f"❌ Notification failed: {e}")
        return False
```

---

## Testing Notifications

### Test Email
1. Enable email notifications in dashboard
2. Add a test website (e.g., https://example.com)
3. Scan it once to establish baseline
4. Manually change something on the website OR
5. Modify the hash in storage to simulate a change
6. Scan again - you should get an email

### Test SMS
1. Enable SMS notifications
2. Enter your phone number with country code (+1234567890)
3. Follow same steps as email testing
4. You'll receive an SMS

---

## Troubleshooting

### Email Not Sending

**Check:**
- Email address is correct
- Email notifications are toggled ON
- Integration is properly set up
- Check spam folder
- Verify email service API key is valid

**Solutions:**
- Re-enter email address
- Toggle notifications off and on again
- Check integration connection status
- Try a different email service

### SMS Not Sending

**For TextBelt:**
- Remember: only 1 free SMS per day
- Use country code (+1 for US)
- Phone number format: +1234567890

**For Twilio:**
- Verify Account SID and Auth Token
- Check Twilio balance
- Verify phone number is verified in Twilio
- Check Twilio logs for errors

### No Notifications at All

**Check:**
- Notifications are enabled (toggled on)
- Email/phone number is entered correctly
- Website actually changed (check hash)
- No errors in console logs
- Integration is connected

---

## Recommended Setup

### For Personal Use
1. **Email:** Gmail integration (easy, free)
2. **SMS:** TextBelt (free, for light use)

### For Small Team
1. **Email:** SendGrid free tier (100 emails/day)
2. **SMS:** Twilio pay-as-you-go

### For Production
1. **Email:** SendGrid or Resend paid plan
2. **SMS:** Twilio with dedicated number
3. **Alternative:** Add Webhook support for Slack/Discord

---

## Advanced: Webhook Notifications

### Coming Soon
Support for webhook notifications to:
- **Slack** - Team notifications in channels
- **Discord** - Server notifications
- **Microsoft Teams** - Team alerts
- **Custom Webhooks** - Integrate with any service

---

## Cost Breakdown

### Free Tier Limits

**TextBelt:**
- 1 SMS per day per phone number
- Perfect for testing

**SendGrid:**
- 100 emails per day
- Perfect for small projects

**Resend:**
- 100 emails per day
- Modern, developer-friendly

**Gmail:**
- Gmail daily sending limits apply
- ~500 emails per day

### Paid Options

**Twilio SMS:**
- ~$0.0075 per SMS in US
- $15 free credit on signup
- ~2000 free SMS to start

**SendGrid Paid:**
- $15/month - 40,000 emails
- $90/month - 100,000 emails

---

## Getting Started

Ready to set up notifications? Just ask me:

1. **"Set up email notifications"** - I'll help you choose and set up an email service
2. **"Set up SMS notifications with Twilio"** - For reliable SMS delivery
3. **"What's the best notification setup for me?"** - I'll recommend based on your needs

---

**Note:** All integrations use Replit's secure secret management, so your API keys are never exposed in code!
