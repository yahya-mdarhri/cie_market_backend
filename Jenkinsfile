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
                        error "❌ Docker is not installed on this Jenkins agent."
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

        stage('Login to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'docker-hub-credentials',
                    usernameVariable: 'hossine',
                    passwordVariable: 'dckr_pat_H7bnJ3xsmMQ3SgTIcMG9bz-T_Yw'
                )]) {
                    sh 'echo $DOCKER_HUB_PASS | docker login -u $DOCKER_HUB_USER --password-stdin'
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
