# 🏥 Healthcare DevOps — Complete CI/CD Flow

This document explains the **complete end-to-end flow** of the `healthcare-devops` project — from writing code on your local machine all the way to a live Streamlit dashboard running inside a Kubernetes cluster.

---

## 📁 Project Files

```
healthcare-devops/
├── app.py                          # Streamlit dashboard (main application)
├── Dockerfile                      # Container image definition
├── deployment.yaml                 # Kubernetes Deployment manifest
├── service.yaml                    # Kubernetes Service manifest
├── README.md                       # Project overview
├── FLOW_README.md                  # This file — full CI/CD flow
└── .github/
    └── workflows/
        └── automation.yaml         # GitHub Actions CI/CD pipeline
```

---

## 🔄 Complete CI/CD Flow Overview

```
Developer (local)
      │
      │  git push origin main
      ▼
GitHub Actions (CI/CD)
      │  ├── Checkout code
      │  ├── Setup Docker Buildx
      │  ├── Login to Docker Hub
      │  └── Build + Push image  ──────► Docker Hub
      │                                  mtousif2303/healthapp:latest
      ▼
Kubernetes (Minikube)
      │  ├── minikube start
      │  ├── kubectl apply -f deployment.yaml  (2 replicas)
      │  ├── kubectl apply -f service.yaml     (LoadBalancer)
      │  └── Pods: Running 2/2
      │
      │  minikube service health-app-service
      ▼
Live Streamlit Dashboard
      http://127.0.0.1:50389
```

---

## 📍 Phase 1 — Developer (Local Machine)

### What happens here
You write all project files locally on your Mac (Darwin arm64) and push to GitHub. A single `git push` is all it takes to trigger the entire pipeline automatically.

### Files you work with
| File | Purpose |
|------|---------|
| `app.py` | Main Streamlit app — fetches patients, services, medications, facilities |
| `Dockerfile` | Defines how to containerise the app |
| `deployment.yaml` | Tells Kubernetes how many replicas to run |
| `service.yaml` | Exposes the app outside the cluster |
| `automation.yaml` | Defines the GitHub Actions CI/CD pipeline |

### Commands

```bash
# Clone the repo
git clone https://github.com/mtousif2303/healthcare-devops.git
cd healthcare-devops

# Stage and commit your changes
git add .
git commit -m "your commit message"

# Push to main — this triggers the CI/CD pipeline automatically
git push origin main
```

---

## 📍 Phase 2 — GitHub Actions (CI/CD Pipeline)

### What happens here
Every `git push` to the `main` branch automatically triggers the `automation.yaml` workflow. GitHub provisions an `ubuntu-latest` runner and executes the `heath-app` job. Your run #2 completed in **1 minute 14 seconds**.

### Workflow file: `.github/workflows/automation.yaml`

```yaml
name: heath-app
on:
  push:
    branches:
    - main
jobs:
  health-app:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout code
      uses: actions/checkout@v2

    - name: Setup docker
      uses: docker/setup-buildx-action@v1

    - name: Login into dockerhub
      uses: docker/login-action@v2
      with:
        username: ${{secrets.dockerhub_username}}
        password: ${{secrets.dockerhub_password}}

    - name: Build + Push
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: mtousif2303/healthapp:latest
```

### Pipeline steps & timing

| Step | Action | Time |
|------|--------|------|
| Set up job | Provisions ubuntu-latest runner | 2s |
| Checkout code | Clones repo into runner | 0s |
| Setup Docker | Enables Docker Buildx for builds | 5s |
| Login to Docker Hub | Authenticates using GitHub Secrets | 0s |
| Build + Push | Builds image and pushes to Docker Hub | 1m 3s |
| Complete job | Post-cleanup steps | 2s |

### Setting up GitHub Secrets

Go to your repo → **Settings → Secrets and Variables → Actions** and add:

| Secret | Value |
|--------|-------|
| `DOCKERHUB_USERNAME` | `mtousif2303` |
| `DOCKERHUB_PASSWORD` | Your Docker Hub password or access token |

---

## 📍 Phase 3 — Docker Hub (Image Registry)

### What happens here
The GitHub Actions pipeline builds a Docker image from your `Dockerfile` and pushes it to Docker Hub. This image is the single source of truth that Kubernetes pulls from.

### Dockerfile

```dockerfile
FROM python:3.9
WORKDIR /app
COPY . /app
RUN pip install streamlit pandas requests
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build locally (manual)

```bash
# Must be lowercase tag
docker build -t healthapp .

# Force rebuild without cache
docker build --no-cache -t healthapp .

# Tag for Docker Hub
docker tag healthapp mtousif2303/healthapp:latest

# Login and push
docker login
docker push mtousif2303/healthapp:latest

# Verify images
docker images
```

### Image details

| Property | Value |
|----------|-------|
| Repository | `mtousif2303/healthapp` |
| Tag | `latest` |
| Size | 2.29 GB |
| Layers | 11 (9 shared, 2 new) |
| Base image | `python:3.9` |
| Digest | `sha256:aa7fb932f406...` |

### Run the container locally

```bash
docker run -p 8501:8501 healthapp
# Visit: http://localhost:8501
```

---

## 📍 Phase 4 — Kubernetes / Minikube (Orchestration)

### What happens here
Minikube runs a local Kubernetes cluster inside Docker Desktop. You apply two manifests — a Deployment and a Service — and Kubernetes schedules 2 pods running your app, managed and restarted automatically.

### Start the cluster

```bash
minikube start
# Uses Docker driver on Darwin arm64
# Kubernetes v1.35.1 on Docker 29.2.1
```

### Deploy the application

```bash
# Create the Deployment (2 replica pods)
kubectl apply -f deployment.yaml

# Create the Service (LoadBalancer on port 8501)
kubectl apply -f service.yaml
```

### deployment.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: healthcare-devops-deployment
spec:
  selector:
    matchLabels:
      app: myapp
  replicas: 2
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: mtousif2303/healthapp:latest
        resources:
          limits:
            memory: "128Mi"
            cpu: "500m"
        ports:
        - containerPort: 8501
```

### service.yaml

```yaml
apiVersion: v1
kind: Service
metadata:
  name: health-app-service
spec:
  selector:
    app: myapp
  ports:
  - port: 8501
    targetPort: 8501
  type: LoadBalancer
```

### Monitor the cluster

```bash
# Check pod status
kubectl get pods

# Check services
kubectl get services

# Describe a pod (debug events)
kubectl describe pod <pod-name>

# View pod logs
kubectl logs <pod-name>

# Open the Kubernetes visual dashboard
minikube dashboard

# Enable metrics (optional)
minikube addons enable metrics-server
```

### Expected pod output

```
NAME                                           READY   STATUS    RESTARTS   AGE
healthcare-devops-deployment-d557db58d-kh27l   1/1     Running   0          5m
healthcare-devops-deployment-d557db58d-stkkw   1/1     Running   0          5m
```

### Kubernetes Dashboard status (verified)

| Resource | Count | Status |
|----------|-------|--------|
| Deployments | 2 | 100% Running |
| Pods | 4 | 100% Running |
| Replica Sets | 2 | 100% Running |

---

## 📍 Phase 5 — Live Streamlit Dashboard

### What happens here
The Minikube service tunnel exposes the Kubernetes LoadBalancer to your local browser. The Streamlit app fetches live data from external APIs and renders charts and tables in real time.

### Open the app

```bash
minikube service health-app-service
# Terminal must stay open while using the app
```

### Service routing

```
Browser (localhost)
      │
      │  http://127.0.0.1:50389
      ▼
Minikube tunnel
      │
      │  192.168.49.2:30660 (cluster internal)
      ▼
health-app-service (LoadBalancer)
      │
      │  port 8501 → targetPort 8501
      ▼
Pod 1 or Pod 2
      │
      └── streamlit run app.py --server.port=8501
```

### What the dashboard shows

| Section | Data source |
|---------|-------------|
| Patient Records | [randomuser.me API](https://randomuser.me/api/?results=50) — 50 patients |
| Healthcare Services | Randomly generated — Checkup, Blood Test, X-Ray, MRI, Surgery |
| Medication Data | Randomly generated — Paracetamol, Ibuprofen, Aspirin, Metformin |
| Healthcare Facilities | [NY Open Health Data API](https://health.data.ny.gov/resource/xdss-u53e.json) |
| Merged Patient Data | All datasets joined on patient + service + medication IDs |
| Charts | Service cost distribution, medication cost over time, service counts |

### Refresh live data

Click the **Refresh Data** button in the dashboard to re-fetch all APIs and regenerate the charts with new data.

---

## ⚠️ Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `invalid tag "healthApp"` | Docker tags must be lowercase | Use `healthapp` not `healthApp` |
| `File does not exist: app.py` | Wrong directory or missing file | `cd healthcare-devops && ls` to confirm `app.py` exists |
| `CACHED [3/4] COPY . /app` | Docker used stale cache | Run `docker build --no-cache -t healthapp .` |
| `containerPort of type int32` | Port value in YAML had quotes | Remove quotes — `containerPort: 8501` not `"8501"` |
| `ErrImagePull` | Kubernetes can't pull image | Check image name in `deployment.yaml` matches Docker Hub exactly |
| `Completed` pod status | App crashed at startup | Run `kubectl logs <pod-name>` to see the error |
| `minikube start` fails | Docker Desktop not running | Start Docker Desktop first, then retry |

---

## 🔁 Full Redeployment (after code changes)

```bash
# 1. Make your code changes locally
# 2. Commit and push — GitHub Actions handles the rest automatically
git add .
git commit -m "update app"
git push origin main

# 3. Wait for GitHub Actions to finish (~1m 14s)
# 4. Restart your pods to pull the new image
kubectl rollout restart deployment/healthcare-devops-deployment

# 5. Verify new pods are running
kubectl get pods
```

---

## 🛑 Tear Down

```bash
# Stop the Kubernetes cluster (keeps config)
minikube stop

# Delete everything
kubectl delete -f deployment.yaml
kubectl delete -f service.yaml
minikube delete
```

---

## 👤 Author

**Mohamed Tousif**
GitHub: [mtousif2303](https://github.com/mtousif2303)
Docker Hub: [mtousif2303](https://hub.docker.com/u/mtousif2303)
