# 데스크탑 최적화 가이드 (barobogi PC)

**작성일**: 2026-06-21  
**환경**: Windows 11 Home / RAM 8GB / C드라이브 SSD 256GB / D드라이브 HDD 1TB

---

## 📊 최초 진단 결과 (2026-06-21)

### 메모리 현황
```
전체: 7.7GB / 사용: 6.6GB / 여유: 1.1GB  ← 거의 꽉 참 (버벅거림 주 원인)
```

### 주요 메모리 점유 프로세스
| 프로세스 | MB | 비고 |
|---|---|---|
| claude (VS Code 확장) | ~637MB (3개) | 필수 |
| vmmem | 309MB | WSL/가상머신 |
| Code (VS Code) | ~600MB (4개) | 필수 |
| chrome | ~526MB (3개) | 브라우저 |
| MsMpEng (Defender) | 232MB | 필수 |
| whale | ~306MB (2개) | 네이버 웨일 브라우저 |
| Memory Compression | 171MB | Windows 시스템 |

### 드라이브 현황
| 드라이브 | 종류 | 전체 | 사용 | 여유 |
|---|---|---|---|---|
| C: (시스템) | SSD (삼성 MZVLQ) | 236GB | 201GB | 35.4GB |
| D: (데이터) | HDD (도시바 DT01) | 914GB | 95.4GB | 818.4GB |

### 시작 프로그램 목록 (최초)
**레지스트리 (HKCU\Run):**
- OneDrive ← 클라우드 동기화 (사용 중, 유지)
- uTorrent ← **제거 완료**
- GoogleDriveFS ← 클라우드 동기화 (사용 중, 유지)
- CrossEXService ← 인터넷 뱅킹용 (유지)
- Teams ← **제거 완료**
- MicrosoftEdgeAutoLaunch ← **제거 완료**
- MicrosoftCopilotAutoLaunch ← **제거 완료**
- MYBOX (네이버) ← 클라우드 동기화 (사용 중, 유지)
- ClaudeMonitor ← **제거 완료**

**시작 폴더:**
- GlobalAutoDeployWatcher.lnk ← master_watch.py (필수, 유지)
- KakaoWatcher.lnk ← (유지)
- Ollama.lnk ← **제거 완료** (수동 실행)
- OneNote로 보내기.lnk ← 시스템 (유지)

---

## ✅ 수행한 최적화 작업

### 2026-06-21 — 1차 최적화: 시작 프로그램 정리

#### 1. ClaudeMonitor.exe 시작 프로그램 제거
- **제거 이유**: Admin API 키 없어서 매 부팅 시 에러만 출력
```powershell
Remove-ItemProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" -Name "ClaudeMonitor" -Confirm:$false
```

#### 2. Edge 자동 실행 제거
- **제거 이유**: 사용 안 해도 백그라운드 자동 실행, 메모리 낭비
```powershell
Remove-ItemProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" -Name "MicrosoftEdgeAutoLaunch_C9A81BCBE85D21C5976B874852BD5AB9" -Confirm:$false
```

#### 3. Copilot 자동 실행 제거
```powershell
Remove-ItemProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" -Name "MicrosoftCopilotAutoLaunch_E6F31C1D4D69D064E12BF0E81DAE27CF" -Confirm:$false
```

#### 4. uTorrent 시작 프로그램 제거
```powershell
Remove-ItemProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" -Name "ut" -Confirm:$false
```

#### 5. Teams 시작 프로그램 제거
```powershell
Remove-ItemProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" -Name "Teams" -Confirm:$false
```

#### 6. Ollama 시작 폴더 제거 (수동)
- `Win+R → shell:startup → Ollama.lnk 삭제`
- 필요 시 검색에서 직접 실행

#### 7. Gradle 캐시 정리 (2.73GB 회수)
- **효과**: C드라이브 35.4GB → 38.1GB
- **주의**: 다음 첫 빌드 시 자동 재생성
```powershell
Remove-Item "C:\Users\82102\.gradle\caches" -Recurse -Force
```

---

### 2026-06-21 — 2차 최적화: C→D 드라이브 이전

**총 효과**: C드라이브 38.1GB → **48.2GB** (+10GB 확보)

#### 8. Python C:\hb → D:\hb 심볼릭 링크 (5.77GB 이전)
```powershell
# 복사
Copy-Item -Path "C:\hb" -Destination "D:\hb" -Recurse -Force
# 원본 삭제 (bash로)
rm -rf "C:/hb"
# 심볼릭 링크 생성
New-Item -ItemType Junction -Path "C:\hb" -Target "D:\hb"
```

#### 9. Android SDK → D:\Android\sdk 심볼릭 링크 (6.21GB 이전)
```powershell
# 복사
Copy-Item -Path "C:\Users\82102\AppData\Local\Android\sdk" -Destination "D:\Android\sdk" -Recurse -Force
# 원본 삭제
rm -rf "C:/Users/82102/AppData/Local/Android/sdk"
# 심볼릭 링크 생성
New-Item -ItemType Junction -Path "C:\Users\82102\AppData\Local\Android\sdk" -Target "D:\Android\sdk"
# 환경변수 업데이트
[System.Environment]::SetEnvironmentVariable("ANDROID_HOME", "D:\Android\sdk", "User")
[System.Environment]::SetEnvironmentVariable("ANDROID_SDK_ROOT", "D:\Android\sdk", "User")
```

#### 10. 개발 도구 캐시 환경변수 → D:\Dev\ 리디렉션
```powershell
# 폴더 생성
New-Item -ItemType Directory -Force "D:\Dev\pub_cache", "D:\Dev\gradle", "D:\Dev\pip_cache", "D:\Dev\npm", "D:\Dev\npm_cache", "D:\Dev\temp"

# 환경변수 설정
[System.Environment]::SetEnvironmentVariable("PUB_CACHE", "D:\Dev\pub_cache", "User")
[System.Environment]::SetEnvironmentVariable("GRADLE_USER_HOME", "D:\Dev\gradle", "User")
[System.Environment]::SetEnvironmentVariable("PIP_CACHE_DIR", "D:\Dev\pip_cache", "User")
[System.Environment]::SetEnvironmentVariable("CARGO_HOME", "D:\Dev\cargo", "User")
[System.Environment]::SetEnvironmentVariable("GOPATH", "D:\Dev\go", "User")
[System.Environment]::SetEnvironmentVariable("TEMP", "D:\Dev\temp", "User")
[System.Environment]::SetEnvironmentVariable("TMP", "D:\Dev\temp", "User")
npm config set prefix "D:\Dev\npm"
npm config set cache "D:\Dev\npm_cache"
```

---

### 2026-06-21 — 3차 최적화: 가상 메모리 설정

#### 11. 페이지 파일 D(HDD) → C(SSD) 이전, 12GB 고정
- **이유**: D는 HDD라 스왑 발생 시 C(SSD)보다 10배 느림
- **효과**: RAM 부족 시 스왑 속도 향상
- **방법**: `Win+R → sysdm.cpl → 고급 → 성능 설정 → 고급 → 가상 메모리 변경`
  - 자동 관리 체크 해제
  - C: 선택 → 사용자 지정 → 처음/최대 크기 `12288` → 설정
  - D: 선택 → 페이징 파일 없음 → 설정
  - 재부팅

---

### 2026-06-21 — 4차 최적화: 환경변수 영구 등록

#### 12. JAVA_HOME 영구 등록
- **이유**: 재부팅 후 초기화되어 Flutter 빌드 시 매번 수동 설정 필요했음
```powershell
[System.Environment]::SetEnvironmentVariable("JAVA_HOME", "C:\Program Files\Android\Android Studio\jbr", "User")
# PATH에 java\bin 추가
$p = [System.Environment]::GetEnvironmentVariable("PATH", "User")
[System.Environment]::SetEnvironmentVariable("PATH", "$p;C:\Program Files\Android\Android Studio\jbr\bin", "User")
```

---

## 📋 현재 환경변수 전체 현황

```
JAVA_HOME        = C:\Program Files\Android\Android Studio\jbr  (JDK 21)
ANDROID_HOME     = D:\Android\sdk
ANDROID_SDK_ROOT = D:\Android\sdk
GRADLE_USER_HOME = D:\Dev\gradle
PUB_CACHE        = D:\Dev\pub_cache
PIP_CACHE_DIR    = D:\Dev\pip_cache
CARGO_HOME       = D:\Dev\cargo
GOPATH           = D:\Dev\go
TEMP / TMP       = D:\Dev\temp
npm prefix       = D:\Dev\npm
npm cache        = D:\Dev\npm_cache
```

---

## 💡 향후 최적화 권장 사항

### 근본 해결책
- **RAM 증설 8GB → 16GB** — 가장 효과적 (DDR4 16GB 약 3~4만원)
  - 현재 여유 0.9~1.1GB로 항상 부족한 상태
  - VS Code + Claude + 빌드 동시 작업 시 스왑 발생

### 새 도구 설치 원칙 (D드라이브 우선)
- SDK/런타임 설치 시 → `D:\Dev\도구명` 경로 지정
- C드라이브 여유 20GB 이하 시 → D 이전 검토
- 빌드 중 캐시/빌드 폴더 삭제 금지 (빌드 강제 종료됨)

### APK 빌드 시 주의사항
- 빌드 중 다른 무거운 작업 자제
- 빌드 완료 후 java 프로세스 종료
```powershell
Get-Process java -ErrorAction SilentlyContinue | Stop-Process -Force
```

---

## 🔧 유용한 진단 명령어

```powershell
# 메모리 사용 TOP 15
Get-Process | Sort-Object WorkingSet -Descending | Select-Object -First 15 Name, @{n='MB';e={[math]::Round($_.WorkingSet/1MB,0)}}

# 메모리 현황 요약
$os = Get-CimInstance Win32_OperatingSystem
"전체: $([math]::Round($os.TotalVisibleMemorySize/1MB,1))GB / 사용: $([math]::Round(($os.TotalVisibleMemorySize-$os.FreePhysicalMemory)/1MB,1))GB / 여유: $([math]::Round($os.FreePhysicalMemory/1MB,1))GB"

# 디스크 여유 확인
Get-PSDrive -PSProvider FileSystem | Where-Object {$_.Used -gt 0} | Select-Object Name, @{n='여유(GB)';e={[math]::Round($_.Free/1GB,1)}}

# 시작 프로그램 확인
Get-ItemProperty "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" | Select-Object * -ExcludeProperty PS*

# 페이지 파일 현황
Get-CimInstance Win32_PageFileUsage | Select-Object Name, AllocatedBaseSize, CurrentUsage

# 가상 메모리 총량
$os = Get-CimInstance Win32_OperatingSystem
"총 가상 메모리: $([math]::Round($os.TotalVirtualMemorySize/1MB,1))GB"
```

---

*마지막 업데이트: 2026-06-21*  
*다음 최적화 시 이 파일에 날짜별로 추가*
