
<p align="center">
<a href="https://duckietown.com"><img src="./assets/images/dtlogo.png" alt="Duckietown Logo" width="50%"></a>
</p>

# **Labo 5: Localisation**

Ce laboratoire porte sur l'utilisation des données transmises par les capteurs, combinées à la connaissance de notre environnement, pour estimer notre état. L'approche optimale est le filtre Bayésien ; cependant, sa mise en œuvre ne possède pas de solution analytique connue, sauf dans les configurations les plus simples. Nous explorerons plusieurs approximations du filtre Bayésien : le filtre de Kalman, le filtre particulaire et le filtre à base d'histogrammes. Chacun repose sur des hypothèses et des conditions d'application spécifiques. Enfin, vous programmerez un filtre de Kalman étendu (EKF) pour localiser votre Duckiebot à l'aide des données des encodeurs de roue et des marqueurs de référence AprilTag observés à des emplacements connus.


##  Mais d'abord...

Assurez-vous que votre système est à jour.

- 💻 Veillez toujours à ce que votre Duckietown Shell soit mise à jour vers la dernière version: 

```
     pipx upgrade duckietown-shell
```

- 💻 Mettre à jour les commandes du shell: 

```
     dts update
```

- 💻 Assurez-vous que toutes les images Docker présentes sur votre ordinateur sont à jour: 

```
     dts desktop update
```

- 💻 Arrêtez et supprimez tous les conteneurs Docker existants (que l'autre groupe aurait pu laisser ouverts par erreur):


```
     docker stop $(docker ps -aq)
     docker rm $(docker ps -aq)
```     

- 💻 Vous devrez peut-être également supprimer ce répertoire temporaire pour avoir les autorisations nécessaires pour y écrire.

```
     sudo rm -rf /tmp/duckiematrix
```
   
- 🚙 Assurez-vous que toutes les images Docker présentes sur votre ordinateur sont à jour: 

```
    dts duckiebot update ROBOTNAME
```

(où ROBOTNAME est le nom de votre Duckiebot — réel ou virtuel. Assurez vous que ce dernier soit actif.)

# Avant de commencer

Chaque caméra étant potentiellement fabriquée différemment et montée à un endroit légèrement différent sur le robot, il sera nécessaire de la calibrer. Cette opération comprendra deux parties :

- Calibrage intrinsèque de la caméra
- Calibrage extrinsèque de la caméra

Suivez ces [instructions](https://docs.duckietown.com/ente/duckietown-manual/20-operations/04-calibrations/duckiebot-camera-calibration.html) pour les deux parties.  




# Comment réaliser cet exercice de laboratoire ?

## Lancez l'éditeur de code.

Ouvrez l'éditeur de code (VSCode) en exécutant la commande suivante:

```
dts code editor
```

Attendez qu'une URL s'affiche dans le terminal, puis cliquez dessus ou copiez-la et collez-la dans la barre d'adresse de votre navigateur pour accéder à l'éditeur de code. Le premier élément que vous verrez dans l'éditeur de code est ce même document. 

**Vous pouvez poursuivre votre travail à partir de là**


## Les notebooks "Jupyter"

**REMARQUE** : Vous devez lire ce message depuis l'éditeur de code de votre navigateur.

Dans l'éditeur de code, utilisez la barre latérale de navigation située à gauche pour accéder au
dossier `notebooks` et ouvrir le premier notebook.

Suivez les instructions du notebook et parcourez les notebooks dans l'ordre.

Une fois que vous avez terminé toutes les tâches des notebooks, vous pouvez suivre les instructions suivantes pour tester votre code.

## Exécution de votre code

### Tester avec la Duckiematrix

Il peut être utile de tester votre code dans un environnement de simulation avant de l'essayer sur le robot réel. Pour cela, nous avons la Duckiematrix.

Pour tester votre code dans Duckiematrix, vous aurez besoin d'un robot virtuel. Vous pouvez en créer un avec la commande suivante:

```
dts duckiebot virtual create [VBOT] -t duckiebot -c DB21J
```

où `[VBOT]` peut être n'importe quoi (mais n'oubliez pas ce nom pour la suite).

Vous pouvez ensuite démarrer votre robot virtuel avec la commande:

```
dts duckiebot virtual start [VBOT] --pull
```

Vous devriez le voir avec le statut « Booting » (démarrage) et enfin « Ready » (prêt) si vous consultez la commande `dts fleet discover` :

```
     | Hardware |   Type    | Model |  Status  | Hostname 
---  | -------- | --------- | ----- | -------- | ---------
[VBOT] |  virtual | duckiebot | DB21J |  Ready   | [VBOT].local
```

Maintenant que votre robot virtuel est prêt, vous pouvez démarrer Duckiematrix. Depuis ce répertoire d'exercices, exécutez la commande suivante :

```
dts code start_matrix
```

Vous devriez voir le simulateur Duckiematrix, basé sur Unity, démarrer. L'écran de démarrage ressemblera à ceci :

![duckiematrix_start](assets/images/duckiematrix-start.png)

À partir d'ici, vous pouvez cliquer n'importe où dans la fenêtre et appuyer sur la touche [ENTRÉE] pour l'activer. Vous pouvez ensuite déplacer le petit canard vers le Duckiebot à l'aide des touches « w », « a », « s » et « d », ou modifier l'angle de la caméra pour observer le Duckiebot avec la souris. Vous pouvez également passer à une vue de dessus en appuyant sur la touche « v », ce qui vous donnera une vue similaire à celle-ci :

![duckiematrix_overhead](assets/images/duckiematrix-overhead.png)


### "Build" votre code

Vous pouvez build le code avec

```
dts code build -R ROBOTNAME
```

où ROBOTNAME peut être un robot réel ou virtuel.

### Tester le code

Vous pouvez ensuite exécuter votre code avec

```
dts code workbench -R ROBOTNAME [-m]
```

où ROBOTNAME peut être un robot réel ou virtuel, mais s'il s'agit d'un robot virtuel, vous devez inclure l'option `-m` pour indiquer que vous souhaitez le tester dans la Duckiematrix.


Dans un autre terminal (sur l'ordinateur), vous pouvez lancer le visualiseur `noVNC` pour cet exercice, qui peut être utile pour envoyer des commandes au robot et visualiser l'odométrie que vous calculez dans la fenêtre RViZ.

```
dts code vnc -R [ROBOTNAME]
```

où `[ROBOTNAME]` peut être le robot réel ou virtuel (utilisez celui avec lequel vous avez exécuté la commande `dts code workbench`).


Vous pouvez maintenant passer au [premier notebook](./notebooks/01-kalman-filter/kalman-filter.ipynb).

# Crédits

Les premiers notebooks sur le filtre de Kalman et le filtre particulaire ont été développés par [Rey Reza Wiyatno](https://rrwiyatn.github.io/).
