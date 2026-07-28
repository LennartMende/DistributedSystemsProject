// package com.mende.examination.soarms;

// import java.util.Map;

// public class ControlMessage {
//     private double processTimeStamp;
//     private String deviceId;
//     private Map<String, Double> data;
//     // public final double processTimeStamp;
//     // public final String deviceId;
//     // public final Map<String, Double> data;

//     public ControlMessage() {
//     }

//     public double getTime() {
//         return processTimeStamp;
//     }

//     public void setTime(double time) {
//         this.processTimeStamp = time;
//     }

//     public String getDeviceId() {
//         return deviceId;
//     }

//     public void setDeviceId(String deviceId) {
//         this.deviceId = deviceId;
//     }

//     public Map<String, Double> getData() {
//         return data;
//     }

//     public void setData(Map<String, Double> data) {
//         this.data = data;
//     }

//     // public ControlMessage(double processTimeStamp, String deviceId, Map<String, Double> data) {
//     //     this.processTimeStamp = processTimeStamp;
//     //     this.deviceId = deviceId;
//     //     this.data = data;
//     // }

//     @Override
//     public String toString() {
//         return "processTimeStamp = %d\ndeviceId = %d\ndata= %s".formatted(processTimeStamp, deviceId, data.toString());
//     }
// }