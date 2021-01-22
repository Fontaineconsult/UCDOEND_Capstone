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

//
//        stage('build image') {
//
//            steps {
//                sh 'aws s3 ls'
//                sh ' docker build -t capstone-test .'
//
//            }
//
//
//        }

        stage('upload image') {


            steps {
                sh 'aws s3 ls'
                sh 'kubectl delete-cluster minikube'
                sh 'kubectl config set-cluster cap3 --server=https://365E2C3E7B69BF167DE75EB24BEE0EEF.yl4.us-west-2.eks.amazonaws.com'
                sh 'kubectl config get-clusters'
                sh 'kubectl get pods'
            }

        }
    }


}