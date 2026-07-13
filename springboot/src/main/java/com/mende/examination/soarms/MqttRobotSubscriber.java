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

    private final RobotStateService robotStateService;

    @Value("${robot.mqtt.broker}")
    private String broker;

    @Value("${robot.mqtt.client-id}")
    private String clientId;

    @Value("${robot.mqtt.pos-topic}")
    private String posTopic;

    @Value("${robot.mqtt.vels-topic}")
    private String velsTopic;

    @Value("${robot.mqtt.state-topic}")
    private String stateTopic;

    public MqttRobotSubscriber(RobotStateService robotStateService) {
        this.robotStateService = robotStateService;
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

        IMqttMessageListener posListener =
        (topic, message) -> handlePos(message);

        IMqttMessageListener velsListener =
        (topic, message) -> handleVels(message);

        IMqttMessageListener stateListener =
        (topic, message) -> handleMachineState(message);

        client.subscribe(posTopic, 1, posListener);
        client.subscribe(velsTopic, 1, velsListener);
        client.subscribe(stateTopic, 1, stateListener);

        System.out.println("MQTT bridge subscribed to " + posTopic);
        System.out.println("MQTT bridge subscribed to " + velsTopic);
        System.out.println("MQTT bridge subscribed to " + stateTopic);
    }

    private void handlePos(MqttMessage message) {
        String payload = new String(message.getPayload());
        try {
            robotStateService.updatePos(payload);
            System.out.println("Positions updated: " + payload);
        } catch (Exception e) {
            System.err.println("Failed to update positions: " + e.getMessage());
            e.printStackTrace();
        }
    }

    private void handleVels(MqttMessage message) {
        String payload = new String(message.getPayload());
        try {
            robotStateService.updateVels(payload);
            System.out.println("Velocities updated: " + payload);
        } catch (Exception e) {
            System.err.println("Failed to update velocities: " + e.getMessage());
            e.printStackTrace();
        }
    }

    private void handleMachineState(MqttMessage message) {
        String payload = new String(message.getPayload());
        robotStateService.updateMachineState(payload);
        System.out.println("Machine state updated: " + payload);
    }
}