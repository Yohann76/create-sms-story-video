# Guideline for create story (SMS Story TikTok)

Ce fichier est le brief complet pour l'agent qui génère les scénarios `scenario.json`.
L'objectif : créer des vidéos SMS virales sur TikTok, Reels et Shorts.

---

## Format technique

- Durée cible : **30 à 60 secondes** de vidéo finale
- Nombre de messages : pas de limite
- Délais entre messages : entre `1800ms` et `3500ms` (pas trop vite, pas trop lent)
- `typingDuration` pour les messages reçus : entre `1500ms` et `3000ms`
- Le champ `myName` est toujours **"Moi"**

---

## Ce qui fait le buzz sur TikTok

### Le hook (les 3 premières secondes)
C'est **le seul critère** qui détermine si quelqu'un regarde ou scrolle.
- La **première notification** doit être intrigante, ambiguë ou émotionnelle
- Exemples de hooks forts :
  - _"T'es libre ce soir ?"_ — tension, mystère
  - _"Je t'ai vu aujourd'hui..."_ — intrigue romantique
  - _"Je sais que c'est bizarre mais..."_ — vulnérabilité
  - _"J'aurais pas dû faire ça"_ — suspense
  - _"Tu peux garder un secret ?"_ — curiosité immédiate
- Le premier message doit planter le décor **immédiatement**, sans introduction inutile

### Ce qui retient l'attention
- Une **tension croissante** : chaque réplique fait monter l'enjeu
- Des **retournements de situation** : un message inattendu qui change tout
- Du **réalisme dans les fautes et le style** : les gens écrivent mal sur leurs téléphones
- Des **silences dramatiques** : une pause longue avant une réponse importante
- Une **chute mémorable** : le dernier message doit laisser quelque chose — sourire, suspense, ou émotion

### Ce qu'il faut éviter
- Messages trop longs et bien rédigés (irréaliste)
- Trop d'emojis — **1 à 2 max par échange**, seulement si naturel
- Résolution trop rapide — garder de la tension jusqu'au bout
- Langage trop formel ou trop littéraire
- Plus de 3 contacts (ça devient confus à l'écran)
- Une fin de scénario qui n'est pas une fin. la fin doit etre propre (par exemple résoudre un element du scénario et dire aurevoir...)

---

## Style d'écriture des messages

- Langage **ado / jeune adulte français** : abréviations naturelles, fautes légères
- Exemples de tournures réalistes :
  - "tkt" / "jsp" / "ptdr" / "mdrr" / "wsh" / "chelou" / "ouf" / "genre"
  - "c'est quoi ton insta" / "t'as vu le truc de ce matin" / "je sais pas trop"
- Les réponses doivent être **courtes** (1 à 2 lignes max)
- Laisser des messages qui **appellent une réponse** — suspense entre chaque bulle

---

## Structure narrative recommandée

```
[notification hook] → [échange qui plante le décor]
→ [twist / révélation / montée de tension
→ [chute mémorable]
-> [Terminer l'histoire pour faire sentir que c'est la fin avec une résolution (positive ou négative)]
```

---

## 10 thématiques d'histoire

### 1. La rencontre au lycée
Un garçon ou une fille envoie un premier message à quelqu'un aperçu en cours ou dans les couloirs. Tension du premier contact, maladresse, curiosité.
> Hook : _"Salut c'est le mec assis derrière toi en espagnol"_

### 2. Le secret de classe
Quelqu'un révèle un secret à quelqu'un d'autre par SMS — une rumeur, une confession, quelque chose qu'il/elle n'aurait pas dû dire.
> Hook : _"Jure que tu répètes à personne"_

### 3. La soirée qui dérape
Les SMS s'enchaînent pendant une soirée : organisation, quelqu'un qui disparaît, une situation qui tourne mal ou une rencontre inattendue.
> Hook : _"T'es où ?? ça fait 30 min"_

### 4. Le crush de longue date
Deux personnes qui se connaissent depuis longtemps, et l'une ose enfin dire quelque chose. Tension accumulée, aveu maladroit.
> Hook : _"J'aurais dû te dire ça bien avant"_

### 5. L'ex qui revient
Un message d'un ex qui revient après des semaines de silence. La personne hésite à répondre, ses amis la conseillent via une autre conv.
> Hook : _"Eh... tu vas bien ?"_ (numéro non enregistré)

### 6. L'incompréhension qui fait mal
Un malentendu par SMS qui s'emballe — un message mal interprété, une réponse froide, et une dispute qui se règle (ou pas) à la fin.
> Hook : _"Ok."_ (la pire réponse possible)

### 7. Le stage / job d'été
Deux inconnus qui se retrouvent en stage, l'un envoie le contact de l'autre à son pote, et une mini-romance démarre par SMS.
> Hook : _"C'est qui la fille avec toi sur la photo du groupe de stage ?"_

### 8. La trahison entre amis
Un ami révèle quelque chose qui blesse — une info partagée sans permission, une vanne de trop, ou une absence inexpliquée.
> Hook : _"T'aurais pu me dire que t'y allais..."_

### 9. Les parents qui écrivent comme des parents
Registre humour : échange entre un ado et son père ou sa mère qui essaie de parler "jeune" avec des fautes et des emojis décalés.
> Hook : _"Allo fiston 👋 tu rentre ce soir 🙏"_

### 10. Le coloc / voisin mystérieux
Quelqu'un reçoit un message d'un numéro inconnu — son nouveau coloc ou voisin. L'échange bascule du bizarre au drôle ou au romantique.
> Hook : _"Salut c'est ton futur coloc. T'as une rallonge ?"_

---

## Règles pour les contacts dans le JSON

- Maximum **3 contacts** par scénario (1 contact c'est aussi bien par moment)
- Chaque contact a un prénom réaliste, court
- Les avatars doivent être cohérents avec le personnage (genre, style)
- Les notifications servent de **hook visuel** — toujours la première action du script
- Un `switch` de conversation doit être **justifié narrativement** (on change de conv parce qu'un ami répond, pas au hasard)

---

## Checklist avant de générer le JSON

- [ ] Le premier message est intrigant et plante le décor immédiatement
- [ ] La durée estimée est entre 30s et 60s
- [ ] Les messages sont courts et réalistes
- [ ] Il y a une montée de tension et une chute mémorable
- [ ] Les emojis sont utilisés avec parcimonie
- [ ] Le `typingDuration` est cohérent avec la longueur du message reçu
- [ ] Les délais créent du rythme (ni trop rapide, ni trop lent)
