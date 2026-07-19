from google import genai
client = genai.Client(api_key='AQ.Ab8RN6LufZgpf1zlTE4sZV6ASoj50ir0nRhl4z7nm4bmM-3bjA')
print('Uploading file...')
audio_file = client.files.upload(file='D:/AI/25_auto_pobbagi/temp_audio.m4a')
print('Transcribing...')
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[audio_file, '이 오디오의 내용을 한국어 자막 형태(전체 텍스트)로 추출해줘. 요약하지 말고 들리는 대로 전부 다 적어줘.']
)
with open('D:/AI/25_auto_pobbagi/transcripts/gUGVPxF3c_s.txt', 'w', encoding='utf-8') as f:
    f.write(response.text)
print('Done!')
