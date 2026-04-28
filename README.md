# PPCguru

Welcome! If you're new to coding, this guide will help you get from **zero to editing and running this project**.

## 1) What this project is

This repository currently contains a simple static website:

- `index.html` (the web page)
- `README.md` (this setup guide)

You can work on this project with only a browser and a code editor.

## 2) Install the basics (one-time setup)

### Required

1. **Git** (for version control)
2. **VS Code** (recommended code editor)
3. **A modern browser** (Chrome, Firefox, Edge)

### Optional but helpful

- **Node.js LTS** (useful if you later add build tools)

## 3) Clone the repository

Run these commands in your terminal:

```bash
git clone <your-repo-url>
cd PPCguru
```

If you already have the folder, just `cd` into it.

## 4) Open the project in VS Code

```bash
code .
```

If `code` isn't recognized, open VS Code manually and choose **File → Open Folder...**.

## 5) Run the project locally

Because this is a static HTML site, you can run it in two easy ways.

### Option A (simplest)

Open `index.html` directly in your browser.

### Option B (recommended)

Start a small local web server so the URL looks like a real site:

```bash
python3 -m http.server 8000
```

Then visit:

- <http://localhost:8000>

Press `Ctrl + C` in terminal to stop the server.

## 6) Make your first change

1. Open `index.html`
2. Change some text (for example, the `<h1>` heading)
3. Save the file
4. Refresh the browser

You should immediately see your update.

## 7) Save your work with Git

```bash
git status
git add .
git commit -m "Update homepage copy"
```

If this is your first commit on a machine, configure Git first:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

## 8) Beginner workflow (repeat this)

1. Pull latest changes: `git pull`
2. Edit files in VS Code
3. Test in browser
4. Commit changes
5. Push branch and open PR

## 9) What to learn next

If you're just starting, focus in this order:

1. Basic HTML tags (`h1`, `p`, `ul`, `li`, `a`, `img`)
2. CSS basics (colors, spacing, fonts, layout)
3. JavaScript basics (variables, functions, DOM)
4. Git basics (branch, commit, push, pull request)

---

If you want, I can also generate a **beginner roadmap for the next 2–4 weeks** specifically for this project.
