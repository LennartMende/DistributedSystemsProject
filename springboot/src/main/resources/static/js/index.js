import {
    set_alarms,
} from "./alarm.js";


const leaderMsElement = document.getElementById("leaderMachineState");

// positions
const leaderPosElements = [document.getElementById("leader_pos_joint0"), document.getElementById("leader_pos_joint1"),
    document.getElementById("leader_pos_joint2"), document.getElementById("leader_pos_joint3"),
    document.getElementById("leader_pos_joint4"), document.getElementById("leader_pos_joint5")
];

const followerPosElements = [document.getElementById("follower_pos_joint0"), document.getElementById("follower_pos_joint1"),
    document.getElementById("follower_pos_joint2"), document.getElementById("follower_pos_joint3"),
    document.getElementById("follower_pos_joint4"), document.getElementById("follower_pos_joint5")
];

// temperatures
const leaderTempElements = [document.getElementById("leader_temp_joint0"), document.getElementById("leader_temp_joint1"),
    document.getElementById("leader_temp_joint2"), document.getElementById("leader_temp_joint3"),
    document.getElementById("leader_temp_joint4"), document.getElementById("leader_temp_joint5")
];

const followerTempElements = [document.getElementById("follower_temp_joint0"), document.getElementById("follower_temp_joint1"),
    document.getElementById("follower_temp_joint2"), document.getElementById("follower_temp_joint3"),
    document.getElementById("follower_temp_joint4"), document.getElementById("follower_temp_joint5")
];

// voltages
const leaderVoltElements = [document.getElementById("leader_volt_joint0"), document.getElementById("leader_volt_joint1"),
    document.getElementById("leader_volt_joint2"), document.getElementById("leader_volt_joint3"),
    document.getElementById("leader_volt_joint4"), document.getElementById("leader_volt_joint5")
];

const followerVoltElements = [document.getElementById("follower_volt_joint0"), document.getElementById("follower_volt_joint1"),
    document.getElementById("follower_volt_joint2"), document.getElementById("follower_volt_joint3"),
    document.getElementById("follower_volt_joint4"), document.getElementById("follower_volt_joint5")
];

async function update() {
    try {
        const leaderState = await fetch(`/api/robot/leader/state`).then(r => r.json());
        const followerState = await fetch(`/api/robot/follower/state`).then(r => r.json());

        set_alarms(leaderState.temp, followerState.temp, leaderState.volt, followerState.volt)
        // Machine state anzeigen
        updateMachineState(leaderMsElement, leaderState)
        //updateMachineState(followerMsElement, followerState)

        updateElementValuesAndColors(leaderState, followerState);
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

function updateLeaderTempElements(values) {
    if (!values) return;

    leaderTempElements.forEach((element, index) => {
        const v = values[index];
        if (v < ALARM.leader.temp.min) {
            element.style.color = "#ff0000";
        } else if (v > ALARM.leader.temp.alarm) {
            element.style.color = "#ff0000";
        } else if (v > ALARM.leader.temp.warn) {
            element.style.color = "#fff700";
        } else {
            element.style.color = "";
        }
    });
}

function updateLeaderVoltElements(values) {
    if (!values) return;

    leaderVoltElements.forEach((element, index) => {
        const v = values[index];
        if (v < ALARM.leader.volt.min) {
            element.style.color = "#ff0000";
        } else if (v > ALARM.leader.volt.max) {
            element.style.color = "#ff0000";
        } else {
            element.style.color = "";
        }
    });
}

function updateFollowerTempElements(values) {
    if (!values) return;

    followerTempElements.forEach((element, index) => {
        const v = values[index];
        if (v < ALARM.follower.temp.min) {
            element.style.color = "#ff0000";
        } else if (v > ALARM.follower.temp.alarm) {
            element.style.color = "#ff0000";
        } else if (v > ALARM.follower.temp.warn) {
            element.style.color = "#fff700";
        } else {
            element.style.color = "";
        }
    });
}

function updateFollowerVoltElements(values) {
    if (!values) return;

    followerVoltElements.forEach((element, index) => {
        const v = values[index];
        if (v < ALARM.follower.volt.min) {
            element.style.color = "#ff0000";
        } else if (v > ALARM.follower.volt.max) {
            element.style.color = "#ff0000";
        } else {
            element.style.color = "";
        }
    });
}

function updateElements(elements, values) {
    if (!elements) {
        return;
    }

    elements.forEach((element, index) => {
        if (element) {
            element.innerText = values && values[index] !== undefined ? values[index] : "-";
        }
    });
}

function updateElementValuesAndColors(leaderState, followerState) {

    // Werte aktualisieren
    updateElements(leaderPosElements, leaderState.pos);
    updateElements(followerPosElements, followerState.pos);

    updateElements(leaderTempElements, leaderState.temp);
    updateElements(leaderVoltElements, leaderState.volt);
    updateElements(followerTempElements, followerState.temp);
    updateElements(followerVoltElements, followerState.volt);

    // Farben aktualisieren
    updateLeaderTempElements(leaderState.temp);
    updateLeaderVoltElements(leaderState.volt);
    updateFollowerTempElements(followerState.temp);
    updateFollowerVoltElements(followerState.volt);
}


//updateMachineState(leaderMsElement, "UNKNOWN")
update();               // einmaliger Start
setInterval(update, 400);  // alle 400 ms aktualisieren