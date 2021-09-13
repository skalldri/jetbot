cp /etc/apt/trusted.gpg.d/jetson-ota-public.asc ../.. # copy to jetbot root

OUTPUT_IMAGE=$JETBOT_DOCKER_REMOTE/jetbot:base-$JETBOT_VERSION-$L4T_VERSION

echo "Building Jetbot Base Image: $OUTPUT_IMAGE"
echo "Using Base Docker Image: $JETBOT_BASE_IMAGE"

sudo -E docker build \
    --build-arg BASE_IMAGE=$JETBOT_BASE_IMAGE \
    -t $OUTPUT_IMAGE \
    -f Dockerfile \
    ../..  # jetbot repo root as context

