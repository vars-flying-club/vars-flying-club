# tools — how the site is generated

**You do not need any of this to edit the website.** Every page in the repository
root is plain HTML; open it, change the words, commit. This folder exists so the
club keeps the machinery, not just the output.

> **Warning — `build_site.py` overwrites the pages it generates.**
> The `.html` files in the repository root are now the source of truth, and
> they contain hand edits made since they were generated. Running
> `build_site.py` would wipe those. Before running it, copy any hand edits
> back into the script. For ordinary text changes, edit the HTML directly and
> leave this folder alone.

## What's here

| File | What it does |
|---|---|
| `build_site.py` | Generates every page in the repository root |
| `build_old.py` | Generates the archived pre-2026 site under `old/` |
| `build_images.py` | Renders the photo archive into `images/photos/` |
| `manifest.py` | Rebuilds `manifest.json` by reading the old Wix site |
| `download.py` | Downloads the full-resolution originals from Wix |
| `sheet.py` | Builds the contact sheets used to choose photographs |
| `template.html` | Page shell used by `sheet.py` |

| Data file | What it holds |
|---|---|
| `manifest.json` / `.csv` | All 290 photographs: code, source page, original Wix id |
| `pick-aircraft.json` | The featured photographs on the Photographs page |
| `pick-history.json` | The 45 chosen for the History page (now superseded — all 178 are shown) |
| `application-form.json` | All 34 questions of the membership application, recovered from the original Google Form |
| `copy.json` | The original Wix site's text, page by page |

## Running them

They need Python 3 and [ImageMagick](https://imagemagick.org) (`magick`).

**The scripts assume a working directory alongside this repository**, holding the
full-resolution originals:

```
~/Desktop/vars-flying-club/          working directory (NOT in git — 216 MB)
    originals/                       the 291 untouched photographs
    work/                            where these scripts expect to run from
~/Desktop/vars-flying-club-site/     this repository
```

Paths are hard-coded to those two locations near the top of each script. If you
put things elsewhere, edit the `B =` and `R =` lines.

```bash
python3 build_site.py     # rebuild the main pages
python3 build_old.py      # rebuild the archived site
python3 build_images.py   # re-render every photograph
```

Each writes directly into the repository. Review with `git diff`, then commit.

## The originals are not in this repository

The 291 full-resolution photographs — 216 MB, straight off the cameras with EXIF
intact — are deliberately not committed; the repo carries web-sized copies
instead. **They exist in only two places: the working directory above, and a set
of 17 zip files emailed on 2026-09-07.**

That is a single point of failure. If they matter to the club, put a copy
somewhere the club collectively controls.
