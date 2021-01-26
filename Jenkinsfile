#!groovy
def awsCredentials = [[$class: 'AmazonWebServicesCredentialsBinding',
                       credentialsId: '88651025-f487-48f4-8324-6cff583725ec']]




//pipeline {
//
//
//    agent {
//        docker {
//            image 'python:3.7.3-stretch'
//            args '-u root:root'
//        }
//
//    }
//    stages {
//
//
//        stage('install') {
//
//            steps {
//                sh 'ls'
//                sh 'pip install --upgrade pip'
//                sh '''#!/bin/bash
//                 pip install pylint
//                '''
//                sh 'apt-get update'
//
//
//
////                sh 'pip install -r requirements.txt'
////                sh 'pip install astroid==2.4.2'
//            }
//
//        }
//        stage('lint') {
//
//
//            steps {
//                echo 'needs to be linted'
//
//            }
//
//        }
//        stage('test') {
//
//            steps {
//                echo 'lint step   STERG'
//
//            }
//
//        }
//
//
//
//
//
//
//
//
//    }
//
//
//}

pipeline {

    environment {
        AWS_REGION = 'us-west-2'

    }
    agent any
    stages {


        stage('Build And Push Image') {

            steps {
                sh '''
                    
                    deployment=$(kubectl get service capstone-app -o=jsonpath={.spec.selector.app})
                    
                    if [ "$deployment" == "blue" ]
                    then
                       docker build -t capstone-green:latest .
                       id=$(docker images -q | awk '{print $1}' | awk 'NR==2')
                       repo="354922583670.dkr.ecr.us-west-2.amazonaws.com/capstone-green:latest"
                       aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 354922583670.dkr.ecr.us-west-2.amazonaws.com
                       docker tag capstone-green:latest $repo
                       docker push $repo
                       kubectl set image Deployment/capstone-green app-container=354922583670.dkr.ecr.us-west-2.amazonaws.com/capstone-green:latest
                      
                    fi
                         
                   if [ "$deployment" == "green" ]
                    then
                      docker build -t capstone-blue:latest .
                      id=$(docker images -q | awk '{print $1}' | awk 'NR==2')
                      repo="354922583670.dkr.ecr.us-west-2.amazonaws.com/capstone-blue:latest"
                       aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 354922583670.dkr.ecr.us-west-2.amazonaws.com
                      docker tag capstone-blue:latest $repo
                      docker push $repo
                      kubectl set image Deployment/capstone-blue app-container=354922583670.dkr.ecr.us-west-2.amazonaws.com/capstone-blue:latest
                      
                   fi                    
                    
                    '''
            }

        }

        stage('Switch Load Balancer') {

            steps {

                  sh '''
                    deployment=$(kubectl get service capstone-app -o=jsonpath={.spec.selector.app})
                    
                    if [ "$deployment" == "blue" ]
                    then
                    kubectl patch service capstone-app -p '{"spec":{"selector":{"app": "green"}}}'
                    fi
                         
                   if [ "$deployment" == "green" ]
                    then
                    kubectl patch service capstone-app -p '{"spec":{"selector":{"app": "blue"}}}'
                   fi                    
                   
                    '''
                  sh 'echo $deployment'

            }

        }
    }


}