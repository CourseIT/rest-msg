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

    if (env.BRANCH_NAME == 'master') {
        stage('Build py dist') {
            sh 'python3 setup.py sdist upload -r course'
        }
    }
}
