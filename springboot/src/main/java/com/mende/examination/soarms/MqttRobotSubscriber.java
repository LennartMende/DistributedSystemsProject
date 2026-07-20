package com.mende.examination.soarms;

import org.eclipse.paho.client.mqttv3.IMqttMessageListener;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.stereotype.Component;

@Component
public class MqttRobotSubscriber implements ApplicationRunner {

    private final LeaderStateService leaderStateService;
    private final FollowerStateService followerStateService;


    @Value("${robot.mqtt.broker}")
    private String broker;

    @Value("${robot.mqtt.client-id}")
    private String clientId;

    @Value("${robot.mqtt.leader.pos-topic}")
    private String leaderPosTopic;

    @Value("${robot.mqtt.leader.vels-topic}")
    private String leaderVelsTopic;

    @Value("${robot.mqtt.leader.state-topic}")
    private String leaderStateTopic;

    @Value("${robot.mqtt.follower.pos-topic}")
    private String followerPosTopic;

    @Value("${robot.mqtt.follower.vels-topic}")
    private String followerVelsTopic;

    @Value("${robot.mqtt.follower.state-topic}")
    private String followerStateTopic;

    public MqttRobotSubscriber(LeaderStateService leaderStateService, FollowerStateService followerStateService) {
        this.leaderStateService = leaderStateService;
        this.followerStateService = followerStateService;
    }

    @Override
    public void run(ApplicationArguments args) throws Exception {
        MqttClient client = new MqttClient(
            broker,
            clientId,
            new MemoryPersistence());

        MqttConnectOptions options = new MqttConnectOptions();
        options.setAutomaticReconnect(true);
        options.setCleanSession(true);
        options.setUserName("username");
        options.setPassword("password".toCharArray());


        client.connect(options);

        // listeners for leader and follower
        IMqttMessageListener leaderPosListener =
            (topic, message) -> handlePos(leaderStateService, message);

        IMqttMessageListener leaderVelsListener =
            (topic, message) -> handleVels(leaderStateService, message);

        IMqttMessageListener leaderStateListener =
            (topic, message) -> handleMachineState(leaderStateService, message);


        IMqttMessageListener followerPosListener =
            (topic, message) -> handlePos(followerStateService, message);

        IMqttMessageListener followerVelsListener =
            (topic, message) -> handleVels(followerStateService, message);

        IMqttMessageListener followerStateListener =
            (topic, message) -> handleMachineState(followerStateService, message);

        // subsciptions for leader and follower
        client.subscribe(leaderPosTopic, 1, leaderPosListener);
        client.subscribe(leaderVelsTopic, 1, leaderVelsListener);
        client.subscribe(leaderStateTopic, 1, leaderStateListener);

        client.subscribe(followerPosTopic, 1, followerPosListener);
        client.subscribe(followerVelsTopic, 1, followerVelsListener);
        client.subscribe(followerStateTopic, 1, followerStateListener);


        System.out.println("MQTT bridge subscribed to " + leaderPosTopic);
        System.out.println("MQTT bridge subscribed to " + leaderVelsTopic);
        System.out.println("MQTT bridge subscribed to " + leaderStateTopic);
        System.out.println("MQTT bridge subscribed to " + followerPosTopic);
        System.out.println("MQTT bridge subscribed to " + followerVelsTopic);
        System.out.println("MQTT bridge subscribed to " + followerStateTopic);
    }

    private void handlePos(RobotStateService service, MqttMessage message) {
        String payload = new String(message.getPayload());
        try {
            service.updatePos(payload);
            System.out.println("Positions updated: " + payload);
        } catch (Exception e) {
            System.err.println("Failed to update positions: " + e.getMessage());
            e.printStackTrace();
        }
    }

    private void handleVels(RobotStateService service, MqttMessage message) {
        String payload = new String(message.getPayload());
        try {
            service.updateVels(payload);
            System.out.println("Velocities updated: " + payload);
        } catch (Exception e) {
            System.err.println("Failed to update velocities: " + e.getMessage());
            e.printStackTrace();
        }
    }

    private void handleMachineState(RobotStateService service, MqttMessage message) {
        String payload = new String(message.getPayload());
        service.updateMachineState(payload);
        System.out.println("Machine state updated: " + payload);
    }
}