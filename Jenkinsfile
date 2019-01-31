node {
    if (!(env.BRANCH_NAME == 'master' || env.BRANCH_NAME.startsWith('PR'))){
        echo 'Not a PR or main branch. Skip build.'
        currentBuild.result = 'SUCCESS'
        return
    }

    def server = Artifactory.server 'ART'
    def buildInfo
    def warnings

    stage ('Clone') {
        checkout scm
    }

    stage ('Static analysis') {
        sh 'rm -f flake8report.txt'
        sh 'python3 -m flake8 --exit-zero --output-file=flake8report.txt'
        sh 'mkdir -p target'
        sh 'echo "flake8_warnings: `wc -l < flake8report.txt`" > target/result.yml'
        archiveArtifacts 'flake8report.txt'
        warnings = readYaml file: 'target/result.yml'
        echo "Flake8 warnings count: ${warnings.flake8_warnings}"
    }

    stage ('Ratcheting') {
        def downloadSpec = """{
            "files": [
                {
                    "pattern": "rest-msg/*/result.yml",
                    "build": "rest-msg :: master/LATEST",
                    "target": "previous.yml",
                    "flat": "true"
                }
            ]
        }"""
        server.download spec: downloadSpec
        //def oldWarnings = readYaml file: 'previous.yml'
        //if (warnings.flake8_warnings > oldWarnings.flake8_warnings) {
        //   error "Number of flake8 warnings ${warnings.flake8_warnings} is greater than previous ${oldWarnings.flake8_warnings}."
        //}
    }

    if (env.BRANCH_NAME == 'master') {
        stage('Build py dist') {
            sh 'python setup.py sdist'
        }

        stage ('Publish dist') {
            def uploadSpec = """{
                "files": [
                {
                    "pattern": "dist/swagger_server-*",
                    "target": "rest-msg/${currentBuild.number}/",
                    "props": "flake8.warnings=${warnings.flake8_warnings}"
                },
                {
                   "pattern": "target/result.yml",
                    "target": "rest-msg/${currentBuild.number}/",
                    "props": "flake8.warnings=${warnings.flake8_warnings}"
                }
                ]
            }"""
            buildInfo = server.upload spec: uploadSpec
            buildInfo.env.capture = true
            server.publishBuildInfo buildInfo
        }
    }
}
