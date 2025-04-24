pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds') // Jenkins Credentials ID
        DOCKER_IMAGE = "rajeeb007/flask-app"
        IMAGE_TAG = "${BUILD_ID}"
        NAMESPACE = "flask-app"
        MINIKUBE_KUBECONFIG = credentials('config')  // Minikube config file credential
        kubeconfig_path = "/home/rajeeb/.kube/config"
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
                    // Set the KUBECONFIG environment variable using the Minikube credential
                    //writeFile(file: '/tmp/kubeconfig', text: MINIKUBE_KUBECONFIG)
                    //sh "export KUBECONFIG=/tmp/kubeconfig"

                    // Ensure namespace exists
                    // sh "kubectl get ns $NAMESPACE || kubectl create ns $NAMESPACE"
                    
                    sh "kubectl --kubeconfig=${kubeconfig_path} apply -f ./k8s/deployment.yaml"

                    // Replace the image tag dynamically in the deployment file and apply
                    //sh """
                      //  sed 's/\${BUILD_ID}/$IMAGE_TAG/g' k8s/deployment.yml | kubectl apply -n $NAMESPACE -f -
                        //kubectl apply -n $NAMESPACE -f k8s/service.yml
                    //"""

                    // Optional: check if pods are running
                   // sh "kubectl get pods -n $NAMESPACE"
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
