# Diet Recommendation System

## Project Overview
The Diet Recommendation System is a Python-based web application designed to provide diet and food recommendations based on user inputs, dietary preferences, and nutritional goals.

## Objectives
- Develop an interactive diet recommendation application.
- Use Python to implement recommendation logic.
- Containerize the application using Docker.
- Automate build, test, and deployment steps using Jenkins.
- Deploy and verify the application using Kubernetes on Minikube hosted on AWS EC2.

## Technologies Used
- **Python** — application logic
- **Streamlit** — web interface
- **Git and GitHub** — version control and source code hosting
- **Docker** — containerization
- **Docker Hub** — container image registry
- **Jenkins** — CI/CD pipeline automation
- **Kubernetes and Minikube** — application deployment and orchestration
- **AWS EC2** — cloud-hosted environment

## Project Structure
- `app.py` — main Streamlit application
- `A_star.py` — recommendation/search logic
- `Inference_engine.py` — inference and recommendation logic
- `requirements.txt` — Python dependencies
- `Dockerfile` — instructions to build the Docker image
- `Jenkinsfile` — automated CI/CD pipeline
- `Data/` — food and recommendation rule data
- `k8s/` — Kubernetes deployment and service configuration

## Running the Application Locally
1. Install Python.
2. Clone this repository.
3. Install the dependencies:
   `pip install -r requirements.txt`
4. Start the application:
   `python -m streamlit run app.py`
5. Open the local URL displayed in the terminal.

## Docker
Build the Docker image:

`docker build -t rithikarajanish/diet-recommendation-system:latest .`

Run the container:

`docker run -p 8501:8501 rithikarajanish/diet-recommendation-system:latest`

## CI/CD Pipeline
The Jenkins pipeline performs the following stages:

1. Checkout source code from GitHub.
2. Check Python syntax and required project files.
3. Build the Docker image.
4. Authenticate with Docker Hub using Jenkins credentials and push the image.
5. Apply Kubernetes configuration files.
6. Verify the deployment, pods, and services.

## Kubernetes Deployment
The Kubernetes configuration is stored in the `k8s/` directory. It defines the application deployment and a NodePort service.

The deployment was verified using Kubernetes commands, including:

- `kubectl get deployments`
- `kubectl get pods`
- `kubectl get services`

## CI/CD Verification
A code change was committed and pushed to GitHub, followed by another Jenkins build. The updated pipeline completed successfully.

## Conclusion
This project demonstrates the integration of a Python web application with Git-based version control, Docker containerization, Jenkins CI/CD automation, and Kubernetes deployment in a cloud-hosted environment.
