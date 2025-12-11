# build
set IMAGE docker.io/orgameron/text-processor:latest
docker build -t $IMAGE .

# push
docker push $IMAGE