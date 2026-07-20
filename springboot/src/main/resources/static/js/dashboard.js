// ---------------------------------------------------------
// 1. Initialisierung
// ---------------------------------------------------------
let currentJoint = 0;
let currentArm = "leader";   // "leader" oder "follower"

const leaderMsElement = document.getElementById("leaderMachineState");
const followerMsElement = document.getElementById("followerMachineState");
const leaderPosElement = document.getElementById("leaderPositions");
const leaderVelsElement = document.getElementById("leaderVels");
const followerPosElement = document.getElementById("followerPositions");
const followerVelsElement = document.getElementById("followerVels");

const ctx = document.getElementById('posChart').getContext('2d');
const posChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [
            {
                label: 'Leader Joint Position',
                data: [],
                borderColor: '#3182ce',
                borderWidth: 2,
                tension: 0.2
            },
            {
                label: 'Follower Joint Position',
                data: [],
                borderColor: '#e53e3e',
                borderWidth: 2,
                tension: 0.2
            }
        ]
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
        const leaderState = await fetch(`/api/robot/leader/state`).then(r => r.json());
        const followerState = await fetch(`/api/robot/follower/state`).then(r => r.json());
        const leaderHistory = await fetch(`/api/robot/leader/posList`).then(r => r.json());
        const followerHistory = await fetch(`/api/robot/follower/posList`).then(r => r.json());

        // Machine state anzeigen
        updateMachineState(leaderMsElement, leaderState)
        updateMachineState(followerMsElement, followerState)
        // leaderMsElement.innerText = leaderState.machineState;

        // if (state.machineState === "RUNNING") {
        //     msElement.className = "value status-running";
        // } else if (state.machineState === "READY") {
        //     msElement.className = "value status-ready";
        // } else if (state.machineState === "STOPPED") {
        //     msElement.className = "value status-stopped";
        // } else {
        //     msElement.className = "value status-error";
        // }

        // Leader Werte
        leaderPosElement.innerText = leaderState.pos ? leaderState.pos.join(", ") : "-";
        leaderVelsElement.innerText = leaderState.vels ? leaderState.vels.join(", ") : "-";

        // Follower Werte
        followerPosElement.innerText = followerState.pos ? followerState.pos.join(", ") : "-";
        followerVelsElement.innerText = followerState.vels ? followerState.vels.join(", ") : "-";

        // Chart update
        const leaderJointValues = leaderHistory.map(h => h[currentJoint]);
        const followerJointValues = followerHistory.map(h => h[currentJoint]);

        // Labels nur einmal setzen
        posChart.data.labels = leaderJointValues.map((_, i) => i);

        // Beide Kurven setzen
        posChart.data.datasets[0].data = leaderJointValues;
        posChart.data.datasets[1].data = followerJointValues;

        posChart.update();

    } catch (err) {
        console.error("Fetch error:", err);
    }
}

function updateMachineState(msElement, state) {
    // Machine state anzeigen
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
}

function selectJoint(jointIndex) {
    currentJoint = jointIndex;
    
    // Alle Buttons zurücksetzen
    const buttons = document.querySelectorAll(".joint-button-clicked");
    buttons.forEach(btn => {
        btn.classList.remove("joint-button-clicked");
        btn.classList.add("joint-button");
    });

    // Geklickten Button aktiv setzen
    const active = document.getElementById("joint" + jointIndex);
    active.classList.remove("joint-button");
    active.classList.add("joint-button-clicked");

    // Chart-Titel aktualisieren
    document.getElementById("chartTitle").innerText =
        `Live Tracking (Joint ${currentJoint})`;

    // Dataset-Labels aktualisieren
    posChart.data.datasets[0].label = `Leader joint ${currentJoint} position`;
    posChart.data.datasets[1].label = `Follower joint ${currentJoint} position`;
}

function selectArm(arm) {
    currentArm = arm;

    // Alle Buttons zurücksetzen
    const buttons = document.querySelectorAll(".arm-switch-button, .arm-switch-button-clicked");
    buttons.forEach(btn => {
        btn.classList.remove("arm-switch-button-clicked");
        btn.classList.add("arm-switch-button");
    });

    // Geklickten Button aktiv setzen
    const active = document.getElementById(arm);
    active.classList.remove("arm-switch-button");
    active.classList.add("arm-switch-button-clicked");

}


// ---------------------------------------------------------
// 3. Startlogik
// ---------------------------------------------------------

update();               // einmaliger Start
setInterval(update, 400);  // alle 400 ms aktualisieren
