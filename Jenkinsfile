#!groovy

pipeline {

    agent any

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