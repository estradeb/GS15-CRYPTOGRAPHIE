<a href="url">
  <img src="https://github.com/stewie05/GS15/blob/main/ressources/menu.png" align="center" height="600" width="600">
  </a>
  
## A propos
*GS15 est une matière de Cryptographie à l'université de technologie de Troyes (UTT) enseignée par Rémi COGRANNE. Le projet consiste en l'implémentation de diverses fonctions :* 

* Chiffrement Kasumi (modifié)
* RC4
* SHA_1 & d'une fonction "éponge"
* Génération de clé publiques et privées
* RSA
* El-Gamal
* Une blockchain

> **ATTENTION : Aucune des implémentations ici n'est sécurisée. Elles  doivent être utilisée uniquement à des fins pédagogique !**

## Sommaire
  * **main** : comprend les algorithmes principaux classés par type (chiffrement symmétrique, chiffrement asymmétrique, Hachage et BlocChain)
  * **ressources** : comprend des scripts d'opération basiques sur les bits ainsi que l'algorithme RC4.
  * **output** : contient les textes chiffrés ainsi que les clés générées
 
## Utilisation & Intallation
  Dépendance :
      Installez le package `pyfinite` avec la commande `pip install pyfinite` (si vous êtes sur linux, pensez à utiliser plutot pip3)
  1. Clonez le dépôt dans un répertoire
  2. Executé le fichier "**menu.py**" avec une console python 3

## Résolution de problème
#### Dépendance
Pyfinite est utilisé pour une inversion dans un corps de Gallois (facultative) dans l'implémentation de Kasumi. Le package n'utilise pas de dépendance pour les opérations binaires
#### Utilisation de la BlockChain
A des fins de démonstration en cours, une chaine est déjà préparée à l'avance. Pour ajouter des blocs et des utilisateurs, vous devez d'abord créer les utilisateurs Pierre et Benoit avec les montants 9999. Vous pouvez ensuite ajouter les utilisateurs que vous souhaitez. 
