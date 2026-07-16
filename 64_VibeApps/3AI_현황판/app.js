document.addEventListener('DOMContentLoaded', () => {
    // 요소 가져오기
    const refreshBtn = document.getElementById('refresh-btn');
    const inProgressList = document.getElementById('in-progress-list');
    const pendingList = document.getElementById('pending-list');
    const inboxCount = document.getElementById('inbox-count');

    // 더미 데이터 세팅 (추후 tasks.json 파싱 로직으로 대체 가능)
    const mockData = {
        agents: {
            manbok: 'online',
            coni: 'offline', // 코니 오프라인 상태 반영
            anti: 'online'
        },
        tasks: {
            inProgress: [
                "T024 바이브코딩 (현황판 웹앱) 초기 개발",
                "T063 슬라이드 자동 생성 프로토타입 작성"
            ],
            pending: [
                "T026 MSA 로깅 시스템 구축",
                "T025 Docker 환경 구성",
                "Improve_stock 시계열 분석 고도화"
            ]
        },
        inbox: 3
    };

    // UI 업데이트 함수
    const updateUI = (data) => {
        // 에이전트 상태 업데이트 (미구현 시 UI에서 하드코딩된 클래스 유지)
        
        // 진행 중 태스크 렌더링
        inProgressList.innerHTML = '';
        if (data.tasks.inProgress.length === 0) {
            inProgressList.innerHTML = '<li>(없음)</li>';
        } else {
            data.tasks.inProgress.forEach(task => {
                const li = document.createElement('li');
                li.textContent = task;
                inProgressList.appendChild(li);
            });
        }

        // 대기 중 태스크 렌더링
        pendingList.innerHTML = '';
        data.tasks.pending.forEach(task => {
            const li = document.createElement('li');
            li.textContent = task;
            pendingList.appendChild(li);
        });

        // 수신함 카운트
        inboxCount.textContent = data.inbox;
    };

    // 초기 렌더링
    updateUI(mockData);

    // 새로고침 버튼 애니메이션 및 효과
    refreshBtn.addEventListener('click', () => {
        refreshBtn.textContent = '불러오는 중...';
        refreshBtn.style.opacity = '0.7';
        
        // 모의 API 호출 딜레이
        setTimeout(() => {
            updateUI(mockData);
            refreshBtn.textContent = '새로고침';
            refreshBtn.style.opacity = '1';
        }, 600);
    });
});
