# Elise Javetski

Website for Elise Javetski, prenatal and postpartum strength coach in Jersey City. Live at https://elisejavetski.com.

This repo is public, so never put passwords, private emails or uncropped original photos in it.

## Editing the site

Edit `_src/site.html` (every page lives in that one file), then run:

    python3 _tools/build.py

That writes the four public pages and `sitemap.xml`:

| Page | Address | File |
|---|---|---|
| Home | `/` | `index.html` |
| Coaching | `/coaching/` | `coaching/index.html` |
| Training Tips | `/training-tips/` | `training-tips/index.html` |
| Get started | `/get-started/` | `get-started/index.html` |

Each page gets its own title, description and search data from the settings at the top of `_tools/build.py`. Don't edit the built pages directly; they're overwritten on every build. Old one-page links like `elisejavetski.com/#book` still go to the right page.

Commit and push to `main`, and the live site updates in about a minute.

- Photos live in `img/`; `assets/` holds source files (logos, brand colors, cropped photos).
- The page has a security policy (the `Content-Security-Policy` tag in `_src/site.html`). Any new outside service (fonts, scripts, embeds) has to be added there or browsers will block it.
- Folders starting with `_` aren't published.

## Hosting and domain

- Hosted free on GitHub Pages from the `main` branch. The `CNAME` file holds the domain; HTTPS is enforced.
- The domain is registered at GoDaddy. DNS records:
  - 4 `A` records for `@`: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
  - `CNAME` `www` → `gjavetski.github.io`
  - `CNAME` `pay` → GoDaddy pay links (leave it)
  - `TXT` `@` → `google-site-verification=…` (Google Search Console; leave it)
- `main` is protected against deletion and force-pushes.

## Contact form

The Get started form sends messages through [Web3Forms](https://web3forms.com) (free) to Elise's email.

- Elise owns the Web3Forms account; the receiving email is set in her Web3Forms dashboard, not in this code, so her address never appears on the site.
- The form's access key is in `_src/site.html`. It's meant to be public: it can only send messages to her.
- Spam protection: hCaptcha (turned on in her dashboard) plus a hidden bot trap field.
- After a message sends, the form is replaced with a thank-you message.
- Messages arrive titled "New enquiry from elisejavetski website" and can be answered with Reply.

## Search (Google)

- Google Search Console: `elisejavetski.com` is added as a Domain property and verified by the TXT record above.
- The sitemap `https://elisejavetski.com/sitemap.xml` is submitted. When adding it, enter the full address, not just the domain.
- Bing Webmaster Tools can import everything from Search Console in one click.
- Search data is built in: each page has its own title and description, plus structured data for Elise, her business, the weekly classes and the FAQs.
- Links from her Instagram, LinkedIn and coach directory listings (Girls Gone Strong, NASM) help her name searches the most.

## Old sites

- `beastwithelise.com` (GoDaddy) forwards to elisejavetski.com and is not being renewed (expires April 2027). To pass its search history on, verify it in Search Console and use Settings → Change of address. Keep the forward running until it expires.
- The old Squarespace site is set to Private; its plan is cancelled and ends July 2027. A backup of its pages, photos and form messages was given to Elise.
