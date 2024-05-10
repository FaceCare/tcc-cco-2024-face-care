#!/bin/bash
cd
sudo yum update -y
sudo amazon-linux-extras install nginx
sudo systemctl start nginx
sudo systemctl enable nginx
sudo yum install docker -y
sudo systemctl start docker
sudo systemctl enable docker
pip3 install jupyter --use-feature=2020-resolver
echo '{
  "NotebookApp": {
    "password": "argon2:$argon2id$v=19$m=10240,t=10,p=8$CdBDe6E1KfVq5Hnss6LzNA$Wq+wtXQ69g7NeIgdCBvQOOtX1t40uasD+/544yot4lk"
  }
}' > ~/.jupyter/jupyter_notebook_config.json
# python3 -m notebook --ip=0.0.0.0 --no-browser
