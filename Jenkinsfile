@Library('pipelinex@development')
import com.iguazio.pipelinex.DockerRepo

properties([
    buildDiscarder(logRotator(artifactDaysToKeepStr: '', artifactNumToKeepStr: '', daysToKeepStr: '30', numToKeepStr: '1000')),
    disableConcurrentBuilds()
])


timestamps {
common.notify_slack {
node('kubespray') {
    stage('git clone') {
        deleteDir()
        checkout scm
    }

    def image = stage('build') {
        withCredentials([string(credentialsId: 'sudo_password', variable: 'sudo_password')]) {
            common.shell(['./prepare_offline_version.sh', env.sudo_password])
        }
        return docker.build("kubespray:${env.BRANCH_NAME}", '--file igz_Dockerfile .')
    }

    try {
        dockerx.images_push([image.id], DockerRepo.ARTIFACTORY_IGUAZIO)
    } finally {
        common.shell(['docker', 'rmi', image.id])
    }
}}}
