import sys
sys.stdout.reconfigure(encoding='utf-8')
from youtube_transcript_api import YouTubeTranscriptApi

api = YouTubeTranscriptApi()
transcript_list = api.list('bieRrMRc-bg')

print("사용 가능한 자막:")
for t in transcript_list:
    print(f"  - {t.language_code}: {t.language} (generated: {t.is_generated})")

# 바로 한국어 자막 fetch
fetched = transcript_list.find_transcript(['ko']).fetch()

lines = []
for t in fetched:
    m = int(t.start // 60)
    s = int(t.start % 60)
    lines.append(f'[{m:02d}:{s:02d}] {t.text}')

text = '\n'.join(lines)
with open(r'D:\AI\Temp_Manbok\alex_transcript.txt', 'w', encoding='utf-8') as f:
    f.write(text)

print(f'\n완료: {len(fetched)}개 세그먼트, {len(text)}자')
print('첫 5줄:')
for line in lines[:5]:
    print(line)
