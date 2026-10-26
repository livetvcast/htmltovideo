import re
import sys
import html
from pathlib import Path
from urllib.parse import urljoin
from bs4 import BeautifulSoup

VIDEO_EXTENSIONS = (
    ".mp4", ".m3u8", ".mpd", ".webm",
    ".mov", ".m4v", ".ts", ".ogv"
)

VIDEO_META = {
    "og:video", "og:video:url", "og:video:secure_url",
    "twitter:player:stream"
}

def extract_video_links(file_path):
    content = Path(file_path).read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(content, "html.parser")
    links = set()

    # Video and media elements
    for tag_name in ("video", "source", "iframe", "embed"):
        for tag in soup.find_all(tag_name):
            for attr in ("src", "data-src", "data-video-url"):
                value = tag.get(attr)
                if value:
                    links.add(value.strip())

    # Open Graph / Twitter metadata
    for meta in soup.find_all("meta"):
        key = (meta.get("property") or meta.get("name") or "").lower()
        if key in VIDEO_META and meta.get("content"):
            links.add(meta["content"].strip())

    # Common data attributes and href values
    for tag in soup.find_all(True):
        for attr in ("href", "data-src", "data-video-url", "content"):
            value = tag.get(attr)
            if value and any(ext in value.lower() for ext in VIDEO_EXTENSIONS):
                links.add(value.strip())

    # Direct video URLs embedded in HTML or JavaScript
    pattern = re.compile(
        r"""https?://[^\s"'<>\\]+?\.(?:mp4|m3u8|mpd|webm|mov|m4v|ts|ogv)(?:\?[^\s"'<>\\]*)?""",
        re.IGNORECASE
    )
    links.update(html.unescape(match) for match in pattern.findall(content))

    cleaned = set()
    for link in links:
        link = html.unescape(link).strip()
        if link.startswith("//"):
            link = "https:" + link
        if link.startswith(("https://", "http://")):
            cleaned.add(link)

    return sorted(cleaned)

if __name__ == "__main__":
    file_path = sys.argv[1] if len(sys.argv) > 1 else "page.html"
    if not Path(file_path).is_file():
        print(f"HTML file not found: {file_path}")
        sys.exit(1)

    results = extract_video_links(file_path)
    Path("links.txt").write_text("\n".join(results), encoding="utf-8")
    print(f"Found {len(results)} direct video links.")
    for link in results:
        print(link)
    print("Saved results to links.txt")
