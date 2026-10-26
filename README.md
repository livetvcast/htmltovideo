# HTML Video Link Extractor

Extracts direct video URLs visible in an HTML file and saves them to `links.txt`.

## GitHub Actions setup
1. Upload the contents of this folder to the root of your GitHub repository.
2. Ensure the workflow file is at `.github/workflows/extract.yml` (not nested in another folder).
3. Commit the files to the `main` branch. The workflow will run automatically after a matching push.
4. Or open **Actions → Extract Video Links → Run workflow**.
5. Open a completed run and download the `video-links` artifact.

## Local run
```bash
python -m pip install -r requirements.txt
python extractor.py page.html
```

## Important limits
This extracts direct URLs exposed in the provided HTML. It does not execute JavaScript, bypass logins, or extract protected/private media. The URLs in `page.html` are placeholders for testing, not real video files.
