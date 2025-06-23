pipeline {
    agent any
    environment {
        DOCKER_IMAGE_NAME = "texsa/flask-app"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Prepare & Build Image') {
            steps {
                script {
                    def IMAGE_TAG
                    if (env.TAG_NAME) {
                        echo "Build dipicu oleh Tag: ${env.TAG_NAME}. Mempersiapkan rilis Produksi."
                        IMAGE_TAG = env.TAG_NAME
                    } else {
                        echo "Build dipicu oleh Branch: ${env.BRANCH_NAME}. Mempersiapkan rilis Pengembangan."
                        IMAGE_TAG = "dev-v${env.BUILD_NUMBER}"
                    }
                    env.IMAGE_TAG = IMAGE_TAG
                    echo "Membangun image: ${DOCKER_IMAGE_NAME}:${IMAGE_TAG}"
                    sh "docker build -t ${DOCKER_IMAGE_NAME}:${IMAGE_TAG} ."
                }
            }
        }


        stage('Push Docker Image') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh 'echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin'
                        sh "docker push ${env.DOCKER_IMAGE_NAME}:${env.IMAGE_TAG}"
                    }
                }
            }
        }
    


        stage('Deploy to Dev') {
            when {
                branch 'main'
            }
            steps {
                echo "Mendeploy image ${DOCKER_IMAGE_NAME}:${env.IMAGE_TAG} ke lingkungan Dev..."
                sh 'kubectl apply -f namespace.yaml'
                sh 'kubectl apply -f dev-configmap.yaml'
                sh 'kubectl apply -f dev-secret.yaml'

                sh "helm upgrade --install flask-dev ./helm-chart --namespace dev --set image.tag=${env.IMAGE_TAG}"
            }
        }


        stage('Deploy to Prod') {
            when {
                tag "v*.*.*"
            }
            steps {
                echo "Mendeploy image ${DOCKER_IMAGE_NAME}:${env.IMAGE_TAG} ke lingkungan Prod..."
                sh 'kubectl apply -f prod-configmap.yaml'
                sh 'kubectl apply -f prod-secret.yaml'

                sh "helm upgrade --install flask-prod ./helm-chart --namespace prod --set image.tag=${env.IMAGE_TAG}"
            }
        }
    }
}
