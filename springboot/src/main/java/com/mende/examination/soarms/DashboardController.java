package com.mende.examination.soarms;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestBody;

@RestController
@RequestMapping("/api/dashboard")
public class DashboardController {

    private volatile String lastMessage;

    private final MqttDashboardPublisher publisher;

    public DashboardController(MqttDashboardPublisher publisher) {
        this.publisher = publisher;
    }

    @PostMapping("/mode")
    public void updateMode(@RequestBody String body) throws Exception {
        this.lastMessage = body;
        //System.out.println("Dashboard mode: " + lastMessage);
        publisher.publish(body);
    }

    @GetMapping(value="/mode", produces="application/json")
    public ResponseEntity<String> getControl() {
        if (lastMessage == null) {
            return ResponseEntity.noContent().build();
        }
        return ResponseEntity.ok(lastMessage);
    }
}