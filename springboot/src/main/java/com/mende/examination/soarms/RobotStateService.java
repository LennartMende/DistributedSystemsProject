package com.mende.examination.soarms;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.stereotype.Service;

@Service
public class RobotStateService {
    private final List<Double[]> posHistory = new ArrayList<>();
    private final List<Double[]> tempHistory = new ArrayList<>();
    private final List<Double[]> voltHistory = new ArrayList<>();
    private int posCounter = 0;
    private int tempCounter = 0;
    private int voltCounter = 0;
    private int sampleRate = 10; // sample every 10th message
    private int bufferCapacity = 180; // store up to 180 samples (30 seconds of data at 10Hz)

    private static final ObjectMapper OBJECT_MAPPER = new ObjectMapper();
    private static final List<String> JOINT_KEYS = List.of(
        "shoulder_pan.pos",
        "shoulder_lift.pos",
        "elbow_flex.pos",
        "wrist_flex.pos",
        "wrist_roll.pos",
        "gripper.pos"
    );

    private final RobotState state = new RobotState();

    // Positions
    public synchronized List<Double[]> getPosList() {
        return new ArrayList<>(posHistory);
    }

    public synchronized void updatePos(String payload) {
        Double[] pos = parseDoubleArray(payload);
        state.setPos(pos);
        extendPosHistory(pos);
    }

    private void extendPosHistory(Double[] pos) {
        if (posCounter++ % sampleRate == 0) { // only store every sampleRate-th sample to reduce memory usage
            posHistory.add(pos);
            if (posHistory.size() > bufferCapacity) { // remove sample if more than bufferCapacity samples
                posHistory.remove(0);
            }
        }
    }

    // Temperatures
    public synchronized List<Double[]> getTempList() {
        return new ArrayList<>(tempHistory);
    }

    public synchronized void updateTemp(String payload) {
        Double[] temp = parseDoubleArray(payload);
        state.setTemp(temp);
        extendTempHistory(temp);
    }

    private void extendTempHistory(Double[] temp) {
        if (tempCounter++ % sampleRate == 0) { // only store every sampleRate-th sample to reduce memory usage
            tempHistory.add(temp);
            if (tempHistory.size() > bufferCapacity) { // remove sample if more than bufferCapacity samples
                tempHistory.remove(0);
            }
        }
    }

    // Voltages
    public synchronized void updateVolt(String payload) {
        Double[] volt = parseDoubleArray(payload);
        state.setVolt(volt);
        extendPosHistory(volt);
    }

    // Machine state
    public synchronized void updateMachineState(String payload) {
        state.setMachineState(payload.trim());
    }

    private Double[] parseDoubleArray(String payload) {
        try {
            return OBJECT_MAPPER.readValue(payload, Double[].class);
        } catch (JsonProcessingException e) {
            try {
                Map<String, Number> map = OBJECT_MAPPER.readValue(payload, new TypeReference<Map<String, Number>>() {});
                return JOINT_KEYS.stream()
                    .map(key -> map.containsKey(key) ? map.get(key).doubleValue() : 0.0)
                    .toArray(Double[]::new);
            } catch (JsonProcessingException ex) {
                throw new IllegalArgumentException("Ungültiges MQTT-Payload-Format: " + payload, ex);
            }
        }
    }

    public synchronized RobotState currentState() {
        RobotState copy = new RobotState();
        if (state.getPos() != null) {
            copy.setPos(state.getPos());
        }
        if (state.getTemp() != null) {
            copy.setTemp(state.getTemp());
        }
        if (state.getVolt() != null) {
            copy.setVolt(state.getVolt());
        }
        if (state.getMachineState() != null) {
            copy.setMachineState(state.getMachineState());
        }
        copy.setLastUpdate(state.getLastUpdate()); // wichtig
        return copy;
    }
}