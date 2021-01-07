#!groovy

pipeline {

    agent {
        docker {
            image 'python:3.7.3-stretch'
            args '-u root:root'
        }
    }

    stages {

        stage('build') {

            steps {
                sh 'ls'
                sh 'python --version'
                sh '''#!/bin/bash
                 pip install pylint
                '''
            }

        }
        stage('lint') {

            steps {
                echo 'python --version'
                sh 'pylint lint_dummy.py'

                echo 'testvcb   fdgdfg step'
            }

        }
        stage('test') {

            steps {
                echo 'lint step   STERG'
            }

        }
        stage('build image') {

            steps {
                echo 'deploy step TEST'
            }

        }

    }


}