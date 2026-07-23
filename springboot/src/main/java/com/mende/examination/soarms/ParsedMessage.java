package com.mende.examination.soarms;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

public class ParsedMessage {
    public final String deviceId;
    public final Double processTimeStamp;
    public final String data;

    private static final ObjectMapper MAPPER = new ObjectMapper();

    public ParsedMessage(String messageJson) {
        try {
            JsonNode root = MAPPER.readTree(messageJson);

            this.deviceId = root.get("deviceId").asText();
            this.processTimeStamp = root.get("processTimeStamp").asDouble();

            JsonNode payloadNode = root.get("data");
            this.data = payloadNode.toString();   // wichtig: als JSON-String
            //System.out.println("Message could be parsed");

        } catch (Exception e) {
            //System.out.println("Message could NOT be parsed");
            throw new IllegalArgumentException("Invalid message format: " + messageJson, e);
        }
    }
}
