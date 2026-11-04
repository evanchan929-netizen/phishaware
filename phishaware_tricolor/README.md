# PhishAware — Flask Starter

An academic prototype with a secretive black-and-green underground intelligence dashboard and a functional **offline URL lexical risk scanner**.

## Requirements
- Python 3.10+

## Setup

```bash
cd phishaware_starter
python -m venv .venv
```

Activate virtual environment:

- Windows PowerShell: `.venv\Scripts\Activate.ps1`
- macOS/Linux: `source .venv/bin/activate`

Install dependencies and run:

```bash
pip install -r requirements.txt
python app.py
```

Open **http://127.0.0.1:5000**.

## Project layout

```
phishaware_starter/
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
├── templates/
│   └── index.html
└── static/
    ├── css/style.css
    └── js/app.js
```

## What works now
- Responsive black/green homepage with left navigation
- URL input and AJAX risk scan (`POST /api/scan`)
- Heuristic score and reasons, with no network requests to scanned sites
- Three **fictional sample** community warnings

## Not yet implemented
- MySQL database / SQLAlchemy
- CRUD for eight planned modules
- Persistent scan history, real community posts, threat verification
- Login or account ownership (intentionally excluded from assessed modules)

The navigation links for future modules lead to a development-status section until those pages are implemented.

## Security / interpretation
This is a **teaching prototype**, not a security verdict. It checks URL text patterns only, does not access scanned sites, and cannot verify whether a domain is malicious. A low score does **not** imply safety. Community examples are fictional `.example` domains. Never auto-fetch arbitrary submitted URLs without SSRF protections and a carefully designed network sandbox.

## Suggested next work
1. Design MySQL ERD and related tables for all eight modules.
2. Introduce Flask Blueprints per module.
3. Add persistent scan records and CRUD validation.
4. Implement moderated community publication with clear unverified/verified status.
5. Add automated tests and evidence screenshots for coursework.
