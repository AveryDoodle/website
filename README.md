# Avery McAllister portfolio

Static HTML/CSS/JavaScript website; no build step needed.

## Free hosting with GitHub Pages

1. Commit and push the website files, including `images/optimized` and `.nojekyll`, to `main` in `AveryDoodle/website`.
2. In the GitHub repository, open **Settings → Pages**.
3. Select **Deploy from a branch**, **main**, and **/(root)**, then Save.
4. Once deployment completes, the expected URL is https://averydoodle.github.io/website/.

GitHub Pages is free for public repositories. A custom domain is optional and purchased separately.
Instructions: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

Cloudflare Pages is another free option, including for a private GitHub repository: import the repository, choose no framework, leave the build command blank, and use `.` as the output directory.
Instructions: https://developers.cloudflare.com/pages/framework-guides/deploy-anything/

## Editing project titles and descriptions

Open `projects.js`. Each project has a title, category, description, and optional year and tools. Change the text inside quotes, keeping the `id` and `image` fields unchanged. Leave year or tools empty to hide those details. Use `\n` inside a description to start a new paragraph.

Commit or upload the edited `projects.js` to the root of the GitHub repository on `main`. GitHub Pages will publish the changes automatically. Click any Work image to see its enlarged image and details; Enter or Space also opens a focused image, and Escape closes it.

## Image optimization

Original images are preserved. Pages use responsive 640px/1280px WebP copies; project popups load full-resolution WebP images only when opened. Work images use native lazy loading. Layout and CSS are unchanged.

After adding images, run `python3 scripts/optimize-images.py` with Pillow installed (`python3 -m pip install Pillow`). Commit generated files; hosting does not need Python.

## Content still needed before launch

- Work references `images/logo-1.png` through `logo-5.png` and `images/fine-art-1.jpg` through `fine-art-5.jpg`, which are missing.
- Resume links to `images/Avery-McAllister-Resume.pdf`, which is missing.
