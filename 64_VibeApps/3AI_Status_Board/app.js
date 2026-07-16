
document.getElementById('refreshBtn').addEventListener('click', () => {
    const btn = document.getElementById('refreshBtn');
    btn.textContent = '불러오는 중...';
    setTimeout(() => {
        btn.textContent = '새로고침';
        // 임시 애니메이션 효과
        document.querySelector('.container').style.opacity = '0.8';
        setTimeout(() => document.querySelector('.container').style.opacity = '1', 200);
    }, 500);
});
