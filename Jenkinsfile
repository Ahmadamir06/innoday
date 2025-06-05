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
                    // Use the SonarQube Scanner step, not the shell command
                    // This uses the scanner installed/configured in Jenkins tools
                    sonarScanner(
                        extraProperties: """
                            sonar.projectKey=Innovation_day
                            sonar.sources=.
                        """
                    )
                }
            }
        }

        stage('Quality Gate ') {
            steps {
                timeout(time: 1, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }
}
