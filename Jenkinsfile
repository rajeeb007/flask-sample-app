pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds') // Jenkins Credentials ID
        DOCKER_IMAGE = "rajeeb007/flask-app"
        IMAGE_TAG = "${BUILD_ID}"
    }

    stages {
        stage('Check Git Version') {
            steps {
                script {
                    // Checking the git version
                    sh 'git --version'
                }
            }
        }
        stage('Checkout Code') {
            steps {
                git credentialsId: 'git-cred', url: 'https://github.com/rajeeb007/flask-sample-app.git', branch: 'main'
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t $DOCKER_IMAGE:$IMAGE_TAG ."
                }
            }
        }
        stage('Docker Login & Push') {
            steps {
                script {
                    sh """
                        echo "${DOCKERHUB_CREDENTIALS_PSW}" | docker login -u "${DOCKERHUB_CREDENTIALS_USR}" --password-stdin
                        docker push ${DOCKER_IMAGE}:${IMAGE_TAG}
                    """
                }
            }
        }
    }

    post {
        success {
            echo '✅ Successfully built, pushed, and deployed!'
        }
        failure {
            echo '❌ Build failed.'
        }
    }
}
