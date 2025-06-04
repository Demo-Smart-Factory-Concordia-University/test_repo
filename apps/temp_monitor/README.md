# 🌡️ Temperature Monitoring OpenFactory App

An OpenFactory application for monitoring temperature sensor data, detecting thresholds, and updating sensor conditions accordingly.

---

## 🚀 Deploying the OpenFactory App

To deploy the app on OpenFactory, follow these steps:

1. **Build the Docker image**
2. **Deploy using the OpenFactory SDK**

---

### 🐳 Build the Docker Image

Run the following command to build the Docker image and tag it as `temp_monitor_app`:

```bash
docker build -t temp_monitor_app .
```

---

### 📦 Deploy the App on OpenFactory

Deploy the app using the OpenFactory SDK:

```bash
openfactory-sdk app up temp_monitor_app.yml
```

To shut down the app:

```bash
openfactory-sdk app down temp_monitor_app.yml
```

> 📝 The `temp_monitor_app.yml` file contains the app's OpenFactory UUID, Docker image configuration, and environment variable definitions passed to the app.

---

## 📈 Follow the App Execution

Monitor the running app using Docker logs. The container name will match the OpenFactory UUID in lowercase.

To view logs:

```bash
docker logs temp-monitor-app
```

To stream logs in real time:

```bash
docker logs -f temp-monitor-app
```

This is especially useful for debugging and observing live behavior during development or after deployment.

---

## 🛠️ Develop the App Without Deployment

You can run the app directly in a local development environment, without deploying it using `openfactory-sdk`. This simplifies development and testing.

However, the virtual OpenFactory infrastructure **must be running**. You can start it using:

```bash
spinup
```

> ✅ This approach is ideal for rapid prototyping and debugging before packaging the app into a Docker image.
