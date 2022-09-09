# lòbèmbè
[![Commitizen friendly](https://img.shields.io/badge/commitizen-friendly-brightgreen.svg)](http://commitizen.github.io/cz-cli/)
> [Baka](https://fr.wikipedia.org/wiki/Baka_(langue_oubanguienne)) language meaning a half-hut, often rectangular and wide open

 Provides access to services used internally by the mongulu collective. An exhasutive list is accessible here: https://lobembe.mongulu.cm/

### Prerequisites
On the AWS cloud:
* A DNS record in Route 53 linking the subdomain www.xxxx.yyy filled in by the `website_bucket_name` variable 

On your computer : 
* aws-cli / git
* terraform
* ansible

### Deployment

#### Tools
In our case, we deployed it on an Oracle Cloud instance (ubuntu image) with the option [always free tier](https://www.oracle.com/cloud/free/)
 We must first [open HTTP/HTTPS](https://youtu.be/yWVD6qmQrb8?t=480):
```
  sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80 -j ACCEPT
  sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 443 -j ACCEPT
```

Then install matomo, heimdall and nginx for reverse proxy:
```
  export ANSIBLE_CONFIG=./ansible.cfg
  ansible-galaxy install -r requirements.yml
  ansible-playbook main.yml ( in case of issue with matomo, just re-execute the playbook )
``` 

You should get a 503 error when accessing to matomo site. To correct this, run on the instance:
```
  sudo systemctl status php7.4-fpm.service
  sudo systemctl restart nginx
```

#### Blog
```
  pushd infra/ ; terraform apply; popd
  aws s3 sync --delete meeting_notes/_site s3://blog.mongulu.cm
```  


### Tests
```
  cd scripts/
  pytest test_reminder.py
``` 