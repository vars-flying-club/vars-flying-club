# VARS site migration — decisions and open flags

Wix → static HTML on GitHub Pages, following the Scottsdale Flying Club pattern
(`~/Desktop/scottsdale-flying-club`, github.com/ScapefoxLLC/scottsdale-flying-club).

## Settled

| | |
|---|---|
| Photographs page | ~10 images max, aircraft only |
| History page | Keep a reduced archival gallery — separate selection |
| Image resolution | Heavily reduced for the web; originals archived only |
| Videos | **Three Vimeo embeds**, restored on the Video page |
| Blog | Delete — 3 untouched Wix demo posts from 2016 |
| Wix Inbox | Not exporting past contact-form submissions |
| Site source | Rebuild in clean HTML; Wix markup is not salvageable |
| Archive | 290 originals, 225 MB, emailed as 17 self-contained zip parts |

## Built and published

- Local: `~/Desktop/vars-flying-club-site` (a sibling of this directory, so the
  225 MB of originals can never be committed)
- Repo: <https://github.com/ScapefoxLLC/vars-flying-club> — public, `main`
- Live: <https://scapefoxllc.github.io/vars-flying-club/> — Pages from `main` at
  root, matching the SFC setup. No CNAME yet, pending the domain decision.

9 pages, 54 images, ~10 MB. P021 and P052 were dropped from the gallery,
leaving 9 photographs.

## Parked copy — to be restored verbatim

The refund terms on the $2,000 membership fee were removed on 2026-09-24 at
Ted's request, to go back **exactly as written**. Both snippets below are the
live wording as it stood immediately before removal. Restore them in
`work/build_site.py`, then rebuild.

**Join page** — inside the Membership `<ul class="facts">`, the `$2,000` item
read:

```html
    <li><strong>$2,000 to join</strong> &mdash; fully refundable during your first year,
      which is a probationary period; $500 of it is refundable after that</li>
```

**For Members page** — the Membership fee row carried this third span:

```html
      <span class="row__note">Fully refundable during the first year, which is a
        probationary period. After that, $500 is refundable when leaving the club.</span>
```

Also recoverable from git: the last commit containing both is `9afff35`
(`git show 9afff35:join.html`).

## Open flags — revisit before go-live

**Contact form delivers to Ted's personal address, not a club one.** The
Web3Forms key `f3547748-…` is wired in and tested end to end (submitted from
the live page, redirect to `thanks.html` confirmed). It points at
theodoredryden@gmail.com. Before this replaces the Wix site, get a new key
registered to a club address and swap it. The key is public by design, so
changing the destination means a *new key*, not editing this one — and the old
one stays visible in git history.

**The `redirect` field still points at the GitHub Pages review URL.** Change it
to the real domain at cutover, or senders will land on the review address.

**Form spam: honeypot only, and Web3Forms has deprecated it.** `contact.html`
uses the `botcheck` honeypot, which Web3Forms' own docs now mark "NOT
RECOMMENDED ... depreciated. Please use any other captcha." Deliberate for now
— see reasoning below — but if spam starts arriving, the fix is hCaptcha (free,
zero-config: one `<div class="h-captcha" data-captcha="true">` plus their
script, then enable it in the Web3Forms dashboard). reCaptcha, Cloudflare
Turnstile and Restrict-to-Domain are all Pro-only. Note hCaptcha adds a puzzle
users must solve, on the club's only enquiry path.

**Applications: DONE.** `apply.html` rebuilds the old "VARS Prospective Member
Profile" Google Form (34 questions, recovered to `work/application-form.json`)
because the original form's owner was unreachable. It posts with Web3Forms key
`c3b797b6-…`, registered to **applications@varsflyingclub.com**, which
Cloudflare Email Routing fans out to the membership committee via an Email
Worker. Tested end to end from the live site 2026-10-01.

To change who receives applications, edit the **Cloudflare routing rule** — the
website needs no change. Past responses to the old Google Form remain with its
owner and are not recoverable.

**Contact form still goes to Ted's personal Gmail.** `contact.html` is still on
the original key `f3547748-…`. To move it, create `contact@varsflyingclub.com`
in Cloudflare, get a key for it at web3forms.com, and swap it in — same
one-line change as the application form.

**Domain: on hold.** Ted is migrating the domain out of Wix separately. Do not
register anything or touch DNS until that lands. The site stays on
scapefoxllc.github.io until then.


**Contact form destination.** Currently set to Ted's own address as a placeholder.
Must be changed to a club address before launch. Needs a new Web3Forms access key
(SFC's key is tied to its own destination) and the final domain in the `redirect`
field.

**Zelle details and dues on `/for-members`.** The current Wix page publishes the
$2000 join fee, quarterly dues, Zelle as preferred payment, and "contact club
treasurer" on a fully public, indexable page. Decide whether that stays public,
gets trimmed, or moves behind something.

**Domain.** Live site is `varsflyingclub.com`, registered *at Wix*, expires
2027-02-17, with `clientTransferProhibited` and `clientUpdateProhibited` set.
Transferring out needs a Wix dashboard unlock plus an auth code.
`varsflyingclub.org` is unregistered and available (~$12/yr) — registering it
sidesteps the Wix registrar entirely and allows a zero-risk launch.

**Cancel Wix last.** Only after DNS has cut over and propagated.

## Carries over free — no work needed

- Membership application is already a Google Form: `forms.gle/FnZu9H9wvF6LaMSW8`
- Scheduling is an external link to AircraftClubs.com
- Falcon Field / AirNav / LiveATC links on the About page

## Layout

```
originals/      290 untouched full-resolution images, by source page
archive/        17 self-contained zip parts (emailed)
work/           manifest, thumbnails, contact-sheet generator, scripts
```

`work/manifest.csv` maps every code (P001, H042, …) to its file and original
Wix media id.
