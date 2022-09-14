# OC-P10-Détecter_des_faux_billets

[![Language](https://img.shields.io/badge/Python-darkblue.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![Framework](https://img.shields.io/badge/sklearn-darkorange.svg?style=flat&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/stable/)
[![Framework](https://img.shields.io/badge/FastAPI-darkgreen.svg?style=flat&logo=fastapi&logoColor=white)](https://app-detection-billet.herokuapp.com/docs)
[![Framework](https://img.shields.io/badge/Streamlit-red.svg?style=flat&logo=streamlit&logoColor=white)](https://thibaultlf-oc-p10-deteter-des-fau-streamlitstreamlit-app-1zcpz1.streamlitapp.com/)
![hosted](https://img.shields.io/badge/Heroku-430098?style=flat&logo=heroku&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-blue?style=flat&logo=docker&logoColor=white)

App de détection de faux billets créée via Streamlit, FastAPI et Docker.  
Streamlit app: https://thibaultlf-oc-p10-deteter-des-fau-streamlitstreamlit-app-1zcpz1.streamlitapp.com/  
API: https://app-detection-billet.herokuapp.com/

## Scénario du projet

Vous êtes consultant Data Analyst dans une entreprise spécialisée dans la data. Votre entreprise a décroché une prestation en régie au sein de l’Organisation nationale de lutte contre le faux-monnayage (ONCFM).  
Cette institution a pour objectif de mettre en place des méthodes d’identification des contrefaçons des billets en euros.

### Besoins en analyse de données:
Nous aimerions pouvoir mettre en concurrence deux méthodes de prédiction :
- Régression logistique classique ;
- K-means, duquel seront utilisés les centroïdes pour réaliser la prédiction.

### **Livrable:**
- Votre code en R ou Python contenant:  
1. l'ensemble des traitements et des tests effectués;  
2. l'application finale.

## Préparation des données
Le jeu de données est fourni par l'ONCFM (sous le nom *billets.csv*). Celui-ci comporte 6 informations géométriques sur un billet:
- *length* : la longueur du billet (en mm) ;
- *height_left* : la hauteur du billet (mesurée sur le côté gauche, en mm) ;
- *height_right* : la hauteur du billet (mesurée sur le côté droit, en mm) ;
- *margin_up* : la marge entre le bord supérieur du billet et l'image de
celui-ci (en mm) ;
- *margin_low* : la marge entre le bord inférieur du billet et l'image de
celui-ci (en mm) ;
- *diagonal* : la diagonale du billet (en mm).

Ainsi qu'une variable *is_genuine* qui indique si le billet est vrai ou faux.

L'analyse exploratoire permet de voir qu'il manque des données dans la variable *margin_law*. Nous imputerons celle-ci par une régression linéaire comme il est demandé dans le projet (voir le notebook pour plus de détails sur la régression linéaire).

Afin de préparer nos données  aux différents modèles essayés, nous allons séparer le jeu de données en un jeu d'entraînement et un jeu de test. Enfin, nous standardiserons les données.

## Modèle
Dans ce projet, il est demandé d'essayer 2 modèles:
- *K-Means*
- *Régression logistique*

La *régression logistique* obtient de meilleurs résultats que *K-Means*. Nous l'utiliserons donc comme modèle final. Pour plus de détails, voir le notebook.

  
## Streamlit app Demo

![App détection billet](https://user-images.githubusercontent.com/110832782/187501309-3bc58e4a-4b0d-4e36-bdde-344245c4c4ca.gif)

## Faire tourner l'API et l'APP Streamlit en local

Etant donné que nous avons plusieurs conteneurs communiquant entre eux, un réseau est créé nommé AIservice. Pour que le tout fonctionne, le fichier *docker-compose.yml* permet d'exécuter simultanément l'API et l'APP Streamlit. Afin d'exécuter cela sur votre ordinateur, suivez les étapes suivantes:

1. Vérifier que vous avez installé docker et que celui-ci est lancé sur votre ordinateur:  
Exécuter la commande dans bash/cmd:
```
docker ps
```
Si cela renvoie une erreur, installer docker et lancer le.

2. Cloner le repo:
```
git clone https://github.com/ThibaultLF/OC-P10-Detecter_des_faux_billets.git
```

3. Changer le répertoire de travail:
```
cd OC-P10-Detecter_des_faux_billets
```
 
4. Créer le réseau AIservice:
```
docker network create AIservice
```

5. Enfin exécuter cette commande
```
docker-compose up -d --build
```
6. L'application Streamlit et l'API tourne en local. Vous pouvez visiter les pages sur votre navigateur préféré avec les liens suivants:
- http://localhost:8000 pour visiter l'API.
- http://localhost:8501 pour visiter l'app Streamlit.

## Déploiement sur internet
L'API a été déployé à l'aide d'**Heroku** en utilisant le Dockerfile et le fichier heroku.yml, l'application Streamlit a été déployée en utilisant **Streamlit cloud**. Voyons comment faire:

<details>
 <summary><b>Déploiement de l'API à l'aide d'Heroku</b></summary>

*Prérequis:*
- Git et Heroku cli installés sur l'ordinateur ainsi qu'un compte Heroku.

1. Cloner le repo:
```
git clone https://github.com/ThibaultLF/OC-P10-Detecter_des_faux_billets.git
```

2. Changer le répertoire de travail:
```
cd OC-P10-Detecter_des_faux_billets
```

3. Créer l'app heroku

``` 
heroku create nom-app
```

Renommer **nom-app** par celui que vous avez choisi.

4. Synchroniser heroku et git

```
heroku git:remote your-app-name
```

5. Définisser le paramètre de *Stacking* sur conteneur:
 
```
heroku stack:set container
```

6. Envoyer le tout
```
git push heroku main
```

Pour le faire sur une de vos applications personnelles, voir la documentation [Heroku](https://devcenter.heroku.com/articles/build-docker-images-heroku-yml).
</details>

<details>
	<summary><b>Déploiement de l'application Streamlit</b></summary>

*Prérequis:*
- Un compte Streamlit

1. Cloner le repo (si ce n'est pas déjà fait...:sweat_smile:):
```
git clone https://github.com/ThibaultLF/OC-P10-Detecter_des_faux_billets.git
```

2. Aller sur https://streamlit.io/cloud

3. Créer une nouvelle application avec le bouton *new app* et choisir le répertoire que vous avez cloné, puis le fichier **"streamlit_app.py"**. Enfin cliquer sur déployer.

![streamlit_sharing_silent](https://user-images.githubusercontent.com/110832782/187501406-9894393a-730d-46e5-afe1-77c97217bf85.gif)


</details>


Je tiens à remercier les auteurs de cet [article](https://medium.com/mlearning-ai/credit-card-fraud-detection-2527ca04c3de) qui m'ont permis de déployer plus facilement ce projet en local comme sur le cloud.

Merci de votre lecture :blush:.
