
function refreshData() {
    const button = document.querySelector('.refresh-btn');
    const originalText = button.textContent;
    
    button.textContent = '🔄 更新中...';
    button.disabled = true;
    
    fetch('/api/refresh')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('✅ データの更新が完了しました！ページを再読み込みします。');
                location.reload();
            } else {
                alert('❌ データの更新に失敗しました: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('❌ エラーが発生しました: ' + error.message);
        })
        .finally(() => {
            button.textContent = originalText;
            button.disabled = false;
        });
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('OSS統計ダッシュボードが読み込まれました！');
    
    const statCards = document.querySelectorAll('.stat-card');
    statCards.forEach((card, index) => {
        setTimeout(() => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            
            setTimeout(() => {
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, 100);
        }, index * 100);
    });
});

function startAutoRefresh(intervalMinutes = 30) {
    setInterval(() => {
        console.log('自動更新を実行中...');
        fetch('/api/refresh')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log('自動更新完了');
                }
            })
            .catch(error => {
                console.error('自動更新エラー:', error);
            });
    }, intervalMinutes * 60 * 1000);
}

function celebrateStats() {
    const statNumbers = document.querySelectorAll('.stat-number');
    statNumbers.forEach(number => {
        number.style.animation = 'sparkle 2s infinite';
    });
}

const style = document.createElement('style');
style.textContent = `
    @keyframes sparkle {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style);
