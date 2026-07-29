// IMPORTS
import { TabManager } from "./tabManager.js";


// GLOBALS
const tabManager = new TabManager("control");
tabManager.start();

const sliders = [document.getElementById("joint0_slider"), document.getElementById("joint1_slider"),
    document.getElementById("joint2_slider"), document.getElementById("joint3_slider"),
    document.getElementById("joint4_slider"), document.getElementById("joint5_slider")
];


// FUNCTIONS
let updateCounter = 0;

async function postSliderValues() {
    const data = {"shoulder_pan.pos":     parseFloat(sliders[0].value), 
            "shoulder_lift.pos":    parseFloat(sliders[1].value),
            "elbow_flex.pos":       parseFloat(sliders[2].value), 
            "wrist_flex.pos":       parseFloat(sliders[3].value), 
            "wrist_roll.pos":       parseFloat(sliders[4].value), 
            "gripper.pos":          parseFloat(sliders[5].value)};

    fetch("/api/control", {
    method: "POST",
    body: JSON.stringify({
        "time": Date.now() / 1000,
        "deviceId": "control_publisher",
        "data": data
    }),
    headers: {
        "Content-type": "application/json; charset=UTF-8"
    }
    }).then(response => {
        if (!response.ok) {
            console.error("POST fehlgeschlagen");
        }
    });

    if (updateCounter % 10 === 0) {
            console.log("Current mode: ", tabManager.getMode());
            console.log("Current pageCounter: ", tabManager.getPageCounter());
        }
    // console.log("time: ", Date.now() / 1000, " deviceId: ", "control_publisher", " data: ", data);
    // console.log("payload: ", JSON.stringify({
    //     "time": Date.now() / 1000,
    //     "deviceId": "control_publisher",
    //     "data": data
    // }));
}


sliders.forEach(slider => {
    slider.addEventListener("input", postSliderValues);
});
setInterval(postSliderValues, 100);