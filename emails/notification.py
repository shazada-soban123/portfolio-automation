"""
Email Notification Module
Sends portfolio website notifications to freelancers and admin
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from datetime import datetime

class EmailNotifier:
    def __init__(self, smtp_server='smtp.gmail.com', smtp_port=587):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = os.environ.get('SENDER_EMAIL', 'sobanluminai@gmail.com')
        self.sender_password = os.environ.get('SENDER_PASSWORD', '')  # App Password
        self.admin_email = 'sobanluminai@gmail.com'
        self.calendly_link = 'https://cal.com/shazada-soban/quick-chat?overlayCalendar=true'

    def send_portfolio_notification(self, freelancer_data, website_url):
        """
        Send notification emails to both freelancer and admin
        """
        results = []

        # Send to freelancer
        freelancer_result = self.send_to_freelancer(freelancer_data, website_url)
        results.append({'to': freelancer_data['email'], 'status': freelancer_result})

        # Send to admin
        admin_result = self.send_to_admin(freelancer_data, website_url)
        results.append({'to': self.admin_email, 'status': admin_result})

        return results

    def send_to_freelancer(self, data, website_url):
        """Send email to the freelancer"""
        subject = f"Your Portfolio Website is Ready! 🚀"

        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white; padding: 40px; text-align: center; border-radius: 16px 16px 0 0; }}
        .content {{ background: #f8fafc; padding: 40px; border-radius: 0 0 16px 16px; }}
        .website-link {{ display: inline-block; background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white; padding: 20px 40px; text-decoration: none; font-size: 18px; font-weight: 600; border-radius: 12px; margin: 20px 0; }}
        .section {{ background: white; padding: 24px; border-radius: 12px; margin: 20px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }}
        .cta-button {{ display: inline-block; background: #10b981; color: white; padding: 16px 32px; text-decoration: none; font-weight: 600; border-radius: 8px; margin-top: 20px; }}
        .footer {{ text-align: center; padding: 20px; color: #64748b; font-size: 14px; }}
        h1 {{ margin: 0; font-size: 28px; }}
        h2 {{ color: #0f172a; margin-top: 0; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🎉 Your Portfolio is Ready!</h1>
    </div>
    <div class="content">
        <h2>Hi {data.get('full_name', 'there')}!</h2>

        <p>Great news! Your professional portfolio website has been generated and is now live.</p>

        <div class="section">
            <h3>🔗 Preview Your Website</h3>
            <p style="text-align: center;">
                <a href="{website_url}" class="website-link">{website_url}</a>
            </p>
        </div>

        <div class="section">
            <h3>📅 Want This Website With Your Own Domain?</h3>
            <p>If you'd like to get this website with your own custom domain name (like yourname.com), let's schedule a quick call to discuss the options:</p>
            <p style="text-align: center;">
                <a href="{self.calendly_link}" class="cta-button">📅 Book a Free 15-Min Call</a>
            </p>
        </div>

        <p>During our call, we can discuss:</p>
        <ul>
            <li>Custom domain setup</li>
            <li>Additional pages and features</li>
            <li>SEO optimization</li>
            <li>Hosting options</li>
        </ul>

        <p>Best regards,<br>The Portfolio Team</p>
    </div>
    <div class="footer">
        <p>© {datetime.now().year} Portfolio Automation. All rights reserved.</p>
    </div>
</body>
</html>
"""

        return self.send_email(data['email'], subject, html_content)

    def send_to_admin(self, data, website_url):
        """Send notification to admin"""
        subject = f"New Portfolio Created: {data.get('full_name', 'Unknown')}"

        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: #0f172a; color: white; padding: 30px; text-align: center; border-radius: 16px 16px 0 0; }}
        .content {{ background: #f8fafc; padding: 30px; border-radius: 0 0 16px 16px; }}
        .website-link {{ background: #e2e8f0; padding: 12px 20px; border-radius: 8px; font-family: monospace; word-break: break-all; }}
        .info-row {{ display: flex; padding: 12px 0; border-bottom: 1px solid #e2e8f0; }}
        .info-label {{ font-weight: 600; width: 140px; color: #475569; }}
        .info-value {{ flex: 1; color: #0f172a; }}
        .badge {{ background: #10b981; color: white; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📋 New Portfolio Notification</h1>
        <span class="badge">Automated</span>
    </div>
    <div class="content">
        <p><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

        <h2>Freelancer Details</h2>
        <div class="info-row">
            <span class="info-label">Name:</span>
            <span class="info-value">{data.get('full_name', 'N/A')}</span>
        </div>
        <div class="info-row">
            <span class="info-label">Email:</span>
            <span class="info-value">{data.get('email', 'N/A')}</span>
        </div>
        <div class="info-row">
            <span class="info-label">Niche:</span>
            <span class="info-value">{data.get('niche', 'N/A')}</span>
        </div>
        <div class="info-row">
            <span class="info-label">Services:</span>
            <span class="info-value">{data.get('services', 'N/A')}</span>
        </div>
        <div class="info-row">
            <span class="info-label">Target Clients:</span>
            <span class="info-value">{data.get('target_clients', 'N/A')}</span>
        </div>

        <h2>Website Details</h2>
        <div class="info-row">
            <span class="info-label">Preview URL:</span>
            <span class="info-value website-link"><a href="{website_url}">{website_url}</a></span>
        </div>
        <div class="info-row">
            <span class="info-label">Brand Colors:</span>
            <span class="info-value">{data.get('brand_colors', 'N/A')}</span>
        </div>
        <div class="info-row">
            <span class="info-label">Preferred Style:</span>
            <span class="info-value">{data.get('preferred_style', 'N/A')}</span>
        </div>
        <div class="info-row">
            <span class="info-label">CTA:</span>
            <span class="info-value">{data.get('cta', 'N/A')}</span>
        </div>

        <p><strong>Work Samples:</strong> {data.get('work_samples', 'N/A')}</p>
        <p><strong>Testimonials:</strong> {data.get('testimonials', 'N/A')}</p>

        <p style="margin-top: 30px;">
            <a href="{self.calendly_link}" style="background: #6366f1; color: white; padding: 12px 24px; text-decoration: none; border-radius: 8px; display: inline-block;">
                📅 Book a Call with Client
            </a>
        </p>
    </div>
</body>
</html>
"""

        return self.send_email(self.admin_email, subject, html_content)

    def send_email(self, to_email, subject, html_content):
        """Send email via SMTP"""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.sender_email
            msg['To'] = to_email

            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                if self.sender_password:
                    server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, to_email, msg.as_string())

            return {'success': True, 'message': f'Email sent to {to_email}'}

        except Exception as e:
            return {'success': False, 'error': str(e)}


def main(data):
    """Main function for sending notifications"""
    website_url = data.get('website_url', 'Not available')

    notifier = EmailNotifier()
    results = notifier.send_portfolio_notification(data, website_url)

    return results


if __name__ == '__main__':
    import json
    import sys

    data = json.loads(sys.stdin.read())
    results = main(data)
    print(json.dumps(results))
