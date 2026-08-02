package com.mende.examination.soarms;

import java.nio.charset.StandardCharsets;

import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.stereotype.Component;
import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.annotation.PostConstruct;


@Component
public class MqttDashboardPublisher {
    
    //private volatile ControlMessage lastMessage;
    private MqttClient client; 
    private final ObjectMapper objectMapper = new ObjectMapper();

    @Value("${robot.mqtt.broker}")
    private String broker;

    @Value("${robot.mqtt.dashboard-id}")
    private String clientId;

    @Value("${robot.mqtt.dashboard.topic}")
    private String dashboardTopic;

    @PostConstruct
    public void connect() throws Exception {
        client = new MqttClient(
            broker,
            clientId,
            new MemoryPersistence()
        );

        MqttConnectOptions options = new MqttConnectOptions();

        options.setAutomaticReconnect(true);
        options.setCleanSession(true);

        options.setSocketFactory(
            SslUtil.getSocketFactory(
                "../mosquitto/certs/truststore.p12",
                "123456",
                "../mosquitto/certs/client_java_dashboard_mode_publisher.p12",
                "123456"
            )
        );

        client.connect(options);

        System.out.println(
            "MQTT on dashboard/mode topic connected: " + client.isConnected()
        );
    }
    

    public void publish(String message) throws Exception {
        System.out.println("===IN MQTT PUBLISHER===");
        if (client == null || !client.isConnected()) {
            throw new IllegalStateException(
                "MQTT client not connected"
            );
        }

        System.out.println(dashboardTopic+ ": " + message);
        MqttMessage mqttMessage =
            new MqttMessage(message.getBytes(StandardCharsets.UTF_8));

        mqttMessage.setQos(1);
        mqttMessage.setRetained(true);

        client.publish(dashboardTopic, mqttMessage);
    }
}
