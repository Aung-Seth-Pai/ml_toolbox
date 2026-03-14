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

```json
{
  "name": "nginx-primer-node",
  "version": "1.0.0",
  "description": "Simple Node webserver for NGINX primer",
  "main": "server.js",
  "scripts": {
    "start": "node server.js"
  },
  "author": "zephyr",
  "license": "MIT"
}
```

---

## src/server.js

```javascript
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 3000;
const APP_NAME = process.env.APP_NAME || "default-app";
const instanceName = process.env.HOSTNAME || "unknown-instance";
const isDev = process.env.NODE_ENV === 'development';

console.log(`Starting instance: ${APP_NAME}`);

const server = http.createServer((req, res) => {

    console.log(`[${instanceName}] Handling request for: ${req.url}`);

    const filePath = path.join(__dirname, 'index.html');
    
    fs.readFile(filePath, 'utf8', (err, data) => {
        if (err) {
            res.writeHead(500, { 'Content-Type': 'text/plain' });
            return res.end('Internal Server Error'); 
        }

        const headers = { 
            'Content-Type': 'text/html',
            'X-App-Name': APP_NAME
        };

        if (isDev) {
            headers['X-Backend-Server'] = instanceName;
        }

        res.writeHead(200, headers);
        res.end(data);
    });
});

server.listen(PORT, () => {
    console.log("SERVICE ONLINE");
    console.log(`APP NAME: ${APP_NAME}`);
    console.log(`INSTANCE ID: ${instanceName}`);
});
```

---

## src/index.html

```html
<!DOCTYPE html>
<html>
<head>
<title>NGINX Load Balancer Demo</title>
</head>
<body>

<h1>Hello from the Node Cluster!</h1>
<p>Check your terminal logs or browser headers to see which instance handled the request.</p>

</body>
</html>
```

---

## Dockerfile

```dockerfile
FROM node:24-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install --only=production

COPY src/ .

EXPOSE 3000

CMD ["node", "server.js"]
```

---

## docker-compose.yml

```yaml
services:

  gateway:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - app

  app:
    image: nginx-primer-node
    build: .
    deploy:
      replicas: 3
    environment:
      - APP_NAME=alpha
      - NODE_ENV=development
      - PORT=3000
```

---

## nginx.conf

```nginx
events {
    worker_connections 1024;
}

http {

    upstream node_cluster {
        server app:3000;
    }

    server {

        listen 80;

        location / {
            proxy_pass http://node_cluster;

            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

    }

}
```

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