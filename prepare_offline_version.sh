export BUILD_PATH="/mnt/nas/kubespray_offline/${BRANCH_NAME}/outputs"

sudo mkdir -p ${BUILD_PATH}
cd  ${BUILD_PATH}
pwd
echo "---->>>>delete all file in path ${BUILD_PATH} ....."
rm -rf *
sleep 20

sudo chmod 777   ${BUILD_PATH}
sudo chown  -R iguazio:iguazio ${BUILD_PATH}

cd ${WORKSPACE}

docker build -t kubespray-offline:${BRANCH_NAME} .
docker run --rm -v ${BUILD_PATH}:/outputs -v /var/run/docker.sock:/var/run/docker.sock kubespray-offline:${BRANCH_NAME}
sudo rm -rf kubespray-offline


echo "list dir:"
ls ${BUILD_PATH}