import sys
sys.stdout.reconfigure(encoding='utf-8')
from youtube_transcript_api import YouTubeTranscriptApi

api = YouTubeTranscriptApi()
transcript_list = api.list('3My9sphTxtk')
fetched = transcript_list.find_transcript(['ko']).fetch()

lines = []
for t in fetched:
    m = int(t.start // 60)
    s = int(t.start % 60)
    lines.append(f'[{m:02d}:{s:02d}] {t.text}')

text = '\n'.join(lines)

with open(r'D:\AI\_Temp_Manbok\langgraph_transcript.txt', 'w', encoding='utf-8') as f:
    f.write(text)

print(f'완료: {len(fetched)}개 세그먼트, {len(text)}자')
print(f'첫 3줄 미리보기:')
for line in lines[:3]:
    print(line)
