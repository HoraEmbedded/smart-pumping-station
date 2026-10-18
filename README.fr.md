# Station de pompage intelligente

**Station de pompage pour utilités industrielles : contrôle par automate (PLC), IHM/SCADA, suivi de la fiabilité et détection d'anomalies explicable**

[English version](README.md)

> **Avertissement de sécurité.** Il s'agit d'une simulation pédagogique. Ce projet ne constitue pas une conception certifiée en matière de sécurité hydraulique, électrique ou fonctionnelle et ne doit pas être utilisé pour exploiter une installation réelle.

## Problématique

Une station d'utilités en usine doit maintenir le niveau d'eau d'un réservoir de stockage entre deux seuils, tout en évitant la marche à sec, les démarrages excessifs, le débordement et les redémarrages dangereux après un défaut critique.

## Aperçu de la solution

Une station simulée à deux pompes pilotée par un automate Siemens S7-1200 (TIA Portal V18), comprenant :

- Architecture automate modulaire (modes de fonctionnement, verrouillages, alternance des pompes, gestion des alarmes)
- IHM opérateur (vue d'ensemble, alarmes, maintenance, courbes de tendance)
- Indicateurs de fiabilité (disponibilité, MTBF, MTTR, énergie spécifique)
- Détection d'anomalies explicable basée sur des règles
- Traçabilité des exigences et preuves de tests documentées

## État du projet

| Version | Objectif | État |
| --- | --- | --- |
| V0 | Conception : exigences, P&ID, liste d'E/S, Grafcet, plan de test | Terminé |
| V1 | Contrôle d'une seule pompe | Terminé |
| V2 | Deux pompes, alternance, gestion des défauts | Terminé|
| V3 | IHM/SCADA | Prévu |
| V4 | Connexion des données et tableau de bord | Prévu |
| V5 | Détection d'anomalies | Prévu |
| V6 | Rapport final et portfolio | Prévu |

## Structure du dépôt

| Dossier | Contenu |
| --- | --- |
| `01_requirements/` | Périmètre, hypothèses, exigences, matrice de traçabilité |
| `02_design/` | P&ID, liste d'E/S, matrice des alarmes, Grafcet |
| `03_plc/` | Exportations et notes relatives à l'automate |
| `04_hmi/` | Écrans IHM et guide opérateur |
| `05_iiot_data/` | Flux de données, jeux de données, analyse Python |
| `06_tests/` | Plan de test, résultats, preuves |
| `07_media/` | Supports de démonstration |
| `08_report/` | Rapport final |
| `docs/` | Documentation transversale et journal des décisions |
| `captures/` | Captures d'écran, classées par iteration |

## Outils

TIA Portal V18, S7-PLCSIM V18 SP2, Python 3.13, Git, VS Code. Voir [docs/workstation.md](docs/workstation.md).



## Perspectives

Cette simulation est une base. Les évolutions possibles incluent un modèle de variateur de fréquence, un échange de données OPC UA, une extension d'apprentissage automatique validée et un banc d'essai matériel en boucle.

Point d’accès OPC UA sécurisé par messages signés et chiffrés et gestion de la confiance des certificats, Évaluation de sécurité par zones et conduits (IEC 62443), Portage sur S7-1500 permettant PLCSIM Advanced, un serveur OPC UA natif et la publication MQTT.
- Détection de fuite par résidu de bilan de masse (variation de niveau contre débit intégré)
- Détecteur statistique ou appris évalué contre ces règles sur des données de terrain

## Licence

MIT, voir [LICENSE](LICENSE).