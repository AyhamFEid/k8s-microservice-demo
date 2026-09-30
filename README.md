# Kubernetes Microservice Demo (`k8s-microservice-demo`)

This project sets up a lightweight, containerized Python Flask API microservice configured for local deployment inside **Minikube** or **Kind**. It demonstrates application lifecycle probes, resource definitions, and data persistence using a `PersistentVolumeClaim`.

---

## 🏗️ Architecture

```
       [ Client Request ]
               │
               ▼
     [ Service: NodePort ] (Port: 30080)
               │
       ┌───────┴───────┐
       ▼               ▼
   [ Pod 1 ]       [ Pod 2 ]  <─── (Deployment: 2 Replicas)
  (Flask App)     (Flask App)
       │               │
       └───────┬───────┘
               ▼
     [ PersistentVolume ] <─── [ PersistentVolumeClaim ]
```

*   **Application Layer:** A tiny Python API running on [Flask](https://flask.palletsprojects.com/) exposing paths for the main business logic (`/`), liveness check (`/healthz`), and readiness status (`/ready`).
*   **Orchestration (Kubernetes):**
    *   **Deployment:** Coordinates 2 redundant replicas of the container, enforces CPU/Memory boundary controls, and monitors application lifecycle via automated HTTP probes.
    *   **PersistentVolumeClaim (PVC):** Allocates block storage dynamically, mounted into `/data` across the containers to keep track of a visual counter file (`clicks.txt`).
    *   **Service (NodePort):** Standardizes internal internal cluster networking while exposing an external mapping boundary on port `30080` for easy hosting checkouts.

---

## 🚀 Execution & Run Instructions

Ensure you have [Docker](https://www.docker.com/) and either **Minikube** or **Kind** configured beforehand.

### Option A: Running on Minikube

1. **Start the local cluster:**
   ```bash
   minikube start
   ```
2. **Point your shell to Minikube's in-cluster Docker daemon:**
   ```bash
   eval $(minikube docker-env)
   ```
3. **Build the container image directly into the cluster environment:**
   ```bash
   docker build -t k8s-microservice-demo:latest .
   ```
4. **Apply the combined manifests configuration:**
   ```bash
   kubectl apply -f k8s-manifests.yaml
   ```
5. **Access the exposed web application interface:**
   ```bash
   minikube service demo-app-service --url
   # Or directly curl via NodePort
   curl $(minikube ip):30080
   ```

### Option B: Running on Kind

1. **Create the cluster with a configured NodePort map:**
   ```bash
   kind create cluster --name demo-cluster
   ```
2. **Build the local docker container image:**
   ```bash
   docker build -t k8s-microservice-demo:latest .
   ```
3. **Sideload the custom container image into your cluster context:**
   ```bash
   kind load docker-image k8s-microservice-demo:latest --name demo-cluster
   ```
4. **Deploy the declarative manifests:**
   ```bash
   kubectl apply -f k8s-manifests.yaml
   ```

---

## 📊 Deployment Verification

### Status of Pods (`kubectl get pods`)
```text
NAME                                   READY   STATUS    RESTARTS   AGE
demo-app-deployment-5fd9b646c7-7w2mx   1/1     Running   0          45s
demo-app-deployment-5fd9b646c7-m9z8p   1/1     Running   0          45s
```

### Verifying Resource Status Hierarchy
To confirm that storage mounts, mappings, and network infrastructure match expectations, query all related elements:
```bash
kubectl get deployments,services,pvc
```
