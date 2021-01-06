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
                echo 'build step'
            }

        }
        stage('test') {

            steps {
                cd accessiblebookchecker/booksearch
                pylint atn_api.py
                echo 'testvcb  fdgdfg step'
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