live-gold-silver-price-api

Free public API providing live Gold and Silver prices with real-time updates. Built for developers, traders, finance apps, jewelry stores, and market dashboards. Fast, reliable, and easy to integrate with JSON responses. Get accurate precious metal rates instantly for websites, mobile apps, and trading tools.
Source: https://livegoldsilver.com

Live Gold & Silver Price Monitor
A serverless, static web application for real-time precious metal tracking and SMS alerting.

Overview
This project provides a lightweight, static web application designed to monitor live gold and silver prices (XAU/USD) and dispatch automated SMS alerts via Twilio upon significant price fluctuations. Built with a 100% serverless architecture, it requires zero backend maintenance and can be hosted entirely for free on GitHub Pages.

Key Features
Real-Time Tracking: Live gold price monitoring integrated with a dynamic, real-time visual chart.

Automated SMS Alerts: Direct integration with Twilio to send immediate SMS notifications when prices cross user-defined thresholds.

Customizable Parameters: Fully configurable data refresh intervals and alert sensitivity settings.

Secure Data Handling: API credentials and alert configurations are stored securely within local browser storage—no external databases or backend servers are used.

Zero Infrastructure Costs: A 100% static architecture eliminates traditional server requirements and hosting fees.

Data Sources
The application prioritizes live market data and incorporates robust fallbacks to ensure continuous operation:

Primary Data Source: Live Gold & Silver Rates

Fallback Source: TradingView

Demo Mode: Simulated random walk algorithm (utilized for testing, demonstration, or when external APIs are temporarily unavailable).

Local Development & Testing
No build step or complex environment setup is required. You can run the application locally using either of the following methods:

Method 1: Direct File Access
Simply open the index.html file directly in any modern web browser.

Method 2: Local HTTP Server
For a more standard development environment, serve the directory using Python's built-in HTTP server:

Bash
python3 -m http.server 8080
Navigate to http://localhost:8080 in your browser.

Deployment Guide (GitHub Pages)
Follow these steps to deploy the application for free using GitHub Pages and GitHub Actions.

Initialize Repository: Create a new repository on GitHub via https://github.com/new.

Push Source Code: Commit and push all project files to the main branch. Ensure the following critical files are included in your push:

index.html

.github/workflows/deploy.yml

Configure GitHub Pages:

Navigate to your repository's Settings → Pages.

Under the Build and deployment section, set the Source to GitHub Actions.

Deploy: Any push to the main branch will automatically trigger the deployment workflow. The process typically completes in approximately one minute.

Access Your App: Once the workflow finishes, your application will be live at https://<your-username>.github.io/<repo-name>/. You can verify the exact URL in the Pages settings.

Twilio Setup (SMS Notifications)
To enable the free SMS alert functionality, you will need an active Twilio account. Input your Twilio Account SID, Auth Token, and designated sender/receiver phone numbers directly into the application's secure local settings UI.
