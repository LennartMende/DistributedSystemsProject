package com.mende.examination.soarms;

import java.util.Map;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestBody;


@RestController
@RequestMapping("/api")
public class WebControlController {

    private volatile String lastMessage; // private volatile ControlMessage lastMessage;

    private final MqttRobotPublisher publisher;

    public WebControlController(MqttRobotPublisher publisher) {
        this.publisher = publisher;
    }

    @PostMapping("/control")
    public ResponseEntity<Void> postControl(@RequestBody String body) {

        lastMessage = body;
        
        System.out.println(body);

        return ResponseEntity.ok().build();
    }


    @GetMapping(value="/control", produces="application/json")
    public ResponseEntity<String> getControl() {

        if (lastMessage == null) {
            return ResponseEntity.noContent().build();
        }

        return ResponseEntity.ok(lastMessage);
    }
}