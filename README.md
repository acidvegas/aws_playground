# AWS Playground

Exploration and documentation of my experiments deploying Elasticsearch and the various facets of the ELK stack *(Elasticsearch, Logstash, and Kibana)* using the sophisticated amalgamation of Terraform and Amazon Web Services *(AWS)*.

This narrative not only encapsulates the mechanistic aspects of automated deployments but also delves into the intricate challenges and nuances that such an integration presents.

While not primed for production, it offers invaluable insights, underscoring my dedication to mastering cutting-edge technologies and showcasing my intellectual rigor in navigating complex cloud-based infrastructures.

## Getting Started
1. Sign up an [AWS account](https://aws.amazon.com/)
2. Create an [IAM User](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html)
  - Add the `AmazonEC2FullAccess` permission policy to a new group
3. Create an [EC2 Key Pair](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html)
4. Create an [EC2 Security Group](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-security-groups.html)
  - For IPv6, edit your VPC & add a IPv6 CDIR 
5. Launch an [EC2 Instance](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html)
    - Select `debian`, on a `t2.micro`, using your keypair & security group created earlier

## AWS CLI
```shell
sudo apt-get install -y awscli && aws configure
```

**Note:** If you get errors about `ImportError: cannot import name 'DEFAULT_CIPHERS' from 'urllib3.util.ssl_'`: `python -m pip install requests "urllib3<2`

## Terraform
```shell
sudo apt-get install -y gnupg software-properties-common
wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg
gpg --no-default-keyring --keyring /usr/share/keyrings/hashicorp-archive-keyring.gpg --fingerprint
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt-get update && sudo apt-get install -y terraform
```

## Elasticsearch
```shell
sudo apt-get install -y gnupg apt-transport-https
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list
sudo apt-get update && sudo apt-get install elasticsearch kibana logstash
sudo certbot certonly --standalone --preferred-challenges http -d elastic.domain.org
```

* Copy your certificates to `/etc/elasticsearch/certs`:
```shell
mkdir -p /etc/elasticsearch/certs/
sudo cp /etc/letsencrypt/live/elastic.domain.org/fullchain.pem /etc/elasticsearch/certs/fullchain.pem
sudo cp /etc/letsencrypt/live/elastic.domain.org/privkey.pem   /etc/elasticsearch/certs/privkey.pem
sudo chmod -R 777 /etc/elasticsearch/certs/
```

* Edit your `/etc/elasticsearch/elasticsearch.yml` and change the follow options:
```yaml
cluster.name: BeeHive
node.name: gibson
network.host: 0.0.0.0    
bootstrap.memory_lock: true
xpack.security.audit.enabled: true
xpack.security.http.ssl:
  enabled: true
  key: /etc/elasticsearch/ssl/privkey.pem
  certificate: /etc/elasticsearch/ssl/fullchain.pem
```

* System changes:
```shell
sudo su  
	ulimit -n 65535
	ulimit -u 4096

echo "elasticsearch  -  nofile  65535" > /etc/security/limits.conf
mkdir -p /etc/systemd/system/elasticsearch.service.d/
echo "[Service]\nLimitMEMLOCK=infinity" > /etc/systemd/system/elasticsearch.service.d/override.conf
sudo swapoff -a
sudo sysctl -w vm.swappiness=1         # Add these
sudo sysctl -w vm.max_map_count=262144 # to /etc/systctl.conf
sudo sysctl -w net.ipv4.tcp_retries2=5 # 
```

* Set the password for Kibana:
`./usr/share/elasticsearch/bin/elasticsearch-reset-password -u kibana_system`

`./usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token --scope kibana # Save this for when we access Kibana the first time`

`./usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s node # enrollment token for a new node`

## Setup Kibana
* Copy your certificates to `/etc/kibana/certs`:
```shell
mkdir -p /etc/kibana/certs/
sudo cp /etc/letsencrypt/live/elastic.domain.org/fullchain.pem /etc/kibana/certs/fullchain.pem
sudo cp /etc/letsencrypt/live/elastic.domain.org/privkey.pem   /etc/kibana/certs/privkey.pem
```

* Edit your `/etc/kibana/kibana.yml` and change the follow options:
```yaml
server.host: "0.0.0.0"
server.publicBaseUrl: "https://elastic.domain.org"
server.ssl.enabled: true 
server.ssl.certificate: /etc/kibana/certs/fullchain.pem
server.ssl.key: /etc/kibana/certs/privkey.pem
elasticsearch.hosts: ["https://elastic.domain.org:9200"]
elasticsearch.username: "kibana_system"
elasticsearch.password: "changeme" # Use the password from the reset command we did earlier
```

## Setup Logstash
* Copy your certificates to `/etc/logstash/certs`:
```shell
mkdir -p /etc/logstash/certs/
sudo cp /etc/letsencrypt/live/elastic.domain.org/fullchain.pem /etc/logstash/certs/cacert.pem
```

* Edit your `/etc/logstash/logstash.yml` and change the follow options:
```yaml
input {
  beats {
    port => 5044
  }
}
output {
  elasticsearch {
    hosts => ["https://elastic.domain.org:9200"]
    index => "%{[@metadata][beat]}-%{[@metadata][version]}-%{+YYYY.MM.dd}"
    user => "elastic"
    password => "changeme"
    cacert => "/etc/logstash/cacert.pem"
  }
}
```

* `logstash-plugin install logstash-input-irc`

## Start the ELK stack:
```shell
sudo systemctl daemon-reload
sudo systemctl enable elasticsearch.service && sudo systemctl start elasticsearch.service
sudo systemctl enable kibana.service        && sudo systemctl start kibana.service
sudo systemctl enable logstash.service      && sudo systemctl start logstash.service
```

___

###### Mirrors for this repository: [acid.vegas](https://git.acid.vegas/aws_playground) • [SuperNETs](https://git.supernets.org/acidvegas/aws_playground) • [GitHub](https://github.com/acidvegas/aws_playground) • [GitLab](https://gitlab.com/acidvegas/aws_playground) • [Codeberg](https://codeberg.org/acidvegas/aws_playground)