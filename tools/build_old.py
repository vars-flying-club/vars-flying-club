#!/usr/bin/env python3
"""Build /old/ — an archived copy of the Wix site as it stood before the 2026
rebuild.

The text is reproduced as it was written, including figures and claims that are
no longer current. Every page carries a banner saying so and a noindex tag, so
search engines never surface it alongside the live site.

Photographs are NOT duplicated: these pages link up to ../images/photos/, the
same files the live site uses.
"""
import json, os

B = os.path.expanduser('~/Desktop/vars-flying-club')
R = os.path.expanduser('~/Desktop/vars-flying-club-site')
OLD = f'{R}/old'
os.makedirs(OLD, exist_ok=True)

MANIFEST = json.load(open(f'{B}/work/manifest.json'))
def codes(page):
    return [r['code'] for r in MANIFEST if r['page'] == page]

NAV = [("index.html", "Home"), ("about.html", "About"), ("join.html", "Join"),
       ("history.html", "History"), ("photographs.html", "Photographs"),
       ("video.html", "Video"), ("for-members.html", "For Members"),
       ("contact.html", "Contact"), ("blog.html", "Blog")]

SCHED = "https://www.aircraftclubs.com"
APPLY = "https://forms.gle/FnZu9H9wvF6LaMSW8"


def nav(active):
    return "\n".join(
        f'      <li><a href="{h}"{" aria-current=\"page\"" if h == active else ""}>{l}</a></li>'
        for h, l in NAV)


def gallery(cs, dense=True):
    cls = "gallery gallery--dense" if dense else "gallery"
    items = "\n".join(
        f'    <figure>\n'
        f'      <a href="../images/photos/{c}.jpg" target="_blank" rel="noopener">\n'
        f'        <img src="../images/photos/thumb/{c}.jpg" alt="Archived photograph {i}" loading="lazy">\n'
        f'      </a>\n'
        f'    </figure>' for i, c in enumerate(cs, 1))
    return f'  <div class="{cls}">\n{items}\n  </div>'


def page(fname, title, body, wide=False):
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{title} (archived) | VARS Flying Club</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500&display=swap">
<link rel="stylesheet" href="../css/style.css">
</head>
<body>

<div class="archive-bar">
  <p><strong>This is an archived copy</strong> of the club website as it stood before the
  2026 rebuild. Fees, availability and other details here are out of date and kept only
  for reference. <a href="../index.html">Go to the current site &rarr;</a></p>
</div>

<header class="masthead">
  <a class="masthead__mark" href="index.html">V.A.R.S.</a>
  <nav class="nav">
    <ul>
{nav(fname)}
    </ul>
  </nav>
</header>

<section class="hero banner">
  <div class="hero__inner">
    <h1 class="wordmark">{title}</h1>
  </div>
</section>

<main class="wrap{' wrap--wide' if wide else ''}">
{body}
</main>

<footer class="footer">
  <p>Archived copy &middot; Valley Aircraft Restoration Society &middot; Falcon Field (KFFZ), Mesa, Arizona</p>
  <p><a href="../index.html">Current site</a></p>
</footer>

</body>
</html>
"""
    open(f'{OLD}/{fname}', 'w').write(html)


# ---------------------------------------------------------------- Home
page("index.html", "V.A.R.S.", """
  <p class="lede">V.A.R.S. &mdash; Valley Aircraft Restoration Society Flying Club</p>

  <p>The old home page was a full-screen photograph of the aircraft with the club name
  over it, and no other text.</p>

  <p><em>All content on this website is subject to copyright laws.</em></p>
""")

# ---------------------------------------------------------------- About
page("about.html", "About Us", """
  <p class="lede">Located at Falcon Field in Mesa, Arizona. VARS is non-profit flying
  club.</p>

  <ul class="facts">
    <li>Our current aircraft is a four seat IFR equipped 1972 Piper Cherokee 235F.</li>
    <li>Our costs are based off Tach time use, dry.</li>
    <li>We keep our aircraft in a locked hangar</li>
    <li>Our club has a cap of 15 members.</li>
    <li>We meet monthly to discuss trips, the aircraft, our spouses, and maintenance.
      Not necessarily in that order.</li>
    <li>We use an online scheduling system</li>
    <li>There is no minimums on use if you want to take the aircraft overnight, or for
      extended trips.</li>
  </ul>

  <ul class="facts">
    <li><a href="http://airnav.com/airport/KFFZ" target="_blank" rel="noopener">KFFZ on AirNav.com</a></li>
    <li><a href="https://www.liveatc.net/play/kffz2.pls" target="_blank" rel="noopener">Listen to KFFZ tower live!</a></li>
    <li><a href="https://goo.gl/maps/TTKYU6vAezL2" target="_blank" rel="noopener">Map to Entry Gate</a></li>
  </ul>

  <h2>Where to go</h2>

  <p>Hover over corner pictures to scroll. Double-click to enlarge.</p>

""" + gallery(codes('about')), wide=True)

# ---------------------------------------------------------------- Join
page("join.html", "Interested in Joining?", f"""
  <p class="page-sub" style="margin:0 0 22px">The original page had a
  &ldquo;Click Here to Fill Out Application&rdquo; button here, pointing at a Google Form
  that is no longer monitored. Use the
  <a href="../apply.html">current application form</a> instead.</p>

  <div class="notice">
    <p>Our membership is currently full. Please understand membership turnover is very
    infrequent. Although we are accepting applications, you may not hear from us for a
    very extended period of time.</p>
  </div>

  <h2>Why Join VARS?</h2>

  <ul class="facts">
    <li>We are a small club with more of a family feel and you become more of a virtual
      owner than a renter.</li>
    <li>Our plane is kept in a hangar!</li>
    <li>While we only have one plane, the ratio of members per plane is less than some
      other clubs.</li>
    <li>We do keep slightly more of the join fee than other clubs but the upfront
      out-of-pocket expense is less.</li>
    <li>Our monthly dues are about half the cost of other clubs.</li>
    <li>Online scheduling and 24hr access.</li>
  </ul>

  <p>We take pride in our aircraft, and love to fly.</p>

  <p>Looking for a place to fly at a reasonable cost and be part of a great group of
  pilots?</p>

  <p>If you're interested in joining or would like more information, please fill out our
  questionnaire and we will get back to you shortly. If you have any other questions
  please check out our <a href="contact.html">Contact page</a>!</p>

  <h2>Membership Info</h2>

  <ul class="facts">
    <li>$2000 to Join ($400 refundable when leaving)</li>
    <li>$100 per Month Dues (Paid Quarterly - $300 every 3 mo)</li>
    <li>$60/hour, Dry Rate (TACH time)</li>
  </ul>

  <p>Members are responsible for fueling aircraft after use. The aircraft burns
  approximately 10.5 to 14 gallons per hour (tach time) at a cruise power setting.</p>

  <p>Our fixed expenses are set up as low monthly dues. Expenses related related to the
  use of the aircraft are factored into the low usage rate.</p>

  <p>We focus on pride of ownership. As a result, our usage rate is based on Tach time
  rather than Hobbs. This encourages flyers to fly with less wear on the engine, and
  greater efficiency. Ultimately, lowering the cost for all, and taking greater care of
  the aircraft.</p>

  <p>We stress that we are not an airplane rental organization. That's what FBO's are
  for. In order to keep flying costs low, members are expected to participate in aircraft
  care and support, and facility (aka "the hangar") maintenance. When practical and
  legal, maintenance is performed by members under the watchful eye of a qualified
  A&amp;P.</p>

  <p>As a non-profit organization, we periodically give back to the community by
  sponsoring functions aimed at introducing aviation to youngsters including local Boy
  and Girl Scout troops as well as underprivileged children.</p>

  <p>If you're interested in joining or would like more information, please visit fill
  out our questionnaire above and we will get back to you shortly.</p>
""")

# ---------------------------------------------------------------- History
page("history.html", "History", """
  <p class="page-sub">Archival &amp; Vintage Pictures</p>

  <h2>The V.A.R.S. Story &amp; History</h2>

  <p>In 1989 several volunteers at the Commemorative Air Force museum at Falcon Field in
  Mesa, Arizona, realized they shared a mutual interest in restoring helicopters for
  static displays. Since the CAF primarily restored World War II-era aircraft to
  airworthiness condition, these individuals, many of whom also worked at the adjacent
  McDonnell Douglas Helicopter Company (formerly Hughes Aircraft), decided to form their
  own organization. These enthusiasts, led by K. B. &ldquo;Doc&rdquo; Smith, began the
  Valley Aircraft Restoration Society in May 1989 as a non-profit corporation.</p>

  <p>Soon VARS members were busy restoring a 1967 OH-6A Cayuse, originally built by
  Hughes Aircraft and much used during the Vietnam War as a Light Observation Helicopter
  (thus, its nickname &ldquo;Loach.&rdquo;). The club eventually donated this aircraft to
  the St. Louis, Missouri, Science Center where over two million annual visitors viewed
  its work. VARS then went to work restoring two Brantly helicopters and an experimental
  one-man jet.</p>

  <p>By the late 1990s, as the original members left VARS, newer members expressed
  interest in turning VARS into a flying club. Soon a 1979 Cessna 152, (N47930), graced
  the floor of the club's hangar at Falcon Field. Well flown but limited in capacity, the
  club sold that airplane in 2003 and acquired a 1976 Grumman American AA-5A Cheetah.
  With seating for four and larger engine the Cheetah offered club members the
  opportunity to expand their cross country adventures. Unfortunately, a hard landing in
  2007 severely damaged the Cheetah and it was no longer flyable. Shortly afterward, a
  1977 Piper Archer II (N4098Q), quickly replaced the Cheetah. Over the next nine years,
  the members of VARS flew the Archer for hundreds of enjoyable hours to locations far
  and near. By late 2016 the Archer had been flown for more than 2,200 hours on the
  original engine. Club members faced a difficult decision: Should money be spent on
  overhauling the engine, upgrading the avionics, to include the FAA-mandated ADS-B out
  equipment, and making other needed repairs to the Archer, or should the club acquire
  another aircraft. It was not an easy decision.</p>

  <p>Ultimately, the club opted to sell the Archer and upgrade its aircraft. In May 2017
  VARS took possession of a pristine 1972 Piper Cherokee 235F. This aircraft provided
  much greater capacity and performance to the members. Well-equipped with a Garmin 530W
  GPS unit, a Garmin 345 ADS-B In/Out transponder, an autopilot slaved to the 530W,
  long-range fuel tanks, and an engine with less than 500 hours, the Cherokee 235, lends
  itself to quick hops for that &ldquo;$100 hamburger&rdquo; or long cross country
  trips.</p>

  <p><em>Written by Edward F. Murphy (Special thanks to DJ Vegh and Pat Butler for their
  input)</em></p>

""" + gallery(codes('history')), wide=True)

# ---------------------------------------------------------------- Photographs
page("photographs.html", "Photographs", """
  <p class="page-sub">Members, Flights &amp; Trips</p>

  <p><em>All content on this website is subject to copyright laws.</em></p>

""" + gallery(codes('photographs')), wide=True)

# ---------------------------------------------------------------- Video
page("video.html", "Video", """
  <p>Optimized for desktop, double-click for full screen.</p>

""" + "\n".join(
    f'  <figure class="video">\n'
    f'    <div class="video__frame">\n'
    f'      <iframe src="https://player.vimeo.com/video/{v}" title="Archived club video"\n'
    f'              frameborder="0" allow="fullscreen; picture-in-picture"\n'
    f'              allowfullscreen loading="lazy"></iframe>\n'
    f'    </div>\n'
    f'  </figure>' for v in ("258317258", "40690971", "40689093")))

# ---------------------------------------------------------------- For Members
page("for-members.html", "For Members", f"""
  <h2>Reserve</h2>

  <p><a class="btn" href="{SCHED}" target="_blank" rel="noopener">Make my reservation</a></p>

  <h2>Take My Money</h2>

  <div class="rows">
    <div class="row">
      <span class="row__label">Membership Fee</span>
      <span class="row__value">One-time $2000.00</span>
      <span class="row__note">$400 Returnable when leaving the club</span>
    </div>
    <div class="row">
      <span class="row__label">Monthly</span>
      <span class="row__value">$100.00 every month via Zelle</span>
    </div>
    <div class="row">
      <span class="row__label">Quarterly</span>
      <span class="row__value">$300 every three months via Zelle</span>
    </div>
  </div>

  <h2>Quarterly Dues</h2>

  <p>Set Up Dues for Automatic Withdrawal. Payments will come out the same reoccurring
  day of the month the initial payment is made.</p>

  <div class="callout">
    <p>Zelle is our preffered form of payment. For additional information contact club
    treasurer.</p>
  </div>
""")

# ---------------------------------------------------------------- Contact
page("contact.html", "Contact Us", """
  <p class="lede">Fill out the information below and we will get back to you as soon as
  we can!</p>

  <div class="notice">
    <p>The original contact form was a Wix form and is not reproduced here &mdash; it no
    longer goes anywhere. To reach the club, use the
    <a href="../contact.html">contact form on the current site</a>.</p>
  </div>

  <p>The form asked for: Name, Email, Phone, Subject and Message.</p>
""")

# ---------------------------------------------------------------- Contact Form
page("contact-form.html", "Interested in Joining?", f"""
  <p>This page held an embedded Google Form. That form is no longer monitored, so it is
  not linked here.</p>

  <p><a class="btn" href="../apply.html">Current application form</a></p>
""")

# ---------------------------------------------------------------- Blog
POSTS = [("NEW BOOK: HOLIDAY SEASON SPECIALS", "November 6, 2016"),
         ("THE FRENCH EXPERIENCE", "November 6, 2016"),
         ("BEHIND THE SCENES OF BREAKFAST DELIGHTS", "November 6, 2016")]

page("blog.html", "Blog", """
  <div class="notice">
    <p>The blog was never used. These three posts are the placeholder content that came
    with the Wix template, left untouched since 2016.</p>
  </div>

  <h2>Recent Posts</h2>

""" + "\n\n".join(
    f'  <article>\n'
    f'    <h3>{t}</h3>\n'
    f'    <p class="page-sub" style="margin:0 0 10px">{d}</p>\n'
    f'    <p>This is your blog post. Use this space to connect with your visitors and\n'
    f'    potential customers in a way that&rsquo;s current and interesting....</p>\n'
    f'  </article>' for t, d in POSTS) + """

  <h2>Search By Tags</h2>

  <ul class="facts">
    <li>Bread &mdash; 3 posts</li>
    <li>Cake &mdash; 3 posts</li>
    <li>Chocolate &mdash; 3 posts</li>
    <li>Desserts &mdash; 3 posts</li>
    <li>Fruits &mdash; 3 posts</li>
    <li>Sugar &mdash; 3 posts</li>
  </ul>

  <p>Stay Up-To-Date with New Posts &mdash; Subscribe Now</p>
""")

print("built /old/:", ", ".join(sorted(os.listdir(OLD))))
