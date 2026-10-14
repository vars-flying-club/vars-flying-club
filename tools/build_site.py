#!/usr/bin/env python3
"""Emit the VARS static site. Output is plain HTML meant to be hand-edited
afterwards — this script exists only so the shared nav and footer stay
identical across every page while the site is being scaffolded."""

import json, os

R = os.path.expanduser('~/Desktop/vars-flying-club-site')
W = os.path.expanduser('~/Desktop/vars-flying-club')

SCHED = "https://www.aircraftclubs.com"
APPLY = "https://forms.gle/FnZu9H9wvF6LaMSW8"

NAV = [("index.html", "Home"), ("about.html", "About"), ("join.html", "Join"),
       ("history.html", "History"), ("photographs.html", "Photographs"),
       ("video.html", "Video"), ("for-members.html", "For Members"),
       ("contact.html", "Contact")]


def nav(active):
    out = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == active else ''
        out.append(f'      <li><a href="{href}"{cur}>{label}</a></li>')
    return "\n".join(out)


def page(fname, title, desc, hero, body, wide=False):
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500&display=swap">
<link rel="stylesheet" href="css/style.css">
</head>
<body>

<header class="masthead">
  <a class="masthead__mark" href="index.html">V.A.R.S.</a>
  <nav class="nav">
    <ul>
{nav(fname)}
    </ul>
  </nav>
</header>

{hero}

<main class="wrap{' wrap--wide' if wide else ''}">
{body}
</main>

<footer class="footer">
  <p>Valley Aircraft Restoration Society &middot; Falcon Field (KFFZ) &middot; Mesa, Arizona</p>
  <p><a href="contact.html">Contact</a> &middot; <a href="{SCHED}" target="_blank" rel="noopener">Member Login</a></p>
  <p>&copy; 2026 Valley Aircraft Restoration Society. All rights reserved.</p>
</footer>

</body>
</html>
"""
    open(os.path.join(R, fname), 'w').write(html)
    return fname


def banner(h1, sub=None):
    s = f'\n    <p class="hero__sub">{sub}</p>' if sub else ''
    return ('<section class="hero banner">\n  <div class="hero__inner">\n'
            f'    <h1 class="wordmark">{h1}</h1>{s}\n  </div>\n</section>')


# Alt text for the photographs we can actually describe. Anything not listed falls
# back to a numbered label, so every gallery link still has an accessible name
# — a link wrapping an image with empty alt text is a link with no name at all.
ALT = {
    "radio-stack": "The radio stack — PS Engineering audio panel, Garmin GNS 530 and "
                   "the number two comm radio",
}


def gallery(codes, dense=False, base=""):
    """Every photograph lives in one store, images/photos/. `base` lets the
    archived pages under /old/ point back up at the same files instead of
    keeping a second copy."""
    cls = "gallery gallery--dense" if dense else "gallery"
    items = []
    for i, c in enumerate(codes, 1):
        alt = ALT.get(c, f"Photograph {i} of {len(codes)}")
        items.append(
            f'    <figure>\n'
            f'      <a href="{base}images/photos/{c}.jpg" target="_blank" rel="noopener">\n'
            f'        <img src="{base}images/photos/thumb/{c}.jpg" alt="{alt}" loading="lazy">\n'
            f'      </a>\n'
            f'    </figure>')
    return f'  <div class="{cls}">\n' + "\n".join(items) + '\n  </div>'


def shelf(title, note):
    """The bar that separates the featured photographs from the archive."""
    return (f'  <div class="shelf">\n'
            f'    <h2>{title}</h2>\n'
            f'    <p>{note}</p>\n'
            f'  </div>')


MANIFEST = json.load(open(f'{W}/work/manifest.json'))
SKIP = {'F001'}                       # Zelle logo, not a photograph

air  = json.load(open(f'{W}/work/pick-aircraft.json'))          # the featured ten
hist = [r['code'] for r in MANIFEST if r['page'] == 'history']  # all 178
rest = [r['code'] for r in MANIFEST                             # everything else
        if r['page'] != 'history' and r['code'] not in air and r['code'] not in SKIP]

# ------------------------------------------------------------------ Home
page("index.html",
     "VARS | Valley Aircraft Restoration Society",
     "The Valley Aircraft Restoration Society — a flying club with a 1972 "
     "Piper Cherokee 235F based at Falcon Field (KFFZ) in Mesa, Arizona.",
     '<section class="hero hero--home">\n'
     '  <img class="hero__img" src="images/hero.jpg"\n'
     '       alt="The club\'s Piper Cherokee 235F, N2653T, departing Falcon Field">\n'
     '  <div class="hero__inner">\n'
     '    <h1 class="wordmark">V.A.R.S.</h1>\n'
     '    <p class="hero__sub">Valley Aircraft Restoration Society</p>\n'
     '  </div>\n</section>',
     f"""
  <h2>Welcome</h2>

  <p class="lede">We are a flying club at Falcon Field in Mesa, Arizona,
  sharing a four-seat, IFR-equipped 1972 Piper Cherokee 235F kept in a locked hangar.</p>

  <p>The club began in 1989 as a group of volunteers restoring helicopters for static
  display, and became a flying club in the late 1990s. The Cherokee has been ours since
  2017. <a href="history.html">The full story is on the History page.</a></p>

  <p>We are small by design — membership is capped at fifteen — and we meet monthly to
  talk about trips, the aircraft, and maintenance.</p>

  <ul class="facts">
    <li><strong>Home field</strong> &mdash; Falcon Field, Mesa, Arizona (KFFZ)</li>
    <li><strong>Aircraft</strong> &mdash; 1972 Piper Cherokee 235F, N2653T &mdash; four seats, IFR equipped</li>
    <li><strong>Rate</strong> &mdash; $60 per hour, dry, on tach time</li>
    <li><strong>Dues</strong> &mdash; $100 per month, paid quarterly</li>
    <li><strong>Membership</strong> &mdash; capped at 15 pilots</li>
    <li><strong>Scheduling</strong> &mdash; online through
      <a href="{SCHED}" target="_blank" rel="noopener">AircraftClubs</a>, with 24-hour access</li>
  </ul>

  <div class="callout">
    <p><strong>Interested in joining?</strong> Our membership is currently full, but we
    still accept applications &mdash; see the <a href="join.html">Join page</a>.</p>
  </div>

  <p><a class="btn" href="join.html">Membership &amp; Rates</a></p>
""")

# ------------------------------------------------------------------ About
page("about.html", "About | VARS Flying Club",
     "About the Valley Aircraft Restoration Society flying club at Falcon Field, Mesa, Arizona.",
     banner("About Us"),
     f"""
  <p class="lede">Located at Falcon Field in Mesa, Arizona, VARS is a flying club. Our
  current aircraft is a four-seat, IFR-equipped 1972 Piper Cherokee 235F.</p>

  <ul class="facts">
    <li><strong>The aircraft</strong> &mdash; 1972 Piper Cherokee 235F, N2653T &mdash; four seats, IFR equipped</li>
    <li><strong>Avionics</strong> &mdash; Garmin GNS 530 WAAS, a new number two comm
      radio, and a six-cylinder JPI engine monitor</li>
    <li><strong>Hangared</strong> &mdash; we keep the aircraft in a locked hangar</li>
    <li><strong>Costs</strong> &mdash; $60 per hour, based on tach time, dry</li>
    <li><strong>Membership</strong> &mdash; capped at 15 members. We currently have a
      short wait list, though turnover is limited.</li>
    <li><strong>Meetings</strong> &mdash; monthly, at the Falcon Field club hangar.
      Members are expected to attend when possible, and interested pilots are welcome to
      attend as well.</li>
    <li><strong>Scheduling</strong> &mdash; an
      <a href="{SCHED}" target="_blank" rel="noopener">online system</a> with 24-hour access</li>
    <li><strong>Usage</strong> &mdash; the airplane flies only 70&ndash;90 hours per year, so
      availability is high. Most trips are day trips in Arizona; extended trips are not
      common.</li>
  </ul>

  <div class="callout">
    <p>More photographs of the aircraft and our trips are on the
    <a href="photographs.html">Photographs page</a>.</p>
  </div>

  <h2 id="how-we-run">How we run</h2>

  <p>We focus on pride of ownership. Our usage rate is based on tach time rather than
  Hobbs, which encourages flying with less wear on the engine and greater efficiency
  &mdash; lowering the cost for everyone and taking better care of the aircraft.</p>

  <p>We stress that we are not an airplane rental organization; that is what FBOs are
  for. To keep flying costs low, every member is expected to contribute something to the
  club. What that looks like varies:</p>

  <ul class="facts">
    <li>Some members serve on the board</li>
    <li>Some routinely wash the plane and clean the hangar</li>
    <li>Some club CFIs may offer free currency flights</li>
    <li>Some members help with maintenance on the airplane</li>
    <li>Some purchase supplies for the club</li>
  </ul>

  <p>Where practical and legal, maintenance is performed by members under the watchful
  eye of a qualified A&amp;P.</p>

  <p>Every member pays the same monthly dues and the same hourly rate. That includes our
  officers and board members &mdash; unlike some clubs in the valley, nobody here gets a
  free ride.</p>

  <div class="giving">
    <h3>Giving back</h3>

    <p>We periodically give back to the community by sponsoring functions that introduce
    aviation to youngsters, including local Boy and Girl Scout troops and underprivileged
    children.</p>

    <p>Our members fly for:</p>

    <ul class="giving__list">
      <li><a href="https://www.eaa.org/eaa/youth/free-ye-flights" target="_blank" rel="noopener">Young Eagles</a></li>
      <li><a href="https://www.angelflightwest.org/" target="_blank" rel="noopener">Angel Flight</a></li>
      <li><a href="https://www.flightsforlife.org/" target="_blank" rel="noopener">Flights for Life</a></li>
      <li><a href="https://www.pilotsnpaws.org/" target="_blank" rel="noopener">Pilots N Paws</a></li>
      <li>The Navajo Airlift</li>
    </ul>
  </div>

  <h2>Where to find us</h2>

  <p>Falcon Field sits on the north-east side of Mesa. The club hangar is reached
  through the entry gate; if you are visiting, <a href="contact.html">get in touch</a>
  first and someone will meet you there.</p>

  <ul class="facts">
    <li><strong>Airport</strong> &mdash;
      <a href="http://www.falconfieldairport.com/home-ffa" target="_blank" rel="noopener">Falcon Field Airport</a></li>
    <li><strong>Airport data</strong> &mdash;
      <a href="http://airnav.com/airport/KFFZ" target="_blank" rel="noopener">KFFZ on AirNav</a></li>
    <li><strong>Listen in</strong> &mdash;
      <a href="https://www.liveatc.net/play/kffz2.pls" target="_blank" rel="noopener">KFFZ tower, live</a></li>
    <li><strong>Map</strong> &mdash;
      <a href="https://goo.gl/maps/TTKYU6vAezL2" target="_blank" rel="noopener">entry gate on Google Maps</a></li>
  </ul>
""")

# ------------------------------------------------------------------ Join
page("join.html", "Join | VARS Flying Club",
     "Membership costs, requirements and application for the Valley Aircraft Restoration "
     "Society flying club at Falcon Field, Mesa, Arizona.",
     banner("Interested in Joining?"),
     f"""
  <div class="notice">
    <p><strong>Our membership is currently full, with a short wait list.</strong>
    Turnover is infrequent. We recommend applying now, as our wait list is the shortest
    it has been in over fifteen years.</p>
  </div>

  <p><a class="btn" href="apply.html">Fill out an application</a></p>

  <h2>Why join VARS?</h2>

  <ul class="facts">
    <li>A small club with a family feel</li>
    <li>Our plane is kept in a hangar</li>
    <li>While we only have one plane, the airplane&rsquo;s utilization is very, very low,
      making it easy to schedule a trip</li>
    <li>Our hourly fee is by far the lowest for a high-performance airplane in Arizona,
      and it is a tach rate, not Hobbs</li>
    <li>The airplane is one of the most capable club airplanes in the state in many ways
      &mdash; a very high useful load, excellent high-density-altitude performance, and
      135 knots cruise at 11 to 12 gallons per hour</li>
    <li>Our monthly dues are about half the cost of other clubs</li>
    <li>Online scheduling and 24-hour access</li>
  </ul>

  <p>We take pride in our aircraft, and we love to fly. If you are looking for a place
  to fly at reasonable cost and to be part of a good group of pilots, fill out the
  questionnaire above and we will get back to you. For anything else, the
  <a href="contact.html">Contact page</a> will reach us.</p>

  <h2>Membership</h2>

  <ul class="facts">
    <li><strong>$100 join fee</strong> &mdash; non-refundable (it goes towards updating
      our Arizona Corporation Commission documentation and paying for a new Falcon Field
      gate key)</li>
    <!-- Refund terms parked 2026-09-24 — exact wording is in DECISIONS.md,
         to be restored verbatim. -->
    <li><strong>$2,000 to join</strong></li>
    <li><strong>$100 per month dues</strong> &mdash; paid quarterly, $300 every three
      months (these cover our fixed costs: insurance, the hangar, registration and
      expected annual charges)</li>
    <li><strong>$60 per hour, dry</strong> &mdash; on tach time</li>
    <li><strong>Payment</strong> &mdash; by Zelle only</li>
  </ul>

  <p>Members are responsible for fueling the aircraft after use. It burns roughly 10.5
  to 13 gallons per hour of tach time at a cruise power setting.</p>

  <p>Our fixed expenses are covered by the low monthly dues, and the expenses related to
  actually flying the aircraft are factored into the low hourly rate.</p>

  <div class="callout">
    <p>Before you apply, it is worth reading <a href="about.html#how-we-run">how we
    run</a> &mdash; we are not a rental operation, and every member is expected to
    contribute something to the club.</p>
  </div>
""")

# ------------------------------------------------------------------ History
page("history.html", "History | VARS Flying Club",
     "The story of the Valley Aircraft Restoration Society, from helicopter restoration "
     "in 1989 to a flying club at Falcon Field, Mesa, Arizona.",
     banner("History", "The V.A.R.S. Story"),
     """
  <p class="lede">In 1989 several volunteers at the Commemorative Air Force museum at
  Falcon Field in Mesa, Arizona, realized they shared a mutual interest in restoring
  helicopters for static display.</p>

  <p>Since the CAF primarily restored World War II-era aircraft to airworthy condition,
  these individuals &mdash; many of whom also worked at the adjacent McDonnell Douglas
  Helicopter Company, formerly Hughes Aircraft &mdash; decided to form their own
  organization. Led by K. B. &ldquo;Doc&rdquo; Smith, they began the Valley Aircraft
  Restoration Society in May 1989.</p>

  <p>Soon VARS members were busy restoring a 1967 OH-6A Cayuse, originally built by
  Hughes Aircraft and much used during the Vietnam War as a Light Observation Helicopter
  &mdash; hence its nickname, the &ldquo;Loach&rdquo;. The club eventually donated this
  aircraft to the St. Louis Science Center in Missouri, where over two million annual
  visitors viewed its work. VARS then went to work restoring two Brantly helicopters and
  an experimental one-man jet.</p>

  <p>By the late 1990s, as the original members left VARS, newer members expressed
  interest in turning VARS into a flying club. Soon a 1979 Cessna 152, N47930, graced
  the floor of the club&rsquo;s hangar at Falcon Field. Well flown but limited in
  capacity, the club sold that airplane in 2003 and acquired a 1976 Grumman American
  AA-5A Cheetah. With seating for four and a larger engine, the Cheetah offered members
  the opportunity to expand their cross-country adventures. Unfortunately a hard landing
  in 2007 severely damaged the Cheetah and it was no longer flyable.</p>

  <p>Shortly afterward a 1977 Piper Archer II, N4098Q, replaced the Cheetah. Over the
  next nine years the members of VARS flew the Archer for hundreds of enjoyable hours to
  locations far and near. By late 2016 it had been flown more than 2,200 hours on the
  original engine, and club members faced a difficult decision: spend money overhauling
  the engine, upgrading the avionics to include the FAA-mandated ADS-B Out equipment,
  and making other needed repairs &mdash; or acquire another aircraft. It was not an
  easy decision.</p>

  <p>Ultimately the club opted to sell the Archer and upgrade. In May 2017 VARS took
  possession of a pristine 1972 Piper Cherokee 235F, an aircraft with much greater
  capacity and performance. Well equipped with a Garmin 530W GPS unit, a Garmin 345
  ADS-B In/Out transponder, an autopilot slaved to the 530W, long-range fuel tanks and
  an engine with less than 500 hours, the Cherokee 235 lends itself equally to a quick
  hop for that &ldquo;$100 hamburger&rdquo; and to long cross-country trips.</p>

  <p><em>Written by Edward F. Murphy. Special thanks to DJ Vegh and Pat Butler for their
  input.</em></p>

  <h2>Archival &amp; vintage pictures</h2>

  <p>The club's full archive &mdash; the helicopter restorations, the aircraft that came
  before the Cherokee, and members over the years. Click any photograph to see it full
  size.</p>

""" + gallery(hist, dense=True), wide=True)

# ------------------------------------------------------------------ Photographs
page("photographs.html", "Photographs | VARS Flying Club",
     "Photographs of the VARS Piper Cherokee 235F, members, flights and trips.",
     banner("Photographs", "Members, Flights &amp; Trips"),
     "  <p>Click any photograph to see it full size.</p>\n\n"
     + gallery(air)
     + "\n\n"
     + shelf("The rest of the archive",
             f"Every other photograph carried over from the old site &mdash; "
             f"{len(rest)} in all, members, flights and trips over the years.")
     + "\n\n"
     + gallery(rest, dense=True), wide=True)

# ------------------------------------------------------------------ Video
VIDEOS = [("258317258", "Verde River Flight from Payson to Falcon Field"),
          ("40690971",  "Club flying"),
          ("40689093",  "Club flying")]

page("video.html", "Video | VARS Flying Club",
     "Video from the Valley Aircraft Restoration Society flying club at Falcon Field, "
     "Mesa, Arizona.",
     banner("Video"),
     "  <p>Flying with the club. Use the full-screen control in each player.</p>\n\n"
     + "\n".join(
         f'  <figure class="video">\n'
         f'    <div class="video__frame">\n'
         f'      <iframe src="https://player.vimeo.com/video/{vid}" title="{title}"\n'
         f'              frameborder="0" allow="fullscreen; picture-in-picture"\n'
         f'              allowfullscreen loading="lazy"></iframe>\n'
         f'    </div>\n'
         f'    <figcaption>{title}</figcaption>\n'
         f'  </figure>' for vid, title in VIDEOS))

# ------------------------------------------------------------------ For Members
page("for-members.html", "For Members | VARS Flying Club",
     "Reservations and dues for members of the Valley Aircraft Restoration Society.",
     banner("For Members"),
     f"""
  <h2>Reserve the aircraft</h2>

  <p>Scheduling is online, with 24-hour access.</p>

  <p><a class="btn" href="{SCHED}" target="_blank" rel="noopener">Make a reservation</a></p>

  <h2>Dues and fees</h2>

  <div class="rows">
    <div class="row">
      <span class="row__label">Join fee</span>
      <span class="row__value">$100 one-time</span>
      <span class="row__note">Non-refundable (it goes towards updating our Arizona
        Corporation Commission documentation and paying for a new Falcon Field gate
        key).</span>
    </div>
    <div class="row">
      <!-- Refund terms parked 2026-09-24 — exact wording is in DECISIONS.md,
           to be restored verbatim. -->
      <span class="row__label">Membership fee</span>
      <span class="row__value">$2,000 one-time</span>
    </div>
    <div class="row">
      <span class="row__label">Dues &mdash; monthly</span>
      <span class="row__value">$100 per month</span>
    </div>
    <div class="row">
      <span class="row__label">Dues &mdash; quarterly</span>
      <span class="row__value">$300 every three months</span>
    </div>
    <div class="row">
      <span class="row__label">Hourly rate</span>
      <span class="row__value">$60 per hour, dry</span>
      <span class="row__note">Charged on tach time. Members fuel the aircraft after use.</span>
    </div>
  </div>

  <p>Payments are accepted by Zelle only.</p>

  <div class="callout">
    <p>For payment arrangements and anything else to do with dues, contact the club
    treasurer.</p>
  </div>
""")

# ------------------------------------------------------------------ Contact
page("contact.html", "Contact | VARS Flying Club",
     "Get in touch with the Valley Aircraft Restoration Society flying club at Falcon "
     "Field, Mesa, Arizona.",
     banner("Contact Us"),
     """
  <p class="lede">Fill out the information below and we will get back to you as soon as
  we can.</p>

  <p>If you are applying for membership, please use the
  <a href="join.html">application form on the Join page</a> instead &mdash; it asks the
  questions we need answered.</p>

  <!-- ============================================================
       This form posts to Web3Forms, which emails each submission to the
       address the access key below is registered to. Nothing is stored on
       our own server, and no server-side code is involved.

       The access key is not a secret — it only says where to deliver mail.

       The access key is not a secret — it only says which mailbox to deliver
       to. To send enquiries somewhere else, get a new key at
       https://web3forms.com and replace it below.

       After sending, people land on thanks.html — that is what "redirect"
       does. If the domain ever changes, that field has to change with it.
       ============================================================ -->
  <form class="form" action="https://api.web3forms.com/submit" method="POST">

    <input type="hidden" name="access_key" value="f3547748-3929-4799-b546-ac9b09d8d53d">
    <input type="hidden" name="subject" value="Enquiry from the VARS Flying Club website">
    <input type="hidden" name="from_name" value="VARS Flying Club website">
    <input type="hidden" name="redirect" value="https://varsflyingclub.com/thanks.html">

    <!-- Spam trap. People never see it; bots fill it in and get rejected. -->
    <input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off">

    <label for="f-name">Your name
      <input id="f-name" name="name" type="text" autocomplete="name" required>
    </label>

    <label for="f-email">Email
      <input id="f-email" name="email" type="email" autocomplete="email" required>
    </label>

    <label for="f-phone">Phone (optional)
      <input id="f-phone" name="phone" type="text" autocomplete="tel">
    </label>

    <label for="f-subject">Subject
      <input id="f-subject" name="subject_line" type="text">
    </label>

    <label for="f-message">Message
      <textarea id="f-message" name="message" required></textarea>
    </label>

    <button type="submit">Send</button>
  </form>

  <h2>Where we are</h2>

  <p>Falcon Field Airport (KFFZ), Mesa, Arizona. The club hangar is reached through the
  entry gate &mdash;
  <a href="https://goo.gl/maps/TTKYU6vAezL2" target="_blank" rel="noopener">see it on Google Maps</a>.</p>
""")

# ------------------------------------------------------------------ Thanks
page("thanks.html", "Thank you | VARS Flying Club",
     "Your message to the Valley Aircraft Restoration Society has been sent.",
     banner("Thank You"),
     """
  <p class="lede">Your message has been sent. We will get back to you as soon as we
  can.</p>

  <p>In the meantime, have a look at the <a href="history.html">club history</a> or the
  <a href="photographs.html">photographs</a>.</p>

  <p><a class="btn" href="index.html">Back to the home page</a></p>
""")

# ------------------------------------------------------------------ Apply
# The membership questionnaire, rebuilt from the original Google Form
# ("VARS Prospective Member Profile") so the club owns it outright. The
# question list lives in work/application-form.json.

FORM = json.load(open(f'{W}/work/application-form.json'))


def field(item, n):
    """One question. The input's `name` is the question text itself, because
    Web3Forms uses it as the label in the email it sends."""
    label = " ".join(item['label'].split())
    nm = label.replace('"', "'")
    req = item.get('required', False)
    star = ' <abbr title="required">*</abbr>' if req else ''
    r = ' required' if req else ''
    t = item['type']
    opts = [o for o in item.get('options', []) if o]

    if t == 'paragraph':
        ctl = f'<textarea id="q{n}" name="{nm}"{r} rows="3"></textarea>'
    elif t in ('multiple_choice', 'dropdown'):
        ctl = '<div class="choices">' + "".join(
            f'<label class="choice"><input type="radio" name="{nm}" '
            f'value="{o}"{r}> {o}</label>' for o in opts) + '</div>'
    elif t == 'checkboxes':
        ctl = '<div class="choices">' + "".join(
            f'<label class="choice"><input type="checkbox" name="{nm}" '
            f'value="{o}"> {o}</label>' for o in opts) + '</div>'
    else:
        ctl = f'<input id="q{n}" name="{nm}" type="text"{r}>'

    # A choice question is a group of inputs, not one control, so it cannot be
    # a <label> — and it must not be a <p> either, since a <p> may not contain
    # a <div> and the browser would silently split it apart. role="group" plus
    # aria-labelledby gives the group an accessible name instead.
    if t in ('multiple_choice', 'dropdown', 'checkboxes'):
        return (f'      <div class="field" role="group" aria-labelledby="q{n}-label">\n'
                f'        <span class="field__label" id="q{n}-label">{label}{star}</span>\n'
                f'        {ctl}\n'
                f'      </div>')
    return (f'      <label class="field" for="q{n}">\n'
            f'        <span class="field__label">{label}{star}</span>\n'
            f'        {ctl}\n'
            f'      </label>')


groups, cur = [], {'title': 'Your details', 'items': []}
for it in FORM['items']:
    if it['type'] == 'section_header':
        groups.append(cur)
        cur = {'title': " ".join(it['label'].split()), 'items': []}
    else:
        cur['items'].append(it)
groups.append(cur)

n = 0
blocks = []
for g in groups:
    if not g['items']:
        continue
    rendered = []
    for it in g['items']:
        n += 1
        rendered.append(field(it, n))
    blocks.append(f'    <fieldset>\n      <legend>{g["title"]}</legend>\n'
                  + "\n".join(rendered) + '\n    </fieldset>')

page("apply.html", "Apply | VARS Flying Club",
     "Membership application for the Valley Aircraft Restoration Society flying club at "
     "Falcon Field, Mesa, Arizona.",
     banner("Membership Application"),
     """
  <p class="lede">This is the club's prospective member profile. It is long, deliberately
  &mdash; we would rather understand a pilot properly than rush the process.</p>

  <div class="notice">
    <p>Our membership is currently full, with a short wait list. We still read every
    application. Questions marked <abbr title="required">*</abbr> are required.</p>
  </div>

  <!-- ============================================================
       Posts to Web3Forms, which emails each application on. The access
       key is not a secret — it only says which mailbox to deliver to.

       This key is registered to applications@varsflyingclub.com, which
       Cloudflare Email Routing fans out to the membership committee. To
       change who receives applications, edit the routing rule in
       Cloudflare — nothing on this page needs to change.
       ============================================================ -->
  <form class="form form--long" action="https://api.web3forms.com/submit" method="POST">

    <input type="hidden" name="access_key" value="c3b797b6-dd1e-4e23-ab02-34333fad2e37">
    <input type="hidden" name="subject" value="Membership application from the VARS website">
    <input type="hidden" name="from_name" value="VARS Flying Club website">
    <input type="hidden" name="redirect" value="https://varsflyingclub.com/applied.html">

    <!-- Spam trap. People never see it; bots fill it in and get rejected. -->
    <input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off">

""" + "\n\n".join(blocks) + """

    <button type="submit">Send application</button>
  </form>
""")

# ------------------------------------------------------------------ Applied
page("applied.html", "Application received | VARS Flying Club",
     "Your membership application to the Valley Aircraft Restoration Society has been sent.",
     banner("Application Received"),
     """
  <p class="lede">Thank you &mdash; your application has been sent.</p>

  <p>Our membership is currently full with a short wait list, and turnover is infrequent,
  so it may be a while before you hear from us. We do read every application.</p>

  <p>In the meantime, have a look at the <a href="history.html">club history</a> or the
  <a href="photographs.html">photographs</a>.</p>

  <p><a class="btn" href="index.html">Back to the home page</a></p>
""")

print("built:", ", ".join(sorted(f for f in os.listdir(R) if f.endswith('.html'))))
