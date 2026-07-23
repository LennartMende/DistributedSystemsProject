package com.mende.examination.soarms;

import java.time.Instant;

public class RobotState {

    private Double[] pos;
    private Double[] temp;
    private Double[] volt;
    private String machineState;
    private Instant lastUpdate;

    private Double processTimeStamp;

    public RobotState() {
        this.lastUpdate = Instant.EPOCH;
    }

    public Double[] getPos() {
        return pos;
    }

    public void setPos(Double[] pos) {
        this.pos = pos;
        this.lastUpdate = Instant.now();
    }

    public Double[] getTemp() {
        return temp;
    }

    public void setTemp(Double[] temp) {
        this.temp = temp;
        this.lastUpdate = Instant.now();
    }

    public Double[] getVolt() {
        return volt;
    }

    public void setVolt(Double[] volt) {
        this.volt = volt;
        this.lastUpdate = Instant.now();
    }

    public String getMachineState() {
        return machineState;
    }

    public void setMachineState(String machineState) {
        this.machineState = machineState;
        this.lastUpdate = Instant.now();
    }

    public Instant getLastUpdate() {
        return lastUpdate;
    }

    public void setLastUpdate(Instant lastUpdate) {
        this.lastUpdate = lastUpdate;
    }

    public Double getProcessTimeStamp() {
        return processTimeStamp;
    }

    public void setProcessTimeStamp(Double processTimeStamp) {
        this.processTimeStamp = processTimeStamp;
        this.lastUpdate = Instant.now();
    }
}