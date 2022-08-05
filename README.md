# lòbèmbè
[![Commitizen friendly](https://img.shields.io/badge/commitizen-friendly-brightgreen.svg)](http://commitizen.github.io/cz-cli/)
> [Baka](https://fr.wikipedia.org/wiki/Baka_(langue_oubanguienne)) language meaning a half-hut, often rectangular and wide open

 Provides access to services used internally by the mongulu collective for communication:
  - http://lobembe.mongulu.cm/?q=notes  
  - http://lobembe.mongulu.cm/?q=meet
  - http://lobembe.mongulu.cm/?q=tasks
  - http://lobembe.mongulu.cm/?q=videos

### Prerequisites
On the AWS cloud:
* A DNS record in Route 53 linking the subdomain www.xxxx.yyy filled in by the `website_bucket_name` variable 

On your computer : 
* aws-cli / git
* terraform
* ansible

### Deployment

#### website
```
  terraform apply
  aws s3 sync --delete html/ s3://lobembe.mongulu.cm
```    

### Tests
```
  cd scripts/
  pytest test_reminder.py
```  

#### Matomo analytics

In our case, we deployed it on an Oracle Cloud instance (ubuntu image) with the option [always free tier](https://www.oracle.com/cloud/free/)
2 instances of 1 GB RAM/public IP addresses. We must first [open HTTP/HTTPS](https://youtu.be/yWVD6qmQrb8?t=480) then:
```
  sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80 -j ACCEPT
  sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 443 -j ACCEPT
```

All you have to do next is to install matomo:
```
  export ANSIBLE_CONFIG=./ansible.cfg
  ansible-galaxy install -r requirements.yml
  ansible-playbook main.yml
  ansible-playbook main.yml (la dernière tâche du playbook échouera, re-éxécutez la juste)
``` 

You should get a 503 error when accessing your site. To correct this, run on the instance:
```
  sudo systemctl status php7.4-fpm.service
  sudo systemctl restart nginx
```
