package com.mende.examination.soarms;

import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/robot")
public class RobotStateController {

    private final LeaderStateService leaderStateService;
    private final FollowerStateService followerStateService;

    public RobotStateController(LeaderStateService leaderStateService, FollowerStateService followerStateService) {
        this.leaderStateService = leaderStateService;
        this.followerStateService = followerStateService;
    }

    private RobotStateService resolveService(String id) {
        switch(id.toLowerCase()) {
            case "leader":
                return leaderStateService;
            case "follower":
                return followerStateService;
            default:
                throw new IllegalArgumentException("Unknown robot id: " + id);
        }
    }

    @GetMapping("/{id}/state")
    public RobotState state(@PathVariable String id) {
        return resolveService(id).currentState();
    }

    @GetMapping("/{id}/posList")
    public List<Double[]> posList(@PathVariable String id) {
        return resolveService(id).getPosList();
    }

    @GetMapping("/timeStampsList")
    public List<Double> timeStampsList() {
        return leaderStateService.getTimeStampsList();
    }
}