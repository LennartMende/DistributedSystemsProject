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
    private final List<Double[]> velsHistory = new ArrayList<>();
    private int posCounter = 0;
    private int velsCounter = 0;

    private static final ObjectMapper OBJECT_MAPPER = new ObjectMapper();
    private static final List<String> JOINT_KEYS = List.of(
        "shoulder_pan",
        "shoulder_lift",
        "elbow_flex",
        "wrist_flex",
        "wrist_roll",
        "gripper"
    );

    private final RobotState state = new RobotState();

    public synchronized List<Double[]> getPosList() {
        return new ArrayList<>(posHistory);
    }

    public synchronized void updatePos(String payload) {
        Double[] pos = parseDoubleArray(payload);
        state.setPos(pos);
        extendPosHistory(pos);
    }

    private void extendPosHistory(Double[] pos) {
        if (posCounter++ % 10 == 0) { // only store every 10th sample to reduce memory usage
            posHistory.add(pos);
            if (posHistory.size() > 1800) { // remove sample if more than 1800 (=30 * 6 for 10th sampled and just latest 30 secs) for perfromance and memory
                posHistory.remove(0);
            }
        }
    }

    public synchronized List<Double[]> getVelsList() {
        return new ArrayList<>(velsHistory);
    }

    public synchronized void updateVels(String payload) {
        Double[] vels = parseDoubleArray(payload);
        state.setVels(vels);
        extendVelsHistory(vels);
    }

    private void extendVelsHistory(Double[] vels) {
        if (velsCounter++ % 10 == 0) { // only store every 10th sample to reduce memory usage
            velsHistory.add(vels);
            if (velsHistory.size() > 1800) { // remove sample if more than 1800 (=30 * 6 for 10th sampled and just latest 30 secs) for perfromance and memory
                velsHistory.remove(0);
            }
        }
    }

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
        if (state.getVels() != null) {
            copy.setVels(state.getVels());
        }
        if (state.getMachineState() != null) {
            copy.setMachineState(state.getMachineState());
        }
        copy.setLastUpdate(state.getLastUpdate()); // wichtig
        return copy;
    }
}