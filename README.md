# lòbèmbè
> Langue [Baka](https://fr.wikipedia.org/wiki/Baka_(langue_oubanguienne)) siginifiant une demi-hutte souvent rectangulaire et largement ouverte

 Donne accès aux services utilisés en interne par le collectif mongulu pour communication:
  - http://lobembe.mongulu.cm/?q=notes  
  - http://lobembe.mongulu.cm/?q=meet
  - http://lobembe.mongulu.cm/?q=tasks
  - http://lobembe.mongulu.cm/?q=videos

### Prérequis
Sur le cloud AWS:
* Un enregistrement DNS dans Route 53 reliant le sous-domaine www.xxxx.yyy  renseigné par la variable `website_bucket_name` 

Sur votre poste : 
* aws-cli / git
* terraform
* ansible

### Déploiement

#### Site web
```
  terraform apply
  aws s3 sync --delete html/ s3://lobembe.mongulu.cm
```    

#### Matomo analytics

Dans notre cas, nous l'avons déployé sur une instance Oracle Cloud (image ubuntu) en bénéficiant de l'option [always free tier](https://www.oracle.com/cloud/free/)
de 2 instances d'1 Go RAM/ adresses IP publiques. Il faut donc au préalable [ouvrir les flux HTTP/HTTPS](https://youtu.be/yWVD6qmQrb8?t=480) puis:
```
  sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80 -j ACCEPT
  sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 443 -j ACCEPT
``` 
sur l'instance.

Il ne vous reste plus qu'à installer matomo:
```
  export ANSIBLE_CONFIG=./ansible.cfg
  ansible-playbook main.yml
  ansible-playbook main.yml (la dernière tâche du playbook échouera, re-éxécutez la juste)
``` 

Vous devriez avoir une erreur 503 en accédant à votre site. Pour corriger cela, éxécutez sur l'instance:
```
  sudo systemctl status php7.4-fpm.service
  sudo systemctl restart nginx
```
