#!groovy

pipeline {

    agent {
        docker {
            image 'python:3.7.3-stretch'
        }
    }

    stages {

        stage('build') {

            steps {
                sh 'ls'
                sh 'python --version'
                bash 'sudo pip install pylint --user'
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