# Gig Alerts 🎤🎸🎹

This project checks for upcoming concerts of selected artists and sends an email notification with concert details for the following countries: PL, DE, FR, CZ, NL, BE.

## How does it work?

- Takes the `artists` list defined in `main.py`
- For each artist, a request is sent to the Ticketmaster Discovery API
- `response.status_code` informs whether the request succeeded (code 200) or failed (any other code)
- If the request succeeds, a JSON response is received and the following data is extracted: Event name, City, Date, Concert venue, Concert hour, Link to tickets
- Duplicates are removed (same city + date)
- A message is built for each artist and sent via email using `smtplib`
- Email sending is handled by the `sendmail` method called on the SMTP connection object. The process runs automatically.
- GitHub Actions runs the script automatically on a virtual machine according to the schedule defined in `.github/workflows/concert-notif.yml` (cron) — the user receives an email with upcoming concert events once a week

## Tracked artists

The list of artists is defined in `main.py` in the `artists` variable. To add or remove an artist, edit that list directly.

## Requirements

- Python 3.11+
- Gmail account with two-step authentication enabled and an app password generated
- API key from Ticketmaster Developer Portal
- Dependencies: `requests`, `python-dotenv`

```bash
pip install -r requirements.txt
```

## Configuration

### Run locally

Create a `.env` file in the root directory with the following variables:

```
TM_API_KEY=your_ticketmaster_api_key
EMAIL=your_gmail_address
EMAIL_PASSWORD=your_gmail_app_password
```

### Automation (fork + GitHub Actions)

Add the same variables as GitHub Secrets:
Settings → Secrets and variables → Actions → New repository secret

- `TM_API_KEY`
- `EMAIL`
- `EMAIL_PASSWORD`
