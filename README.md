# Portfolio Automation System

Complete automation workflow: **Google Sheet → AI Website Generator → GitHub Pages → Email Notifications**

---

## Overview

This automation system creates stunning, agency-level portfolio websites from Google Sheet data and automatically deploys them to GitHub Pages while sending notification emails.

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Google Sheet│────▶│  Website    │────▶│  GitHub     │────▶│   Email     │
│  New Row    │     │  Generator  │     │  Deploy     │     │ Notification│
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

---

## Features

- ✅ **Automatic Detection**: Monitors Google Sheet for new entries
- ✅ **AI-Generated Portfolios**: Stunning, agency-level design
- ✅ **High-Converting Design**: Optimized for freelancer success
- ✅ **GitHub Integration**: Automatic repository creation and deployment
- ✅ **Email Notifications**: Sent to both freelancer and admin
- ✅ **Cal.com Integration**: Booking links in emails

---

## Google Sheet Format

Your spreadsheet should have these columns (Row 1 = Headers):

| Column | Field | Example |
|--------|-------|---------|
| A | Full Name | John Smith |
| B | Email | john@example.com |
| C | Niche | Web Development |
| D | Services | React, Node.js, Python |
| E | Target Clients | Startups, E-commerce |
| F | Work Samples | https://example.com/project1 |
| G | Testimonials | "Great work!" |
| H | Brand Colors | #6366f1,#8b5cf6 |
| I | Preferred Style | modern |
| J | CTA | Hire Me Now |

---

## Setup Instructions

### Step 1: Set Up Google Apps Script

1. Open your Google Sheet
2. Go to **Extensions → Apps Script**
3. Copy the code from `google-apps-script/Code.js`
4. Replace `YOUR_WEBHOOK_URL_HERE` with your API endpoint
5. Save and name the project
6. Run `initializeSheet()` from the script editor
7. Set up trigger: **Edit → Triggers → Add Trigger**
   - Function: `triggerOnNewRow`
   - Event: `On change`

### Step 2: Deploy the API Server

You have two options:

#### Option A: Deploy to Railway/Render (Recommended)

1. Push this code to a GitHub repository
2. Connect to Railway.app or Render.com
3. Set environment variables:
   - `GITHUB_TOKEN`: Your GitHub Personal Access Token
   - `GITHUB_USERNAME`: Your GitHub username
   - `SENDER_EMAIL`: Your Gmail address
   - `SENDER_PASSWORD`: Gmail App Password

#### Option B: Run Locally

```bash
cd portfolio-automation
pip install flask requests

# Set environment variables
export GITHUB_TOKEN="ghp_xxxxx"
export GITHUB_USERNAME="yourusername"

# Run the server
python api/server.py
```

### Step 3: Get Gmail App Password

1. Go to [Google Account Settings](https://myaccount.google.com)
2. Navigate to **Security → 2-Step Verification**
3. Enable 2-Step Verification
4. Go to **Security → App Passwords**
5. Create a new app password for "Portfolio Automation"
6. Copy the password

### Step 4: Get GitHub Personal Access Token

1. Go to GitHub → Settings → Developer settings
2. Personal access tokens → Generate new token
3. Select scopes: `repo`, `workflow`
4. Copy the token

---

## Configuration

Edit `api/main.py` to configure:

```python
GITHUB_TOKEN = 'your_token'  # Already set with your token
GITHUB_USERNAME = 'YOUR_USERNAME'  # UPDATE THIS
ADMIN_EMAIL = 'sobanluminai@gmail.com'  # Your control email
CALENDLY_LINK = 'https://cal.com/shazada-soban/quick-chat?overlayCalendar=true'
```

---

## Project Structure

```
portfolio-automation/
├── api/
│   ├── main.py              # Main automation runner
│   ├── server.py            # Flask webhook server
│   └── github_integration.py # GitHub API wrapper
├── google-apps-script/
│   └── Code.js              # Google Apps Script
├── website-generator/
│   ├── generate.py          # Website generator
│   ├── script.js            # Frontend JavaScript
│   └── styles.css           # (generated)
├── emails/
│   └── notification.py      # Email sender
├── templates/
│   └── email-templates.html # Email templates
└── README.md
```

---

## Email Templates

### Freelancer Email
- Subject: "Your Portfolio Website is Ready! 🚀"
- Contains: Preview link, Call-to-action button, Calendly booking link

### Admin Email
- Subject: "New Portfolio Created: [Name]"
- Contains: All freelancer details, Work samples, Website preview link

---

## Testing

### Test the Website Generator

```bash
cd /workspace/portfolio-automation
python -c "
from website_generator.generate import generate_portfolio
data = {
    'full_name': 'Test User',
    'email': 'test@example.com',
    'niche': 'Web Development',
    'services': 'React, Node.js',
    'target_clients': 'Startups',
    'work_samples': [],
    'testimonials': ['Great work!'],
    'brand_colors': '#6366f1,#8b5cf6',
    'preferred_style': 'modern',
    'cta': 'Hire Me'
}
result = generate_portfolio(data)
print(result)
"
```

### Test the Full Workflow

```bash
cd /workspace/portfolio-automation
echo '{
    "full_name": "Test User",
    "email": "test@example.com",
    "niche": "Web Development",
    "services": "React, Node.js",
    "target_clients": "Startups",
    "work_samples": [],
    "testimonials": [],
    "brand_colors": "#6366f1,#8b5cf6",
    "preferred_style": "modern",
    "cta": "Hire Me"
}' | python api/main.py
```

---

## Troubleshooting

### Google Apps Script Not Triggering
- Ensure you've added a trigger (Edit → Triggers → Add Trigger)
- Check that the sheet name matches (default: "Sheet1")
- Run `testWebhook()` manually to debug

### GitHub Deployment Fails
- Verify your GitHub token has `repo` scope
- Ensure the username is correct
- Check if repository name already exists

### Emails Not Sending
- Verify Gmail App Password is correct
- Ensure 2-Step Verification is enabled
- Check spam folder

---

## Support

For issues or questions:
- Email: sobanluminai@gmail.com
- Calendly: https://cal.com/shazada-soban/quick-chat

---

## License

MIT License - Use freely for your portfolio automation needs.
