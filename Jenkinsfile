#!groovy
def awsCredentials = [[$class: 'AmazonWebServicesCredentialsBinding',
                       credentialsId: '88651025-f487-48f4-8324-6cff583725ec']]




pipeline {

    environment {
        AWS_REGION = 'us-west-2'

    }

    options {
        withCredentials(awsCredentials)
    }

    agent {
        docker {
            image 'python:3.7.3-stretch'
            args '-u root:root'
        }
    }

    stages {

//        stage('Initialize'){
//
//            steps{
//                def dockerHome = tool 'JenkinsDocker'
//                env.PATH = "${dockerHome}/bin:${env.PATH}"
//            }
//
//
//        }

        stage('install') {

            steps {
                sh 'ls'
                sh 'pip install --upgrade pip'
                sh '''#!/bin/bash
                 pip install pylint
                '''
                sh 'apt-get update'
                sh 'apt-get install -y awscli'
//                sh 'apt-get install -y docker'

//                sh 'pip install -r requirements.txt'
//                sh 'pip install astroid==2.4.2'
            }

        }
        stage('lint') {


            steps {
                echo 'needs to be linted'

            }

        }
        stage('test') {

            steps {
                echo 'lint step   STERG'

            }

        }
        stage('build image') {

            steps {
                sh 'aws s3 ls'
                sh 'docker build capstone-test . '

                script {

                    dockerImage = docker.build "test" + ":$BUILD_NUMBER"

                }

            }

        }

        stage('upload image') {

            steps {
                sh 'aws s3 ls'
                sh 'docker images'

            }

        }

    }


}