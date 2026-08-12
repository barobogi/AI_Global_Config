import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

def find_ffmpeg() -> str:
    candidates = [
        r"D:\AI\63_youtube_creator\pipeline\ffmpeg.exe",
        r"D:\AI\63_youtube_creator\pipeline\ffmpeg\bin\ffmpeg.exe",
        r"D:\AI\25_auto_pobbagi\ffmpeg.exe",
        "ffmpeg"
    ]
    for c in candidates:
        if os.path.isabs(c) and os.path.exists(c):
            return c
    return "ffmpeg"

FFMPEG_EXE = find_ffmpeg()

class SilenceCutter:
    def __init__(
        self,
        input_file: str,
        output_file: str = None,
        noise_threshold_db: float = -30.0,
        min_silence_duration_sec: float = 0.5
    ):
        self.input_file = Path(input_file).resolve()
        if not self.input_file.exists():
            raise FileNotFoundError(f"입력 파일을 찾을 수 없습니다: {self.input_file}")
            
        if output_file:
            self.output_file = Path(output_file).resolve()
        else:
            suffix = self.input_file.suffix
            stem = self.input_file.stem
            self.output_file = self.input_file.parent / f"{stem}_silence_cut{suffix}"

        self.noise_threshold_db = noise_threshold_db
        self.min_silence_duration_sec = min_silence_duration_sec

    def _detect_silence_intervals() -> list[tuple[float, float]]:
        """FFmpeg silencedetect 필터로 무음 구간 (start, end) 목록 파싱"""
        cmd = [
            FFMPEG_EXE,
            "-hide_banner",
            "-i", str(self.input_file),
            "-af", f"silencedetect=noise={self.noise_threshold_db}dB:d={self.min_silence_duration_sec}",
            "-f", "null",
            "-"
        ]
        
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        stderr = res.stderr

        silence_starts = []
        silence_ends = []

        for line in stderr.splitlines():
            if "silence_start:" in line:
                m = re.search(r"silence_start:\s*([\d\.]+)", line)
                if m:
                    silence_starts.append(float(m.group(1)))
            elif "silence_end:" in line:
                m = re.search(r"silence_end:\s*([\d\.]+)", line)
                if m:
                    silence_ends.append(float(m.group(1)))

        # 쌍 맞추기
        silence_intervals = []
        for i in range(min(len(silence_starts), len(silence_ends))):
            silence_intervals.append((silence_starts[i], silence_ends[i]))

        return silence_intervals

    def _get_media_duration() -> float:
        """FFmpeg / ffprobe 기반 미디어 전체 길이 추출"""
        cmd = [
            FFMPEG_EXE,
            "-hide_banner",
            "-i", str(self.input_file)
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        m = re.search(r"Duration:\s*(\d+):(\d+):([\d\.]+)", res.stderr)
        if m:
            hours, mins, secs = float(m.group(1)), float(m.group(2)), float(m.group(3))
            return hours * 3600 + mins * 60 + secs
        return 0.0

    def cut_silence() -> bool:
        """무음 구간 제거 및 컷팅 수행"""
        print(f"🎬 [SilenceCutter] 무음 감지 시작: {self.input_file.name}")
        silence_intervals = self._detect_silence_intervals()
        total_duration = self._get_media_duration()

        print(f"📊 감지된 무음 구간 개수: {len(silence_intervals)}개, 미디어 길이: {total_duration:.2f}초")

        if not silence_intervals:
            print("ℹ️ 제거할 무음 구간이 감지되지 않았습니다. 원본 유지.")
            # 원본과 동일하게 복사/저장
            cmd = [FFMPEG_EXE, "-y", "-i", str(self.input_file), "-c", "copy", str(self.output_file)]
            subprocess.run(cmd, capture_output=True)
            return True

        # Keep Intervals (유지할 미디어 구간) 계산
        keep_intervals = []
        last_end = 0.0

        for start, end in silence_intervals:
            if start > last_end + 0.1:  # 최소 0.1초 이상 유효 구간인 경우
                keep_intervals.append((last_end, start))
            last_end = end

        if last_end < total_duration - 0.1:
            keep_intervals.append((last_end, total_duration))

        if not keep_intervals:
            print("⚠️ 전체 영상이 무음으로 감지되어 커편집을 중단합니다.")
            return False

        print(f"✂️ 유지할 구간 개수: {len(keep_intervals)}개")

        # FFmpeg complex_filter 생성
        is_video = self.input_file.suffix.lower() in [".mp4", ".mkv", ".avi", ".mov", ".webm"]
        
        filter_parts = []
        for idx, (start, end) in enumerate(keep_intervals):
            if is_video:
                filter_parts.append(f"[0:v]between(t,{start},{end})[v{idx}]; ")
                filter_parts.append(f"[0:a]between(t,{start},{end})[a{idx}]; ")
            else:
                filter_parts.append(f"[0:a]atrim={start}:{end},asetpts=PTS-STARTPTS[a{idx}]; ")

        concat_v_parts = "".join([f"[v{i}]" for i in range(len(keep_intervals))])
        concat_a_parts = "".join([f"[a{i}]" for i in range(len(keep_intervals))])

        if is_video:
            filter_parts.append(f"{concat_v_parts}concat=n={len(keep_intervals)}:v=1:a=0[outv]; ")
            filter_parts.append(f"{concat_a_parts}concat=n={len(keep_intervals)}:v=0:a=1[outa]")
            filter_complex = "".join(filter_parts)
            
            # select filter 기반
            select_v = "+".join([f"between(t,{s},{e})" for s, e in keep_intervals])
            select_a = "+".join([f"between(t,{s},{e})" for s, e in keep_intervals])
            fc = f"[0:v]select='{select_v}',setpts=N/FRAME_RATE/TB[outv];[0:a]aselect='{select_a}',asetpts=N/SR/TB[outa]"
            
            cmd = [
                FFMPEG_EXE, "-y",
                "-i", str(self.input_file),
                "-filter_complex", fc,
                "-map", "[outv]",
                "-map", "[outa]",
                str(self.output_file)
            ]
        else:
            fc = "".join(filter_parts) + f"{concat_a_parts}concat=n={len(keep_intervals)}:v=0:a=1[outa]"
            cmd = [
                FFMPEG_EXE, "-y",
                "-i", str(self.input_file),
                "-filter_complex", fc,
                "-map", "[outa]",
                str(self.output_file)
            ]

        print(f"🚀 FFmpeg 무음 컷팅 명령 실행 중...")
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        
        if res.returncode == 0 and self.output_file.exists():
            cut_duration = self._get_media_duration_path(self.output_file)
            saved_time = total_duration - cut_duration
            print(f"✅ 커편집 완료! 최종 길이: {cut_duration:.2f}초 (단축된 시간: {saved_time:.2f}초)")
            print(f"📁 결과 파일: {self.output_file}")
            return True
        else:
            print(f"❌ FFmpeg 실행 실패. Error: {res.stderr[:300]}", file=sys.stderr)
            return False

    def _get_media_duration_path(self, path: Path) -> float:
        cmd = [FFMPEG_EXE, "-hide_banner", "-i", str(path)]
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        m = re.search(r"Duration:\s*(\d+):(\d+):([\d\.]+)", res.stderr)
        if m:
            hours, mins, secs = float(m.group(1)), float(m.group(2)), float(m.group(3))
            return hours * 3600 + mins * 60 + secs
        return 0.0

def main():
    parser = argparse.ArgumentParser(description="T063_젠컷 — 무음 구간 커편집 자동화 모듈")
    parser.add_argument("--input", required=True, help="입력 오디오/비디오 파일 경로")
    parser.add_argument("--output", default=None, help="출력 파일 경로 (기본: _silence_cut 접미사)")
    parser.add_argument("--noise-thresh", type=float, default=-30.0, help="무음 감지 임계값 (dB, 기본값: -30.0)")
    parser.add_argument("--min-silence-len", type=float, default=0.5, help="무음 최소 지속 시간 (초, 기본값: 0.5)")

    args = parser.parse_args()

    cutter = SilenceCutter(
        input_file=args.input,
        output_file=args.output,
        noise_threshold_db=args.noise_thresh,
        min_silence_duration_sec=args.min_silence_len
    )
    success = cutter.cut_silence()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
