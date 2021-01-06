#!groovy

pipeline {

    agent {
        docker {
            image 'ubuntu'
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