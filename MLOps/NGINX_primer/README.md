# NGINX + Node.js Load Balancer (Docker)

A simple demonstration of **NGINX acting as a load balancer** in front of multiple **Node.js application instances** running in Docker.

This project shows:

- Reverse proxy with NGINX
- Horizontal scaling of Node.js containers
- Load balancing across replicas
- Observing which backend served each request
- Chaos testing by killing containers

---

# Architecture

```
            Client (Browser)
                   │
                   ▼
            ┌─────────────┐
            │    NGINX    │
            │ Load Balancer│
            └──────┬──────┘
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
   Node App    Node App    Node App
   Instance 1  Instance 2  Instance 3
```

NGINX receives all requests and distributes them across multiple **Node.js containers**.

---

# Table of Contents

- [Project Structure](#project-structure)
- [Source Code](#source-code)
- [Running the Project](#running-the-project)
- [Testing Load Balancing](#testing-load-balancing)
- [Chaos Engineering Test](#chaos-engineering-test)
- [Clean Up](#clean-up)

---

# Project Structure

Your project should look like this:

```
my-project/
├── docker-compose.yml
├── Dockerfile
├── package.json
├── nginx.conf
└── src/
    ├── server.js
    └── index.html
```

---

# Source Code

## package.json

This file defines the Node.js project's metadata and scripts.

- [package.json](package.json)

---

## src/server.js

This is the core Node.js application server, handling HTTP requests and exposing instance information in development mode.

- [src/server.js](src/server.js)

---

## src/index.html

The simple HTML page served by the Node.js application.

- [src/index.html](src/index.html)

---

## Dockerfile

This file defines how the Node.js application Docker image is built.

- [Dockerfile](Dockerfile)

---

## docker-compose.yml

This file orchestrates the NGINX gateway and multiple Node.js application instances.

- [docker-compose.yaml](docker-compose.yaml)

---

## nginx.conf

This file contains the NGINX configuration for load balancing requests to the Node.js cluster.

- [nginx.conf](nginx.conf)

---

# Running the Project

Start the cluster:

```bash
docker compose up --build
```

You should see **three Node instances start up**, each with a different container hostname.

---

# Testing Load Balancing

Open your browser:

```
http://localhost
```

Refresh the page several times.

In your terminal logs you will see:

```
[container-id-1] Handling request
[container-id-2] Handling request
[container-id-3] Handling request
```

This proves that **NGINX is distributing traffic between containers**.

---

# Inspect Response Headers

Open **Developer Tools → Network Tab**

Click the page request and check:

```
X-Backend-Server
```

This header shows **which container served the request**.

---

# Chaos Engineering Test

Test resilience by killing a backend container.

### List containers

```bash
docker ps
```

### Stop one instance

```bash
docker stop nginx_primer-app-2
```

Now refresh the website repeatedly.

Result:

- Website stays online
- Remaining containers serve requests

NGINX automatically routes around the failed instance.

---

### Automated Chaos Test

To run a continuous, automated chaos test that randomly stops and starts backend instances, use the provided `chaos_test.sh` script. This script will demonstrate NGINX's ability to maintain service availability even under fluctuating backend conditions.

1.  **Make the script executable:**
    ```bash
    chmod +x chaos_test.sh
    ```

2.  **Run the script:**
    ```bash
    ./chaos_test.sh
    ```

    While the script is running, continuously refresh `http://localhost` in your browser. You should observe that the application remains accessible, and the `X-Backend-Server` header will show different instances handling requests, even as some are being stopped and restarted.

3.  **Stop the script:**
    Press `Ctrl+C` in the terminal where the script is running.

---

### Bring the container back

```bash
docker start nginx_primer-app-2
```

NGINX will automatically add it back into the load balancing pool.

---

# Clean Up

Stop and remove everything:

```bash
docker compose down
```

---

# Key Concepts Demonstrated

- Reverse Proxy
- Load Balancing
- Horizontal Scaling
- Container Networking
- High Availability
- Chaos Testing
---

## Learning Notes

For detailed explanations of Docker and NGINX architecture used in this project:

[Docker & NGINX Learning Notes](docs/docker-nginx-reference-notes.md)

---

# License

MIT