
pipeline {
    agent any

    environment {
        IMAGE_NAME = 'rithikarajanish/diet-recommendation-system'
        IMAGE_TAG = 'latest'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo 'Source code checked out successfully.'
            }
        }

        stage('Build and Test') {
            steps {
                sh '''
                    set -eu

                    echo "Checking Python version..."
                    python3 --version

                    echo "Checking Python syntax..."
                    python3 -m py_compile app.py A_star.py Inference_engine.py

                    echo "Checking required files..."
                    test -f requirements.txt
                    test -f Dockerfile
                    test -f Data/Food_data.json
                    test -f Data/Rules.json

                    echo "Build and Test checks passed."
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    set -eu
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        set -eu
                        trap 'docker logout >/dev/null 2>&1 || true' EXIT

                        echo "$DOCKER_PASS" | docker login \
                            --username "$DOCKER_USER" \
                            --password-stdin

                        docker push ${IMAGE_NAME}:${IMAGE_TAG}
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    set -eu
                    kubectl apply -f k8s/
                    kubectl rollout status deployment/diet-recommendation \
                        --timeout=180s
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                    set -eu
                    kubectl get deployments
                    kubectl get pods
                    kubectl get services
                '''
            }
        }
    }

    post {
        success {
            echo 'CI/CD pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check Console Output for the first error.'
        }
    }
}
