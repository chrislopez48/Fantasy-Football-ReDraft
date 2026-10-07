#file is to just run pipeline on fargate
#!/bin/bash

aws ecs run-task \
  --cluster fantasy-redraft-cluster \
  --launch-type FARGATE \
  --task-definition fantasy-redraft-task \
  --network-configuration 'awsvpcConfiguration={subnets=[subnet-0a41948b12a1eaa2b,subnet-066c9523f8db8533c,subnet-0e16ddde61ea57005,subnet-0485e78ced06f50c7,subnet-0c70a7651bd7dda13,subnet-035ae8cb7db56eb4e],securityGroups=[sg-0de653944950eeae9],assignPublicIp=ENABLED}' \
  --region us-east-1 \
  --no-cli-pager