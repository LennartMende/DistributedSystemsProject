const leaderMsElement = document.getElementById("leaderMachineState");
//const followerMsElement = document.getElementById("followerMachineState");

// positions
leaderPosElements = [document.getElementById("leader_pos_joint0"), document.getElementById("leader_pos_joint1"),
    document.getElementById("leader_pos_joint2"), document.getElementById("leader_pos_joint3"),
    document.getElementById("leader_pos_joint4"), document.getElementById("leader_pos_joint5")
];

followerPosElements = [document.getElementById("follower_pos_joint0"), document.getElementById("follower_pos_joint1"),
    document.getElementById("follower_pos_joint2"), document.getElementById("follower_pos_joint3"),
    document.getElementById("follower_pos_joint4"), document.getElementById("follower_pos_joint5")
];

// temperatures
leaderTempElements = [document.getElementById("leader_temp_joint0"), document.getElementById("leader_temp_joint1"),
    document.getElementById("leader_temp_joint2"), document.getElementById("leader_temp_joint3"),
    document.getElementById("leader_temp_joint4"), document.getElementById("leader_temp_joint5")
];

followerTempElements = [document.getElementById("follower_temp_joint0"), document.getElementById("follower_temp_joint1"),
    document.getElementById("follower_temp_joint2"), document.getElementById("follower_temp_joint3"),
    document.getElementById("follower_temp_joint4"), document.getElementById("follower_temp_joint5")
];

// voltages
leaderVoltElements = [document.getElementById("leader_volt_joint0"), document.getElementById("leader_volt_joint1"),
    document.getElementById("leader_volt_joint2"), document.getElementById("leader_volt_joint3"),
    document.getElementById("leader_volt_joint4"), document.getElementById("leader_volt_joint5")
];

followerVoltElements = [document.getElementById("follower_volt_joint0"), document.getElementById("follower_volt_joint1"),
    document.getElementById("follower_volt_joint2"), document.getElementById("follower_volt_joint3"),
    document.getElementById("follower_volt_joint4"), document.getElementById("follower_volt_joint5")
];

async function update() {
    try {
        const leaderState = await fetch(`/api/robot/leader/state`).then(r => r.json());
        const followerState = await fetch(`/api/robot/follower/state`).then(r => r.json());

        // Machine state anzeigen
        updateMachineState(leaderMsElement, leaderState)
        //updateMachineState(followerMsElement, followerState)

        // Leader Werte
        updateElements(leaderPosElements, leaderState.pos);
        updateElements(leaderTempElements, leaderState.temp);
        updateElements(leaderVoltElements, leaderState.volt);

        // Follower Werte
        updateElements(followerPosElements, followerState.pos);
        updateElements(followerTempElements, followerState.temp);
        updateElements(followerVoltElements, followerState.volt);

    } catch (err) {
        console.error("Fetch error:", err);
    }
}

function updateMachineState(msElement, state) {
    if (!msElement || !state.machineState || state.machineState==="UNKNOWN") {
        msElement.innerText = "STATUS UNKNOWN";
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

//updateMachineState(leaderMsElement, "UNKNOWN")
update();               // einmaliger Start
update();
setInterval(update, 400);  // alle 400 ms aktualisieren