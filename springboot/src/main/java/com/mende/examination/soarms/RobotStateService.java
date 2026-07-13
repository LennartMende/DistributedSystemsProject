package com.mende.examination.soarms;

import java.util.List;
import java.util.Map;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.stereotype.Service;

@Service
public class RobotStateService {

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

    public synchronized void updatePos(String payload) {
        state.setPos(parseDoubleArray(payload));
    }

    public synchronized void updateVels(String payload) {
        state.setVels(parseDoubleArray(payload));
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