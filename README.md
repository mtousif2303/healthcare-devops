# 🏥 healthcare-devops

A real-time healthcare App
built and deployed using a full DevOps stack: Python + Streamlit, Docker, GitHub Actions CI/CD, and Kubernetes (Minikube).

---

## 📁 Project Structure

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



<img width="1112" height="1186" alt="image" src="https://github.com/user-attachments/assets/ca5229cc-a7a9-4172-b0c1-2bd0a16523b0" />


---

## 🧰 Tech Stack

| Tool             | Purpose                                      |
|------------------|----------------------------------------------|
| Python 3.9       | Application runtime                          |
| Streamlit        | Real-time web dashboard UI                   |
| Pandas           | Data manipulation                            |
| Requests         | External API calls                           |
| Docker           | Containerisation                             |
| Docker Hub       | Container image registry                     |
| GitHub Actions   | CI/CD automation (build + push on push)      |
| Kubernetes       | Container orchestration                      |
| Minikube         | Local Kubernetes cluster                     |

---

## 🚀 Getting Started

### Prerequisites

- Docker Desktop installed and running
- Minikube installed (`brew install minikube`)
- kubectl installed (`brew install kubectl`)
- A Docker Hub account

---

## 📋 Step-by-Step Commands

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/healthcare-devops.git
cd healthcare-devops
```

### 2. Build the Docker Image

```bash
# Build image (must be lowercase tag)
docker build -t healthapp .

# Verify image was created
docker images
```

### 3. Run Locally with Docker

```bash
docker run -p 8501:8501 healthapp
# Visit: http://localhost:8501
```

### 4. Tag & Push to Docker Hub

```bash
# Tag for Docker Hub
docker tag healthapp mtousif2303/healthapp:latest

# Login
docker login

# Push
docker push mtousif2303/healthapp:latest
```

### 5. Start Minikube

```bash
minikube start

# Verify cluster is running
kubectl get nodes
```

### 6. Deploy to Kubernetes

```bash
# Apply deployment
kubectl apply -f deployment.yaml

# Apply service
kubectl apply -f service.yaml

# Check pod status
kubectl get pods

# Check services
kubectl get services
```

### 7. Access the App via Minikube

```bash
minikube service health-app-service
# Opens http://127.0.0.1:<port> in your browser
```

### 8. Optional: Open Kubernetes Dashboard

```bash
minikube dashboard
```

### 9. Enable Metrics (Optional)

```bash
minikube addons enable metrics-server
```

---

## ⚙️ GitHub Actions CI/CD

The pipeline defined in `.github/workflows/automation.yaml` automatically:

1. **Triggers** on every push to the `main` branch
2. **Checks out** the repository code
3. **Sets up** Docker Buildx
4. **Logs into** Docker Hub using GitHub Secrets
5. **Builds and pushes** the image to `mtousif2303/healthapp:latest`

### Setting Up GitHub Secrets

Go to your GitHub repo → **Settings → Secrets and Variables → Actions** and add:

| Secret Name          | Value                    |
|----------------------|--------------------------|
| `DOCKERHUB_USERNAME` | Your Docker Hub username |
| `DOCKERHUB_PASSWORD` | Your Docker Hub password or access token |

---

## 🔍 Useful Debug Commands

```bash
# Describe a pod (see events + errors)
kubectl describe pod <pod-name>

# View pod logs
kubectl logs <pod-name>

# Force rebuild without Docker cache
docker build --no-cache -t healthapp .

# List all running pods
kubectl get pods -A

# Delete and re-apply deployment
kubectl delete -f deployment.yaml
kubectl apply -f deployment.yaml
```

---

## 📊 App Features

The Streamlit dashboard simulates a real-time healthcare data pipeline showing:

- **Patient Records** — Fetched from the [Random User API](https://randomuser.me/)
- **Healthcare Services** — Randomly generated (Checkup, X-Ray, MRI, Surgery, etc.)
- **Medication Data** — Randomly generated (Paracetamol, Ibuprofen, Metformin, etc.)
- **Healthcare Facilities** — Fetched from [NY Open Health Data](https://health.data.ny.gov/)
- **Merged Data View** — Patients joined with their services and medications
- **Charts** — Service cost distribution, medication cost over time, service counts

---

## ⚠️ Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `invalid tag "healthApp"` | Docker tags must be lowercase | Use `healthapp` not `healthApp` |
| `File does not exist: app.py` | Wrong directory or missing file | `cd healthcare-devops && ls` to confirm `app.py` exists |
| `CACHED [3/4] COPY . /app` | Docker used stale cache | Run `docker build --no-cache -t healthapp .` |
| `containerPort of type int32` | Port in YAML was a string | Ensure `containerPort: 8501` has no quotes |
| `ErrImagePull` | Kubernetes can't pull image | Check image name in `deployment.yaml` matches Docker Hub |
| `Completed` status on pod | App crashed at startup | Run `kubectl logs <pod-name>` to see why |

---

## 📌 Kubernetes Manifests

### deployment.yaml

- Deploys **2 replicas** of the app
- Uses image `mtousif2303/healthapp:latest`
- Resource limits: `128Mi` memory, `500m` CPU
- Exposes port `8501`

### service.yaml

- Type: `LoadBalancer`
- Routes external traffic on port `8501` to pod port `8501`
- Selector matches pods with label `app: myapp`

---

## 👤 Author

**Mohamed Tousif**
Docker Hub: [mtousif2303](https://hub.docker.com/u/mtousif2303)

---

## 📄 License

This project is for educational and portfolio purposes.
