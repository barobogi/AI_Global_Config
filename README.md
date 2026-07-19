# YouTube Subtitle Extractor (Playwright)

A simple CLI tool to extract subtitles from YouTube videos using Playwright to bypass recent Bot‑Detection mechanisms.

## Prerequisites

- Node.js (v14 or later)
- `npm` (comes with Node)

## Installation

```bash
git clone <repo-url>  # or copy the folder
cd cline
npm install
npx playwright install  # installs browser binaries
```

## Usage

```bash
npm run subtitles -- <video_url> <cookies_path> [output_path]
```

- `<video_url>`: Full YouTube video URL.
- `<cookies_path>`: Path to the Netscape‑format `cookies.txt` file (must contain valid YouTube cookies).
- `[output_path]`: Optional path for the extracted subtitle file. If omitted, the file is saved under `transcripts/` using the video title.

### Example

```bash
npm run subtitles -- https://www.youtube.com/watch?v=ZQX1eDhXlV0 25_auto_pobbagi/cookies.txt transcripts/example.srt
```

The script will:

1. Launch a headful Chromium browser.
2. Load the provided cookies to authenticate the request.
3. Navigate to the video page and open the transcript panel.
4. Extract subtitle text (with retry logic for flaky UI).
5. Write the subtitles to the specified output file.

## Output Format

Subtitles are saved as plain `.srt` files containing the textual content of each line. Timestamps are currently not included; if you need formatted timestamps, you can extend the extraction logic.

## Configuration

- **Maximum retry attempts:** 3 (adjustable in `extractSubtitles` function)
- **Wait time between retries:** 2 seconds
- **Timeout for page navigation / selector waiting:** 60 seconds for navigation, 8‑15 seconds for transcript elements

## License

MIT