# Simple pub-sub app

A simple application that produces and consumes data, using RabbitMQ as a message broker. App is using Docker Compose for deploy.
- An application that periodically sends data for calculation to RabbitMQ using routing.
- An application that processes data, applying various operations, and writes the result to a log. If the operation failed, then reject the message to DLQ.


### Requirements

- Docker
- Docker Compose

### Steps

Step 0: Clone the repo:

```bash
git clone https://github.com/glaucomaa/Simple-pub-sub-app.git
```

Step 1: Navigate to the cloned repo:

```bash
cd Simple-pub-sub-app
```

Step 2: Build docker images:

```bash
docker compose up --build -d
```

### Logging

You can look at messages being sent and received with this commands:

```bash
docker-compose logs producer
```

```bash
docker-compose logs consumer
```

### Cleanup

To stop the containers:

```bash
docker compose down
```

#### Additional information

Instead of

```bash
docker compose
```

can be used 
```bash
docker-compose
```
