# Source — Strategie_IA_COMEX_Indigo.pptx

*Extracted 2026-10-13 by `studio extract` from `/Users/satcheenshakya/Documents/IndigoNeo/presentations/Strategie_IA_COMEX_Indigo.pptx`.*

## Slide 1 — Stratégie IA : dépasser le mythe, cibler la valeur
- Comité exécutif, octobre 2026

> Notes: Mesdames et messieurs, bonjour.
> 
> On nous présente souvent l'intelligence artificielle comme une baguette magique, capable de transformer une organisation du jour au lendemain. 
> 
> Mon objectif aujourd'hui n'est pas d'alimenter ce discours, mais de vous apporter un regard d'ingénieur : lucide, pragmatique, et ancré dans la réalité de nos opérations.
> 
> En quelques minutes : ce qu'est vraiment l'IA, ce qu'elle peut faire pour nous, et comment nous y prendre.

## Slide 2 — De quoi parle-t-on quand on dit « IA » ?
- Un LLM est entraîné à produire une réponse plausible, pas une réponse vérifiée
- IA
- MACHINE LEARNING
- LLM
- Intelligence artificielle
- Machine learning
- Grands modèles de langage (LLM)
- Un terme parapluie : tout système qui imite une capacité
- humaine. Souvent, un argument marketing.
- Des modèles qui apprennent des motifs dans des données pour prédire un résultat.
- Ils prédisent la suite de texte la plus probable : fluide et
- convaincante, pas forcément exacte.

> Notes: Commençons par le vocabulaire.
> 
> « Intelligence artificielle » est un terme parapluie : il désigne tout système qui imite une capacité humaine, et c'est devenu un argument commercial.
> 
> Techniquement, ce que nous utilisons au quotidien, c'est du machine learning, de l'apprentissage automatique : des modèles qui apprennent des motifs dans des données pour prédire un résultat.
> 
> Les grands modèles de langage, les LLM, comme ChatGPT, Copilot ou Mistral, en sont une famille particulière : ils prédisent la suite de texte la plus probable. C'est ce qui les rend si fluides… et c'est aussi leur limite. Ils sont entraînés à produire une réponse plausible, pas une réponse vérifiée. Quand ils se trompent, ils se trompent avec assurance.
> 
> Dans nos métiers, où l'exactitude compte, cette nuance change tout.Speak about deep leaning a little and combine that

## Slide 3 — Assister ou automatiser : deux métiers différents
- Comme le cerveau humain, nos outils fonctionnent sur deux systèmes
- ASSISTANCE (AI)
- Système 2 : lent, réfléchi
- AUTOMATISATION (NOT AI)
- Système 1 : rapide, réflexe
- L'humain reste aux commandes
- Il relit, corrige, valide.
- Du langage ouvert
- Rédiger, résumer, reformuler.
- Tolère l'imprécision
- L'erreur est rattrapée par l'agent.
- Aucun humain dans la boucle
- Le système décide seul.
- Règles et modèles de décision
- Classer, router, déclencher.
- Exige une erreur bornée
- Les cas incertains repartent vers un humain.
- Suggérer à l'agent une réponse à partir de l'historique client
- Router automatiquement le ticket vers le bon agent

> Notes: D'où la distinction centrale de cette présentation : assister ou automatiser.
> 
> On peut s'inspirer du cerveau humain, qui fonctionne avec deux systèmes : un système lent et réfléchi, et un système rapide et réflexe.
> 
> L'assistance, c'est le premier. Le modèle de langage rédige, résume, reformule, et l'humain reste aux commandes : il relit et il valide. Une erreur est rattrapée.
> 
> L'automatisation, c'est le second. Le système agit seul. Il faut donc des règles et des modèles de décision dont l'erreur est connue et bornée, et tout cas incertain doit repartir vers un humain.
> 
> Prenons le CRC. Suggérer une réponse à un agent à partir de l'historique client, c'est de l'assistance : l'agent garde la main. Router automatiquement un ticket vers le bon agent, c'est de l'automatisation, et cela ne se conçoit pas du tout de la même façon.
> 
> Le même mot « IA » recouvre deux projets radicalement différents.

## Slide 4 — chatbot InPark : ce que le PROJET nous a appris
- Le modèle comprend la question ; encore faut-il lui donner accès à la donnée
- La question
- L'utilisateur s'exprime en langage naturel.
- Réalisé
- Le harnais
- Comprend l'intention et structure la demande.
- À construire
- Les outils (type MCP)
- Donnent au modèle un accès direct et lisible à la base InPark.
- La réponse
- Exacte et à jour, car fondée sur la donnée réelle.
- Internaliser les compétences. Avoir une équipe dédier qui connait le métier et la technique : c'est là que se joue la qualité.

> Notes: Un exemple concret : le chatbot InPark.
> 
> Nous avons construit ce qu'on appelle un harnais : une couche qui aide le modèle à comprendre ce que l'utilisateur veut vraiment, et à structurer sa réponse. Cette partie fonctionne.
> 
> Ce qui manque, c'est la brique suivante : donner au modèle des outils pour aller lire directement la donnée dans la base InPark, sous une forme qu'il peut exploiter. C'est ce que standardise aujourd'hui un protocole comme MCP. Sans cette brique, le modèle comprend la question, mais il travaille avec une donnée incomplète, et c'est ce qui limite la qualité des réponses.
> 
> La leçon est importante : avoir les competence en interne, voila ou on peut commencer a créer de la reele valeur. Car des equipes en interne qui connaisent et le metier et la technique aront les comptence pour modeliser les donner et les processus afin de les optimiser pour les modeles d’IA.NOT direct access to the data -> but aces to  »gold » data

## Slide 5 — La qualité de l'IA dépend de notre organisation
- La réponse vaut ce que vaut la donnée ; l'action vaut ce que vaut le processus
- QUALITÉ DESRÉPONSES
- MCP
- DONNÉES PROPRES
- Fiables, structurées, accessibles
- QUALITÉ DES ACTIONS
- ALGO
- PROCESSUS DOCUMENTÉS
- Chaque étape, chaque exception, chaque erreur connue
- Le chantier est d'abord organisationnel, ensuite technologique.
- Une IA branchée sur des données incomplètes ou des processus flous ne corrige pas le désordre : elle l'automatise.
- Cibler d'abord les périmètres où données et processus sont déjà solides.

> Notes: Cela nous amène au cœur du sujet.
> 
> La qualité d'une réponse dépend de la qualité de la donnée. Et demain, si nous voulons des agents qui agissent, la qualité d'une action dépendra de la qualité du processus en place.
> 
> Une IA branchée sur des données incomplètes ou des processus flous ne corrige pas le désordre : elle l'automatise, et plus vite.
> 
> Le vrai chantier est donc d'abord organisationnel. Il demande des changements opérationnels réels. C'est pourquoi il faut cibler des périmètres précis, là où les données et les processus sont déjà solides, tout en restant attentifs à ce que le marché propose.
> The link here is a little to directe

## Slide 6 — Construire, assembler ou s'associer ?
- Investir là où nous créons de la valeur métier
- Construire
- Coût
- (Entraîner notre propre modèle sur nos données.)
- –  Infrastructure de calcul lourde
- –  Talents rares sur le marché
- –  Retour sur investissement incertain
- Prématuré aujourd'hui
- NOTRE VOIE
- Assembler
- Coût
- Modèles du marché outils branchés sur nos données.
- –  L'approche InPark
- –  Investissement maîtrisé
- –  S'appuie sur l'équipe digitale
- Notre voie
- S'associer
- Coût
- Un partenaire européen Mistral, si un besoin spécifique émerge.
- –  Expertise externe
- –  Risque partagé
- –  Souveraineté des données
- Option à terme

> Notes: Faut-il construire notre propre IA ?
> 
> C'est techniquement possible : reproduire un outil de type ChatGPT ou Copilot sur nos propres données. Mais entraîner notre propre modèle mobilise une infrastructure de calcul lourde et des talents très rares, pour un retour incertain. Et surtout, cela suppose des processus et une documentation qui ne sont pas encore en place. Aujourd'hui, c'est prématuré.
> 
> Notre voie, c'est d'assembler : des modèles du marché, branchés sur nos données, comme nous l'avons fait avec InPark.
> 
> Et si un besoin spécifique émerge, un partenariat avec un acteur européen comme Mistral nous permettrait de partager le risque tout en gardant la maîtrise de nos données.I need to make this slide a little more self explanatoryEntraîner notre propre modèle sur nos données. -> this is not clear and we have to explain

## Slide 7 — Notre plan en trois temps
- Préparer le terrain aujourd'hui pour automatiser à grande échelle demain
- 01
- CARTOGRAPHIER
- Iidentifier et documenter ce qui est réellement automatisable.
- 02
- OUTILLER
- Donner à l'équipe digitale existante des outils et une vraie culture de l'IA.
- 03
- EXPÉRIMENTER
- Des pilotes ciblés et mesurables, par exemple l'assistance aux agents du CRC.
- Horizon 3 ans : automatiser à grande échelle, sur un socle maîtrisé

> Notes: change the order here -> to make it iterative experiement (like InPark)you don’t need to “catrographier” everything in one go. You can do it step AGILE FEEDBACK LOOP !!!Concrètement, je propose trois temps.
> 
> D'abord, cartographier. Le vrai changement  est culturel: comprendre ce qui est réellement automatisable, puis le documenter. Ce sont des réunions, du travail de fond, mais c'est la condition de tout le reste.
> 
> Ensuite, outiller. Nous avons déjà une équipe digitale qui fonctionne très bien. Il ne s'agit pas de former tout le monde, mais de lui donner des outils et une vraie culture de l'IA, pour qu'elle identifie elle-même les processus à optimiser.
> 
> Enfin, expérimenter. Des pilotes ciblés, avec un gain mesurable. Par exemple aider les agents du CRC à mieux répondre, plutôt que de faire répondre une IA à leur place.
> 
> C'est en préparant ce terrain aujourd'hui que nous pourrons, d'ici trois ans, automatiser beaucoup plus largement, sans fragiliser nos opérations.

## Slide 8 — L'IA doit amplifier nos équipes, pas penser à leur place
- Pragmatisme, rigueur, valeur
- PRAGMATISME
- Cibler des cas d'usage précis plutôt que suivre le battage médiatique.
- RIGUEUR
- Des données propres et des processus documentés avant toute automatisation.
- VALEUR
- Mesurer chaque gain avant d'aller plus loin.
- NOTRE PROPOSITION
- TO BE DEFINED

> Notes: Pour résumer.
> 
> Pragmatisme : cibler des cas d'usage précis plutôt que suivre le battage médiatique.
> Rigueur : investir d'abord dans nos données et nos processus.
> Valeur : mesurer chaque gain avant d'aller plus loin.
> 
> L'IA ne doit pas penser à notre place : elle doit amplifier l'efficacité de nos équipes, sur des processus maîtrisés.
> 
> Ma proposition : TO BE DEFINED
> ideation:  
> 1= lancer un premier pilote d'assistance aux agents du CRC, et engager la cartographie des processus candidats à l'automatisation.
> 
> Je vous remercie, et je suis à votre disposition pour vos questions.

## Slide 9

> Notes: Merci pour votre attention. Place à vos questions.
