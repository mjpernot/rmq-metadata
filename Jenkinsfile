pipeline {
    agent any
    stages {
        stage('build') {
            steps {
                sh 'python --version'
            }
        }
        stage('Test') {
            steps {
                dir ('lib') {
                    git branch: "mod/294", credentialsId: "2cfb403c-be21-4fac-94d7-c8cd5c531feb", url: "https://gitlab.code.dicelab.net/JAC-IDM/python-lib.git"
                }
                dir ('rabbit_lib') {
                    git branch: "mod/221", credentialsId: "2cfb403c-be21-4fac-94d7-c8cd5c531feb", url: "https://gitlab.code.dicelab.net/JAC-IDM/rabbitmq-lib.git"
                }
                dir ('mongo_lib') {
                    git branch: "mod/422", credentialsId: "2cfb403c-be21-4fac-94d7-c8cd5c531feb", url: "https://gitlab.code.dicelab.net/JAC-IDM/mongo-lib.git"
                }
                dir ('mongo_lib/lib') {
                    git branch: "mod/294", credentialsId: "2cfb403c-be21-4fac-94d7-c8cd5c531feb", url: "https://gitlab.code.dicelab.net/JAC-IDM/python-lib.git"
                }
                sh """
                virtualenv test_env
                source test_env/bin/activate
                pip2 install Pillow==6.2.2 --user
                pip2 install PyPDF2==1.26.0 --user
                pip2 install mock==2.0.0 --user
                pip2 install nltk==3.4.0 --user
                pip2 install pdfminer==20191010 --user
                pip2 install pika==1.2.0 --user
                pip2 install psutil==5.4.3 --user
                pip2 install pymongo==3.8.0 --user
                pip2 install simplejson==2.0.9 --user
                pip2 install soupsieve==1.9.6 --user
                pip2 install textract==1.6.3 --user
                /usr/bin/python ./test/unit/rmq_metadata/convert_data.py
                /usr/bin/python ./test/unit/rmq_metadata/create_metadata.py
                /usr/bin/python ./test/unit/rmq_metadata/extract_pdf.py
                /usr/bin/python ./test/unit/rmq_metadata/find_tokens.py
                /usr/bin/python ./test/unit/rmq_metadata/get_pdfminer_data.py
                /usr/bin/python ./test/unit/rmq_metadata/get_pypdf2_data.py
                /usr/bin/python ./test/unit/rmq_metadata/get_textract_data.py
                /usr/bin/python ./test/unit/rmq_metadata/help_message.py
                /usr/bin/python ./test/unit/rmq_metadata/main.py
                /usr/bin/python ./test/unit/rmq_metadata/merge_data.py
                /usr/bin/python ./test/unit/rmq_metadata/monitor_queue.py
                /usr/bin/python ./test/unit/rmq_metadata/non_proc_msg.py
                /usr/bin/python ./test/unit/rmq_metadata/pdf_to_string.py
                /usr/bin/python ./test/unit/rmq_metadata/process_message.py
                /usr/bin/python ./test/unit/rmq_metadata/process_msg.py
                /usr/bin/python ./test/unit/rmq_metadata/read_pdf.py
                /usr/bin/python ./test/unit/rmq_metadata/run_program.py
                /usr/bin/python ./test/unit/rmq_metadata/sort_data.py
                /usr/bin/python ./test/unit/rmq_metadata/summarize_data.py
                /usr/bin/python ./test/unit/rmq_metadata/validate_create_settings.py
                /usr/bin/python ./test/unit/rmq_metadata/validate_files.py
                /usr/bin/python ./test/unit/daemon_rmq_metadata/is_active.py
                /usr/bin/python ./test/unit/daemon_rmq_metadata/main.py
                deactivate
                rm -rf test_env
                """
            }
        }
        stage('SonarQube analysis') {
            steps {
                sh './test/unit/sonarqube_code_coverage.sh'
                sh 'rm -rf lib'
                sh 'rm -rf rabbit_lib'
                sh 'rm -rf mongo_lib'
                script {
                    scannerHome = tool 'sonar-scanner';
                }
                withSonarQubeEnv('Sonar') {
                    sh "${scannerHome}/bin/sonar-scanner -Dproject.settings=sonar-project.JACIDM.properties"
                }
            }
        }
        stage('Artifactory upload') {
            steps {
                script {
                    server = Artifactory.server('Artifactory')
                    server.credentialsId = 'art-svc-highpoint-dev'
                    uploadSpec = """{
                        "files": [
                            {
                                "pattern": "./*.py",
                                "recursive": false,
                                "excludePatterns": [],
                                "target": "pypi-proj-local/highpoint/rmq-metadata/"
                            },
                            {
                                "pattern": "./*.txt",
                                "recursive": false,
                                "excludePatterns": [],
                                "target": "pypi-proj-local/highpoint/rmq-metadata/"
                            },
                            {
                                "pattern": "./*.md",
                                "recursive": false,
                                "excludePatterns": [],
                                "target": "pypi-proj-local/highpoint/rmq-metadata/"
                            },
                            {
                                "pattern": "*.TEMPLATE",
                                "recursive": true,
                                "excludePatterns": [],
                                "target": "pypi-proj-local/highpoint/rmq-metadata/config/"
                            }
                        ]
                    }"""
                    server.upload(uploadSpec)
                }
            }
        }
    }
    post {
        always {
            cleanWs disableDeferredWipeout: true
        }
    }
}
