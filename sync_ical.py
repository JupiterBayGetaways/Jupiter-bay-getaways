import json, os, urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
config = json.loads((ROOT / 'config.json').read_text())

def unfold(s):
    return s.replace('\r\n ', '').replace('\n ', '')

def parse_dt(v):
    v = v.strip()
    if 'T' in v:
        try:
            return datetime.strptime(v[:15], '%Y%m%dT%H%M%S').date()
        except ValueError:
            pass
    try:
        return datetime.strptime(v[:8], '%Y%m%d').date()
    except ValueError:
        return None

def fetch(url):
    if not url:
        raise RuntimeError('Missing calendar URL environment variable')
    req = urllib.request.Request(url, headers={'User-Agent': 'JupiterBayGetawaysCalendarSync/1.0'})
    with urllib.request.urlopen(req, timeout=45) as response:
        return response.read().decode('utf-8', 'replace')

def blocked_dates(ics_text):
    lines = unfold(ics_text).replace('\r\n', '\n').split('\n')
    dates = []
    cur = None
    for line in lines:
        if line.startswith('DTSTART') and ':' in line:
            cur = parse_dt(line.split(':', 1)[1])
        elif line.startswith('DTEND') and cur and ':' in line:
            end = parse_dt(line.split(':', 1)[1])
            if end:
                d = cur
                while d < end:
                    dates.append(d.isoformat())
                    d += timedelta(days=1)
            cur = None
    return sorted(set(dates))

out = {
    'updatedAt': datetime.now(timezone.utc).isoformat(),
    'source': 'VRBO iCal feeds',
    'properties': {}
}

for p in config['properties']:
    env_name = p['env']
    url = os.environ.get(env_name)
    if not url:
        raise RuntimeError(f'Missing GitHub Actions secret: {env_name}')
    dates = blocked_dates(fetch(url))
    out['properties'][p['id']] = {
        'name': p['name'],
        'unavailable': dates
    }

(ROOT / 'availability.json').write_text(json.dumps(out, indent=2))
print('Wrote availability.json for', len(out['properties']), 'properties')
