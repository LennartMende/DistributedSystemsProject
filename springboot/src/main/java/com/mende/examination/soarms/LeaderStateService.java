package com.mende.examination.soarms;

import org.springframework.stereotype.Service;

@Service
public class LeaderStateService extends RobotStateService {
    public LeaderStateService() {
        super("leader");
    }
}
