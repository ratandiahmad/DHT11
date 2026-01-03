import org.eclipse.paho.client.mqttv3.*;
import com.google.gson.*;

public class AnomalyDetector implements MqttCallback {

    private static final String BROKER = "tcp://localhost:1883";
    private static final String SUB_TOPIC = "dht/raw";
    private static final String PUB_TOPIC = "dht/anomaly";

    private static final double TEMP_THRESHOLD = 30.0;

    private MqttClient client;
    private Gson gson = new Gson();

    public AnomalyDetector() throws MqttException {

        client = new MqttClient(BROKER, "JavaAnomalyDetector");

        MqttConnectOptions options = new MqttConnectOptions();
        options.setAutomaticReconnect(true);
        options.setCleanSession(true);

        client.setCallback(this);
        client.connect(options);
        client.subscribe(SUB_TOPIC);

        System.out.println("✅ Java Anomaly Detector RUNNING");
    }

    @Override
    public void messageArrived(String topic, MqttMessage message) {

        try {
            String payload = new String(message.getPayload());
            JsonObject data = gson.fromJson(payload, JsonObject.class);

            double temperature = data.get("temperature").getAsDouble();
            double humidity = data.get("humidity").getAsDouble();

            if (temperature > TEMP_THRESHOLD) {

                JsonObject anomaly = new JsonObject();
                anomaly.addProperty("temperature", temperature);
                anomaly.addProperty("humidity", humidity);
                anomaly.addProperty("status", "ANOMALY");

                MqttMessage msg = new MqttMessage(anomaly.toString().getBytes());
                msg.setQos(1);

                client.publish(PUB_TOPIC, msg);

                System.out.println("🔥 ANOMALI TERDETEKSI → " + anomaly);

            } else {
                System.out.println("Normal: " + temperature + "°C");
            }

        } catch (Exception e) {
            System.out.println("❌ Error parsing message: " + e.getMessage());
        }
    }

    @Override
    public void connectionLost(Throwable cause) {
        System.out.println("⚠️ MQTT connection lost");
    }

    @Override
    public void deliveryComplete(IMqttDeliveryToken token) {
        // optional
    }

    public static void main(String[] args) throws Exception {
        new AnomalyDetector();
    }
}
