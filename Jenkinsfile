pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds') // Jenkins Credentials ID
        DOCKER_IMAGE = "rajeeb007/flask-app"
        IMAGE_TAG = "${BUILD_ID}"
        NAMESPACE = "flask-app"
        kubeconfig_path = "/var/lib/jenkins/.kube/config"
    }

    stages {
        stage('Check Git Version') {
            steps {
                script {
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

        stage('Deploy to Minikube') {
            steps {
                script {
                    
                    
                    sh "kubectl --kubeconfig=${kubeconfig_path} apply -f ./k8s/deployment.yml"

                    
                }
            }
        }
    }

    post {
        success {
            echo '✅ Successfully built, pushed to Docker Hub, and deployed to Minikube!'
        }
        failure {
            echo '❌ Build or deployment failed.'
        }
    }
}
