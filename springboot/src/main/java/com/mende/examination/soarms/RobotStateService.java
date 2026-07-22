package com.mende.examination.soarms;

import java.util.ArrayList;
import java.util.List;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonNode;
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
        "shoulder_pan",
        "shoulder_lift",
        "elbow_flex",
        "wrist_flex",
        "wrist_roll",
        "gripper"
    );

    private static final List<String> POS_KEYS = JOINT_KEYS.stream()
        .map(key -> key + ".pos")
        .toList();

    private static final List<String> TEMP_KEYS = JOINT_KEYS.stream()
        .map(key -> key + ".temp")
        .toList();

    private static final List<String> VOLT_KEYS = JOINT_KEYS.stream()
        .map(key -> key + ".volt")
        .toList();

    private final RobotState state = new RobotState();

    // Positions
    public synchronized List<Double[]> getPosList() {
        return new ArrayList<>(posHistory);
    }

    public synchronized void updatePos(String payload) {
        Double[] pos = parseDoubleArray(payload, POS_KEYS);
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
        Double[] temp = parseDoubleArray(payload, TEMP_KEYS);
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

    private void extendVoltHistory(Double[] volt) {
        if (voltCounter++ % sampleRate == 0) { // only store every sampleRate-th sample to reduce memory usage
            voltHistory.add(volt);
            if (voltHistory.size() > bufferCapacity) { // remove sample if more than bufferCapacity samples
                voltHistory.remove(0);
            }
        }
    }

    // Voltages
    public synchronized void updateVolt(String payload) {
        Double[] volt = parseDoubleArray(payload, VOLT_KEYS);
        state.setVolt(volt);
        extendVoltHistory(volt);
    }

    // Machine state
    public synchronized void updateMachineState(String payload) {
        try {
            JsonNode root = OBJECT_MAPPER.readTree(payload);

            // 1) {"machineState": "STOPPED"}
            if (root.has("machineState")) {
                state.setMachineState(root.get("machineState").asText());
                return;
            }

            // 2) {"state": "STOPPED"}
            if (root.has("state")) {
                state.setMachineState(root.get("state").asText());
                return;
            }

            // 3) {"machine_state": "STOPPED"}
            if (root.has("machine_state")) {
                state.setMachineState(root.get("machine_state").asText());
                return;
            }

            // 4) Fallback: plain string
            state.setMachineState(payload.trim());

        } catch (Exception e) {
            // Fallback: plain string
            state.setMachineState(payload.trim());
        }
    }


    private Double[] parseDoubleArray(String payload, List<String> KEYS) {
        try {
            JsonNode root = OBJECT_MAPPER.readTree(payload);

            if (root.isArray()) {
                Double[] values = new Double[root.size()];
                for (int i = 0; i < root.size(); i++) {
                    values[i] = root.get(i).doubleValue();
                }
                return values;
            }

            if (root.isObject()) {
                return KEYS.stream()
                    .map(key -> extractDoubleValueFromNode(root, key))
                    .toArray(Double[]::new);
            }
        } catch (JsonProcessingException e) {
            throw new IllegalArgumentException("Ungültiges MQTT-Payload-Format: " + payload, e);
        }

        throw new IllegalArgumentException("Ungültiges MQTT-Payload-Format: " + payload);
    }

    private Double extractDoubleValueFromNode(JsonNode root, String key) {
        JsonNode node = root.get(key);
        if (node != null && !node.isNull()) {
            return node.doubleValue();
        }

        // Fallback: ohne Suffix
        String simpleKey = key.split("\\.")[0];
        JsonNode simpleNode = root.get(simpleKey);
        if (simpleNode != null && !simpleNode.isNull()) {
            return simpleNode.doubleValue();
        }

        return -1.0;
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