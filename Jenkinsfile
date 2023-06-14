@Library('pipelinex@_s3_python3') _
//test

timestamps {
common.notify_slack {
node('centos76') {

    stage('git clone') {
        deleteDir()
        def scm_vars = checkout scm
        env.kubespray_hash = scm_vars.GIT_COMMIT
        currentBuild.description = "hash = ${env.kubespray_hash}"
    }

    def img_name = "kubespray:${env.kubespray_hash}"
    def image = stage('build') {
        withCredentials([string(credentialsId: 'sudo_password', variable: 'sudo_password')]) {
        sh "ls -ltrh "
        sh "cd ${WORKSPACE} ; bash prepare_offline_version.sh"
//             common.shell(['cd ${WORKSPACE} ; bash prepare_offline_version.sh', env.sudo_password])
        }
    }

    def rel_dir = "build_by_hash/kubespray/${env.kubespray_hash}/pkg/kubespray"
    def nas_dir = "/mnt/nas/${rel_dir}"
//     def output_name = 'kubespray.tar.xz'
    def nas_target = "${nas_dir}/"
    stage('save to nas') {
            common.shell(['mkdir', '-p', nas_dir])
            "ls -ltrh /mnt/nas/kubespray/${BRANCH_NAME}/"
            sh("mv /mnt/nas/kubespray_offline/${BRANCH_NAME}/outputs  ${nas_target}")

    }

//     stage('upload to s3') {
//         def bucket = 'iguazio-versions'
//         def bucket_region = 'us-east-1'
//         sh"""
//         export LC_ALL=en_US.UTF-8
//         export LANG=en_US.UTF-8
//         """
//         common.upload_to_s3(bucket, bucket_region, nas_image, "${rel_dir}/${output_name}")
//     }
}
}
}
