echo "**************************RUNNING CONTAINER*****************************#"
sudo docker run -it \
    --device=/dev/vcsm \
    --device=/dev/vchiq \
    --device=/dev/video0 \
    -v /opt/vc:/opt/vc \
    --env LD_LIBRARY_PATH=/opt/vc/lib \
    --mount type=bind,source="$(pwd)/../service",target=/service \
    --mount type=bind,source="$(pwd)/../../shared",target=/shared \
    ${PWD##*/} \
    bash