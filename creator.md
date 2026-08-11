# Guideline for create story (SMS Story TikTok)

Ce fichier est le brief complet pour l'agent qui génère les scénarios `scenario.json`.
L'objectif : créer des vidéos SMS virales sur TikTok, Reels et Shorts.

---

## Format technique

- Durée cible : **1 minute 30 à 3 minutes** de vidéo finale
- Nombre de messages : **20 à 40 messages** selon les délais et les switchs
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

### Ce qui retient l'attention sur la durée
- Une **tension croissante** : chaque réplique fait monter l'enjeu, jamais descendre
- Des **rebondissements** : au moins 1 à 2 twists dans le scénario (révélation inattendue, revirement, info qui change tout)
- Du **réalisme dans les fautes et le style** : les gens écrivent mal sur leurs téléphones
- Des **silences dramatiques** : une longue pause avant une réponse importante (`delay` élevé)
- Un **changement de conversation** pour varier le point de vue et ajouter une couche narrative
- Une **chute mémorable** : le dernier message doit laisser quelque chose — sourire, suspense, ou émotion

### Ce qu'il faut éviter
- Messages trop longs et bien rédigés (irréaliste)
- Trop d'emojis — **1 à 2 max par échange**, seulement si naturel
- Résolution trop rapide — tenir la tension jusqu'à la toute fin
- Langage trop formel ou trop littéraire
- Plus de 3 contacts (ça devient confus à l'écran)
- Une fin qui n'en est pas une — la fin doit résoudre clairement quelque chose

---

## Réalisme et logique narrative — règle fondamentale

**Chaque action dans le scénario doit avoir une cause logique.** Si quelque chose se passe, c'est parce qu'une action préalable l'a rendu possible.

### Les switchs de conversation doivent être déclenchés par Moi

Quand on switch vers une autre conversation, c'est **Moi qui envoie le premier message** dans cette nouvelle conversation — pas l'autre personne qui écrit "par magie".

| ❌ Incohérent | ✓ Logique |
|---|---|
| Switch vers Lucas → Lucas reçoit un message sans raison | Switch vers Lucas → Moi envoie `"t'as filé mon num à Emma ???"` → Lucas répond |
| Switch vers une amie → elle écrit spontanément | Switch vers une amie → Moi lui envoie `"t'es au courant pour ce soir ?"` → elle répond |

La seule exception : si une **notification** justifie le switch (Lucas envoie une notif d'abord, ça déclenche qu'on ouvre sa conversation).

### Exemples de transitions réalistes

**Avec notification** (justification externe) :
```
[dans conv Emma] ...
→ notification de Lucas : "t'as vu Emma aujourd'hui ?"
→ switch vers Lucas (on ouvre sa notif)
→ received Lucas : "alors t'as parlé à Emma ??"
→ sent : "ouais elle m'a écrit ce soir"
```

**Sans notification** (Moi initie) :
```
[dans conv Emma] ...
→ switch vers Lucas
→ sent : "LUCAS je vais te tuer"
→ received Lucas : "ptdr pourquoi ?"
→ sent : "t'as filé mon num à Emma"
→ received Lucas : "de rien 😎"
```

### Autres règles de cohérence
- Si quelqu'un mentionne une info (`"Lucas m'a dit que..."`), Lucas doit exister dans les contacts ou avoir été mentionné avant
- Ne pas switcher vers une conversation et recevoir immédiatement un message sans avoir rien envoyé
- Les réactions doivent être proportionnelles : un aveu fort = une réponse forte, pas un simple "ok"
- La timeline doit tenir : tout se passe dans la même soirée/journée, les références temporelles doivent être cohérentes

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

Pour une vidéo de 1m30 à 3 minutes, le scénario doit avoir plusieurs temps forts :

```
ACTE 1 — Mise en place (20-30% du scénario)
  [notification hook]
  → [échange d'introduction : qui, quoi, contexte]
  → [premier élément de tension]

ACTE 2 — Montée de tension + rebondissements (50-60%)
  → [révélation ou twist 1 : info inattendue]
  → [switch de conversation si pertinent : point de vue d'un ami, conseil, réaction]
  → [retour à la conv principale avec nouvel enjeu]
  → [twist 2 ou moment de crise : "ok." / silence / aveu]

ACTE 3 — Résolution (20-30%)
  → [réponse au twist / dénouement]
  → [conclusion claire et mémorable]
  → [dernière ligne forte — sourire, émotion, ou punch line]
```

---

## Règles absolues sur les messages

### Chaque message doit être une phrase complète et finie
Ne jamais couper une phrase en plein milieu — même pour créer du suspense. Le suspense vient de CE QU'ON DIT, pas d'une phrase incomplète.

| ❌ Interdit | ✓ Correct |
|---|---|
| `"attends c'est pas ce que-"` | `"attends, c'est pas ce que tu crois"` |
| `"j'aurais voulu te dire que..."` | `"j'aurais dû te le dire plus tôt"` |
| `"je savais pas comment te dire-"` | `"je savais pas comment te le dire, mais je t'aime bien"` |

Les `"..."` sont acceptables **uniquement** comme marque de pause/hésitation dans une phrase complète :
- `"jsp... ouais"` ✓ — hésitation naturelle
- `"je voulais juste..."` ❌ — phrase non terminée

### L'histoire doit avoir une résolution claire
Le scénario doit se terminer sur un **dénouement explicite**. Le spectateur doit comprendre comment l'histoire finit.

Exemples de bonnes fins :
- Rendez-vous pris : `"ok on se voit demain alors 🙂"`
- Aveu assumé : `"tant mieux que tu l'aies dit"`
- Réconciliation : `"c'est bon, on en reparle de vive voix"`
- Punch line : `"de rien 😎 je savais que vous étiez faits pour vous parler"`
- Fin négative mais claire : `"ok. bonne continuation alors"`

---

## 10 thématiques d'histoire

### 1. La rencontre au lycée
Un garçon ou une fille envoie un premier message à quelqu'un aperçu en cours ou dans les couloirs. Tension du premier contact, maladresse, curiosité. Un ami commun a donné le numéro — on peut switch vers cet ami pour savoir ce qu'il a dit.
> Hook : _"Salut c'est le mec assis derrière toi en espagnol"_

### 2. Le secret de classe
Quelqu'un révèle un secret à quelqu'un d'autre par SMS — une rumeur, une confession, quelque chose qu'il/elle n'aurait pas dû dire. On switch vers un autre ami pour confirmer ou infirmer le secret.
> Hook : _"Jure que tu répètes à personne"_

### 3. La soirée qui dérape
Les SMS s'enchaînent pendant une soirée : organisation, quelqu'un qui disparaît, une situation qui tourne mal ou une rencontre inattendue. Plusieurs switchs pour coordonner le groupe.
> Hook : _"T'es où ?? ça fait 30 min"_

### 4. Le crush de longue date
Deux personnes qui se connaissent depuis longtemps, et l'une ose enfin dire quelque chose. Tension accumulée, aveu maladroit. On switch vers un meilleur ami pour se faire coacher avant d'envoyer le message décisif.
> Hook : _"J'aurais dû te dire ça bien avant"_

### 5. L'ex qui revient
Un message d'un ex qui revient après des semaines de silence. La personne hésite à répondre, demande conseil à son meilleur ami (switch), puis décide quoi faire.
> Hook : _"Eh... tu vas bien ?"_ (numéro non enregistré)

### 6. L'incompréhension qui fait mal
Un malentendu par SMS qui s'emballe — un message mal interprété, une réponse froide, une dispute. On switch vers un ami commun pour comprendre ce qui se passe, puis retour pour résoudre.
> Hook : _"Ok."_ (la pire réponse possible)

### 7. Le stage / job d'été
Deux inconnus se retrouvent en stage. On switch vers un pote pour lui parler de cette personne, il nous pousse à écrire, et la mini-romance démarre.
> Hook : _"C'est qui la fille avec toi sur la photo du groupe de stage ?"_

### 8. La trahison entre amis
Un ami révèle quelque chose qui blesse — une info partagée sans permission, une vanne de trop, une absence inexpliquée. L'échange monte en tension, s'emballe, puis trouve une issue.
> Hook : _"T'aurais pu me dire que t'y allais..."_

### 9. Les parents qui écrivent comme des parents
Registre humour : échange entre un ado et son père ou sa mère qui essaie de parler "jeune" avec des fautes et des emojis décalés. On switch vers un frère/une sœur pour se moquer ensemble.
> Hook : _"Allo fiston 👋 tu rentre ce soir 🙏"_

### 10. Le coloc / voisin mystérieux
Quelqu'un reçoit un message d'un numéro inconnu — son nouveau coloc ou voisin. L'échange bascule du bizarre au drôle ou au romantique. On switch vers un ami pour partager les screenshots et avoir son avis.
> Hook : _"Salut c'est ton futur coloc. T'as une rallonge ?"_

---

## Règles pour les contacts dans le JSON

- Maximum **3 contacts** par scénario (1 contact c'est aussi bien par moment)
- Chaque contact a un prénom réaliste, court
- Les avatars doivent être cohérents avec le personnage (genre, style)
- La **première action du script** est toujours une `notification` — c'est le hook visuel
- L'action `open` doit avoir un `delay` de **200ms maximum** — la conversation doit apparaître immédiatement
- La première `notification` doit avoir un `delay` de **100ms maximum** — le hook doit frapper dans la première seconde, pas après 1-2 secondes de vide
- Un `switch` est toujours suivi d'un message **envoyé par Moi** en premier, sauf si une notification justifie l'ouverture
- Le `delay` d'un `switch` doit être **minimum 2500ms** pour laisser le temps de lire le dernier message avant que la conversation change

---

## Checklist avant de générer le JSON

- [ ] Le premier message est intrigant et plante le décor immédiatement
- [ ] La durée estimée est entre **1min30 et 3 minutes**
- [ ] Le scénario contient **20 à 40 messages**
- [ ] Il y a au moins **1 rebondissement / twist** au milieu du scénario
- [ ] Les messages sont courts et réalistes (langage ado français)
- [ ] **Chaque message est une phrase complète — aucune phrase coupée en milieu d'idée**
- [ ] **Chaque switch est logique** : Moi envoie le premier message, ou une notification justifie le switch
- [ ] Il y a une montée de tension et une chute mémorable
- [ ] **L'histoire se conclut clairement** — le spectateur sait comment ça finit
- [ ] Les emojis sont utilisés avec parcimonie
- [ ] Le `typingDuration` est cohérent avec la longueur du message reçu
- [ ] Les délais créent du rythme (ni trop rapide, ni trop lent)
