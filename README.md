# Les données de BlueSphere

`experiments.csv` est construit par `tools/build_dataset.py` à partir des tableaux d'essais de PSI, copiés tels quels dans `raw/` (seuls les espaces en trop ont été retirés). Une ligne = un essai, ou un groupe d'essais identiques (colonne `n_tests`).

Unités : oxygène en % du volume, pression en kPa, vitesse de l'air en cm/s, épaisseur en mm.

## Comment chaque tableau est lu

**BASS-II (PSI-25), 129 essais.** La colonne « Air display » est lue comme la vitesse de l'air en cm/s : le tunnel de BASS-II imposait jusqu'à 40 cm/s. Les valeurs entre parenthèses et celles qui suivent « pot » sont des lectures du potentiomètre du ventilateur, pas des vitesses : elles sont ignorées. « <1 » devient 0,5 cm/s. L'oxygène est la valeur initiale calibrée. Le résultat vient des mots notés dans le tableau : « ext » ou « extinguished » (éteinte en réduisant l'air), « blowoff » (soufflée par un air trop rapide), « no ign » (pas d'allumage), « off » (ventilateur coupé, résultat inconnu). Le point de l'Atlas est placé à la plus faible vitesse notée, ou à la plus forte en cas de « blowoff ». Le texte brut reste dans la colonne `notes`.

**Saffire-I, II et III (PSI-98, 99, 100).** Lus directement. Pour Saffire-II, l'oxygène a été déduit du CO₂ mesuré (note 1 du tableau). L'échantillon 2-7 est séparé en deux lignes : le PMMA a brûlé, le Nomex ne s'est pas allumé. Le tableau de Saffire-III ne donne ni l'oxygène ni le résultat : ses deux essais ne sont pas sur la carte.

**FLEX (PSI-69), 274 gouttes.** Regroupées par combustible, pression, oxygène, dilution (CO₂ ou hélium) et fin d'essai : 149 groupes (`raw/PSI-69_FLEX_grouped.csv`). « Extinction » = la flamme s'est éteinte avant la fin de la goutte ; « Completion » et « Disruption » = la goutte a brûlé. Air immobile (0 cm/s).

**ACME BRE (PSI-20), 194 flammes.** Le tableau de PSI résume chaque journée : les concentrations d'oxygène où des flammes ont pris, et le nombre de flammes allumées. Une ligne par journée et par concentration ; le nombre exact par concentration n'est pas connu. « 3400% » et « 2100% » sont lus comme 34 % et 21 %. Air immobile.

**FLEX-2 (PSI-68).** PSI ne donne que les plages étudiées (17 à 30 % d'O₂, 0,5 à 3 atm, 0,1 à 5 cm/s), pas chaque essai : FLEX-2 n'est pas sur la carte.

**CFI-G (PSI-159), 154 essais.** Flammes inversées : l'oxygène (jusqu'à 85 %) sort du brûleur dans une atmosphère de combustible. Ce n'est pas l'oxygène de l'air ambiant, donc CFI-G n'est pas sur la carte. Les essais sont regroupés dans `raw/PSI-159_CFI-G_grouped.csv`.
