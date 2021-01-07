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
                 sudo pip install pylint
                '''
            }

        }
        stage('test') {

            steps {
                echo 'python --version'
                sh 'pylint accessiblebookchecker/booksearch/atn_api.py'


                echo 'testvcb   fdgdfg step'
            }

        }
        stage('lint') {

            steps {
                echo 'lint step   STERG'
            }

        }
        stage('deploy') {

            steps {
                echo 'deploy step TEST'
            }

        }

    }


}