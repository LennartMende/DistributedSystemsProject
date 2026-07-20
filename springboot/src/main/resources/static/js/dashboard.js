// ---------------------------------------------------------
// 1. Initialisierung
// ---------------------------------------------------------

const msElement = document.getElementById("machineState");
const posElement = document.getElementById("positions");
const velsElement = document.getElementById("vels");

const ctx = document.getElementById('posChart').getContext('2d');
const posChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Joint 0 Position',
            data: [],
            borderColor: '#3182ce',
            borderWidth: 2,
            tension: 0.2
        }]
    },
    options: {
        animation: false,
        scales: {
            x: { title: { display: true, text: 'time' }},
            y: { title: { display: true, text: 'angle' }}
        }
    }
});


// ---------------------------------------------------------
// 2. Funktionen
// ---------------------------------------------------------

async function update() {
    try {
        const state = await fetch("/api/robot/leader/state").then(r => r.json());
        const history = await fetch("/api/robot/leader/posList").then(r => r.json());

        // Machine state
        msElement.innerText = state.machineState;

        if (state.machineState === "RUNNING") {
            msElement.className = "value status-running";
        } else if (state.machineState === "READY") {
            msElement.className = "value status-ready";
        } else if (state.machineState === "STOPPED") {
            msElement.className = "value status-stopped";
        } else {
            msElement.className = "value status-error";
        }

        // Positions
        posElement.innerText = state.pos ? state.pos.join(", ") : "-";

        // Velocities
        velsElement.innerText = state.vels ? state.vels.join(", ") : "-";

        // Chart update
        const joint0 = history.map(h => h[0]);
        posChart.data.labels = joint0.map((_, i) => i);
        posChart.data.datasets[0].data = joint0;
        posChart.update();

    } catch (err) {
        console.error("Fetch error:", err);
    }
}


// ---------------------------------------------------------
// 3. Startlogik
// ---------------------------------------------------------

update();               // einmaliger Start
setInterval(update, 400);  // alle 400 ms aktualisieren
