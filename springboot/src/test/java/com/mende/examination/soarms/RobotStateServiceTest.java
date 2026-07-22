package com.mende.examination.soarms;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;

import org.junit.jupiter.api.Test;

class RobotStateServiceTest {

    @Test
    void updatePosShouldParsePythonStyleJsonPayload() {
        RobotStateService service = new RobotStateService();

        String payload = "{\"shoulder_pan\":1.0,\"shoulder_lift\":2.0,\"elbow_flex\":3.0,\"wrist_flex\":4.0,\"wrist_roll\":5.0,\"gripper\":6.0}";

        service.updatePos(payload);

        RobotState state = service.currentState();
        assertArrayEquals(new Double[]{1.0, 2.0, 3.0, 4.0, 5.0, 6.0}, state.getPos());
    }
}
