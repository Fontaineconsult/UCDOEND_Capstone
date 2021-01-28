#!groovy
def awsCredentials = [[$class: 'AmazonWebServicesCredentialsBinding',
                       credentialsId: '88651025-f487-48f4-8324-6cff583725ec']]

pipeline {
    environment {
        AWS_REGION = 'us-west-2'

    }

    agent {
        docker {
            image 'python:3.7.3-stretch'
            args '-u root:root'
        }

    }
    stages {


        stage('Install Python Dependence') {
            agent {
                docker {
                    image 'python:3.7.3-stretch'
                    args '-u root:root'
                }

            }
            steps {
                sh 'ls'
                sh 'pip install --upgrade pip'
                sh '''#!/bin/bash
                 pip install pylint
                '''
                sh 'apt-get update'

                sh 'pip install -r requirements.txt'
                sh 'pip install astroid==2.4.2'
            }

        }
        stage('Lint Python Backend') {
            agent {
                docker {
                    image 'python:3.7.3-stretch'
                    args '-u root:root'
                }

            }
            steps {
                sh 'pylint --disable=R,C,W1203 file_to_lint.py'

            }

        }

        stage('Lint Node Frontend') {

            agent {
                docker {
                    image 'python:3.7.3-stretch'
                    args '-u root:root'
                }

            }
            steps {
                sh "echo Implement Lint Node Lint"

            }

        }
        stage('Build Node') {
            agent {
                docker {
                    image 'python:3.7.3-stretch'
                    args '-u root:root'
                }

            }
            steps {
                sh "echo Build Frontend"

            }
        }
        stage('Lint Node') {

            agent {
                docker {
                    image 'python:3.7.3-stretch'
                    args '-u root:root'
                }

            }
            steps {
                sh "echo needs to be linted"

            }

        }

        stage('Build And Push Image') {
            agent any
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
                       kubectl set image deployment/capstone-green capstone-green=354922583670.dkr.ecr.us-west-2.amazonaws.com/capstone-green:latest
                      kubectl rollout restart deployment/capstone-green
                    fi

                   if [ "$deployment" == "green" ]
                    then
                      docker build -t capstone-blue:latest .
                      id=$(docker images -q | awk '{print $1}' | awk 'NR==2')
                      repo="354922583670.dkr.ecr.us-west-2.amazonaws.com/capstone-blue:latest"
                       aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 354922583670.dkr.ecr.us-west-2.amazonaws.com
                      docker tag capstone-blue:latest $repo
                      docker push $repo
                      kubectl set image deployment/capstone-blue capstone-blue=354922583670.dkr.ecr.us-west-2.amazonaws.com/capstone-blue:latest
                      kubectl rollout restart deployment/capstone-blue
                   fi

                    '''
            }

        }
        stage('Switch Load Balancer') {
            agent any
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
        stage('Clean Up') {
            agent any
            steps {

                sh '''
                IMAGES_TO_DELETE=$( aws ecr list-images --region us-west-2 --repository-name capstone-blue --filter "tagStatus=UNTAGGED" --query 'imageIds[*]' --output json )
                aws ecr batch-delete-image --region us-west-2 --repository-name $ECR_REPO --image-ids "$IMAGES_TO_DELETE" || true

                IMAGES_TO_DELETE=$( aws ecr list-images --region us-west-2 --repository-name capstone-green --filter "tagStatus=UNTAGGED" --query 'imageIds[*]' --output json )
                aws ecr batch-delete-image --region us-west-2 --repository-name $ECR_REPO --image-ids "$IMAGES_TO_DELETE" || true
                    '''



            }

        }

    }

}

//pipeline {
//
//    environment {
//        AWS_REGION = 'us-west-2'
//
//    }
//    agent any
//    stages {
//
//
//        stage('Build And Push Image') {
//            agent any
//            steps {
//                sh '''
//
//                    deployment=$(kubectl get service capstone-app -o=jsonpath={.spec.selector.app})
//
//                    if [ "$deployment" == "blue" ]
//                    then
//                       docker build -t capstone-green:latest .
//                       id=$(docker images -q | awk '{print $1}' | awk 'NR==2')
//                       repo="354922583670.dkr.ecr.us-west-2.amazonaws.com/capstone-green:latest"
//                       aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 354922583670.dkr.ecr.us-west-2.amazonaws.com
//                       docker tag capstone-green:latest $repo
//                       docker push $repo
//                       kubectl set image deployment/capstone-green capstone-green=354922583670.dkr.ecr.us-west-2.amazonaws.com/capstone-green:latest
//                      kubectl rollout restart deployment/capstone-green
//                    fi
//
//                   if [ "$deployment" == "green" ]
//                    then
//                      docker build -t capstone-blue:latest .
//                      id=$(docker images -q | awk '{print $1}' | awk 'NR==2')
//                      repo="354922583670.dkr.ecr.us-west-2.amazonaws.com/capstone-blue:latest"
//                       aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 354922583670.dkr.ecr.us-west-2.amazonaws.com
//                      docker tag capstone-blue:latest $repo
//                      docker push $repo
//                      kubectl set image deployment/capstone-blue capstone-blue=354922583670.dkr.ecr.us-west-2.amazonaws.com/capstone-blue:latest
//                      kubectl rollout restart deployment/capstone-blue
//                   fi
//
//                    '''
//            }
//
//        }
//        stage('Switch Load Balancer') {
//            agent any
//            steps {
//
//                  sh '''
//                    deployment=$(kubectl get service capstone-app -o=jsonpath={.spec.selector.app})
//
//                    if [ "$deployment" == "blue" ]
//                    then
//                    kubectl patch service capstone-app -p '{"spec":{"selector":{"app": "green"}}}'
//                    fi
//
//                   if [ "$deployment" == "green" ]
//                    then
//                    kubectl patch service capstone-app -p '{"spec":{"selector":{"app": "blue"}}}'
//                   fi
//
//                    '''
//                  sh 'echo $deployment'
//
//            }
//
//        }
//        stage('Clean Up') {
//            agent any
//            steps {
//
//                sh '''
//                IMAGES_TO_DELETE=$( aws ecr list-images --region us-west-2 --repository-name capstone-blue --filter "tagStatus=UNTAGGED" --query 'imageIds[*]' --output json )
//                aws ecr batch-delete-image --region us-west-2 --repository-name $ECR_REPO --image-ids "$IMAGES_TO_DELETE" || true
//
//                IMAGES_TO_DELETE=$( aws ecr list-images --region us-west-2 --repository-name capstone-green --filter "tagStatus=UNTAGGED" --query 'imageIds[*]' --output json )
//                aws ecr batch-delete-image --region us-west-2 --repository-name $ECR_REPO --image-ids "$IMAGES_TO_DELETE" || true
//                    '''
//
//
//
//            }
//
//        }
//    }
//
//
//}