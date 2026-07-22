leaderTempAlarmElement = document.getElementById("leaderTempAlarm");
leaderVoltAlarmElement = document.getElementById("leaderVoltAlarm");
followerTempAlarmElement = document.getElementById("followerTempAlarm");
followerVoltAlarmElement = document.getElementById("followerVoltAlarm");

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

export function set_alarms(leaderTemp, followerTemp, leaderVolt, followerVolt) {
    // DEBUG:
    console.log("leaderTemp = ", leaderTemp, ", followerTemp = ", followerTemp,
         ", leaderVolt = ", leaderVolt, ", followerVolt = ", followerVolt);

    // leader temp
    if (leaderTemp < ALARM.leader.temp.min) {
        leaderTempAlarmElement.innerText = "Temperature is too low. " + TEMP_ALARM_TEXT + "Shutdown recommended.";
    } else if (leaderTemp > ALARM.leader.temp.warn) {
        leaderTempAlarmElement.innerText = "Temperature is too high. " + TEMP_ALARM_TEXT + 
            "Keep a watchful eye on the temperature.";
    } else if (leaderTempAlarmElement > ALARM.leader.temp.alarm) {
        leaderVoltAlarmElement.innerText = "Temperature is too high." + TEMP_ALARM_TEXT + "Shutdown recommended.";
    }

    // leader volt
    if (leaderVolt < ALARM.leader.volt.min) {
        leaderVoltAlarmElement.innerText = "Voltage is too low. " + VOLT_ALARM_TEXT + "Shutdown recommended. ";
    } else if (leaderVolt > ALARM.leader.volt.max) {
        leaderVoltAlarmElement.innerText = "Voltage is too high. " + VOLT_ALARM_TEXT + "Shutdown recommended. ";
    }

    // follower temp
    if (followerTemp < ALARM.follower.temp.min) {
        followerTempAlarmElement.innerText = "Temperature is too low. Shutdown recommended.";
    } else if (followerTemp > ALARM.follower.temp.warn) {
        followerTempAlarmElement.innerText = "Temperature is too high. " + TEMP_ALARM_TEXT + 
            "Keep a watchful eye on the temperature.";
    } else if (followerTemp > ALARM.follower.temp.alarm) {
        followerTempAlarmElement.innerText = "Temperature is too high. " + TEMP_ALARM_TEXT + "Shutdown recommended.";
    }

    if (followerVolt < ALARM.follower.volt.min) {
        followerVoltAlarmElement.innerText = "Voltage is too low. " + VOLT_ALARM_TEXT + "Shutdown recommended.";
    } else if (followerVolt > ALARM.follower.volt.max) {
        followerVoltAlarmElement.innerText = "Voltage is too high. " + VOLT_ALARM_TEXT + "Shutdown recommended.";
    }
}
