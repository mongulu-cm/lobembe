# lòbèmbè
> Langue [Baka](https://fr.wikipedia.org/wiki/Baka_(langue_oubanguienne)) siginifiant une demi-hutte souvent rectangulaire et largement ouverte

 Donne accès aux services utilisés en interne par le collectif mongulu pour communication:
  - http://lobembe.mongulu.cm/?q=notes  
  - http://lobembe.mongulu.cm/?q=meet
  - http://lobembe.mongulu.cm/?q=tasks


### Prérequis
Sur le cloud AWS:
* Un enregistrement DNS dans Route 53 reliant le sous-domaine www.xxxx.yyy  renseigné par la variable `website_bucket_name` 

Sur votre poste : 
* aws-cli / git
* terraform

### Déploiement

```
  terraform apply
  aws s3 sync --delete html/ s3://lobembe.mongulu.cm
```    