pipeline{
    agent any
    stages{
        stage("code"){
            steps{
                echo "cloning the code from git"
                git url: "https://github.com/lovepandit/pythonflask.git" , branch: "main"
            }
        }
        stage("build"){
            steps{
                echo "build the image"
                sh "docker build -t flask-temp ."
            }
        }
        stage("push"){
            steps{
                echo "pushing image to dockerhub"
                withCredentials([usernamePassword(credentialsId:"tglp42723",passwordVariable:"passvar",usernameVariable:"uservar")]){
                    sh "docker tag flask-temp ${env.uservar}/flask-temp:latest"
                    sh "docker login -u ${env.uservar} -p ${env.passvar}"
                    sh "docker push ${env.uservar}/flask-temp:latest"
                }
            }
        }
        stage("deploy"){
            steps{
                echo "deploying the container"
                sh  "docker-compose down && docker-compose up -d"
            }
        }
    }
}
