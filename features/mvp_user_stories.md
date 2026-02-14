# MVP – Reconstruction 3D depuis une vidéo offline

Ce document décrit le projet sous forme de **user stories**, chacune correspondant à une étape claire et actionnable du MVP.

---

## Epic 1 – Préparer l’environnement de travail

### US-01 – Initialisation du projet
**En tant que** développeur
**Je veux** initialiser un dépôt de projet clair et structuré
**Afin de** pouvoir développer, tester et faire évoluer le pipeline facilement.

**Critères d’acceptation**
- Un dépôt Git est créé
- Une arborescence claire est définie (frames, scripts, output)
- Un README décrit le projet et les prérequis

---

### US-02 – Installer les dépendances
**En tant que** développeur
**Je veux** installer toutes les dépendances logicielles nécessaires
**Afin de** pouvoir exécuter le pipeline de reconstruction 3D.

**Critères d’acceptation**
- Python 3.11 installé
- OpenCV avec module ArUco fonctionnel
- COLMAP installé et accessible en ligne de commande
- FFmpeg installé

---

## Epic 2 – Acquisition et préparation des données

### US-03 – Préparer la scène physique
**En tant que** utilisateur
**Je veux** placer des objets de référence de forme et taille connues dans la scène
**Afin de** fournir une échelle réelle et stabiliser la reconstruction.

**Critères d’acceptation**
- Plusieurs marqueurs ArUco sont placés dans la scène
- Les tailles des marqueurs sont connues et documentées
- Les marqueurs ne sont pas tous coplanaires

---

### US-04 – Capturer la vidéo
**En tant que** utilisateur
**Je veux** capturer une vidéo de la scène avec un mouvement contrôlé
**Afin de** maximiser la qualité de la reconstruction 3D.

**Critères d’acceptation**
- Vidéo en résolution 1080p minimum
- Pas de zoom pendant l’enregistrement
- Mouvement lent avec fort recouvrement visuel

---

### US-05 – Extraire les frames de la vidéo
**En tant que** développeur
**Je veux** extraire des images clés depuis la vidéo
**Afin de** les utiliser comme entrée pour la photogrammétrie.

**Critères d’acceptation**
- Les frames sont extraites à un FPS défini (ex: 2 FPS)
- Les images sont stockées dans un dossier dédié
- Les noms de fichiers sont ordonnés et exploitables

---

## Epic 3 – Analyse par vision par ordinateur

### US-06 – Calibrer la caméra
**En tant que** développeur
**Je veux** calibrer la caméra utilisée pour la capture
**Afin de** corriger les distorsions et améliorer la précision géométrique.

**Critères d’acceptation**
- Une matrice de caméra est calculée ou fournie
- Les coefficients de distorsion sont disponibles
- La calibration est validée sur des images tests

---

### US-07 – Détecter les marqueurs ArUco
**En tant que** développeur
**Je veux** détecter automatiquement les marqueurs ArUco dans les images
**Afin de** estimer la pose de la caméra et définir une échelle réelle.

**Critères d’acceptation**
- Les marqueurs sont détectés sur plusieurs frames
- Les identifiants des marqueurs sont reconnus
- Les poses caméra (rvec, tvec) sont stockées

---

## Epic 4 – Reconstruction 3D

### US-08 – Lancer la reconstruction sparse
**En tant que** développeur
**Je veux** lancer COLMAP sur les images extraites
**Afin de** reconstruire la trajectoire caméra et un nuage de points sparse.

**Critères d’acceptation**
- Les features sont extraites
- Les images sont appariées
- Une reconstruction sparse est générée

---

### US-09 – Aligner l’échelle de la scène
**En tant que** développeur
**Je veux** aligner l’échelle de la reconstruction COLMAP avec les mesures réelles
**Afin de** produire un modèle 3D à l’échelle métrique.

**Critères d’acceptation**
- Les poses COLMAP sont comparées aux poses ArUco
- Un facteur d’échelle est calculé
- La scène est redimensionnée correctement

---

### US-10 – Générer un nuage de points dense (optionnel)
**En tant que** utilisateur
**Je veux** générer un nuage de points dense ou un mesh
**Afin de** visualiser la scène 3D de manière plus réaliste.

**Critères d’acceptation**
- Une reconstruction dense est générée
- Les fichiers sont exportés en PLY / OBJ
- Les résultats sont visualisables dans un outil 3D

---

## Epic 5 – Validation et exploitation

### US-11 – Visualiser et valider la reconstruction
**En tant que** utilisateur
**Je veux** visualiser la scène reconstruite
**Afin de** vérifier la cohérence géométrique et l’échelle.

**Critères d’acceptation**
- Le nuage de points est lisible
- La trajectoire caméra est cohérente
- Les dimensions correspondent au réel

---

### US-12 – Documenter le pipeline
**En tant que** développeur
**Je veux** documenter le pipeline complet
**Afin de** pouvoir le reproduire et le faire évoluer.

**Critères d’acceptation**
- Le README décrit chaque étape
- Les commandes principales sont documentées
- Les limites connues du MVP sont listées

---

## Epic 6 – Validation par les tests (ATDD / BDD)

Ce projet est piloté par les tests. Chaque fonctionnalité est considérée comme validée uniquement si les scénarios suivants passent.

---

### US-13 – Validation de l’extraction des frames

**Scénario : Extraire des frames exploitables depuis une vidéo**

**Étant donné** une vidéo MP4 valide en entrée  
**Et** un paramètre FPS configuré à 2 images par seconde  
**Quand** le script d’extraction est exécuté  
**Alors** un dossier de frames est créé  
**Et** les images sont ordonnées séquentiellement  
**Et** chaque image est lisible par OpenCV

---

### US-14 – Validation de la calibration caméra

**Scénario : Charger une calibration caméra valide**

**Étant donné** un fichier de calibration caméra  
**Quand** le pipeline démarre  
**Alors** la matrice de la caméra est chargée  
**Et** les coefficients de distorsion sont disponibles  
**Et** aucune erreur de projection n’est levée lors d’un test sur image

---

### US-15 – Validation de la détection des marqueurs ArUco

**Scénario : Détecter des marqueurs ArUco dans une image**

**Étant donné** une image contenant au moins un marqueur ArUco connu  
**Quand** l’algorithme de détection est exécuté  
**Alors** au moins un identifiant de marqueur est détecté  
**Et** la pose caméra associée est calculée  
**Et** les données sont persistées pour la frame correspondante

---

### US-16 – Validation de la couverture des marqueurs dans la vidéo

**Scénario : Vérifier la visibilité des marqueurs sur plusieurs frames**

**Étant donné** un jeu de frames extraites  
**Quand** la détection ArUco est exécutée sur l’ensemble du jeu  
**Alors** chaque marqueur de référence est détecté dans plusieurs frames  
**Et** aucune frame critique n’est totalement dépourvue de marqueurs

---

### US-17 – Validation de la reconstruction sparse

**Scénario : Générer une reconstruction sparse avec COLMAP**

**Étant donné** un dossier d’images valide  
**Quand** COLMAP est exécuté avec succès  
**Alors** un modèle sparse est généré  
**Et** des poses caméra sont disponibles  
**Et** un nuage de points sparse non vide est exporté

---

### US-18 – Validation de la cohérence des poses caméra

**Scénario : Vérifier la continuité de la trajectoire caméra**

**Étant donné** les poses caméra estimées par COLMAP  
**Quand** la trajectoire est analysée  
**Alors** les déplacements entre frames successives sont continus  
**Et** aucune discontinuité extrême n’est détectée

---

### US-19 – Validation de l’alignement d’échelle

**Scénario : Calculer un facteur d’échelle cohérent**

**Étant donné** des poses caméra issues de COLMAP  
**Et** des poses caméra issues des marqueurs ArUco  
**Quand** l’algorithme d’alignement est exécuté  
**Alors** un facteur d’échelle unique est calculé  
**Et** ce facteur est stable sur plusieurs frames

---

### US-20 – Validation métrique de la scène reconstruite

**Scénario : Vérifier les distances réelles dans la scène 3D**

**Étant donné** un modèle 3D mis à l’échelle  
**Et** deux marqueurs dont la distance réelle est connue  
**Quand** la distance entre ces deux marqueurs est mesurée dans le modèle  
**Alors** l’erreur est inférieure à un seuil défini (ex : < 5%)

---

### US-21 – Validation du nuage de points dense (optionnel)

**Scénario : Générer un nuage de points dense exploitable**

**Étant donné** une reconstruction sparse valide  
**Quand** la reconstruction dense est lancée  
**Alors** un nuage dense est généré  
**Et** le fichier est visualisable dans un outil 3D standard

---

### US-22 – Validation globale du pipeline

**Scénario : Exécuter le pipeline complet de bout en bout**

**Étant donné** une vidéo valide en entrée  
**Quand** le pipeline complet est exécuté  
**Alors** une scène 3D à l’échelle réelle est produite  
**Et** toutes les étapes intermédiaires sont validées  
**Et** aucun échec critique n’est levé

---

## Fin du MVP

Le MVP est considéré comme terminé lorsque l’ensemble des scénarios ci-dessus passent automatiquement.  
La documentation est implicitement portée par les tests (approche ATDD / BDD).

