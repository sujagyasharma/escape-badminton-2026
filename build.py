"""Builds site/index.html for GitHub Pages from ../escape-badminton-2026.html.

Usage:  python3 site/build.py            (from the project folder)
Set FORM_URL below to the Google Form's public link once it exists.
"""
import pathlib, re, shutil

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdqi6wUXn7TLGzNCddYiROwS0295HAV4ag6rurBFojpj00Tqw/viewform"

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
SITE_URL = "https://escape.aptilab.in/"

src = (ROOT / "escape-badminton-2026.html").read_text()

# The page source has no <head> of its own (claude.ai adds one), so split off
# the <title>/<meta>/<link>/<style> preamble and put it in a real <head>.
body_start = src.index('<header class="top">')
preamble, body = src[:body_start], src[body_start:]
preamble = re.sub(r'<meta name="claude:viewport-fit-sides"[^>]*>\n', "", preamble)

def sub1(old, new):
    global body
    assert body.count(old) == 1, old[:60]
    body = body.replace(old, new)

# Hero: point people at registration.
sub1('Registration forms, online and on paper, will be shared soon.',
     'Register online or on paper. See Registration below.')
sub1('<div class="row" style="justify-content:center">\n            <a class="btn light"',
     '<div class="row" style="justify-content:center">\n            <a class="btn sun" href="#register">Register</a>\n            <a class="btn light"')

# Registration steps + form area.
open_now = bool(FORM_URL)
sub1('<li><h3>Register</h3><p class="muted">Online and paper registration forms will be shared soon in the WhatsApp group.</p><span class="pill status">Coming soon</span></li>',
     '<li><h3>Register</h3><p class="muted">Fill in one form per player. For a doubles pair or a couple, one player fills in the form for both. '
     'You can enter at most 2 categories, plus Couples. '
     'Last date: 17 Nov for Under-10, Under-14 and Couples; 25 Nov for Under-18, Men, Women, Mixed and 60+.</p>'
     f'<span class="pill status">{"Open now" if open_now else "Opening soon"}</span></li>')

if open_now:
    embed = FORM_URL.split("?")[0] + "?embedded=true"
    form_area = f'''
      <div class="formbox" id="form">
        <div class="formhead">
          <h3>Registration form</h3>
          <div class="row">
            <a class="btn wa" href="{FORM_URL}" target="_blank" rel="noopener">Open the form in a new tab</a>
            <a class="btn ghost" href="paper-registration-form.pdf" target="_blank" rel="noopener">Paper form (PDF)</a>
          </div>
        </div>
        <iframe src="{embed}" title="Escape Badminton Tournament 2026 registration form" loading="lazy">Loading…</iframe>
      </div>'''
else:
    form_area = '''
      <div class="formbox" id="form">
        <div class="formhead">
          <h3>Registration form</h3>
          <p class="muted">The online form opens soon. We'll post the link in the WhatsApp group.</p>
          <div class="row">
            <a class="btn ghost" href="paper-registration-form.pdf" target="_blank" rel="noopener">Paper form (PDF)</a>
          </div>
        </div>
      </div>'''
sub1('''<span class="pill status">From 21 Nov</span></li>
      </ol>''', '''<span class="pill status">From 21 Nov</span></li>
      </ol>''' + form_area)

extra_css = '''
/* registration form */
.formbox{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:clamp(16px,3vw,24px);display:grid;gap:16px;min-width:0}
.formhead{display:grid;gap:10px}
.formbox iframe{display:block;width:100%;height:2300px;border:0;border-radius:8px;background:#fff}
@media (max-width:640px){.formbox iframe{height:2800px}}
'''
preamble = preamble.replace("</style>", extra_css + "</style>", 1)

desc = ("Escape residents' badminton tournament: 21, 22, 28 and 29 November at the Escape badminton court. "
        "Categories, rules and registration.")
head = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="{desc}">
<meta name="theme-color" content="#1D6A55">
<meta property="og:type" content="website">
<meta property="og:title" content="Escape Badminton Tournament 2026">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE_URL}">
<meta property="og:image" content="{SITE_URL}images/banner.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 26 26'%3E%3Ccircle cx='13' cy='20' r='4.5' fill='%23B8730F'/%3E%3Cpath d='M9 18 L5 3 M13 16 V2 M17 18 L21 3 M7 10 H19' stroke='%231D6A55' stroke-width='2' fill='none' stroke-linecap='round'/%3E%3C/svg%3E">
<style>body{{margin:0}}img{{max-width:100%}}[hidden]{{display:none!important}}:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}</style>
{preamble.strip()}
</head>
<body>
'''
(SITE / "index.html").write_text(head + body.rstrip() + "\n</body>\n</html>\n")

(SITE / "images").mkdir(exist_ok=True)
shutil.copy(ROOT / "google/images/banner.png", SITE / "images/banner.png")
shutil.copy(ROOT / "google/paper-registration-form.pdf", SITE / "paper-registration-form.pdf")
(SITE / ".nojekyll").write_text("")
print("built", SITE / "index.html", "form:", "open" if open_now else "not yet")
