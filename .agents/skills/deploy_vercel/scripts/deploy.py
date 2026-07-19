import os
import subprocess
import argparse
import sys

def run_cmd(cmd, cwd=None):
    print(f"🏃 실행 중: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ 에러 발생:\n{result.stderr}")
        sys.exit(1)
    print(f"✅ 성공:\n{result.stdout}")
    return result.stdout

def deploy_to_vercel(project_dir):
    print("🚀 Vercel 원클릭 배포 파이프라인 시작...")
    
    # 1. Git 확인 및 커밋
    if not os.path.exists(os.path.join(project_dir, ".git")):
        run_cmd("git init", cwd=project_dir)
    
    run_cmd("git add .", cwd=project_dir)
    # 수정사항이 없을 경우 예외 처리
    try:
        run_cmd('git commit -m "Auto deploy via Anti 3AI"', cwd=project_dir)
    except SystemExit:
        print("⚠️ 커밋할 새 변경사항이 없습니다. 배포를 계속 진행합니다.")
        pass
    
    # 2. Vercel 배포 (미리 인증되어 있다고 가정)
    print("⚡ Vercel Production 배포 중...")
    output = run_cmd("npx vercel --prod --yes", cwd=project_dir)
    
    # URL 추출 (대략적인 파싱)
    for line in output.split("\n"):
        if "https://" in line and "vercel.app" in line:
            print(f"🎉 배포 완료! Live URL: {line.strip()}")
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vercel 원클릭 자동 배포 스크립트")
    parser.add_argument("--dir", type=str, required=True, help="배포할 프로젝트 폴더 경로")
    args = parser.parse_args()
    
    deploy_to_vercel(args.dir)
