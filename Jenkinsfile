pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds') // Jenkins Credentials ID
        DOCKER_IMAGE = "rajeeb007/flask-app"
        IMAGE_TAG = "latest"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git 'https://github.com/rajeeb007/flask-sample-app.git'
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
