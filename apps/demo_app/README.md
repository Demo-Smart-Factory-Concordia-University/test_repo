# Simple Demonstration OpenFactory App

This demo comes in two versions:

* `demo_app.py`: Run interactively for local testing.
* `demo_ofa_app.py`: An OpenFactory-compatible app for deployment on OpenFactory.

---

## Deploying the OpenFactory App

To deploy the app on OpenFactory, follow these steps:

1. Implement your application using the `OpenFactoryApp` class.
2. Build a Docker image for the app.
3. Deploy the app using the OpenFactory SDK.

---

### Build the Docker Image

Use the following command to build the Docker image and tag it as `demo_ofa_app`:

```bash
docker build -t demo_ofa_app .
```

---

### Deploy the App on OpenFactory

Deploy the app with the `openfactory-sdk`:

```bash
openfactory-sdk app up demo_ofa_app.yml
```

To shut down the app:

```bash
openfactory-sdk app down demo_ofa_app.yml
```

Deployment configuration details are specified in the `demo_ofa_app.yml` file:
```yaml
apps:
  demo_ofa_app:
    uuid: DEMO-APP
    image: demo_ofa_app
```
which assigns an OpenFactory UUID to your app and specifies the Docker image to use.

## Follow the App Execution
The execution of the deployed app, can be followed using the Docker logs command:
```bash
docker logs demo-app
```
the container name beeing the OpenFactory UUID in lowercase.

To stream logs in real time, use:
```bash
docker logs -f demo-app
```
This is useful for debugging and observing live behavior during development or after deployment.
