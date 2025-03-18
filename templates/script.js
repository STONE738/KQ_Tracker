<script>
    let currentTab = 'main-lobby';
    let currentSubTab = '';
    let currentKQ = [];
    let kqLength = 4;
    let currentSoso = [];
    let isAnalyzed = false;

    function formatInput(inputElement) {
        let value = inputElement.value.replace(/\s+/g, '').toLowerCase();
        if (value) {
            let formatted = value.split('').join(' ');
            inputElement.value = formatted;
        }
    }

    function convertToCL(value) {
        value = value.toUpperCase();
        if (['C', 'L'].includes(value)) return value;
        return ['0', '2', '4'].includes(value) ? 'C' : 'L';
    }

    function showTab(tab, subTab = '') {
        document.querySelectorAll('.tab-content').forEach(t => t.style.display = 'none');
        document.querySelectorAll('.sub-tab-content').forEach(st => st.style.display = 'none');
        document.querySelectorAll('.sub-tab-details').forEach(dt => dt.style.display = 'none');
        document.querySelectorAll('.prediction-box').forEach(pb => pb.style.display = 'none');
        document.getElementById('main-lobby').style.display = 'none';
        
        const headers = document.querySelectorAll('.header');
        headers.forEach(h => h.style.display = 'none');

        if (tab === 'main-lobby') {
            document.getElementById('main-lobby').style.display = 'grid';
            currentTab = tab;
            currentSubTab = '';
        } else {
            const tabElement = document.getElementById(tab);
            if (tabElement) tabElement.style.display = 'block';
            if (subTab) {
                const subTabElement = document.getElementById(`${subTab}-sub-tab`);
                if (subTabElement) subTabElement.style.display = 'block';
                currentSubTab = subTab;
            }
            const header = document.getElementById(`${tab}-header`);
            if (header) header.style.display = 'flex';
            if (tab === 'chanle_lobby' && subTab === 'chanle' && currentSubTab === 'chanle-details') {
                const predictionBox = document.getElementById('chanle-prediction-box');
                if (predictionBox) predictionBox.style.display = 'flex';
            }
            currentTab = tab;
        }
    }

    function showAnalysisTab(subTab) {
        document.querySelectorAll('.sub-tab-content').forEach(st => st.style.display = 'none');
        document.querySelectorAll('.sub-tab-details').forEach(dt => dt.style.display = 'none');
        document.querySelectorAll('.prediction-box').forEach(pb => pb.style.display = 'none');
        const details = document.getElementById(subTab);
        if (details) details.style.display = 'block';
        if (subTab === 'chanle-details') {
            const predictionBox = document.getElementById('chanle-prediction-box');
            if (predictionBox) predictionBox.style.display = 'flex';
        }
    }

    function showSimulateTab(subTab) {
        document.querySelectorAll('.sub-tab-content').forEach(st => st.style.display = 'none');
        document.querySelectorAll('.sub-tab-details').forEach(dt => dt.style.display = 'none');
        document.querySelectorAll('.prediction-box').forEach(pb => pb.style.display = 'none');
        const details = document.getElementById(subTab);
        if (details) details.style.display = 'block';
    }

    function goBack() {
        document.querySelectorAll('.tab-content').forEach(t => t.style.display = 'none');
        document.querySelectorAll('.sub-tab-content').forEach(st => st.style.display = 'none');
        document.querySelectorAll('.sub-tab-details').forEach(dt => dt.style.display = 'none');
        document.querySelectorAll('.prediction-box').forEach(pb => pb.style.display = 'none');
        document.getElementById('main-lobby').style.display = 'grid';
        currentTab = 'main-lobby';
        currentSubTab = '';
    }

    function appendResult(value) {
        if (!isAnalyzed) return;
        value = convertToCL(value);
        currentKQ.push(value);
        document.getElementById('chanle-kq-input').value = '';
        analyzeData();
    }

    function resetData(type) {
        if (type === 'chanle') {
            currentKQ = [];
            kqLength = parseInt(document.getElementById('chanle-kq-length').value);
            isAnalyzed = false;
            document.getElementById('chanle-kq-input').value = '';
            document.getElementById('chanle-analyze-btn').textContent = 'Phân Tích';
            document.getElementById('chanle-result-buttons').style.display = 'none';
            updateResultSection({
                current_kq: 'Chưa có chuỗi KQ',
                total_matches: 0,
                c_percentage: 0,
                l_percentage: 0,
                number_stats: { '0': 0, '1': 0, '2': 0, '3': 0, '4': 0 },
                prediction: '',
                prediction_rate: 0
            });
        } else if (type === 'soso') {
            currentSoso = [];
            document.getElementById('soso_input').value = '';
            document.getElementById('soso-analyze-btn').textContent = 'Phân Tích';
            updateSosoResultSection({
                total_count: 0,
                number_stats: { '0': 0, '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0 },
                prediction: '?',
                prediction_rate: 0
            });
        }
    }

    function showLoginModal() {
        document.getElementById('login-modal').style.display = 'block';
        document.getElementById('overlay').style.display = 'block';
        showLoginTab();
    }

    function hideLoginModal() {
        document.getElementById('login-modal').style.display = 'none';
        document.getElementById('overlay').style.display = 'none';
    }

    function showLoginTab() {
        document.querySelectorAll('.modal-tab').forEach(tab => tab.style.display = 'none');
        document.getElementById('modal-tab-login').style.display = 'block';
    }

    function showRegisterTab() {
        document.querySelectorAll('.modal-tab').forEach(tab => tab.style.display = 'none');
        document.getElementById('modal-tab-register').style.display = 'block';
    }

    function showForgotPasswordTab() {
        document.querySelectorAll('.modal-tab').forEach(tab => tab.style.display = 'none');
        document.getElementById('modal-tab-forgot').style.display = 'block';
    }

    function checkLoginAndAnalyze() {
        fetch('/check_login', {
            method: 'GET',
            credentials: 'include'
        })
        .then(response => response.json())
        .then(data => {
            if (!data.logged_in) {
                showLoginModal();
                return;
            }
            let input = document.getElementById('chanle-kq-input').value.trim();
            const analyzeBtn = document.getElementById('chanle-analyze-btn');
            const resultButtons = document.getElementById('chanle-result-buttons');
            kqLength = parseInt(document.getElementById('chanle-kq-length').value);

            input = input.replace(/\s+/g, '').toLowerCase();
            const validInputs = input ? input.split('') : [];
            let newResults = validInputs.map(val => convertToCL(val));

            if (analyzeBtn.textContent === 'Cập Nhật') {
                if (!input && currentKQ.length === 0) {
                    alert('Vui lòng nhập KQ thực tế (C, L, hoặc 0-4)!');
                    return;
                }
                newResults = validInputs.map(val => convertToCL(val));
                currentKQ = currentKQ.concat(newResults);
                document.getElementById('chanle-kq-input').value = '';
                analyzeBtn.textContent = 'Cập Nhật';
                resultButtons.style.display = 'flex';
            } else {
                if (newResults.length > 0) {
                    currentKQ = newResults;
                } else if (currentKQ.length < 4) {
                    alert('Vui lòng nhập hoặc chọn ít nhất 4 kết quả (C, L, hoặc 0-4)!');
                    return;
                }
                analyzeBtn.textContent = 'Cập Nhật';
                resultButtons.style.display = 'flex';
                isAnalyzed = true;
            }
            analyzeData();
        })
        .catch(error => {
            console.error('Error checking login:', error);
            showLoginModal();
        });
    }

    function checkLoginAndAnalyzeSoso() {
        fetch('/check_login', {
            method: 'GET',
            credentials: 'include'
        })
        .then(response => response.json())
        .then(data => {
            if (!data.logged_in) {
                showLoginModal();
                return;
            }
            const input = document.getElementById('soso_input').value.trim();
            const analyzeBtn = document.getElementById('soso-analyze-btn');
            const sosoLength = parseInt(document.getElementById('soso_length').value);

            if (analyzeBtn.textContent === 'Cập Nhật') {
                if (!input && currentSoso.length === 0) {
                    alert('Vui lòng nhập số (0-9)!');
                    return;
                }
                const newResult = input ? input.split(' ').filter(val => /^[0-9]$/.test(val)) : [];
                if (newResult.length > 1) {
                    alert('Chỉ nhập 1 số (0-9)!');
                    return;
                }
                if (newResult.length === 1) currentSoso.push(newResult[0]);
                if (currentSoso.length > 6) currentSoso.shift();
                document.getElementById('soso_input').value = '';
                analyzeBtn.textContent = 'Phân Tích';
            } else {
                if (!input && currentSoso.length < 4) {
                    alert('Vui lòng nhập hoặc chọn ít nhất 4 số (0-9)!');
                    return;
                }
                const validNumbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];
                const results = input ? input.split(' ').filter(val => validNumbers.includes(val)) : currentSoso;
                if (results.length < 4) {
                    alert('Vui lòng nhập hoặc chọn ít nhất 4 số (0-9)!');
                    return;
                }
                currentSoso = results.slice(-sosoLength);
                analyzeBtn.textContent = 'Cập Nhật';
            }
            analyzeSosoData();
        })
        .catch(error => {
            console.error('Error checking login:', error);
            showLoginModal();
        });
    }

    function analyzeData() {
        const kqString = currentKQ.join(' ') || '';
        const formData = new FormData();
        formData.append('kq_input', kqString);
        formData.append('kq_length', kqLength);

        fetch('/analyze', {
            method: 'POST',
            body: formData,
            credentials: 'include'
        })
        .then(response => response.json())
        .then(result => {
            if (result.error) {
                alert(result.error);
                if (result.error === 'Vui lòng đăng nhập để phân tích!') {
                    showLoginModal();
                }
                return;
            }
            updateResultSection(result);
        })
        .catch(error => {
            console.error('Error analyzing data:', error);
            alert('Đã có lỗi xảy ra khi phân tích!');
            showLoginModal();
        });
    }

    function analyzeSosoData() {
        const sosoString = currentSoso.join(' ') || '';
        const formData = new FormData();
        formData.append('soso_input', sosoString);
        formData.append('soso_length', document.getElementById('soso_length').value);

        fetch('/analyze_soso', {
            method: 'POST',
            body: formData,
            credentials: 'include'
        })
        .then(response => response.json())
        .then(result => {
            if (result.error) {
                alert(result.error);
                if (result.error === 'Vui lòng đăng nhập để phân tích!') {
                    showLoginModal();
                }
                return;
            }
            updateSosoResultSection(result);
        })
        .catch(error => {
            console.error('Error analyzing soso data:', error);
            alert('Đã có lỗi xảy ra khi phân tích!');
            showLoginModal();
        });
    }

    function updateResultSection(result) {
        document.getElementById('chanle-match-count').textContent = result.total_matches || '0';
        document.getElementById('chanle-chan-rate').textContent = `${result.c_percentage || 0}%`;
        document.getElementById('chanle-le-rate').textContent = `${result.l_percentage || 0}%`;
        document.getElementById('chanle-prediction-rate').textContent = `${result.prediction_rate || 0}%`;
        document.getElementById('chanle-prediction-text-display').textContent = result.prediction || '';
        document.getElementById('chanle-rate-0').textContent = `${result.number_stats['0'] || 0}%`;
        document.getElementById('chanle-rate-1').textContent = `${result.number_stats['1'] || 0}%`;
        document.getElementById('chanle-rate-2').textContent = `${result.number_stats['2'] || 0}%`;
        document.getElementById('chanle-rate-3').textContent = `${result.number_stats['3'] || 0}%`;
        document.getElementById('chanle-rate-4').textContent = `${result.number_stats['4'] || 0}%`;
        
        const currentKQElement = document.getElementById('chanle-current-kq');
        if (currentKQ.length === 0) {
            currentKQElement.textContent = 'Chưa có chuỗi KQ';
        } else {
            currentKQElement.innerHTML = '';
            for (let i = 0; i < currentKQ.length; i += 25) {
                const row = document.createElement('div');
                row.className = 'current-kq-row';
                const rowResults = currentKQ.slice(i, i + 25);
                rowResults.forEach(val => {
                    const span = document.createElement('span');
                    span.textContent = val;
                    row.appendChild(span);
                });
                currentKQElement.appendChild(row);
            }
        }

        const predictionCircle = document.getElementById('chanle-prediction-circle');
        if (currentKQ.length === 0) {
            predictionCircle.removeAttribute('data-percentage');
        } else {
            predictionCircle.setAttribute('data-percentage', `${result.prediction_rate || 0}%`);
        }
    }

    function updateSosoResultSection(result) {
        document.getElementById('soso-current-soso').textContent = result.total_count ? currentSoso.join(' ') : 'Chưa có chuỗi số';
        document.getElementById('soso-rate-0').textContent = `${result.number_stats['0'] || 0}%`;
        document.getElementById('soso-rate-1').textContent = `${result.number_stats['1'] || 0}%`;
        document.getElementById('soso-rate-2').textContent = `${result.number_stats['2'] || 0}%`;
        document.getElementById('soso-rate-3').textContent = `${result.number_stats['3'] || 0}%`;
        document.getElementById('soso-rate-4').textContent = `${result.number_stats['4'] || 0}%`;
        document.getElementById('soso-rate-5').textContent = `${result.number_stats['5'] || 0}%`;
        document.getElementById('soso-rate-6').textContent = `${result.number_stats['6'] || 0}%`;
        document.getElementById('soso-rate-7').textContent = `${result.number_stats['7'] || 0}%`;
        document.getElementById('soso-rate-8').textContent = `${result.number_stats['8'] || 0}%`;
        document.getElementById('soso-rate-9').textContent = `${result.number_stats['9'] || 0}%`;
        const predictionCircle = document.getElementById('soso-prediction-circle');
        document.getElementById('soso-prediction').textContent = result.prediction || '?';
        predictionCircle.setAttribute('data-percentage', `${result.prediction_rate || 0}%`);
    }

    function showSimulateForm() {
        document.getElementById('simulate-form').style.display = 'block';
        document.getElementById('overlay').style.display = 'block';
    }

    function hideSimulateForm() {
        document.getElementById('simulate-form').style.display = 'none';
        document.getElementById('overlay').style.display = 'none';
    }

    function handleSimulate(event) {
        event.preventDefault();
        const form = document.getElementById('simulate-form-data');
        const formData = new FormData(form);
        formData.append('kq_input', currentKQ.join(' '));
        formData.append('kq_length', kqLength);

        fetch('/simulate', {
            method: 'POST',
            body: formData,
            credentials: 'include'
        })
        .then(response => response.json())
        .then(result => {
            if (result.error) {
                if (result.error === 'Vui lòng đăng nhập để mô phỏng!') {
                    showLoginModal();
                } else {
                    alert(result.error);
                }
                return;
            }
            document.getElementById('initial-capital').textContent = result.initial_capital;
            document.getElementById('final-capital').textContent = result.final_capital;
            document.getElementById('profit-loss').textContent = result.profit_loss;
            document.getElementById('win-count').textContent = result.win_count;
            document.getElementById('lose-count').textContent = result.lose_count;
            hideSimulateForm();
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Đã có lỗi xảy ra khi mô phỏng!');
        });
    }

    function handleLogin(event) {
        event.preventDefault();
        const form = document.getElementById('login-form');
        const formData = new FormData(form);

        fetch('/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams(formData).toString(),
            credentials: 'include'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                sessionStorage.setItem('loggedIn', 'true');
                hideLoginModal();
                const loginButtons = document.querySelectorAll('.login-btn');
                loginButtons.forEach(btn => {
                    btn.outerHTML = `<span class="logout-text">
                        <span class="greeting">Chào ${data.username || formData.get('username')}.</span>
                        <span class="logout-link" onclick="logout()">Thoát</span>
                    </span>`;
                });
            } else {
                alert(data.message || 'Đăng nhập thất bại!');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Đã có lỗi xảy ra. Vui lòng thử lại!');
        });
    }

    function handleRegister(event) {
        event.preventDefault();
        const form = document.getElementById('register-form');
        const formData = new FormData(form);

        fetch('/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams(formData).toString(),
            credentials: 'include'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                showLoginTab();
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Đã có lỗi xảy ra. Vui lòng thử lại!');
        });
    }

    function handleForgotPassword(event) {
        event.preventDefault();
        const form = document.getElementById('forgot-password-form');
        const formData = new FormData(form);

        fetch('/forgot_password', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams(formData).toString(),
            credentials: 'include'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                showLoginTab();
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Đã có lỗi xảy ra. Vui lòng thử lại!');
        });
    }

    function logout() {
        sessionStorage.removeItem('loggedIn');
        fetch('/logout', {
            method: 'POST',
            credentials: 'include'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const logoutTexts = document.querySelectorAll('.logout-text');
                logoutTexts.forEach(text => {
                    text.outerHTML = `<button class="login-btn" onclick="showLoginModal()">Đăng nhập</button>`;
                });
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Đã có lỗi xảy ra khi thoát!');
        });
    }

    window.onload = function() {
        showTab('main-lobby');
        document.getElementById('chanle-kq-length').addEventListener('change', function() {
            kqLength = parseInt(this.value);
            if (isAnalyzed) analyzeData();
        });
        document.getElementById('soso_length').addEventListener('change', function() {
            const sosoLength = parseInt(this.value);
            if (currentSoso.length > sosoLength) {
                currentSoso = currentSoso.slice(-sosoLength);
                if (currentSoso.length >= 4) analyzeSosoData();
            }
        });
        document.getElementById('chanle-result-buttons').style.display = 'none';
    };
</script>