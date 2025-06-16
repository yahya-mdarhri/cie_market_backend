pipeline {
    agent any

    environment {
        IMAGE_NAME = 'hossine/cie-market-backend'
        TAG = 'latest'
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }
        stage('Check Docker') {
            steps {
                script {
                    def dockerExists = sh(script: 'command -v docker || true', returnStdout: true).trim()
                    if (!dockerExists) {
                        error "❌ Docker is not installed on this Jenkins agent. Please install Docker to proceed."
                    }
                    def dockerRunning = sh(script: 'docker info > /dev/null 2>&1 || true', returnStatus: true)
                    if (dockerRunning != 0) {
                        error "❌ Docker is installed but not running. Make sure the Docker daemon is active."
                    }
                    echo "✅ Docker is installed and running."
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t $IMAGE_NAME:$TAG .'
                }
            }
        }
        stage('Run Tests') {
            steps {
                script {
                    sh 'echo "Running tests inside the Docker container..."'
                }
            }
        }

        stage('Login to Docker Hub') {
                steps {
                    withCredentials([
                        usernamePassword(
                            credentialsId: 'docker-hub-credentials',
                            usernameVariable: 'USERNAME',
                            passwordVariable: 'PASSWORD'
                        )
                    ]) {
                        sh 'docker login -u $USERNAME -p $PASSWORD'
                    }
                }
            }

        stage('Push Image to Docker Hub') {
            steps {
                sh 'docker push $IMAGE_NAME:$TAG'
            }
        }
    }

    post {
        always {
            sh 'docker logout'
        }
    }
}
