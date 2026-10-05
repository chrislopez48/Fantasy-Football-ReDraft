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