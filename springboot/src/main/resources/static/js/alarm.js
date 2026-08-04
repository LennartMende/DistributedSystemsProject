let currentLeaderTempAlarmId = 0;
let currentLeaderVoltAlarmId = 0;
let currentFollowerTempAlarmId = 0;
let currentFollowerVoltAlarmId = 0;

let sumOfAlarms = 0;


export const alarmElementList = ".leader-temp-critical, .leader-temp-warn, .leader-volt-critical, \
                 .follower-temp-warn, .follower-temp-critical, .follower-volt-critical"

export const ALARM = {
    leader: {
        temp: {
            min: 5,
            warn: 50,
            alarm: 55
        },
        volt: {
            min: 4.5,
            max: 5.5
        }
    },
    follower: {
        temp: {
            min: 5,
            warn: 55,
            alarm: 60
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

    // leader temp
    if (leaderTemp != null) { 
        const leaderTempStatus = checkTempArray(leaderTemp, ALARM.leader.temp);
        //const wasInactive = !leaderTempAlarmElement.className;
        const wasInactive = currentLeaderTempAlarmId === 0;
        if (leaderTempStatus.tooLow) {
            leaderTempAlarmElement.innerText = "Temperature on leader is too low. Shutdown recommended.";
            if (leaderTempAlarmElement.className !== "leader-temp-critical") {
                leaderTempAlarmElement.className = "leader-temp-critical";
            }
            if (wasInactive) {
                // leaderTempAlarmElement.style.top = `${document.querySelectorAll(
                //     alarmElementList
                // ).length * 200 + 50}px`;
                //if (currentLeaderTempAlarmId === 0) {
                    sumOfAlarms += 1;
                    currentLeaderTempAlarmId = sumOfAlarms;
                    // setAlarmPositions(leaderTempAlarmElement,
                    //     leaderVoltAlarmElement,
                    //     followerTempAlarmElement,
                    //     followerVoltAlarmElement);
                    // console.log("currentLeaderTempAlarmId = ", currentLeaderTempAlarmId);
                    // console.log("sumOfAlarms = ", sumOfAlarms);
                //}
            }
        } else if (leaderTempStatus.warn) {
            leaderTempAlarmElement.innerText = "Temperature on leader is too high. Keep a watchful eye on it.";
            if (leaderTempAlarmElement.className !== "leader-temp-warn") {
                leaderTempAlarmElement.className = "leader-temp-warn";
            }
            if (wasInactive) {
                
                // leaderTempAlarmElement.style.top = `${document.querySelectorAll(
                //     alarmElementList
                // ).length * 200 + 50}px`;
                // if (currentLeaderTempAlarmId === 0) {
                    sumOfAlarms += 1;
                    currentLeaderTempAlarmId = sumOfAlarms;
                    // console.log("currentLeaderTempAlarmId = ", currentLeaderTempAlarmId);
                    // console.log("sumOfAlarms = ", sumOfAlarms);
                    // setAlarmPositions(leaderTempAlarmElement,
                    //     leaderVoltAlarmElement,
                    //     followerTempAlarmElement,
                    //     followerVoltAlarmElement);
                // }

            }
        } else if (leaderTempStatus.tooHigh) {
            leaderTempAlarmElement.innerText = "Temperature on leader is too high. Shutdown recommended.";
            if (leaderTempAlarmElement.className !== "leader-temp-critical") {
                leaderTempAlarmElement.className = "leader-temp-critical";
            }
            if (wasInactive) {
                // leaderTempAlarmElement.style.top = `${document.querySelectorAll(
                //     alarmElementList
                // ).length * 200 + 50}px`;
                // if (currentLeaderTempAlarmId === 0) {
                    sumOfAlarms += 1;
                    currentLeaderTempAlarmId = sumOfAlarms;
                    // console.log("currentLeaderTempAlarmId = ", currentLeaderTempAlarmId);
                    // console.log("sumOfAlarms = ", sumOfAlarms);
                    // setAlarmPositions(leaderTempAlarmElement,
                    //     leaderVoltAlarmElement,
                    //     followerTempAlarmElement,
                    //     followerVoltAlarmElement);
                // }
            }
        } else {
            leaderTempAlarmElement.innerText = "";
            leaderTempAlarmElement.className = "";
            leaderTempAlarmElement.style.top = "";
            if (currentLeaderTempAlarmId != 0) {
                currentLeaderTempAlarmId = 0;
            //     setAlarmPositions(leaderTempAlarmElement,
            //         leaderVoltAlarmElement,
            //         followerTempAlarmElement,
            //         followerVoltAlarmElement);
            }
        }
    } else {
        leaderTempAlarmElement.innerText = "";
        leaderTempAlarmElement.className = "";
        leaderTempAlarmElement.style.top = "";
    }
    
    // leader volt
    if (leaderVolt != null) {
        const leaderVoltStatus = checkVoltArray(leaderVolt, ALARM.leader.volt);
        //const wasInactive = !leaderVoltAlarmElement.className;
        const wasInactive = currentLeaderVoltAlarmId === 0;

        if (leaderVoltStatus.tooLow) {
            leaderVoltAlarmElement.innerText = "Voltage on leader is too low. Shutdown recommended. ";
            if (leaderVoltAlarmElement.className !== "leader-volt-critical") {
                leaderVoltAlarmElement.className = "leader-volt-critical";
            }
            if (wasInactive) {
                // leaderVoltAlarmElement.style.top = `${document.querySelectorAll(
                //     alarmElementList
                // ).length * 200 + 50}px`;
                // if (currentLeaderVoltAlarmId === 0) {
                    sumOfAlarms += 1;
                    currentLeaderVoltAlarmId = sumOfAlarms;
                    // console.log("currentLeaderVoltAlarmId = ", currentLeaderVoltAlarmId);
                    // console.log("sumOfAlarms = ", sumOfAlarms);
                    // setAlarmPositions(leaderTempAlarmElement,
                    //     leaderVoltAlarmElement,
                    //     followerTempAlarmElement,
                    //     followerVoltAlarmElement);
                // }
            }
        } else if (leaderVoltStatus.tooHigh) {
            leaderVoltAlarmElement.innerText = "Voltage on leader is too high. Shutdown recommended.";
            if (leaderVoltAlarmElement.className !== "leader-volt-critical") {
                leaderVoltAlarmElement.className = "leader-volt-critical";
            }
            if (wasInactive) {
                // leaderVoltAlarmElement.style.top = `${document.querySelectorAll(
                //     alarmElementList
                // ).length * 200 + 50}px`;
                // if (currentLeaderVoltAlarmId === 0) {
                    sumOfAlarms += 1;
                    currentLeaderVoltAlarmId = sumOfAlarms;
                    // console.log("currentLeaderVoltAlarmId = ", currentLeaderVoltAlarmId);
                    // console.log("sumOfAlarms = ", sumOfAlarms);
                    // setAlarmPositions(leaderTempAlarmElement,
                    //     leaderVoltAlarmElement,
                    //     followerTempAlarmElement,
                    //     followerVoltAlarmElement);
                // }
            }
        } else {
            leaderVoltAlarmElement.innerText = "";
            leaderVoltAlarmElement.className = "";
            leaderVoltAlarmElement.style.top = "";
            if (currentLeaderVoltAlarmId != 0) {
                currentLeaderVoltAlarmId = 0;
                // setAlarmPositions(leaderTempAlarmElement,
                //     leaderVoltAlarmElement,
                //     followerTempAlarmElement,
                //     followerVoltAlarmElement);
            }
        }
    } else {leaderVoltAlarmElement.innerText = "";
        leaderVoltAlarmElement.className = "";
        leaderVoltAlarmElement.style.top = "";
    }
    
    // follower temp
    if (followerTemp != null) {
        const followerTempStatus = checkTempArray(followerTemp, ALARM.follower.temp);
        //const wasInactive = !followerTempAlarmElement.className;
        const wasInactive = currentFollowerTempAlarmId === 0;

        if (followerTempStatus.tooLow) {
            followerTempAlarmElement.innerText = "Temperature on follower is too low. Shutdown recommended.";
            if (followerTempAlarmElement.className !== "follower-temp-critical") {
                followerTempAlarmElement.className = "follower-temp-critical";
            }
            if (wasInactive) {
                // followerTempAlarmElement.style.top = `${document.querySelectorAll(
                //     alarmElementList
                // ).length * 200 + 50}px`;
                // if (currentFollowerTempAlarmId === 0) {
                    sumOfAlarms += 1;
                    currentFollowerTempAlarmId = sumOfAlarms;
                    // console.log("currentFollowerTempAlarmId = ", currentFollowerTempAlarmId);
                    // console.log("sumOfAlarms = ", sumOfAlarms);
                    // setAlarmPositions(leaderTempAlarmElement,
                    //     leaderVoltAlarmElement,
                    //     followerTempAlarmElement,
                    //     followerVoltAlarmElement);
                // }
            }
        } else if (followerTempStatus.warn) {
            followerTempAlarmElement.innerText = "Temperature on follower is too high. Keep a watchful eye on it.";
            if (followerTempAlarmElement.className !== "follower-temp-warn") {
                followerTempAlarmElement.className = "follower-temp-warn";
            }
            if (wasInactive) {
                // followerTempAlarmElement.style.top = `${document.querySelectorAll(
                //     alarmElementList
                // ).length * 200 + 50}px`;
                // if (currentFollowerTempAlarmId === 0) {
                    sumOfAlarms += 1;
                    currentFollowerTempAlarmId = sumOfAlarms;
                    // console.log("currentFollowerTempAlarmId = ", currentFollowerTempAlarmId);
                    // console.log("sumOfAlarms = ", sumOfAlarms);
                    // setAlarmPositions(leaderTempAlarmElement,
                    //     leaderVoltAlarmElement,
                    //     followerTempAlarmElement,
                    //     followerVoltAlarmElement);
                // }
            }
        } else if (followerTempStatus.tooHigh) {
            followerTempAlarmElement.innerText = "Temperature on follower is too high. Shutdown recommended.";
            if (followerTempAlarmElement.className !== "follower-temp-critical") {
                followerTempAlarmElement.className = "follower-temp-critical";
            }
            if (wasInactive) {
                // followerTempAlarmElement.style.top = `${document.querySelectorAll(
                //     alarmElementList
                // ).length * 200 + 50}px`;
                // if (currentFollowerTempAlarmId === 0) {
                    sumOfAlarms += 1;
                    currentFollowerTempAlarmId = sumOfAlarms;
                    // console.log("currentFollowerTempAlarmId = ", currentFollowerTempAlarmId);
                    // console.log("sumOfAlarms = ", sumOfAlarms);
                    // setAlarmPositions(leaderTempAlarmElement,
                    //     leaderVoltAlarmElement,
                    //     followerTempAlarmElement,
                    //     followerVoltAlarmElement);
                // }
            }
        } else {
            followerTempAlarmElement.innerText = "";
            followerTempAlarmElement.className = "";
            // if (wasInactive) { // THIS  LINE AND NEXT 4 LINES ARE OLD CODE
            //     followerTempAlarmElement.style.top = `${document.querySelectorAll(
            //         alarmElementList
            //     ).length * 200 + 50}px`;
            // }
            followerTempAlarmElement.style.top = "";
            if (currentFollowerTempAlarmId != 0) {
                currentFollowerTempAlarmId = 0;
                // setAlarmPositions(leaderTempAlarmElement,
                //     leaderVoltAlarmElement,
                //     followerTempAlarmElement,
                //     followerVoltAlarmElement);
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
        //const wasInactive = !followerVoltAlarmElement.className;
        const wasInactive = currentFollowerVoltAlarmId === 0;

        if (followerVoltStatus.tooLow) {
            followerVoltAlarmElement.innerText = "Voltage on follower is too low. Shutdown recommended.";
            if (followerVoltAlarmElement.className !== "follower-volt-critical") {
                followerVoltAlarmElement.className = "follower-volt-critical";
            }
            if (wasInactive) {
                // followerVoltAlarmElement.style.top = `${document.querySelectorAll(
                //     alarmElementList
                // ).length * 200 + 50}px`;
                if (currentFollowerVoltAlarmId === 0) {
                    sumOfAlarms += 1;
                    currentFollowerVoltAlarmId = sumOfAlarms;
                    // setAlarmPositions(leaderTempAlarmElement,
                    // leaderVoltAlarmElement,
                    // followerTempAlarmElement,
                    // followerVoltAlarmElement);
                    // console.log("currentFollowerVoltAlarmId = ", currentFollowerVoltAlarmId);
                    // console.log("sumOfAlarms = ", sumOfAlarms);
                }
            }
        } else if (followerVoltStatus.tooHigh) {
            followerVoltAlarmElement.innerText = "Voltage on follower is too high. Shutdown recommended.";
            if (followerVoltAlarmElement.className !== "follower-volt-critical") {
                followerVoltAlarmElement.className = "follower-volt-critical";
            }
            if (wasInactive) {
                
                // followerVoltAlarmElement.style.top = `${document.querySelectorAll(
                //     alarmElementList
                // ).length * 200 + 50}px`;
                if (currentFollowerVoltAlarmId === 0) {
                    sumOfAlarms += 1;
                    currentFollowerVoltAlarmId = sumOfAlarms;
                    // setAlarmPositions(leaderTempAlarmElement,
                    // leaderVoltAlarmElement,
                    // followerTempAlarmElement,
                    // followerVoltAlarmElement);
                    // console.log("currentFollowerVoltAlarmId = ", currentFollowerVoltAlarmId);
                    // console.log("sumOfAlarms = ", sumOfAlarms);
                }
            }
        } else {
            followerVoltAlarmElement.innerText = "";
            followerVoltAlarmElement.className = "";
            // if (wasInactive) { // THIS  LINE AND NEXT 4 LINES ARE OLD CODE
            //     followerVoltAlarmElement.style.top = `${document.querySelectorAll(
            //         alarmElementList
            //     ).length * 200 + 50}px`;
            // }
            followerVoltAlarmElement.style.top = "";
            if (currentFollowerVoltAlarmId != 0) {
                currentFollowerVoltAlarmId = 0;
                // setAlarmPositions(leaderTempAlarmElement,
                //     leaderVoltAlarmElement,
                //     followerTempAlarmElement,
                //     followerVoltAlarmElement);
            }
        }
    } else {
        followerVoltAlarmElement.innerText = "";
        followerVoltAlarmElement.className = "";
        followerVoltAlarmElement.style.top = "";
    }
    setAlarmPositions(leaderTempAlarmElement,
        leaderVoltAlarmElement,
        followerTempAlarmElement,
        followerVoltAlarmElement);
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


function setAlarmPositions(leaderTempAlarmElement,
    leaderVoltAlarmElement,
    followerTempAlarmElement,
    followerVoltAlarmElement) {
    // console.log("setAlarmPositions()");
    [
        leaderTempAlarmElement,
        leaderVoltAlarmElement,
        followerTempAlarmElement,
        followerVoltAlarmElement
    ].forEach(e => {
        e.style.display = "none";
        e.style.top = "";
    });
    const alarms = [
        {id: currentLeaderTempAlarmId, element: leaderTempAlarmElement},
        {id: currentLeaderVoltAlarmId, element: leaderVoltAlarmElement},
        {id: currentFollowerTempAlarmId, element: followerTempAlarmElement},
        {id: currentFollowerVoltAlarmId, element: followerVoltAlarmElement}
    ];
    // console.log([
    //     { name: "leaderTemp", id: currentLeaderTempAlarmId },
    //     { name: "leaderVolt", id: currentLeaderVoltAlarmId },
    //     { name: "followerTemp", id: currentFollowerTempAlarmId },
    //     { name: "followerVolt", id: currentFollowerVoltAlarmId },
    // ]);

    // DEBUG:
    // console.log(
    //     leaderTempAlarmElement,
    //     leaderVoltAlarmElement,
    //     followerTempAlarmElement,
    //     followerVoltAlarmElement
    // );
    const activeAlarms = alarms.filter(a => a.id !== 0);
    activeAlarms.sort((a, b) => b.id - a.id);
    for (let i = 0; i < activeAlarms.length; i++) {
        if (i < 4) {
            activeAlarms[i].element.style.top = `${500 + i * 80}px`;
            activeAlarms[i].element.style.display = "block";
        } else {
            activeAlarms[i].element.innerText = "";
            activeAlarms[i].element.className = "";
            activeAlarms[i].element.style.top = "";
            activeAlarms[i].element.style.display = "none";
        }
    }
    // console.log("activeAlarms.length = ", activeAlarms.length);
}
