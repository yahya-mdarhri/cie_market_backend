pipeline {
    agent any

    environment {
        IMAGE_NAME = 'hossine/cie-market-backend'
        TAG = 'latest'
        HEROKU_APP = 'backendciemarket'
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
                echo "✅ Tests would run here inside Docker container."
                // You can add real tests if you have them
            }
        }

        stage('Login to Heroku') {
            steps {
                withCredentials([
                    string(credentialsId: 'heroku-api-key', variable: 'HEROKU_API_KEY')
                ]) {
                    sh 'echo $HEROKU_API_KEY | docker login --username=_ --password-stdin registry.heroku.com'
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

        stage('Tag and Push to Heroku') {
            steps {
                script {
                    def herokuImage = "registry.heroku.com/${HEROKU_APP}/web"
                    sh """
                        docker build --platform=linux/amd64 -t registry.heroku.com/backendciemarket/web . --provenance=false
                        docker push registry.heroku.com/backendciemarket/web
                        heroku container:release web --app backendciemarket
                    """
                }
            }
        }

        stage('Release Heroku App') {
            steps {
                withCredentials([
                    string(credentialsId: 'heroku-api-key', variable: 'HEROKU_API_KEY')
                ]) {
                    sh "heroku container:release web --app backendciemarket"
                }
            }
        }
    }

    post {
        always {
            sh 'docker logout'
        }
    }
}
