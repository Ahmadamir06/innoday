pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo 'Building the project...'
                sh 'ls -la'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('MyLocalSonar') {
                    script {
                        def scannerHome = tool 'SonarQube Scanner'
                        sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=Innovation_day -Dsonar.sources=appdemo"
                    }
                }
            }
        }

        stage('Save SonarQube Results') {
            steps {
                echo 'Saving SonarQube analysis JSON results...'
                sh '''
                    mkdir -p agent
                    curl -s -u <SONARQUBE_USER>:<SONARQUBE_TOKEN> \
                    "http://localhost:9000/api/measures/component?component=Innovation_day&metricKeys=coverage,bugs,vulnerabilities" \
                    -o agent/sonarqube-results.json
                '''
            }
        }

        stage('Quality Gate ') {
            steps {
                timeout(time: 10, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }
}
