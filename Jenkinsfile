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

        stage('install') {

            steps {
                sh 'ls'
                sh 'python --version'
                sh '''#!/bin/bash
                 pip install pylint
                '''
                sh 'pip install -r requirements.txt'
                sh 'pip install astroid==2.4.2'
            }

        }
        stage('lint') {

            steps {
                echo 'python --version'
                sh 'pylint file_to_lint.py'
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
                echo 'deploy step TEST'
            }

        }

    }


}