pipeline{
    agent any

    options{
        buildDiscarder(logRotator(
            numToKeepStr : '10',
            artifactNumToKeepStr: '5'
        ))
        
        
    }
  
    stages{
        stage('checkout'){
            steps{
                echo 'Project checked out successfully'
            }
        }
        stage('setup python'){
            steps{
                bat '''
                if not exist ".venv\\Scripts\\python.exe" (
                "C:\\Users\\Koushik\\AppData\\Local\\Programs\\Python\\Python314\\python.exe" -m venv .venv
                if errorlevel 1 exit /b 1
                )
                '''
            }
        }
        stage('install dependencies'){
            steps{
                bat '''
                .venv\\Scripts\\python.exe -m pip install -r requirements.txt
                if errorlevel 1 exit /b 1 
                echo dependencies installed successfully
                '''
            }
        }
        stage('Run tests'){
            steps{
                bat '''
                set PLAYWRIGHT_BROWSERS_PATH=C:\\Users\\Koushik\\AppData\\Local\\ms-playwright
                .venv\\Scripts\\python.exe -m pytest tests\\test_login.py -v --html=login_report.html --self-contained-html
                if errorlevel 1 exit /b 1
                '''
            }
        }

        stage('publish report'){
            steps{
                publishHTML(target:[
                    reportDir : '.',
                    reportFiles:'login_report.html',
                    reportName : 'playwright test report',
                    keepAll : true,
                    allowMissing : false
                ])
            }
        }
    }
}