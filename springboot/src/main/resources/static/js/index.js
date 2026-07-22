leaderTempAlarmElement = document.getElementById("leaderTempAlarm");
leaderVoltAlarmElement = document.getElementById("leaderVoltAlarm");
followerTempAlarmElement = document.getElementById("followerTempAlarm");
followerVoltAlarmElement = document.getElementById("followerVoltAlarm");

alarmElementList = ".leader-temp-critical, .leader-temp-warn, .leader-volt-critical, \
                .follower-temp-warn, .follower-temp-critical, .follower-volt-critical"

const ALARM = {
    leader: {
        temp: {
            min: 20,
            warn: 33,
            alarm: 35
        },
        volt: {
            min: 4.5,
            max: 5.5
        }
    },
    follower: {
        temp: {
            min: 20,
            warn: 38,
            alarm: 40
        },
        volt: {
            min: 11.5,
            max: 12.5
        }
    }
};

TEMP_ALARM_TEXT = "There could be an issue with the power supply, the motor or the temperature sensor. "
VOLT_ALARM_TEXT = "There could be an issue with the power supply, the motor or the voltage sensor. "


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

        set_alarms(leaderState.temp, followerState.temp, leaderState.volt, followerState.volt)
        // Machine state anzeigen
        updateMachineState(leaderMsElement, leaderState)
        //updateMachineState(followerMsElement, followerState)

        updateElementValuesAndColors(leaderState, followerState);
    } catch (err) {
        console.error("Fetch error:", err);
    }
}

function set_alarms(leaderTemp, followerTemp, leaderVolt, followerVolt) {
    // DEBUG:
    console.log("leaderTemp = ", leaderTemp, ", followerTemp = ", followerTemp,
         ", leaderVolt = ", leaderVolt, ", followerVolt = ", followerVolt);

    // leader temp
    if (leaderTemp != null) { 
        const leaderTempStatus = checkTempArray(leaderTemp, ALARM.leader.temp);
        const wasInactive = !leaderTempAlarmElement.className;
        if (leaderTempStatus.tooLow) {
            leaderTempAlarmElement.innerText = "Temperature on leader is too low. Shutdown recommended.";
            leaderTempAlarmElement.className = "leader-temp-critical";
            if (wasInactive) {
                leaderTempAlarmElement.style.top = `${document.querySelectorAll(
                    alarmElementList
                ).length * 200 + 50}px`;
            }
        } else if (leaderTempStatus.warn) {
            leaderTempAlarmElement.innerText = "Temperature on leader is too high. Keep a watchful eye on the temperature.";
            leaderTempAlarmElement.className = "leader-temp-warn";
            if (wasInactive) {
                leaderTempAlarmElement.style.top = `${document.querySelectorAll(
                    alarmElementList
                ).length * 200 + 50}px`;
            }
        } else if (leaderTempStatus.tooHigh) {
            leaderTempAlarmElement.innerText = "Temperature on leader is too high. Shutdown recommended.";
            leaderTempAlarmElement.className = "leader-temp-critical";
            if (wasInactive) {
                leaderTempAlarmElement.style.top = `${document.querySelectorAll(
                    alarmElementList
                ).length * 200 + 50}px`;
            }
        } else {
            leaderTempAlarmElement.innerText = "";
            leaderTempAlarmElement.className = "";
            leaderTempAlarmElement.style.top = "";
        }
    } else {
        leaderTempAlarmElement.innerText = "";
        leaderTempAlarmElement.className = "";
        leaderTempAlarmElement.style.top = "";
    }
    
    // leader volt
    if (leaderVolt != null) {
        const leaderVoltStatus = checkVoltArray(leaderVolt, ALARM.leader.volt);
        const wasInactive = !leaderVoltAlarmElement.className;
        if (leaderVoltStatus.tooLow) {
            leaderVoltAlarmElement.innerText = "Voltage on leader is too low. Shutdown recommended. ";
            leaderVoltAlarmElement.className = "leader-volt-critical";
            if (wasInactive) {
                leaderVoltAlarmElement.style.top = `${document.querySelectorAll(
                    alarmElementList
                ).length * 200 + 50}px`;
            }
        } else if (leaderVoltStatus.tooHigh) {
            leaderVoltAlarmElement.innerText = "Voltage on leader is too high. Shutdown recommended.";
            leaderVoltAlarmElement.className = "leader-volt-critical";
            if (wasInactive) {
                leaderVoltAlarmElement.style.top = `${document.querySelectorAll(
                    alarmElementList
                ).length * 200 + 50}px`;
            }
        } else {
            leaderVoltAlarmElement.innerText = "";
            leaderVoltAlarmElement.className = "";
            leaderVoltAlarmElement.style.top = "";
        }
    } else {leaderVoltAlarmElement.innerText = "";
        leaderVoltAlarmElement.className = "";
        leaderVoltAlarmElement.style.top = "";
    }
    
    // follower temp
    if (followerTemp != null) {
        const followerTempStatus = checkTempArray(followerTemp, ALARM.follower.temp);
        const wasInactive = !followerTempAlarmElement.className;
        if (followerTempStatus.tooLow) {
            followerTempAlarmElement.innerText = "Temperature on follower is too low. Shutdown recommended.";
            followerTempAlarmElement.className = "follower-temp-critical";
            if (wasInactive) {
                followerTempAlarmElement.style.top = `${document.querySelectorAll(
                    alarmElementList
                ).length * 200 + 50}px`;
            }
        } else if (followerTempStatus.warn) {
            followerTempAlarmElement.innerText = "Temperature on follower is too high. Keep a watchful eye on the temperature.";
            followerTempAlarmElement.className = "follower-temp-warn";
            if (wasInactive) {
                followerTempAlarmElement.style.top = `${document.querySelectorAll(
                    alarmElementList
                ).length * 200 + 50}px`;
            }
        } else if (followerTempStatus.tooHigh) {
            followerTempAlarmElement.innerText = "Temperature on follower is too high. Shutdown recommended.";
            followerTempAlarmElement.className = "follower-temp-critical";
            if (wasInactive) {
                followerTempAlarmElement.style.top = `${document.querySelectorAll(
                    alarmElementList
                ).length * 200 + 50}px`;
            }
        } else {
            followerTempAlarmElement.innerText = "";
            followerTempAlarmElement.className = "";
            if (wasInactive) {
                followerTempAlarmElement.style.top = `${document.querySelectorAll(
                    alarmElementList
                ).length * 200 + 50}px`;
            }
        }
    } else {
        followerTempAlarmElement.innerText = "";
        followerTempAlarmElement.className = "";
        followerTempAlarmElement.style.top = "";
    }

    // follower volt
    if (followerVolt != null) {
        const followerVoltStatus = checkVoltArray(followerVolt, ALARM.follower.volt);
        const wasInactive = !followerVoltAlarmElement.className;
        if (followerVoltStatus.tooLow) {
            followerVoltAlarmElement.innerText = "Voltage on follower is too low. Shutdown recommended.";
            followerVoltAlarmElement.className = "follower-volt-critical";
            if (wasInactive) {
                followerVoltAlarmElement.style.top = `${document.querySelectorAll(
                    alarmElementList
                ).length * 200 + 50}px`;
            }
        } else if (followerVoltStatus.tooHigh) {
            followerVoltAlarmElement.innerText = "Voltage on follower is too high. Shutdown recommended.";
            followerVoltAlarmElement.className = "follower-volt-critical";
            if (wasInactive) {
                followerVoltAlarmElement.style.top = `${document.querySelectorAll(
                    alarmElementList
                ).length * 200 + 50}px`;
            }
        } else {
            followerVoltAlarmElement.innerText = "";
            followerVoltAlarmElement.className = "";
            if (wasInactive) {
                followerVoltAlarmElement.style.top = `${document.querySelectorAll(
                    alarmElementList
                ).length * 200 + 50}px`;
            }
        }
    } else {
        followerVoltAlarmElement.innerText = "";
        followerVoltAlarmElement.className = "";
        followerVoltAlarmElement.style.top = "";
    }
}

function checkTempArray(tempArray, thresholds) {
    let tooLow = false;
    let warn = false;
    let tooHigh = false;

    tempArray.forEach(temp => {
        if (temp < thresholds.min) {
            tooLow = true;
        } else if (temp > thresholds.alarm) {
            tooHigh = true;
        } else if (temp > thresholds.warn) {
            warn = true;
        }
    });

    return { tooLow, warn, tooHigh };
}

function checkVoltArray(voltArray, thresholds) {
    let tooLow = false;
    let tooHigh = false;

    voltArray.forEach(volt => {
        if (volt < thresholds.min) tooLow = true;
        if (volt > thresholds.max) tooHigh = true;
    });

    return { tooLow, tooHigh };
}

function markLeaderTemps() {
    elements.forEach((element, index) => {
        if (element) {
            element.innerText = values && values[index] !== undefined ? values[index] : "-";
        }
    });
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