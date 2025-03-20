let currentTab = 'main-lobby';
let currentSubTab = '';
let currentKQ = [];
let currentAiKQ = [];
let currentSimKQ = [];
let kqLength = 6;
let aiKqLength = 6;
let simKqLength = 6;
let currentSoso = [];
let isAnalyzed = false;
let isAiAnalyzed = false;
let isSimulated = false;
let totalWins = 0;
let totalLosses = 0;
let maxWinStreak = 0;
let maxLoseStreak = 0;
let currentWinStreak = 0;
let currentLoseStreak = 0;
let lastPrediction = '';
let aiTotalWins = 0;
let aiTotalLosses = 0;
let aiMaxWinStreak = 0;
let aiMaxLoseStreak = 0;
let aiCurrentWinStreak = 0;
let aiCurrentLoseStreak = 0;
let aiLastPrediction = '';
let simTotalRounds = 0;
let simWinCount = 0;
let simLoseCount = 0;
let simInitialCapital = 0;
let simFinalCapital = 0;
let simProfitLoss = 0;
let simMaxProfit = 0;
let simMaxLoss = 0;
let simMaxWinStreak = 0;
let simMaxLoseStreak = 0;
let simDetails = [];
let userBettingSettings = JSON.parse(localStorage.getItem(`bettingSettings_${sessionStorage.getItem('loggedInUser') || 'default'}`)) || {
    initialCapital: 0,
    win1: 0, win2: 0, win3: 0, win4: 0, win5: 0, win6: 0,
    lose1: 0, lose2: 0, lose3: 0, lose4: 0, lose5: 0, lose6: 0
};

function formatInput(inputElement) {
    let value = inputElement.value.replace(/\s+/g, '').toUpperCase();
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

function updateStats(predicted, actualResult) {
    const isWin = predicted === actualResult;
    if (isWin) {
        totalWins++;
        currentWinStreak++;
        currentLoseStreak = 0;
        maxWinStreak = Math.max(maxWinStreak, currentWinStreak);
    } else {
        totalLosses++;
        currentLoseStreak++;
        currentWinStreak = 0;
        maxLoseStreak = Math.max(maxLoseStreak, currentLoseStreak);
    }
    const chanleTotalWin = document.getElementById('chanle-total-win');
    const chanleTotalLose = document.getElementById('chanle-total-lose');
    const chanleMaxWinStreak = document.getElementById('chanle-max-win-streak');
    const chanleMaxLoseStreak = document.getElementById('chanle-max-lose-streak');
    const chanleCurrentWinStreak = document.getElementById('chanle-current-win-streak');
    const chanleCurrentLoseStreak = document.getElementById('chanle-current-lose-streak');

    if (chanleTotalWin) chanleTotalWin.textContent = totalWins;
    if (chanleTotalLose) chanleTotalLose.textContent = totalLosses;
    if (chanleMaxWinStreak) chanleMaxWinStreak.textContent = maxWinStreak;
    if (chanleMaxLoseStreak) chanleMaxLoseStreak.textContent = maxLoseStreak;
    if (chanleCurrentWinStreak) chanleCurrentWinStreak.textContent = currentWinStreak;
    if (chanleCurrentLoseStreak) chanleCurrentLoseStreak.textContent = currentLoseStreak;
}

function updateAiStats(predicted, actualResult) {
    const isWin = predicted === actualResult;
    if (isWin) {
        aiTotalWins++;
        aiCurrentWinStreak++;
        aiCurrentLoseStreak = 0;
        aiMaxWinStreak = Math.max(aiMaxWinStreak, aiCurrentWinStreak);
    } else {
        aiTotalLosses++;
        aiCurrentLoseStreak++;
        aiCurrentWinStreak = 0;
        aiMaxLoseStreak = Math.max(aiMaxLoseStreak, aiCurrentLoseStreak);
    }
    const chanleAiTotalWin = document.getElementById('chanle-ai-total-win');
    const chanleAiTotalLose = document.getElementById('chanle-ai-total-lose');
    const chanleAiMaxWinStreak = document.getElementById('chanle-ai-max-win-streak');
    const chanleAiMaxLoseStreak = document.getElementById('chanle-ai-max-lose-streak');
    const chanleAiCurrentWinStreak = document.getElementById('chanle-ai-current-win-streak');
    const chanleAiCurrentLoseStreak = document.getElementById('chanle-ai-current-lose-streak');

    if (chanleAiTotalWin) chanleAiTotalWin.textContent = aiTotalWins;
    if (chanleAiTotalLose) chanleAiTotalLose.textContent = aiTotalLosses;
    if (chanleAiMaxWinStreak) chanleAiMaxWinStreak.textContent = aiMaxWinStreak;
    if (chanleAiMaxLoseStreak) chanleAiMaxLoseStreak.textContent = aiMaxLoseStreak;
    if (chanleAiCurrentWinStreak) chanleAiCurrentWinStreak.textContent = aiCurrentWinStreak;
    if (chanleAiCurrentLoseStreak) chanleAiCurrentLoseStreak.textContent = aiCurrentLoseStreak;
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
        document.getElementById('betting-modal').style.display = 'none';
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
        if (tab === 'chanle_lobby' && subTab === 'chanle' && currentSubTab === 'chanle-ai-details') {
            const predictionBox = document.getElementById('chanle-ai-prediction-box');
            if (predictionBox) predictionBox.style.display = 'flex';
        }
        currentTab = tab;
        if (currentSubTab !== 'chanle-simulate') {
            document.getElementById('betting-modal').style.display = 'none';
            document.getElementById('use-betting').checked = false;
        }
    }
}

function showAnalysisTab(subTab) {
    fetch('/check_login', { method: 'GET', credentials: 'include' })
        .then(response => response.json())
        .then(data => {
            if (!data.logged_in) {
                showLoginModal();
                return;
            }
            document.querySelectorAll('.sub-tab-content').forEach(st => st.style.display = 'none');
            document.querySelectorAll('.sub-tab-details').forEach(dt => dt.style.display = 'none');
            document.querySelectorAll('.prediction-box').forEach(pb => pb.style.display = 'none');
            const details = document.getElementById(subTab);
            if (details) details.style.display = 'block';
            if (subTab === 'chanle-details') {
                const predictionBox = document.getElementById('chanle-prediction-box');
                if (predictionBox) predictionBox.style.display = 'flex';
            }
            currentSubTab = subTab;
            document.getElementById('betting-modal').style.display = 'none';
            document.getElementById('use-betting').checked = false;
        })
        .catch(error => {
            console.error('Error checking login:', error);
            showLoginModal();
        });
}

function showAiPredictionTab(subTab) {
    fetch('/check_login', { method: 'GET', credentials: 'include' })
        .then(response => response.json())
        .then(data => {
            if (!data.logged_in) {
                showLoginModal();
                return;
            }
            document.querySelectorAll('.sub-tab-content').forEach(st => st.style.display = 'none');
            document.querySelectorAll('.sub-tab-details').forEach(dt => dt.style.display = 'none');
            document.querySelectorAll('.prediction-box').forEach(pb => pb.style.display = 'none');
            const details = document.getElementById(subTab);
            if (details) details.style.display = 'block';
            if (subTab === 'chanle-ai-details') {
                const predictionBox = document.getElementById('chanle-ai-prediction-box');
                if (predictionBox) predictionBox.style.display = 'flex';
            }
            currentSubTab = subTab;
            document.getElementById('betting-modal').style.display = 'none';
            document.getElementById('use-betting').checked = false;
        })
        .catch(error => {
            console.error('Error checking login:', error);
            showLoginModal();
        });
}

function showSimulateTab(subTab) {
    fetch('/check_login', { method: 'GET', credentials: 'include' })
        .then(response => response.json())
        .then(data => {
            if (!data.logged_in) {
                showLoginModal();
                return;
            }
            document.querySelectorAll('.sub-tab-content').forEach(st => st.style.display = 'none');
            document.querySelectorAll('.sub-tab-details').forEach(dt => dt.style.display = 'none');
            document.querySelectorAll('.prediction-box').forEach(pb => pb.style.display = 'none');
            const details = document.getElementById(subTab);
            if (details) details.style.display = 'block';
            currentSubTab = subTab;
            loadBettingSettings();
            if (isSimulated) updateSimulateResultSection();
        })
        .catch(error => {
            console.error('Error checking login:', error);
            showLoginModal();
        });
}

function goBack() {
    document.querySelectorAll('.tab-content').forEach(t => t.style.display = 'none');
    document.querySelectorAll('.sub-tab-content').forEach(st => st.style.display = 'none');
    document.querySelectorAll('.sub-tab-details').forEach(dt => dt.style.display = 'none');
    document.querySelectorAll('.prediction-box').forEach(pb => pb.style.display = 'none');
    document.getElementById('main-lobby').style.display = 'grid';
    currentTab = 'main-lobby';
    currentSubTab = '';
    document.getElementById('betting-modal').style.display = 'none';
    document.getElementById('use-betting').checked = false;
}

function appendResult(value) {
    if (!isAnalyzed) return;
    value = convertToCL(value);
    currentKQ.push(value);
    document.getElementById('chanle-kq-input').value = '';
    updateResultSection({
        current_kq: currentKQ.join(' '),
        total_matches: document.getElementById('chanle-match-count')?.textContent || '0',
        sample_c_percentage: document.getElementById('chanle-sample-chan-rate')?.textContent?.replace('%', '') || '0',
        sample_l_percentage: document.getElementById('chanle-sample-le-rate')?.textContent?.replace('%', '') || '0',
        prediction: lastPrediction,
        prediction_rate: document.getElementById('chanle-prediction-rate')?.textContent?.replace('%', '') || '0'
    });
    if (lastPrediction) updateStats(lastPrediction, value);
    analyzeData();
}

function appendAiResult(value) {
    if (!isAiAnalyzed) return;
    value = convertToCL(value);
    currentAiKQ.push(value);
    document.getElementById('chanle-ai-kq-input').value = '';
    updateAiResultSection({
        current_kq: currentAiKQ.join(' '),
        total_matches: document.getElementById('chanle-ai-match-count')?.textContent || '0',
        sample_c_percentage: document.getElementById('chanle-ai-sample-chan-rate')?.textContent?.replace('%', '') || '0',
        sample_l_percentage: document.getElementById('chanle-ai-sample-le-rate')?.textContent?.replace('%', '') || '0',
        prediction: aiLastPrediction,
        prediction_rate: document.getElementById('chanle-ai-prediction-circle')?.getAttribute('data-percentage')?.replace('%', '') || '0'
    });
    if (aiLastPrediction) updateAiStats(aiLastPrediction, value);
    aiAnalyzeData();
}

function resetData(type) {
    if (type === 'chanle') {
        currentKQ = [];
        kqLength = parseInt(document.getElementById('chanle-kq-length').value);
        isAnalyzed = false;
        totalWins = 0;
        totalLosses = 0;
        maxWinStreak = 0;
        maxLoseStreak = 0;
        currentWinStreak = 0;
        currentLoseStreak = 0;
        lastPrediction = '';
        document.getElementById('chanle-kq-input').value = '';
        document.getElementById('chanle-analyze-btn').textContent = 'Cập Nhật';
        document.getElementById('chanle-result-buttons').style.display = 'none';
        updateResultSection({
            current_kq: 'Chưa có chuỗi KQ',
            total_matches: 0,
            sample_c_percentage: 0,
            sample_l_percentage: 0,
            prediction: '',
            prediction_rate: 0
        });
        updateStats({ prediction: '' }, '');
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

function resetAiData(type) {
    if (type === 'chanle-ai') {
        currentAiKQ = [];
        aiKqLength = parseInt(document.getElementById('chanle-ai-kq-length').value);
        isAiAnalyzed = false;
        aiTotalWins = 0;
        aiTotalLosses = 0;
        aiMaxWinStreak = 0;
        aiMaxLoseStreak = 0;
        aiCurrentWinStreak = 0;
        aiCurrentLoseStreak = 0;
        aiLastPrediction = '';
        document.getElementById('chanle-ai-kq-input').value = '';
        document.getElementById('chanle-ai-analyze-btn').textContent = 'Cập Nhật';
        document.getElementById('chanle-ai-result-buttons').style.display = 'none';
        updateAiResultSection({
            current_kq: 'Chưa có chuỗi KQ',
            total_matches: 0,
            sample_c_percentage: 0,
            sample_l_percentage: 0,
            prediction: '',
            prediction_rate: 0
        });
        updateAiStats({ prediction: '' }, '');
    }
}

function resetSimulateData() {
    currentSimKQ = [];
    simKqLength = parseInt(document.getElementById('sim-kq-length').value);
    isSimulated = false;
    simTotalRounds = 0;
    simWinCount = 0;
    simLoseCount = 0;
    simInitialCapital = userBettingSettings.initialCapital || 0;
    simFinalCapital = 0;
    simProfitLoss = 0;
    simMaxProfit = 0;
    simMaxLoss = 0;
    simMaxWinStreak = 0;
    simMaxLoseStreak = 0;
    simDetails = [];
    document.getElementById('sim-kq-input').value = '';
    const simulateCard = document.getElementById('simulate-card');
    if (simulateCard) simulateCard.style.display = 'none';
    loadBettingSettings();
}

function showLoginModal() {
    if (document.getElementById('betting-modal').style.display === 'block') {
        hideModal('betting-modal');
    }
    document.getElementById('login-modal').style.display = 'block';
    document.getElementById('overlay').style.display = 'block';
    showLoginTab();
}

function hideModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
    if (document.querySelectorAll('.login-modal[style*="display: block"], .betting-modal[style*="display: block"]').length === 0) {
        document.getElementById('overlay').style.display = 'none';
    }
    if (modalId === 'betting-modal') {
        document.getElementById('use-betting').checked = false;
    }
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

function showBettingModal() {
    if (document.getElementById('login-modal').style.display === 'block') {
        hideModal('login-modal');
    }
    if (document.getElementById('use-betting').checked && currentSubTab === 'chanle-simulate') {
        document.getElementById('betting-modal').style.display = 'block';
        document.getElementById('overlay').style.display = 'block';
        loadBettingSettingsToForm();
    }
}

function loadBettingSettings() {
    const username = sessionStorage.getItem('loggedInUser') || 'default';
    userBettingSettings = JSON.parse(localStorage.getItem(`bettingSettings_${username}`)) || {
        initialCapital: 0,
        win1: 0, win2: 0, win3: 0, win4: 0, win5: 0, win6: 0,
        lose1: 0, lose2: 0, lose3: 0, lose4: 0, lose5: 0, lose6: 0
    };
    console.log("Loaded betting settings:", userBettingSettings);
    const initialCapitalInput = document.getElementById('sim-initial-capital-input');
    const win1Input = document.getElementById('sim-win-1');
    const win2Input = document.getElementById('sim-win-2');
    const win3Input = document.getElementById('sim-win-3');
    const win4Input = document.getElementById('sim-win-4');
    const win5Input = document.getElementById('sim-win-5');
    const win6Input = document.getElementById('sim-win-6');
    const lose1Input = document.getElementById('sim-lose-1');
    const lose2Input = document.getElementById('sim-lose-2');
    const lose3Input = document.getElementById('sim-lose-3');
    const lose4Input = document.getElementById('sim-lose-4');
    const lose5Input = document.getElementById('sim-lose-5');
    const lose6Input = document.getElementById('sim-lose-6');

    if (initialCapitalInput) initialCapitalInput.value = userBettingSettings.initialCapital || 0;
    if (win1Input) win1Input.value = userBettingSettings.win1 || 0;
    if (win2Input) win2Input.value = userBettingSettings.win2 || 0;
    if (win3Input) win3Input.value = userBettingSettings.win3 || 0;
    if (win4Input) win4Input.value = userBettingSettings.win4 || 0;
    if (win5Input) win5Input.value = userBettingSettings.win5 || 0;
    if (win6Input) win6Input.value = userBettingSettings.win6 || 0;
    if (lose1Input) lose1Input.value = userBettingSettings.lose1 || 0;
    if (lose2Input) lose2Input.value = userBettingSettings.lose2 || 0;
    if (lose3Input) lose3Input.value = userBettingSettings.lose3 || 0;
    if (lose4Input) lose4Input.value = userBettingSettings.lose4 || 0;
    if (lose5Input) lose5Input.value = userBettingSettings.lose5 || 0;
    if (lose6Input) lose6Input.value = userBettingSettings.lose6 || 0;
}

function loadBettingSettingsToForm() {
    const settings = userBettingSettings;
    const initialCapitalInput = document.getElementById('sim-initial-capital-input');
    const win1Input = document.getElementById('sim-win-1');
    const win2Input = document.getElementById('sim-win-2');
    const win3Input = document.getElementById('sim-win-3');
    const win4Input = document.getElementById('sim-win-4');
    const win5Input = document.getElementById('sim-win-5');
    const win6Input = document.getElementById('sim-win-6');
    const lose1Input = document.getElementById('sim-lose-1');
    const lose2Input = document.getElementById('sim-lose-2');
    const lose3Input = document.getElementById('sim-lose-3');
    const lose4Input = document.getElementById('sim-lose-4');
    const lose5Input = document.getElementById('sim-lose-5');
    const lose6Input = document.getElementById('sim-lose-6');

    if (initialCapitalInput) initialCapitalInput.value = settings.initialCapital || 0;
    if (win1Input) win1Input.value = settings.win1 || 0;
    if (win2Input) win2Input.value = settings.win2 || 0;
    if (win3Input) win3Input.value = settings.win3 || 0;
    if (win4Input) win4Input.value = settings.win4 || 0;
    if (win5Input) win5Input.value = settings.win5 || 0;
    if (win6Input) win6Input.value = settings.win6 || 0;
    if (lose1Input) lose1Input.value = settings.lose1 || 0;
    if (lose2Input) lose2Input.value = settings.lose2 || 0;
    if (lose3Input) lose3Input.value = settings.lose3 || 0;
    if (lose4Input) lose4Input.value = settings.lose4 || 0;
    if (lose5Input) lose5Input.value = settings.lose5 || 0;
    if (lose6Input) lose6Input.value = settings.lose6 || 0;
}

function saveBettingSettings(event) {
    event.preventDefault();
    const newSettings = {
        initialCapital: parseInt(document.getElementById('sim-initial-capital-input').value) || 0,
        win1: parseInt(document.getElementById('sim-win-1').value) || 0,
        win2: parseInt(document.getElementById('sim-win-2').value) || 0,
        win3: parseInt(document.getElementById('sim-win-3').value) || 0,
        win4: parseInt(document.getElementById('sim-win-4').value) || 0,
        win5: parseInt(document.getElementById('sim-win-5').value) || 0,
        win6: parseInt(document.getElementById('sim-win-6').value) || 0,
        lose1: parseInt(document.getElementById('sim-lose-1').value) || 0,
        lose2: parseInt(document.getElementById('sim-lose-2').value) || 0,
        lose3: parseInt(document.getElementById('sim-lose-3').value) || 0,
        lose4: parseInt(document.getElementById('sim-lose-4').value) || 0,
        lose5: parseInt(document.getElementById('sim-lose-5').value) || 0,
        lose6: parseInt(document.getElementById('sim-lose-6').value) || 0
    };
    userBettingSettings = { ...newSettings };
    const username = sessionStorage.getItem('loggedInUser') || 'default';
    localStorage.setItem(`bettingSettings_${username}`, JSON.stringify(userBettingSettings));
    console.log("Saved betting settings:", userBettingSettings);
    hideModal('betting-modal');
    document.getElementById('use-betting').checked = true;
}

function checkLoginAndAnalyze() {
    fetch('/check_login', { method: 'GET', credentials: 'include' })
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
            input = input.replace(/\s+/g, '').toUpperCase();
            const validInputs = input ? input.split('') : [];
            let newResults = validInputs.map(val => convertToCL(val));
            if (!input && currentKQ.length === 0) {
                alert('Vui lòng nhập KQ thực tế (C, L, hoặc 0-4)!');
                return;
            }
            newResults = validInputs.map(val => convertToCL(val));
            currentKQ = currentKQ.concat(newResults);
            document.getElementById('chanle-kq-input').value = '';
            analyzeBtn.textContent = 'Cập Nhật';
            resultButtons.style.display = 'flex';
            isAnalyzed = true;
            newResults.forEach(result => {
                if (lastPrediction) updateStats(lastPrediction, result);
            });
            analyzeData();
        })
        .catch(error => {
            console.error('Error checking login:', error);
            showLoginModal();
        });
}

function checkLoginAndAiAnalyze() {
    fetch('/check_login', { method: 'GET', credentials: 'include' })
        .then(response => response.json())
        .then(data => {
            if (!data.logged_in) {
                showLoginModal();
                return;
            }
            let input = document.getElementById('chanle-ai-kq-input').value.trim();
            const analyzeBtn = document.getElementById('chanle-ai-analyze-btn');
            const resultButtons = document.getElementById('chanle-ai-result-buttons');
            aiKqLength = parseInt(document.getElementById('chanle-ai-kq-length').value);
            input = input.replace(/\s+/g, '').toUpperCase();
            const validInputs = input ? input.split('') : [];
            let newResults = validInputs.map(val => convertToCL(val));
            if (!input && currentAiKQ.length === 0) {
                alert('Vui lòng nhập KQ thực tế (C, L, hoặc 0-4)!');
                return;
            }
            newResults = validInputs.map(val => convertToCL(val));
            currentAiKQ = currentAiKQ.concat(newResults);
            document.getElementById('chanle-ai-kq-input').value = '';
            analyzeBtn.textContent = 'Cập Nhật';
            resultButtons.style.display = 'flex';
            isAiAnalyzed = true;
            newResults.forEach(result => {
                if (aiLastPrediction) updateAiStats(aiLastPrediction, result);
            });
            aiAnalyzeData();
        })
        .catch(error => {
            console.error('Error checking login:', error);
            showLoginModal();
        });
}

function checkLoginAndSimulate() {
    fetch('/check_login', { method: 'GET', credentials: 'include' })
        .then(response => response.json())
        .then(data => {
            if (!data.logged_in) {
                showLoginModal();
                return;
            }
            let input = document.getElementById('sim-kq-input').value.trim();
            simKqLength = parseInt(document.getElementById('sim-kq-length').value);
            const predictionTool = document.getElementById('sim-prediction-tool').value;
            input = input.replace(/\s+/g, '').toUpperCase();
            const validInputs = input ? input.split('') : [];
            let newResults = validInputs.map(val => convertToCL(val));
            currentSimKQ = newResults;
            if (currentSimKQ.length < simKqLength + 1) {
                alert(`Chuỗi KQ phải có ít nhất ${simKqLength + 1} kết quả để mô phỏng!`);
                return;
            }
            isSimulated = true;
            const formData = new FormData();
            formData.append('kq_input', currentSimKQ.join(' '));
            formData.append('kq_length', simKqLength);
            formData.append('prediction_tool', predictionTool);
            const useBetting = document.getElementById('use-betting').checked;
            formData.append('use_betting', useBetting.toString());
            loadBettingSettings();
            if (useBetting) {
                if (userBettingSettings.initialCapital <= 0) {
                    alert("Vui lòng thiết lập Vốn ban đầu lớn hơn 0 trong Thiết lập cược!");
                    return;
                }
                if (!userBettingSettings.win1 && !userBettingSettings.lose1) {
                    alert("Vui lòng thiết lập ít nhất mức cược Win 1 hoặc Lose 1!");
                    return;
                }
            }
            formData.append('betting_settings', JSON.stringify(userBettingSettings));
            console.log("Sent betting data:", userBettingSettings);
            fetch('/simulate', { method: 'POST', body: formData, credentials: 'include' })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(result => {
                    console.log("Simulation result:", result);
                    if (result.error) {
                        console.error('Simulation error:', result.error);
                        if (result.error === 'Vui lòng đăng nhập để sử dụng chức năng này!') {
                            showLoginModal();
                        } else {
                            alert(result.error);
                            simTotalRounds = 0;
                            simWinCount = 0;
                            simLoseCount = 0;
                            simInitialCapital = 0;
                            simFinalCapital = 0;
                            simProfitLoss = 0;
                            simMaxProfit = 0;
                            simMaxLoss = 0;
                            simMaxWinStreak = 0;
                            simMaxLoseStreak = 0;
                            simDetails = [];
                        }
                        updateSimulateResultSection();
                        return;
                    }
                    simTotalRounds = result.total_rounds || 0;
                    simWinCount = result.win_count || 0;
                    simLoseCount = result.lose_count || 0;
                    simInitialCapital = result.initial_capital || 0;
                    simFinalCapital = result.final_capital || 0;
                    simProfitLoss = result.profit_loss || 0;
                    simMaxProfit = result.max_profit || 0;
                    simMaxLoss = result.max_loss || 0;
                    simMaxWinStreak = result.max_win_streak || 0;
                    simMaxLoseStreak = result.max_lose_streak || 0;
                    simDetails = result.round_details || [];
                    updateSimulateResultSection();
                })
                .catch(error => {
                    console.error('Error simulating:', error);
                    alert(`Lỗi khi mô phỏng: ${error.message}. Vui lòng kiểm tra kết nối server.`);
                    simTotalRounds = 0;
                    simWinCount = 0;
                    simLoseCount = 0;
                    simInitialCapital = 0;
                    simFinalCapital = 0;
                    simProfitLoss = 0;
                    simMaxProfit = 0;
                    simMaxLoss = 0;
                    simMaxWinStreak = 0;
                    simMaxLoseStreak = 0;
                    simDetails = [];
                    updateSimulateResultSection();
                });
        })
        .catch(error => {
            console.error('Error checking login:', error);
            showLoginModal();
        });
}

function updateResultSection(data) {
    const chanleCurrentKq = document.getElementById('chanle-current-kq');
    const chanleMatchCount = document.getElementById('chanle-match-count');
    const chanleSampleChanRate = document.getElementById('chanle-sample-chan-rate');
    const chanleSampleLeRate = document.getElementById('chanle-sample-le-rate');
    const predictionText = document.getElementById('chanle-prediction-text');
    const predictionRate = document.getElementById('chanle-prediction-rate');
    const predictionRect = document.getElementById('chanle-prediction-rectangle');

    if (chanleCurrentKq) chanleCurrentKq.textContent = data.current_kq || 'Chưa có chuỗi KQ';
    if (chanleMatchCount) chanleMatchCount.textContent = data.total_matches || 0;
    if (chanleSampleChanRate) chanleSampleChanRate.textContent = `${data.sample_c_percentage || 0}%`;
    if (chanleSampleLeRate) chanleSampleLeRate.textContent = `${data.sample_l_percentage || 0}%`;
    if (predictionText) {
        if (data.prediction) {
            predictionText.textContent = data.prediction;
            if (predictionRate) predictionRate.textContent = `${data.prediction_rate || 0}%`;
            if (predictionRect) {
                predictionRect.className = 'prediction-rectangle';
                predictionRect.classList.add(data.prediction === 'C' ? 'chan' : 'le');
            }
            lastPrediction = data.prediction;
        } else {
            predictionText.textContent = 'Chưa có dự đoán';
            if (predictionRate) predictionRate.textContent = '';
            if (predictionRect) predictionRect.className = 'prediction-rectangle';
            lastPrediction = '';
        }
    }
}

function updateAiResultSection(data) {
    const chanleAiCurrentKq = document.getElementById('chanle-ai-current-kq');
    const predictionText = document.getElementById('chanle-ai-prediction-text');
    const predictionCircle = document.getElementById('chanle-ai-prediction-circle');

    if (chanleAiCurrentKq) chanleAiCurrentKq.textContent = data.current_kq || 'Chưa có chuỗi KQ';
    if (predictionText) {
        if (data.prediction) {
            predictionText.textContent = data.prediction;
            if (predictionCircle) {
                predictionCircle.setAttribute('data-percentage', `${data.prediction_rate || 0}%`);
                predictionCircle.style.background = data.prediction === 'C' ? 'linear-gradient(135deg, #00C4B4 0%, #00897B 100%)' : 'linear-gradient(135deg, #FF6F61 0%, #D32F2F 100%)';
            }
            aiLastPrediction = data.prediction;
        } else {
            predictionText.textContent = 'Chưa có dự đoán';
            if (predictionCircle) {
                predictionCircle.setAttribute('data-percentage', '0%');
                predictionCircle.style.background = 'linear-gradient(135deg, #555 0%, #333 100%)';
            }
            aiLastPrediction = '';
        }
    }
}

function updateSimulateResultSection() {
    const simulateCard = document.getElementById('simulate-card');
    if (!simulateCard) {
        console.error("simulate-card element not found");
        return;
    }
    simulateCard.style.display = isSimulated ? 'grid' : 'none';

    const simInitialKq = document.getElementById('sim-initial-kq');
    if (simInitialKq) simInitialKq.textContent = currentSimKQ.join(' ') || 'Chưa có chuỗi KQ';

    simulateCard.innerHTML = `
        <div><span>Tổng ván:</span><span class="highlight">${simTotalRounds || 0}</span></div>
        <div><span>Win:</span><span class="highlight">${simWinCount || 0}</span></div>
        <div><span>Lose:</span><span class="highlight">${simLoseCount || 0}</span></div>
        <div><span>Max Win Streak:</span><span class="highlight">${simMaxWinStreak || 0}</span></div>
        <div><span>Max Lose Streak:</span><span class="highlight">${simMaxLoseStreak || 0}</span></div>
        <div><span>Vốn ban đầu:</span><span class="highlight">${simInitialCapital ? simInitialCapital.toFixed(1) : 0}</span></div>
        <div><span>Vốn cược:</span><span class="highlight">${simFinalCapital ? simFinalCapital.toFixed(1) : 0}</span></div>
        <div><span>Lãi/Lỗ:</span><span class="highlight">${simProfitLoss ? simProfitLoss.toFixed(1) : 0}</span></div>
        <div><span>Max Lãi:</span><span class="highlight">${simMaxProfit ? simMaxProfit.toFixed(1) : 0}</span></div>
        <div><span>Max Lỗ:</span><span class="highlight">${simMaxLoss ? simMaxLoss.toFixed(1) : 0}</span></div>
    `;

    const simDetailsDiv = document.getElementById('sim-details');
    if (simDetailsDiv) {
        const showDetailsCheckbox = document.getElementById('showSimDetails');
        if (showDetailsCheckbox && showDetailsCheckbox.checked) {
            simDetailsDiv.style.display = 'block';
            let tableHTML = `
                <table style="width: 100%; border-collapse: collapse;">
                    <thead>
                        <tr style="background: #FFA500; color: #0F0C2F;">
                            <th>Ván</th>
                            <th>Dự đoán</th>
                            <th>Thực tế</th>
                            <th>Kết quả</th>
                            <th>Cược</th>
                            <th>Lãi/Lỗ</th>
                            <th>Vốn sau</th>
                        </tr>
                    </thead>
                    <tbody>
            `;
            simDetails.forEach(round => {
                const resultColor = round.result === 'Win' ? 'green' : 'red';
                const predictionDisplay = round.prediction_rate ? `${round.prediction} (${round.prediction_rate}%)` : round.prediction || 'N/A';
                const streakDisplay = round.result === 'Win' ? round.win_streak : round.lose_streak;
                tableHTML += `
                    <tr style="color: ${resultColor};">
                        <td>${round.round}</td>
                        <td>${predictionDisplay}</td>
                        <td>${round.actual || 'N/A'}</td>
                        <td>${round.result} (${streakDisplay})</td>
                        <td>${round.bet !== undefined ? Number(round.bet).toFixed(1) : '0'}</td>
                        <td>${round.profit_loss !== undefined ? Number(round.profit_loss).toFixed(1) : '0'}</td>
                        <td>${round.capital_after !== undefined ? Number(round.capital_after).toFixed(1) : simInitialCapital}</td>
                    </tr>
                `;
            });
            tableHTML += `
                    </tbody>
                </table>
            `;
            simDetailsDiv.innerHTML = tableHTML;
        } else {
            simDetailsDiv.style.display = 'none';
        }
    }
}

function toggleSimDetails() {
    const simDetailsDiv = document.getElementById('sim-details');
    const showDetailsCheckbox = document.getElementById('showSimDetails');
    if (simDetailsDiv && showDetailsCheckbox) {
        simDetailsDiv.style.display = showDetailsCheckbox.checked ? 'block' : 'none';
        if (showDetailsCheckbox.checked) {
            updateSimulateResultSection();
        }
    }
}

function checkLoginAndAnalyzeSoso() {
    let sosoInput = document.getElementById('soso_input').value.trim();
    const sosoLength = parseInt(document.getElementById('soso_length').value);
    sosoInput = sosoInput.replace(/\s+/g, '');
    if (!/^[0-9]+$/.test(sosoInput)) {
        alert('Vui lòng nhập chuỗi số hợp lệ (chỉ chứa các chữ số từ 0-9)!');
        return;
    }
    currentSoso = sosoInput.split('').slice(-sosoLength);
    const formData = new FormData();
    formData.append('soso_input', currentSoso.join(''));
    formData.append('soso_length', sosoLength);
    fetch('/analyze_soso', { method: 'POST', body: formData })
        .then(response => response.json())
        .then(result => {
            if (result.error) {
                alert(result.error);
                return;
            }
            updateSosoResultSection(result);
        })
        .catch(error => {
            console.error('Error analyzing soso:', error);
        });
}

function updateSosoResultSection(data) {
    const sosoCurrentSoso = document.getElementById('soso-current-soso');
    if (sosoCurrentSoso) sosoCurrentSoso.textContent = currentSoso.join(' ') || 'Chưa có chuỗi số';
    for (let i = 0; i <= 9; i++) {
        const sosoRate = document.getElementById(`soso-rate-${i}`);
        if (sosoRate) sosoRate.textContent = `${data.number_stats[i.toString()] || 0}%`;
    }
    const predictionCircle = document.getElementById('soso-prediction-circle');
    const sosoPrediction = document.getElementById('soso-prediction');
    if (sosoPrediction) sosoPrediction.textContent = data.prediction || '?';
    if (predictionCircle) predictionCircle.setAttribute('data-percentage', `${data.prediction_rate || 0}%`);
}

function handleLogin(event) {
    event.preventDefault();
    const form = document.getElementById('login-form');
    const formData = new FormData(form);
    fetch('/login', { method: 'POST', body: formData, credentials: 'include' })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                sessionStorage.setItem('loggedInUser', data.username);
                userBettingSettings = JSON.parse(localStorage.getItem(`bettingSettings_${data.username}`)) || userBettingSettings;
                hideModal('login-modal');
                const loginBtnContainer = document.getElementById('login-btn-container');
                loginBtnContainer.innerHTML = `
                    <span class="welcome-text">Chào, ${data.username} | </span><span class="logout-link" onclick="logout()">Thoát</span>
                `;
                if (currentSubTab === 'chanle-details') checkLoginAndAnalyze();
                else if (currentSubTab === 'chanle-ai-details') checkLoginAndAiAnalyze();
                else if (currentSubTab === 'chanle-simulate') checkLoginAndSimulate();
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error logging in:', error);
        });
}

function handleRegister(event) {
    event.preventDefault();
    const form = document.getElementById('register-form');
    const formData = new FormData(form);
    fetch('/register', { method: 'POST', body: formData })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            if (data.success) {
                showLoginTab();
            }
        })
        .catch(error => {
            console.error('Error registering:', error);
        });
}

function handleForgotPassword(event) {
    event.preventDefault();
    const form = document.getElementById('forgot-password-form');
    const formData = new FormData(form);
    fetch('/forgot_password', { method: 'POST', body: formData })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            if (data.success) {
                showLoginTab();
            }
        })
        .catch(error => {
            console.error('Error requesting password reset:', error);
        });
}

function analyzeData() {
    const formData = new FormData();
    formData.append('kq_input', currentKQ.join(' '));
    formData.append('kq_length', kqLength);
    fetch('/analyze', { method: 'POST', body: formData, credentials: 'include' })
        .then(response => response.json())
        .then(result => {
            if (result.error) {
                if (result.error === 'Vui lòng đăng nhập để sử dụng chức năng này!') {
                    showLoginModal();
                } else {
                    alert(result.error);
                }
                return;
            }
            updateResultSection(result);
        })
        .catch(error => {
            console.error('Error analyzing:', error);
        });
}

function aiAnalyzeData() {
    const formData = new FormData();
    formData.append('kq_input', currentAiKQ.join(' '));
    formData.append('kq_length', aiKqLength);
    fetch('/ai_analyze', { method: 'POST', body: formData, credentials: 'include' })
        .then(response => response.json())
        .then(result => {
            if (result.error) {
                if (result.error === 'Vui lòng đăng nhập để sử dụng chức năng này!') {
                    showLoginModal();
                } else {
                    alert(result.error);
                }
                return;
            }
            updateAiResultSection(result);
        })
        .catch(error => {
            console.error('Error analyzing with AI:', error);
        });
}

function hideAllModals() {
    hideModal('login-modal');
    hideModal('betting-modal');
}

function logout() {
    fetch('/logout', { method: 'POST', credentials: 'include' })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                sessionStorage.removeItem('loggedInUser');
                userBettingSettings = { initialCapital: 0, win1: 0, win2: 0, win3: 0, win4: 0, win5: 0, win6: 0, lose1: 0, lose2: 0, lose3: 0, lose4: 0, lose5: 0, lose6: 0 };
                const loginBtnContainer = document.getElementById('login-btn-container');
                loginBtnContainer.innerHTML = `
                    <button class="login-btn" onclick="showLoginModal()">Đăng nhập</button>
                `;
                resetData('chanle');
                resetAiData('chanle-ai');
                resetSimulateData();
                resetData('soso');
                goBack();
            } else {
                alert(data.message);
            }
        })
        .catch(error => console.error('Error logging out:', error));
}

document.addEventListener('DOMContentLoaded', () => {
    fetch('/check_login', { method: 'GET', credentials: 'include' })
        .then(response => response.json())
        .then(data => {
            const loginBtnContainer = document.getElementById('login-btn-container');
            if (data.logged_in) {
                sessionStorage.setItem('loggedInUser', data.username);
                userBettingSettings = JSON.parse(localStorage.getItem(`bettingSettings_${data.username}`)) || userBettingSettings;
                loginBtnContainer.innerHTML = `
                    <span class="welcome-text">Chào, ${data.username} | </span><span class="logout-link" onclick="logout()">Thoát</span>
                `;
            } else {
                loginBtnContainer.innerHTML = `
                    <button class="login-btn" onclick="showLoginModal()">Đăng nhập</button>
                `;
            }
        })
        .catch(error => console.error('Error checking login on load:', error));
});

document.addEventListener('DOMContentLoaded', () => {
    fetch('/check_login', { method: 'GET', credentials: 'include' })
        .then(response => response.json())
        .then(data => {
            const loginBtnContainer = document.getElementById('login-btn-container');
            if (data.logged_in) {
                sessionStorage.setItem('loggedInUser', data.username);
                userBettingSettings = JSON.parse(localStorage.getItem(`bettingSettings_${data.username}`)) || userBettingSettings;
                loginBtnContainer.innerHTML = `
                    <span class="welcome-text">Chào, ${data.username} | </span><span class="logout-link" onclick="logout()">Thoát</span>
                `;
            } else {
                loginBtnContainer.innerHTML = `
                    <button class="login-btn" onclick="showLoginModal()">Đăng nhập</button>
                `;
            }
        })
        .catch(error => console.error('Error checking login on load:', error));

    // Gắn sự kiện cho các lobby card
    const xocdiaCard = document.getElementById('xocdia-card');
    const xosoCard = document.getElementById('xoso-card');

    if (xocdiaCard) {
        xocdiaCard.addEventListener('click', () => {
            showTab('chanle_lobby', 'chanle');
        });
    }

    if (xosoCard) {
        xosoCard.addEventListener('click', () => {
            showTab('soso_lobby', 'soso');
        });
    }
});