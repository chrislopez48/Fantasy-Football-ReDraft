bind mount- way to connect a folder on your computer to a folder inside a container. -v "$(pwd)/data:/app/data"
--rm - when container stops, remove it
bind mount- you choose folder on your computer. run code inside docker, but store the data in a project folder. we will replace it with s3 soon
docker volume- docker manages the storage location for you
terraform init takes up a lot of space. put on gitignore
terraform-provider-aws is a compiled binary executable. very big in file size
AT some point, we can run terraform inside container. but for now, we'll install terraform on pc and mac
boto3 is a aws SDK for python, giving python ways to communicate with buckets, ec2, dbs etc
docker run `
  -v ${HOME}\.aws:/root/.aws:ro `
  fantasy-redraft
image= finished template of everything needed to create container
container= running instance created from an image

"output" in terraform files is the print version basically
terraform init- prepares terra folder and downloads aws resoirces
terraform plan - compares tf files, saved state, and what aws has. an updater that determines add change or destroy
terraform apply- makes changes to aws

docker build -t fantasy-redraft .
docker tag fantasy-redraft:latest YOUR_ECR_URL:latest
docker push YOUR_ECR_URL:latest
use the 3 lines above every time we build a new image^ jenkins will automate this later

ECR stores docker images. like github but for docker images
fargate gives us the CPU and ram to actually run our images
without fargate, we have to maintain ec2 servers, install docker, patch os, etc.

PKCE- proof key for code exchange - helps that the program starting the yahoo sign in is the same as the one exchanging auth for tokens. we create a random verifier, send a yahoo challange, send the original verifier with an auth code, then yahoo hashes that verifier and makes sure it matches the challenge
SHA-256 - hashing algorithm we use to create the challenge
docker pull jenkins/jenkins:lts-jdk21 command to download jenkins
image- our blueprint for everything needed to run jenkinsfile
container- instance created ffrom jenkinsfile image
volume-persistent storage existing independent of container that can outlive and be reused by containers. we created a volume with all jenkinsfile and attached it so we dont lose progress if we delete containers
#checkout is our first phase, steps is commands jenkins will execute
we make a docker network so containers can communicate with each other.
jenkins controller- manages jobs, schedules builds, etc
jenkins agent- executes actual build commands
docker network- allows agent cond controller containers to communicate.
docker network is a virtuasl network allowing containers to communicate with each other.
Jenkins synposis- created our jenkins docker environment-> created a image/conatiner/volume for the jenkins controller and agent->used a docker network to onnect agent and controller-> connected jenkins to github with jenkinsfile
in docker networking= driver = network type
pytest-python testing framework; just quick way to see if our funcs give us the results we want

sh 'echo "hello"' is the print statement variant for our jenkinsfile
"scm" is source code management. its basically our github; jenkins uses it to retrieve code

#"assert" means result has to be correct or test fails

docker keeps containers in seperate environments; we need to create a network to connect our jenkins controller and jenkins agent containers

DinD- docker engine insode docker container;
we have docker data volume to store images and build data, and docker certs to store certs used for connections
docker desktop is just a docker engine with a gui. we built a seperate docker engine in our dind. second engine will build images in our jenkins pipeline


docker run -d \
  --name fantasy-build-agent \
  --network jenkins-network \
  --env-file ~/.jenkins-agent.env \
  -e DOCKER_HOST=tcp://docker:2376 \
  -e DOCKER_TLS_VERIFY=1 \
  -e DOCKER_CERT_PATH=/certs/client \
  -v fantasy-agent-workspace:/home/jenkins/agent \
  -v fantasy-jenkins-client-certs:/certs/client:ro \
  fantasy-jenkins-agent

  always smart to keep a backup. "fantasy-build-agent-pre-aws is our pre cli

  need to create IAM policy for our jenkins to connect to ecr

aws ecr describe-repositories \
  --repository-names fantasy-redraft \
  --region us-east-1 \
  --query 'repositories[0].repositoryUri' \
  --output text this command is to veryify ecr repo

  we made an IAM policy to give us permissions on what ecr actions are allowed, made an IAM user to give jenkins aws identity, and an access key that allows authentication.

  on our terraform file, we dont put the physical actual vpc id, but the "default" so that we are more flexible and portable between multiple aws acounts that have different vpcs.

  ARN= amazon resource name
  subnet- where does our container connect to the network. we set up subnets so our fargate container can communicate with the internet and aws services.
  security group- what network traffic can enter or leave

  $() is a command substitution; executes the command inside the parenthesis anc captures its standard output.

  every time ecs launches a new task, aws generates a new, unique id task

