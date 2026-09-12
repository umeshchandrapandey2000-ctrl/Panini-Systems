# Panini Systems | Website Editing & Client Contact Guide

This guide teaches you how the website is built, how to customize any text or design, and how the **Contact & Analysis Request system** sends emails and phone calls directly to you.

---

## 1. The 3 Core Files of the Website

All website code lives inside the [`web/`](file:///c:/Users/upand/OneDrive/Desktop/Panini%20Systems/web/) folder:

| File | What it controls | When to edit it |
|---|---|---|
| **[`web/index.html`](file:///c:/Users/upand/OneDrive/Desktop/Panini%20Systems/web/index.html)** | **Structure & Text** | Edit company name, headlines, service descriptions, form labels, or add new sections. |
| **[`web/app.js`](file:///c:/Users/upand/OneDrive/Desktop/Panini%20Systems/web/app.js)** | **Logic & Configuration** | Set your **email**, **phone number**, math presets, simulation rules, and form submission. |
| **[`web/styles.css`](file:///c:/Users/upand/OneDrive/Desktop/Panini%20Systems/web/styles.css)** | **Visual Styling** | Change accent colors (emerald, gold, cyan), typography, glassmorphism, or card spacing. |

---

## 2. Setting Up Your Phone Number, WhatsApp & Email

At the top of [`web/app.js`](file:///c:/Users/upand/OneDrive/Desktop/Panini%20Systems/web/app.js#L75-L85), you will find the **`CONSULTANT_CONFIG`** object. This is your master settings hub:

```javascript
// web/app.js (Lines ~75-85)
const CONSULTANT_CONFIG = {
  consultantName: "Lead Game Mathematician",
  companyName: "Panini Systems",
  email: "your_real_email@gmail.com",       // <-- Change to your email address
  phone: "+91 98765 43210",                 // <-- Change to your display phone number
  phoneRaw: "+919876543210",                // <-- Numbers only with '+' (for click-to-call)
  whatsappRaw: "919876543210",              // <-- Numbers only without '+' (for WhatsApp link)
  web3FormsAccessKey: "",                   // <-- (Optional) Paste free key to receive emails directly
};
```

When you edit this single object:
* The **"Call"** button automatically calls your phone number when clicked on mobile or desktop.
* The **"WhatsApp"** button automatically opens a WhatsApp chat pre-addressed to you.
* The **"Direct Email"** button and form send inquiries to your email.

---

## 3. How the Form Sends Analysis Requests to Your Email

You have **two powerful options** for receiving email inquiries:

### Option A: Direct Background Email Delivery (Recommended — 100% Free)
You can receive client submissions directly in your email inbox without needing a backend server:
1. Go to **[https://web3forms.com](https://web3forms.com)** (Free, no credit card required).
2. Type in your email address and click **"Create Access Key"**.
3. Check your email for your access key (looks like `a1b2c3d4-5678-90ab-cdef-1234567890ab`).
4. Open [`web/app.js`](file:///c:/Users/upand/OneDrive/Desktop/Panini%20Systems/web/app.js#L84) and paste your key into:
   ```javascript
   web3FormsAccessKey: "your-access-key-here",
   ```
5. **Done!** Whenever a client clicks *"Submit Analysis Request"*, Web3Forms delivers their name, company, email, phone number, and game analysis requirements straight to your inbox within seconds!

### Option B: Pre-Filled Email App Draft (Works with Zero Setup)
Even if you don't enter an access key:
* When a client submits the form or clicks **"Send via Email App"**, the website automatically opens their default email client (Gmail, Apple Mail, Outlook) with a complete project brief pre-filled and addressed to you!
* No message can ever be lost.

---

## 4. How to Edit Text & Sections on the Website

To edit any text on the website, open [`web/index.html`](file:///c:/Users/upand/OneDrive/Desktop/Panini%20Systems/web/index.html) in your text editor (VS Code, Notepad++, etc.).

### A. Editing the Main Headline & Subtitle
Search for `<!-- HERO SECTION -->` in `index.html`:
```html
<h1 class="display-title text-4xl sm:text-6xl font-bold tracking-tight text-white ...">
  Mathematical Rigor Behind <br class="hidden sm:inline">
  <span class="bg-clip-text text-transparent bg-gradient-to-r from-emerald-400 via-teal-200 to-amber-300">
    World-Class Games & Economies
  </span>
</h1>
```
Replace the words with your preferred messaging.

### B. Editing Service Cards
Search for `<!-- FLAGSHIP PRACTICE SECTION -->` in `index.html`. You will see the three main cards:
1. **Slot Math & PAR Design**
2. **Regulatory Audits & GLI Prep**
3. **F2P Economy & Gacha Math**

You can freely change the text inside `<h3 ...>` and `<p ...>` or edit the bullet points.

---

## 5. How to Deploy Your Website Online (Free)

When you are ready to make the website public on the internet so clients can visit it:

### Method 1: Netlify Drop (Easiest — 30 Seconds)
1. Go to [https://app.netlify.com/drop](https://app.netlify.com/drop).
2. Drag and drop the `web` folder directly into the browser window.
3. You instantly get a live public URL (e.g., `https://panini-systems.netlify.app`) that you can share with clients or link to a custom domain (`paninisystems.com`).

### Method 2: GitHub Pages (Free Hosting with Git)
1. Push this repository to GitHub.
2. In your repository settings, go to **Pages**.
3. Under **Source**, select `Deploy from a branch` and choose `/web` as the root folder.
4. Your site will be live at `https://your-username.github.io/Panini-Systems/`.

---

## 6. Instant Preview

To see your changes immediately:
* Simply double-click [`web/index.html`](file:///c:/Users/upand/OneDrive/Desktop/Panini%20Systems/web/index.html) to view it in Chrome, Edge, or Brave.
* Any time you save edits to `index.html`, `app.js`, or `styles.css`, simply press **F5 (Refresh)** in your browser!
