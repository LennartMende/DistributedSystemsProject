export const alarmElementList = ".leader-temp-critical, .leader-temp-warn, .leader-volt-critical, \
                 .follower-temp-warn, .follower-temp-critical, .follower-volt-critical"

export const ALARM = {
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

export const TEMP_ALARM_TEXT =
    "There could be an issue with the power supply, the motor or the temperature sensor.";

export const VOLT_ALARM_TEXT =
    "There could be an issue with the power supply, the motor or the voltage sensor.";

export function set_alarms(leaderTemp, followerTemp, leaderVolt, followerVolt) {
    const leaderTempAlarmElement = document.getElementById("leaderTempAlarm");
    const leaderVoltAlarmElement = document.getElementById("leaderVoltAlarm");
    const followerTempAlarmElement = document.getElementById("followerTempAlarm");
    const followerVoltAlarmElement = document.getElementById("followerVoltAlarm");
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

export function checkTempArray(tempArray, thresholds) {
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

export function checkVoltArray(voltArray, thresholds) {
    let tooLow = false;
    let tooHigh = false;

    voltArray.forEach(volt => {
        if (volt < thresholds.min) tooLow = true;
        if (volt > thresholds.max) tooHigh = true;
    });

    return { tooLow, tooHigh };
}