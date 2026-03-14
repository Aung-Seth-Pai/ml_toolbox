# Docker & NGINX Concepts: Learning Reference Notebook

This document captures the **concepts, architectural decisions, and best practices** learned while building a **load-balanced Node.js cluster using Docker and NGINX**.

The goal is to explain *why the system was designed this way*, not just how to run it.

---

# Table of Contents

1. Docker Compose: Replicas vs Separate Services  
2. Security: Information Leakage & Debug Headers  
3. Dockerfile Best Practice: `node` vs `npm start`  
4. Dockerfile `COPY` Command Nuance  
5. NGINX Worker Processes & Connections  
6. Docker Internal Networking  
7. NGINX Core Architecture  
8. Load Balancing Strategies  
9. Performance Optimization  
10. Ecosystem Comparison  
11. NGINX Configuration Basics  

---

# 1. Docker Compose: Replicas vs Separate Services

When running multiple instances of the same application, there are two possible approaches.

## The Clunky Way: Separate Services

```yaml
services:
  app1:
    ...
  app2:
    ...
  app3:
    ...
```

### Why This Is Bad

- Violates **DRY (Don't Repeat Yourself)**
- Hard to maintain
- Scaling requires copying service blocks
- Configuration updates must be repeated multiple times

---

## The Docker-Native Way: Replicas

```yaml
services:
  app:
    deploy:
      replicas: 3
```

### Why This Is Better

- Single configuration block
- Easy scaling
- Docker handles container discovery automatically

Docker’s **internal DNS** resolves the service name.

Example:

```
http://app:3000
```

Docker automatically resolves this to **all running containers** for that service.

---

# 2. Security: Information Leakage & Headers

During development, exposing internal container IDs can help debugging.

Example debug header:

```
X-Backend-Server
```

However, in production this creates **information leakage**.

Attackers may use headers to:

- Map internal infrastructure
- Identify technologies in use
- Target specific versions or vulnerabilities

---

## Secure Approach: Environment-Based Debugging

```javascript
const isDev = process.env.NODE_ENV === 'development';

if (isDev) {
    headers['X-Backend-Server'] = instanceName;
}
```

### Development Mode

Shows debugging headers.

### Production Mode

Headers are hidden.

Production environments typically rely on **centralized logging systems**, such as:

- ELK Stack
- Grafana Loki
- Datadog

---

# 3. Dockerfile Best Practice: `node server.js` vs `npm start`

Running Node applications in Docker has two approaches.

## Recommended

```
CMD ["node", "server.js"]
```

## Less Ideal

```
CMD ["npm", "start"]
```

### Comparison

| Feature | `node server.js` | `npm start` |
|------|------|------|
| Speed | Faster | Slightly slower |
| Memory | Lower | Higher |
| Process Count | 1 | 2 |
| Signal Handling | Correct | Sometimes broken |

### Why It Matters

Docker sends **SIGTERM** when stopping containers.

Using `node` directly ensures **graceful shutdown**.

---

# 4. Dockerfile COPY Command Nuance

The `COPY` command affects **file structure inside the container**.

## Scenario A

```
COPY src/ .
```

Result:

```
/app/server.js
```

Start command:

```
CMD ["node", "server.js"]
```

---

## Scenario B

```
COPY src/ ./src/
```

Result:

```
/app/src/server.js
```

Start command:

```
CMD ["node", "src/server.js"]
```

Understanding this avoids **path-related container errors**.

---

# 5. NGINX Worker Processes and Connections

NGINX uses an **event-driven architecture**, unlike traditional thread-based web servers.

Example configuration:

```
events {
    worker_connections 1024;
}
```

### Key Components

**Master Process**

- Reads configuration
- Manages worker processes

### Worker Processes (`worker_processes`)
- **Setting**: `worker_processes auto;`
- **Logic**: Spawns one worker per CPU core.
- **Precaution**: If your Docker container has strict CPU limits (e.g., `cpus: 0.5`), set this to `1` manually. Using `auto` on a limited container can cause "CPU Thrashing" as multiple processes fight for a tiny slice of processing time.

### Worker Connections (`worker_connections`)
- Defines how many simultaneous connections each worker can handle.
- **Total Capacity Formula**: $Max\ Connections = worker\_processes \times worker\_connections$

### Example

If a system has:

```
4 workers
worker_connections 1024
```

Maximum concurrent connections:

```
4 × 1024 = 4096 users
```

---

# 6. Docker Internal Networking

Beginner Docker setups expose ports like:

```
ports:
  - "3001:3000"
```

However, when using **NGINX as a load balancer**, this is unnecessary.

---

## Better Architecture

```
Client
   │
   ▼
NGINX (port 80 exposed)
   │
   ▼
Node containers (internal network only)
```

The Node containers:

- expose port **3000 internally**
- are **not exposed to the host**

NGINX communicates with them through Docker's **internal virtual network**.

Benefits:

- Increased security
- Cleaner architecture
- Reduced attack surface

---

# 7. NGINX Core Architecture

NGINX started as a **web server**, but evolved into a powerful:

- Reverse Proxy
- Load Balancer
- Edge Gateway

---

## Key Responsibilities

### Reverse Proxy

Routes client requests to backend services.

### Security Layer

Provides a **single public entry point**.

### Centralization

Handles:

- Logging
- Monitoring
- Authentication
- Rate limiting

---

# 8. Load Balancing Strategies

Configured using the `upstream` block.

Example:

```
upstream backend_cluster {
    server backend1.example.com;
    server backend2.example.com;
}
```

---

## Round Robin (Default)

Requests are distributed sequentially.

Best for:

- identical servers
- evenly distributed workloads

---

## Least Connections

Routes requests to the server with **fewest active connections**.

Best for:

- uneven workloads
- slow processing tasks

```
least_conn;
```

---

## IP Hash

Routes requests based on **client IP**.

Useful for:

- sticky sessions
- session persistence

```
ip_hash;
```

---

# 9. Performance Optimization

## Caching

NGINX can cache backend responses.

Benefits:

- reduced backend load
- faster responses

Example:

```
proxy_cache_path /data/nginx/cache;
```

---

## SSL/TLS Termination

NGINX handles encryption.

Flow:

```
Client HTTPS
     │
     ▼
NGINX decrypts
     │
     ▼
Backend receives plain HTTP
```

Benefits:

- reduced backend CPU load
- centralized certificate management

---

## Compression

Enable gzip compression.

```
gzip on;
```

Benefits:

- smaller responses
- faster page loads

---

# 10. Ecosystem Comparison

| Tool | Role |
|-----|-----|
| NGINX | Reverse proxy, load balancer |
| HAProxy | High-performance load balancer |
| Apache | Flexible traditional web server |
| Caddy | Automatic HTTPS server |
| Uvicorn | Python ASGI server |

---

# 11. Kubernetes Integration

In Kubernetes environments, NGINX is often used as an **Ingress Controller**.

Typical production architecture:

```
Client
   │
   ▼
Cloud Load Balancer (AWS ELB)
   │
   ▼
NGINX Ingress Controller
   │
   ▼
Kubernetes Services
   │
   ▼
Pods
```

This layered architecture improves:

- scalability
- reliability
- observability

---

# 12. NGINX Configuration Structure

NGINX uses **hierarchical configuration blocks**.

```
Main
 └── http
      └── server
           └── location
```

---

## Example

```
http {

    upstream backend_cluster {
        server backend1;
        server backend2;
    }

    server {

        listen 80;
        server_name example.com;

        location / {
            proxy_pass http://backend_cluster;
        }

    }

}
```

# 13. SSL/TLS Termination & Proxy Headers

In this project, NGINX handles the "heavy lifting" of decryption.

### Why terminate SSL at NGINX?
1. **CPU Efficiency**: Node.js is single-threaded; offloading decryption to NGINX (multi-process) keeps the app fast.
2. **Simplified Management**: You only need to manage certificates in one place, not in every microservice.
3. **Internal Security**: NGINX talks to Node over a private Docker network via plain HTTP, which is safe since that network isn't exposed to the internet.

### Critical Proxy Headers
When NGINX proxies a request, it must "hand off" the client's identity using these headers:
- `X-Real-IP`: The actual IP of the user.
- `X-Forwarded-Proto`: Tells the app if the user is on `https`.
- `X-Forwarded-For`: The full path of IPs the request took.

---

# References

Official Documentation:

https://nginx.org/en/docs/

NGINX Directive Index:

https://nginx.org/en/docs/dirindex.html

Awesome Tutorial by [TechWorld with Nana](https://www.youtube.com/@TechWorldwithNana)

https://www.youtube.com/watch?v=q8OleYuqntY&t=1742s