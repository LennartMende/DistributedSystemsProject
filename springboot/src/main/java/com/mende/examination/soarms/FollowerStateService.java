package com.mende.examination.soarms;

import org.springframework.stereotype.Service;

@Service
public class FollowerStateService extends RobotStateService {
    public FollowerStateService() {
        super("follower");
    }
}
