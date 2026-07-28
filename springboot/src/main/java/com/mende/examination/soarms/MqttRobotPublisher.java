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


@Component
public class MqttRobotPublisher implements ApplicationRunner {
    
    //private volatile ControlMessage lastMessage;
    private MqttClient client; 
    private final ObjectMapper objectMapper = new ObjectMapper();

    @Value("${robot.mqtt.broker}")
    private String broker;

    @Value("${robot.mqtt.controller-id}")
    private String clientId;

    @Value("${robot.mqtt.controller.topic}")
    private String controllerTopic;
    
    @Override
    public void run(ApplicationArguments args) throws Exception {
        client = new MqttClient(
            broker,
            clientId,
            new MemoryPersistence());

        MqttConnectOptions options = new MqttConnectOptions();
        options.setAutomaticReconnect(true);
        options.setCleanSession(true);

        // username + password:
        // options.setUserName("username");
        // options.setPassword("password".toCharArray());

        // TLS
        
        options.setSocketFactory(
            SslUtil.getSocketFactory(
            "../mosquitto/certs/truststore.p12",              // CA (Truststore)
            "123456",                               // Truststore-Passwort
            "../mosquitto/certs/client_java_publisher.p12",  // Client-Zertifikat (Keystore)
            "123456"                                  // Keystore-Passwort
            )
        );
        System.setProperty("javax.net.ssl.trustStore", "../mosquitto/certs/truststore.p12");
        System.setProperty("javax.net.ssl.trustStorePassword", "123456");

        client.connect(options);
        System.out.println("MQTT bridge able to publish onto " + controllerTopic);
    }

    public void publish(String message) throws Exception {

        MqttMessage mqttMessage =
            new MqttMessage(message.getBytes(StandardCharsets.UTF_8));

        mqttMessage.setQos(1);

        client.publish(controllerTopic, mqttMessage);
    }
}
