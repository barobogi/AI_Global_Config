import os
import subprocess
import sys
import unittest
from pathlib import Path

sys.path.insert(0, r"D:\AI\63_youtube_creator\pipeline")
from silence_cutter import SilenceCutter, FFMPEG_EXE

print("Detected FFMPEG_EXE:", FFMPEG_EXE)

class TestSilenceCutter(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(r"D:\AI\63_youtube_creator\pipeline\tests")
        self.test_dir.mkdir(parents=True, exist_ok=True)
        self.sample_audio = self.test_dir / "sample_test_audio.mp3"
        self.output_audio = self.test_dir / "sample_test_audio_silence_cut.mp3"

        # FFmpeg 테스트 파형 생성: 2초 무음 + 3초 소리 + 2초 무음 (총 7초)
        cmd = [
            FFMPEG_EXE, "-y", "-hide_banner",
            "-f", "lavfi", "-i", "sine=frequency=440:duration=3",
            "-af", "adelay=2000|2000,apad=pad_dur=2",
            str(self.sample_audio)
        ]
        res = subprocess.run(cmd, capture_output=True)
        if res.returncode != 0:
            self.skipTest("FFmpeg 파형 생성 실패로 유닛테스트를 건너땁니다.")

    def tearDown(self):
        if self.sample_audio.exists():
            try:
                os.remove(self.sample_audio)
            except Exception:
                pass
        if self.output_audio.exists():
            try:
                os.remove(self.output_audio)
            except Exception:
                pass

    def test_silence_cutting(self):
        """무음 제거 커편집 유닛테스트"""
        cutter = SilenceCutter(
            input_file=str(self.sample_audio),
            output_file=str(self.output_audio),
            noise_threshold_db=-30.0,
            min_silence_duration_sec=0.5
        )
        success = cutter.cut_silence()
        self.assertTrue(success)
        self.assertTrue(self.output_audio.exists())
        
        # 결과 파일 길이가 원본보다 짧은지 확인
        orig_dur = cutter._get_media_duration_path(self.sample_audio)
        cut_dur = cutter._get_media_duration_path(self.output_audio)
        self.assertLess(cut_dur, orig_dur)

if __name__ == "__main__":
    unittest.main()
