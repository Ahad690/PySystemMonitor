// Initialize Charts
const chartConfig = (color) => ({
    type: 'doughnut',
    data: {
        datasets: [{
            data: [0, 100],
            backgroundColor: [color, '#444'],
            borderWidth: 0,
            circumference: 180,
            rotation: 270
        }]
    },
    options: {
        cutout: '80%',
        responsive: true,
        maintainAspectRatio: false,
        plugins: { tooltip: { enabled: false } },
        animation: { duration: 500 }
    }
});

let cpuChart, memChart;

function initCharts() {
    const ctxCpu = document.getElementById('cpuChart').getContext('2d');
    cpuChart = new Chart(ctxCpu, chartConfig('#00bcd4'));

    const ctxMem = document.getElementById('memChart').getContext('2d');
    memChart = new Chart(ctxMem, chartConfig('#4caf50'));
}

// Modal Functions
function showModal(title, msg) {
    document.getElementById('modalTitle').innerText = title;
    document.getElementById('modalMsg').innerText = msg;
    document.getElementById('cmdModal').classList.remove('hidden');
}

function closeModal() {
    document.getElementById('cmdModal').classList.add('hidden');
}

// Kill Process Function - writes to commands.json
function killProcess(pid, name) {
    if (!confirm(`Are you sure you want to kill process "${name}" (PID: ${pid})?`)) {
        return;
    }

    // Write command to file using a hidden iframe form POST trick won't work for file://
    // Instead: Use localStorage as a bridge that PS can't read...
    // BEST: Write a small text file that PS polls. We'll use a download trick.

    // For simplicity, we'll just show the command to run in PowerShell
    showModal('Kill Process', `To kill this process, run this command in the PowerShell terminal:\n\nStop-Process -Id ${pid} -Force\n\nOr press K in the CLI and enter PID: ${pid}`);
}

// Global update function called by JSONP
window.updateData = function (data) {
    if (!data) return;

    // Update Timestamp
    document.getElementById('timestamp').innerText = data.Timestamp;

    // Update CPU
    const cpuVal = data.Cpu.Current;
    document.getElementById('cpuValue').innerText = cpuVal + '%';
    if (cpuChart) {
        cpuChart.data.datasets[0].data = [cpuVal, 100 - cpuVal];
        cpuChart.data.datasets[0].backgroundColor[0] = cpuVal > 80 ? '#f44336' : (cpuVal > 50 ? '#ff9800' : '#00bcd4');
        cpuChart.update();
    }

    // Update Memory
    const memVal = parseFloat(data.Memory.percent);
    document.getElementById('memValue').innerText = memVal + '%';
    document.getElementById('memUsed').innerText = data.Memory.used;
    document.getElementById('memTotal').innerText = data.Memory.total;
    if (memChart) {
        memChart.data.datasets[0].data = [memVal, 100 - memVal];
        memChart.data.datasets[0].backgroundColor[0] = memVal > 90 ? '#f44336' : (memVal > 70 ? '#ff9800' : '#4caf50');
        memChart.update();
    }

    // Network
    document.getElementById('netUp').innerText = data.Network.upload + '/s';
    document.getElementById('netDown').innerText = data.Network.download + '/s';

    // Disk
    document.getElementById('diskRead').innerText = data.DiskIo.read_rate + '/s';
    document.getElementById('diskWrite').innerText = data.DiskIo.write_rate + '/s';

    // Health
    const health = data.Health;
    const hEl = document.getElementById('healthScore');
    hEl.innerText = health.score;
    hEl.style.color = health.score > 80 ? '#4caf50' : (health.score > 50 ? '#ff9800' : '#f44336');
    document.getElementById('healthStatus').innerText = health.status;

    // Processes - with Kill button
    const tbody = document.querySelector('#procTable tbody');
    tbody.innerHTML = '';
    data.Processes.forEach(p => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${p.pid}</td>
            <td>${p.name}</td>
            <td>${p.cpu_percent.toFixed(1)}</td>
            <td>${p.memory_percent.toFixed(1)}</td>
            <td>${p.status}</td>
            <td><button class="btn-kill" onclick="killProcess(${p.pid}, '${p.name}')">Kill</button></td>
        `;
        tbody.appendChild(row);
    });

    // Alerts
    const alertList = document.getElementById('alertList');
    alertList.innerHTML = '';
    data.Alerts.forEach(a => {
        if (a) {
            const cls = a.Severity === 'CRITICAL' ? 'alert-critical' : 'alert-warning';
            const html = `<div class="alert-item ${cls}">
                <span class="alert-timestamp">${a.Timestamp}</span>
                <span class="alert-msg">${a.Message}</span>
            </div>`;
            alertList.innerHTML += html;
        }
    });

    // Services (New)
    const svcBody = document.querySelector('#serviceTable tbody');
    if (svcBody && data.Services) {
        svcBody.innerHTML = '';
        data.Services.forEach(s => {
            // Status: 4=Running, 1=Stopped, 2=StartPending, etc.
            const statusText = s.Status === 4 || s.Status === 'Running' ? 'Running' : 'Stopped';
            const color = statusText === 'Running' ? '#4caf50' : '#f44336';
            const row = `<tr>
                <td>${s.Name}</td>
                <td style="color:${color}">${statusText}</td>
                <td>${s.StartType}</td>
            </tr>`;
            svcBody.innerHTML += row;
        });
    }

    // Recommendations (Renamed to Insights)
    const recList = document.getElementById('recList');
    if (recList) {
        recList.innerHTML = '';
        // Handle both array and object
        let list = data.Insights || data.Recommendations || [];
        if (!Array.isArray(list)) list = Object.values(list);

        if (list.length > 0) {
            list.forEach(r => {
                const html = `<div class="alert-item" style="border-left: 3px solid #00bcd4;">
                    <span class="alert-msg">${r}</span>
                </div>`;
                recList.innerHTML += html;
            });
        } else {
            recList.innerHTML = '<div style="padding:10px; color:#4caf50;">✓ No active insights. System healthy.</div>';
        }
    }

    // Clean up old script tags
    const loader = document.getElementById('dataLoader');
    if (loader) {
        loader.remove();
    }
}

// Initial Load
document.addEventListener('DOMContentLoaded', () => {
    initCharts();

    // Polling loop to re-inject script tag
    setInterval(() => {
        const oldScript = document.getElementById('dynamicLoader');
        if (oldScript) oldScript.remove();

        const script = document.createElement('script');
        script.id = 'dynamicLoader';
        // Add random query param to prevent caching
        script.src = 'data.js?t=' + new Date().getTime();
        document.body.appendChild(script);
    }, 1000);
});
