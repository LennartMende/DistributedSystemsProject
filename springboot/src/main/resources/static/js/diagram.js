// ---------------------------------------------------------
// 0. Imports
// ---------------------------------------------------------
import {
    set_alarms,
} from "./alarm.js";

// ---------------------------------------------------------
// 1. Initialisierung
// ---------------------------------------------------------
const leaderMsElement = document.getElementById("leaderMachineState");
let currentJoint = 0;
let currentArm = "leader";   // "leader" oder "follower"

const chartCanvas = document.getElementById('posChart');
const chartTitle = document.getElementById('chartTitle');
let posChart = null;

if (chartCanvas && typeof Chart !== 'undefined') {
    const ctx = chartCanvas.getContext('2d');
    posChart = new Chart(ctx, {
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
                x: {
                    type: 'linear',
                    title: {
                        display: true,
                        text: 'time'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'angle'
                    }
                }
            }
        }
    });
} else {
    console.error('Chart could not be initialized. The canvas or Chart.js is missing.');
}


// ---------------------------------------------------------
// 2. Funktionen
// ---------------------------------------------------------

async function update() {
    if (!posChart) {
        return;
    }

    try {
        const leaderState = await fetch(`/api/robot/leader/state`).then(r => r.json());
        const followerState = await fetch(`/api/robot/follower/state`).then(r => r.json());

        const leaderHistory = await fetch(`/api/robot/leader/posList`).then(r => r.json());
        const followerHistory = await fetch(`/api/robot/follower/posList`).then(r => r.json())

        const timeStamps = await fetch(`/api/robot/timeStampsList`).then(r => r.json());

        const leaderJointValues = leaderHistory.map(h => h[currentJoint]);
        const followerJointValues = followerHistory.map(h => h[currentJoint]);

        console.log(timeStamps);
        console.log(leaderJointValues.length);
        console.log(timeStamps.length);

        set_alarms(leaderState.temp, followerState.temp, leaderState.volt, followerState.volt)

        // Machine state anzeigen
        updateMachineState(leaderMsElement, leaderState)
        //updateMachineState(followerMsElement, followerState)

        // Chart update
        

        

        // Beide Kurven setzen
        posChart.data.datasets[0].data = leaderHistory.map((h, i) => ({
            x: timeStamps[i],
            y: h[currentJoint]
        }));

        posChart.data.datasets[1].data = followerHistory.map((h, i) => ({
            x: timeStamps[i],
            y: h[currentJoint]
        }));

        posChart.update();

    } catch (err) {
        console.error("Fetch error:", err);
    }
}

function updateMachineState(msElement, state) {
    if (!msElement || !state.machineState || state.machineState==="UNKNOWN") {
        msElement.innerText = "STATE UNKNOWN";
        msElement.className = "value status-unknown";
        return;
    }

    msElement.innerText = state.machineState;

    console.log("machineState =", state.machineState);

    if (state.machineState === "RUNNING") {
        msElement.className = "value status-running";
    } else if (state.machineState === "READY") {
        msElement.className = "value status-ready";
    } else if (state.machineState === "STOPPED") {
        msElement.className = "value status-stopped";
    } else {
        msElement.innerText = "ERROR";
        msElement.className = "value status-error";
    }
}

function selectJoint(jointIndex) {
    if (!posChart) {
        return;
    }

    currentJoint = jointIndex;
    
    // Alle Buttons zurücksetzen
    const buttons = document.querySelectorAll(".joint-button-clicked");
    buttons.forEach(btn => {
        btn.classList.remove("joint-button-clicked");
        btn.classList.add("joint-button");
    });

    // Geklickten Button aktiv setzen
    const active = document.getElementById("joint" + jointIndex);
    if (active) {
        active.classList.remove("joint-button");
        active.classList.add("joint-button-clicked");
    }

    // Chart-Titel aktualisieren
    if (chartTitle) {
        chartTitle.innerText = `Live Tracking (Joint ${currentJoint})`;
    }

    // Dataset-Labels aktualisieren
    posChart.data.datasets[0].label = `Leader joint ${currentJoint} position`;
    posChart.data.datasets[1].label = `Follower joint ${currentJoint} position`;
}

document.getElementById("joint0").addEventListener("click", () => selectJoint(0));
document.getElementById("joint1").addEventListener("click", () => selectJoint(1));
document.getElementById("joint2").addEventListener("click", () => selectJoint(2));
document.getElementById("joint3").addEventListener("click", () => selectJoint(3));
document.getElementById("joint4").addEventListener("click", () => selectJoint(4));
document.getElementById("joint5").addEventListener("click", () => selectJoint(5));

// ---------------------------------------------------------
// 3. Startlogik
// ---------------------------------------------------------

update();               // einmaliger Start
setInterval(update, 400);  // alle 400 ms aktualisieren
