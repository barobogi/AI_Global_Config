const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

/**
 * Load cookies from a JSON file and add them to the given page context.
 * @param {Object} context - Playwright browser context
 * @param {string} cookiesPath - Path to cookies.txt (will be parsed as JSON)
 */
async function loadCookies(context, cookiesPath) {
  const raw = fs.readFileSync(cookiesPath, 'utf8');
  const cookies = JSON.parse(raw);
  await context.addCookies(cookies);
}

/**
 * Extract subtitles from a YouTube video page.
 * @param {string} videoUrl - Full YouTube video URL
 * @param {string} cookiesPath - Path to cookies.txt used for authentication
 * @param {string} outputPath - Where to write the extracted subtitles
 */
async function extractSubtitles(videoUrl, cookiesPath, outputPath) {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();

  try {
    // Navigate to the video page, waiting for network to be idle
    await page.goto(videoUrl, { waitUntil: 'networkidle', timeout: 60000 });

    // Wait for the transcript button / panel to appear.
    // YouTube’s UI may vary; adjust selectors based on actual DOM.
    await page.waitForSelector('button[aria-label="Open transcript"]', { timeout: 10000 });
    await page.click('button[aria-label="Open transcript"]');

    // Wait for the transcript text elements to be populated.
    await page.waitForSelector('div#movie_player → ytd-transcript-renderer', { timeout: 15000 });

    // Extract subtitle text (including timestamps if desired)
    const subtitleText = await page.evaluate(() => {
      // Adjust selector to match the actual transcript items in the page
      const items = Array.from(document.querySelectorAll('ytd-transcript-line-renderer, .yt-text-bottom'))
        .map(el => el.innerText.trim())
        .filter(line => line.length > 0);
      return items.join('\n');
    });

    // Ensure the output directory exists
    const outputDir = path.dirname(outputPath);
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }

    // Write the subtitles to the output file
    fs.writeFileSync(outputPath, subtitleText, 'utf8');
    console.log(`✅ Subtitles saved to ${outputPath}`);
  } catch (err) {
    console.error('❌ Failed to extract subtitles:', err);
    throw err;
  } finally {
    await browser.close();
  }
}

/**
 * CLI entry point.
 * Usage: node youtube_subtitle_extractor.js <video_url> <cookies_path> [output_path]
 */
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length < 2) {
    console.error('Usage: node youtube_subtitle_extractor.js <video_url> <cookies_path> [output_path]');
    process.exit(1);
  }
  const [videoUrl, cookiesPath, maybeOutPath] = args;
  const outputPath = maybeOutPath || path.join(__dirname, 'transcripts', `${path.basename(videoUrl)}.srt`);
  extractSubtitles(videoUrl, cookiesPath, outputPath).catch(() => process.exit(1));
}