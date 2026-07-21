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

    @Value("${robot.mqtt.leader.temp-topic}")
    private String leaderTempTopic;

    @Value("${robot.mqtt.leader.volt-topic}")
    private String leaderVoltTopic;

    @Value("${robot.mqtt.leader.state-topic}")
    private String leaderStateTopic;

    @Value("${robot.mqtt.follower.pos-topic}")
    private String followerPosTopic;

    @Value("${robot.mqtt.follower.temp-topic}")
    private String followerTempTopic;

    @Value("${robot.mqtt.follower.volt-topic}")
    private String followerVoltTopic;

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

        IMqttMessageListener leaderTempListener =
            (topic, message) -> handleTemp(leaderStateService, message);
        
        IMqttMessageListener leaderVoltListener =
            (topic, message) -> handleVolt(leaderStateService, message);

        IMqttMessageListener leaderStateListener =
            (topic, message) -> handleMachineState(leaderStateService, message);


        IMqttMessageListener followerPosListener =
            (topic, message) -> handlePos(followerStateService, message);

        IMqttMessageListener followerTempListener =
            (topic, message) -> handleTemp(followerStateService, message);

        IMqttMessageListener followerVoltListener =
            (topic, message) -> handleVolt(followerStateService, message);

        IMqttMessageListener followerStateListener =
            (topic, message) -> handleMachineState(followerStateService, message);

        // subsciptions for leader and follower
        client.subscribe(leaderPosTopic, 1, leaderPosListener);
        client.subscribe(leaderTempTopic, 1, leaderTempListener);
        client.subscribe(leaderVoltTopic, 1, leaderVoltListener);
        client.subscribe(leaderStateTopic, 1, leaderStateListener);

        client.subscribe(followerPosTopic, 1, followerPosListener);
        client.subscribe(followerTempTopic, 1, followerTempListener);
        client.subscribe(followerVoltTopic, 1, followerVoltListener);
        client.subscribe(followerStateTopic, 1, followerStateListener);


        System.out.println("MQTT bridge subscribed to " + leaderPosTopic);
        System.out.println("MQTT bridge subscribed to " + leaderTempTopic);
        System.out.println("MQTT bridge subscribed to " + leaderVoltTopic);
        System.out.println("MQTT bridge subscribed to " + leaderStateTopic);
        System.out.println("MQTT bridge subscribed to " + followerPosTopic);
        System.out.println("MQTT bridge subscribed to " + followerTempTopic);
        System.out.println("MQTT bridge subscribed to " + followerVoltTopic);
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

    private void handleTemp(RobotStateService service, MqttMessage message) {
        String payload = new String(message.getPayload());
        try {
            service.updateTemp(payload);
            System.out.println("Temperatures updated: " + payload);
        } catch (Exception e) {
            System.err.println("Failed to update voltages: " + e.getMessage());
            e.printStackTrace();
        }
    }

    private void handleVolt(RobotStateService service, MqttMessage message) {
        String payload = new String(message.getPayload());
        try {
            service.updateVolt(payload);
            System.out.println("Voltages updated: " + payload);
        } catch (Exception e) {
            System.err.println("Failed to update voltages: " + e.getMessage());
            e.printStackTrace();
        }
    }

    private void handleMachineState(RobotStateService service, MqttMessage message) {
        String payload = new String(message.getPayload());
        service.updateMachineState(payload);
        System.out.println("Machine state updated: " + payload);
    }
}