package com.mende.examination.soarms;

import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/robot")
public class RobotStateController {

    private final RobotStateService robotStateService;

    public RobotStateController(RobotStateService robotStateService) {
        this.robotStateService = robotStateService;
    }

    @GetMapping("/state")
    public RobotState state() {
        return robotStateService.currentState();
    }

    @GetMapping("/posList")
    public List<Double[]> posList() {
        return robotStateService.getPosList();
    }
}