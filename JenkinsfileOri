pipeline {
  agent any

  environment {
    IMAGE_NAME = "texsa/flask-app"
    IMAGE_TAG = "latest"
    NAMESPACE = "dev"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build Docker Image') {
      steps {
        sh 'docker build -t $IMAGE_NAME:$IMAGE_TAG .'
      }
    }

    stage('Push Docker Image') {
      steps {
        script {
          withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
            sh 'echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin'
            sh 'docker push $IMAGE_NAME:$IMAGE_TAG'
          }
        }
      }
    }
    
    stage('Deploy to Dev') {
      steps {
        sh 'kubectl apply -f namespace.yaml'
        sh 'kubectl apply -f dev-configmap.yaml'
        sh 'kubectl apply -f dev-secret.yaml'
        sh 'helm upgrade --install flask-dev ./helm-chart --namespace dev'
      }
    }


    stage('Approve Prod') {
    steps {
        input message: "Deploy to Production?", ok: "Yes, Deploy to Prod"
      }
    }

    stage('Deploy to Prod') {
    steps {
        sh 'kubectl apply -f prod-configmap.yaml'
        sh 'kubectl apply -f prod-secret.yaml'
	sh 'helm upgrade --install flask-prod ./helm-chart --namespace prod'
      }
    }
  }
}
