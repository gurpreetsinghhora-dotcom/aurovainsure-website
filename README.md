# Aurova Insure website

Source code for **https://aurovainsure.co.uk**, the website of Aurova Insure (a trading name of SBR Ventures Ltd).

## How it's built

- Plain HTML, CSS and a small JavaScript file. No framework, no paid services, no tracking.
- Fonts (Inter and Space Grotesk) are hosted with the site, so visitors' browsers don't contact Google.
- `src/pages/*.html` holds the content of each page.
- `src/build.py` adds the shared header, footer and SEO tags, and writes the finished site into `docs/`.
- `src/contact.json` holds the public email address, the domain mailbox switch and the form key.

To change the text on a page, edit the file in `src/pages/`, then run:

```
python3 src/build.py
```

Then commit and push. GitHub Pages republishes the site within about a minute.

## Hosting

| Item | Detail |
|---|---|
| Host | GitHub Pages (free), serving the `docs/` folder of the `main` branch |
| Domain | aurovainsure.co.uk, registered at GoDaddy (DNS stays at GoDaddy) |
| HTTPS | Free certificate issued automatically by GitHub Pages |
| Recurring cost | £0 (you only pay GoDaddy for the domain renewal) |

### DNS records at GoDaddy

| Type | Name | Value |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | gurpreetsinghhora-dotcom.github.io |

The domain had no email (MX) records when the site was set up, so no email settings were changed.

## Enquiry form

- With no key in `src/contact.json`, the form opens the visitor's email app with the enquiry ready to send.
- To send enquiries straight to your inbox instead, get a free access key from https://web3forms.com, put it in `web3forms_key`, rebuild and push.

## Before relying on the legal pages

The privacy policy and terms are drafts, marked "pending legal review" on the pages. Ask a solicitor to review them, and add the ICO registration number to `src/pages/privacy.html` once it's issued.
