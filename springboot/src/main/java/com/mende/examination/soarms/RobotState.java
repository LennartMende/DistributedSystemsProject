package com.mende.examination.soarms;

import java.time.Instant;

public class RobotState {

    private Double[] pos;
    private Double[] vels;
    private String machineState;
    private Instant lastUpdate;

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

    public Double[] getVels() {
        return vels;
    }

    public void setVels(Double[] vels) {
        this.vels = vels;
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
}