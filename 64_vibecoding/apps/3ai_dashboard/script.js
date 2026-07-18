// script.js
// 실시간 동기화 시뮬레이션: 실제 백엔드가 없으므로 클라이언트에서
// 주기적으로 상태/지표/로그를 갱신하며 "라이브" 느낌을 구현한다.

document.addEventListener('DOMContentLoaded', () => {
    console.log('3AI 현황판 대시보드가 로드되었습니다.');

    const SYNC_INTERVAL_MS = 4000; // 4초마다 동기화

    const lastSyncEl = document.getElementById('last-sync-time');
    const modelListEl = document.getElementById('model-status-list');
    const logListEl = document.getElementById('log-list');
    const metricTodayEl = document.getElementById('metric-today');
    const metricWeeklyEl = document.getElementById('metric-weekly');
    const metricSpeedEl = document.getElementById('metric-speed');

    const STATUS_TYPES = [
        { cls: 'online', label: '정상 작동 중' },
        { cls: 'warning', label: '경고 - CPU 사용량 높음' },
        { cls: 'offline', label: '오프라인 - 재연결 시도 중' },
    ];

    const LOG_EVENTS = [
        '헬스체크 정상 응답',
        '데이터 배치 처리 완료',
        '캐시 갱신 완료',
        'API 응답 지연 감지 (모니터링 중)',
        '신규 요청 큐 처리 완료',
        '노드 간 동기화 완료',
    ];

    const formatTime = (date) => date.toLocaleTimeString('ko-KR', { hour12: false });

    const formatNumber = (n) => n.toLocaleString('ko-KR');

    const flashCard = (cardEl) => {
        cardEl.classList.add('updated');
        setTimeout(() => cardEl.classList.remove('updated'), 700);
    };

    const updateLastSyncTime = () => {
        if (lastSyncEl) lastSyncEl.textContent = formatTime(new Date());
    };

    const updateModelStatus = () => {
        if (!modelListEl) return;
        const items = modelListEl.querySelectorAll('li');
        const target = items[Math.floor(Math.random() * items.length)];
        const nextStatus = STATUS_TYPES[Math.floor(Math.random() * STATUS_TYPES.length)];

        const indicator = target.querySelector('.status-indicator');
        const statusText = target.querySelector('.status-text');
        indicator.className = `status-indicator ${nextStatus.cls}`;
        statusText.textContent = nextStatus.label;

        flashCard(document.getElementById('card-model-status'));
    };

    const updateMetrics = () => {
        if (!metricTodayEl) return;
        const today = 1000 + Math.floor(Math.random() * 800);
        const weekly = 900 + Math.floor(Math.random() * 400);
        const speed = 100 + Math.floor(Math.random() * 100);

        metricTodayEl.textContent = formatNumber(today);
        metricWeeklyEl.textContent = formatNumber(weekly);
        metricSpeedEl.textContent = formatNumber(speed);

        flashCard(document.getElementById('card-metrics'));
    };

    const appendLogEntry = () => {
        if (!logListEl) return;
        const now = new Date();
        const timestamp = now.toISOString().slice(0, 19).replace('T', ' ');
        const message = LOG_EVENTS[Math.floor(Math.random() * LOG_EVENTS.length)];

        const li = document.createElement('li');
        li.textContent = `[${timestamp}] ${message}`;
        logListEl.prepend(li);

        // 로그는 최근 6개만 유지
        while (logListEl.children.length > 6) {
            logListEl.removeChild(logListEl.lastChild);
        }

        flashCard(document.getElementById('card-logs'));
    };

    const syncTick = () => {
        updateLastSyncTime();
        updateModelStatus();
        updateMetrics();
        appendLogEntry();
    };

    // 최초 1회 즉시 동기화 후 주기 실행
    syncTick();
    setInterval(syncTick, SYNC_INTERVAL_MS);
});