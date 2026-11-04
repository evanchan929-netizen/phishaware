from flask import Flask, render_template, request, jsonify
from urllib.parse import urlsplit
import ipaddress
import re

app = Flask(__name__)

DEMO_REPORTS = [
    {"title": "Impersonated account verification page", "url": "https://account-check.example", "risk": "HIGH", "detail": "Example community warning — demonstration data only.", "time": "DEMO"},
    {"title": "Suspicious giveaway message", "url": "https://prize-notice.example", "risk": "MEDIUM", "detail": "Example community warning — demonstration data only.", "time": "DEMO"},
    {"title": "Fake delivery notification", "url": "https://parcel-alert.example", "risk": "HIGH", "detail": "Example community warning — demonstration data only.", "time": "DEMO"},
]

@app.get('/')
def home():
    return render_template('index.html', reports=DEMO_REPORTS)

@app.post('/api/scan')
def scan():
    payload = request.get_json(silent=True) or {}
    raw = str(payload.get('url', '')).strip()
    if not raw or len(raw) > 2048:
        return jsonify(error='Enter a URL of up to 2048 characters.'), 400
    if any(c.isspace() for c in raw):
        return jsonify(error='URL must not contain spaces.'), 400
    candidate = raw if '://' in raw else 'https://' + raw
    try:
        parts = urlsplit(candidate)
        host = parts.hostname
        if parts.scheme not in ('http', 'https') or not host or parts.username or parts.password:
            raise ValueError()
        if not re.fullmatch(r'[A-Za-z0-9.\-:\[\]]+', parts.netloc):
            raise ValueError()
        if host == 'localhost' or host.endswith('.local'):
            raise ValueError()
    except (ValueError, TypeError):
        return jsonify(error='Enter a valid public HTTP or HTTPS URL.'), 400

    # Offline lexical heuristics only. No network requests or page fetching.
    score, reasons = 0, []
    def add(points, message):
        nonlocal score
        score += points
        reasons.append(message)
    if parts.scheme == 'http':
        add(15, 'Uses HTTP rather than HTTPS.')
    try:
        ipaddress.ip_address(host)
        add(30, 'Uses an IP address rather than a domain name.')
    except ValueError:
        pass
    if len(candidate) > 100:
        add(15, 'URL is unusually long.')
    if host.count('.') >= 3:
        add(15, 'Contains several subdomains.')
    if host.count('-') >= 3:
        add(15, 'Domain contains many hyphens.')
    if re.search(r'(verify|urgent|password|secure-login|account-update|confirm)', candidate, re.I):
        add(20, 'Contains keywords sometimes used in phishing lures.')
    if '@' in parts.path or '%40' in candidate.lower():
        add(10, 'Contains an encoded or unusual @ character.')
    score = min(score, 100)
    level = 'HIGH' if score >= 60 else 'MEDIUM' if score >= 30 else 'LOW'
    return jsonify(url=candidate, score=score, level=level, indicators=reasons or ['No configured lexical warning signs were found.'], disclaimer='Educational heuristic only. A LOW score does not mean the site is safe. No live reputation check was performed.')

if __name__ == '__main__':
    app.run(debug=True)
