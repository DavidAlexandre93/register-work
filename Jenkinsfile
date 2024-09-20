pipeline {
    agent any

    environment {
        COMPANY_CODE = credentials('COMPANY_CODE')
        MATRICULA = credentials('MATRICULA')
        PASSWORD = credentials('PASSWORD')
    }

    stages {
        stage('Verify Environment Variables') {
            steps {
                script {
                    echo 'Verifying environment variables...'
                    echo 'COMPANY_CODE: ****'
                    echo 'MATRICULA: ****'
                    echo 'PASSWORD: ****' // Never log the actual password
                }
            }
        }

        stage('Prepare Environment (Windows)') {
            steps {
                script {
                    echo 'Preparing environment for Windows...'
                }
            }
        }

        stage('Fix Pip Issues') {
            steps {
                script {
                    // Reinstall pip to fix potential issues with invalid distribution
                    bat '''
                    python -m pip uninstall pip setuptools -y
                    if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%
                    
                    python -m ensurepip --upgrade
                    if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%

                    python -m pip install --upgrade pip setuptools
                    if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%
                    '''
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    // Install Poetry and project dependencies
                    bat '''
                    if not exist "%APPDATA%\\Python\\Scripts\\poetry.exe" (
                        pip install poetry
                        if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%
                    )
                    '''
                    
                    // Check for pyproject.toml and install dependencies
                    bat '''
                    if exist "pyproject.toml" (
                        poetry install
                        if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%
                    ) else (
                        echo "pyproject.toml not found!"
                        exit /b 1
                    )
                    '''
                }
            }
        }

        stage('Setup ChromeDriver (Windows)') {
            steps {
                script {
                    // Attempt to get Chrome version and download the matching ChromeDriver
                    bat '''
                    setlocal EnableDelayedExpansion
                    for /f "tokens=3" %%i in ('reg query "HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon" /v version 2^>nul') do set CHROME_VERSION=%%i
                    if not defined CHROME_VERSION (
                        for /f "tokens=3" %%i in ('reg query "HKEY_LOCAL_MACHINE\\Software\\Google\\Chrome\\BLBeacon" /v version 2^>nul') do set CHROME_VERSION=%%i
                    )
                    if not defined CHROME_VERSION (
                        echo "Google Chrome is not installed or version not found!"
                        exit /b 1
                    )
                    set CHROME_VERSION=!CHROME_VERSION:~0,-2!
                    set CHROMEDRIVER_VERSION=
                    for /f %%i in ('curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE_!CHROME_VERSION!') do set CHROMEDRIVER_VERSION=%%i
                    if not defined CHROMEDRIVER_VERSION (
                        echo "Error fetching ChromeDriver version!"
                        exit /b 1
                    )
                    curl -O https://chromedriver.storage.googleapis.com/!CHROMEDRIVER_VERSION!/chromedriver_win32.zip
                    tar.exe -xf chromedriver_win32.zip
                    if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%
                    move /Y chromedriver.exe C:\\Windows\\System32\\chromedriver.exe
                    if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%
                    del chromedriver_win32.zip
                    endlocal
                    '''
                }
            }
        }

        stage('Run Selenium Script') {
            steps {
                script {
                    withEnv([
                        "COMPANY_CODE=${COMPANY_CODE}",
                        "MATRICULA=${MATRICULA}",
                        "PASSWORD=${PASSWORD}"
                    ]) {
                        bat 'poetry run python script.py'
                        if (currentBuild.result == 'FAILURE') {
                            echo 'Selenium script execution failed!'
                        }
                    }
                }
            }
        }
    }
}
