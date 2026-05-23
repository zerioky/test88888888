# -*- coding: utf-8 -*-
"""
leia_spacy_engine.py — Moteur linguistique profond V2.3 (Pure Python)
Corrections V2.3 :
  - Chunker GV absorbe clitiques PRON par recul (pas avalement)
  - Lemmatisation protégée : noms <= 5 caractères conservés
  - DiscourseContext réinitialisé entre tests
  - Verbes réfléchis + résister dans le lexique
"""

from __future__ import annotations
import math, re, time, unicodedata
from collections import Counter, defaultdict, deque
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple, Union

# ─── LEXIQUE ─────────────────────────────────────────────────────────────────
_STOP = {"le","la","les","l","un","une","des","du","de","d","au","aux","en","et","est","à","il","elle","ils","elles","on","je","tu","nous","vous","me","te","se","ce","cet","cette","ces","son","sa","ses","mon","ma","mes","ton","ta","tes","notre","nos","votre","vos","leur","leurs","mien","tien","sien","quoi","dont","où","mais","ou","or","ni","car","qu","que","qui","ceci","cela","ça","ca","y","en","lui","soi","j","m","t","s","n","c","jusque","quoique","lorsque","puisque","quand","comment","combien"}
_PRON_SUBJ = {"je","tu","il","elle","on","nous","vous","ils","elles"}
_PRON_OBJ = {"me","te","se","le","la","les","lui","leur","nous","vous","en","y","l'","l"}
_PRON_DEM = {"ce","ceci","cela","ça","ca","celui","celui-ci","celle","celle-ci","ceux","ceux-ci"}
_PRON_REL = {"qui","que","quoi","dont","où","lequel","laquelle","lesquels"}
_PRON_INT = {"qui","que","quoi","quel","quelle","quels","quelles","comment","pourquoi","combien"}
_PRON_ALL = _PRON_SUBJ | _PRON_OBJ | _PRON_DEM | _PRON_REL | _PRON_INT
_CONTRACTIONS = {"m'","t'","s'","n'","c'","j'","l'","d'","qu'"}

_AUX_BE = {"être","suis","es","est","sommes","êtes","sont","étais","était","étions","étiez","étaient","serai","seras","sera","serons","serez","seront","sois","soit","soyons","soyez","soient","fus","fut","fûmes","fûtes","furent","étant"}
_AUX_HAVE = {"avoir","ai","as","a","avons","avez","ont","avais","avait","avions","aviez","avaient","aurai","auras","aura","aurons","aurez","auront","eus","eut","eûmes","eûtes","eurent","ayant","eu"}
_AUX_MODAL = {"pouvoir","peux","peut","pouvons","pouvez","peuvent","devoir","dois","doit","devons","devez","doivent","vouloir","veux","veut","voulons","voulez","veulent","falloir","faut","faudra","faudrait","pourra","pourras","pourrai","pourront","pourrons","pourrez","devrait","devras","devrai","devront","devrons","devrez"}
_COPULA = _AUX_BE | {"paraître","sembler","devenir","rester","demeurer","paraissait","paraît","semble","semblait"}

# Verbes : liste racines + toutes formes irrégulières fréquentes
_VERBS = {
    # Racines / infinitifs
    "être","avoir","faire","dire","aller","voir","savoir","pouvoir","falloir","vouloir","venir","prendre","passer","trouver","donner","parler","aimer","croire","penser","montrer","entendre","comprendre","rester","porter","devenir","revenir","entrer","rendre","vivre","tenir","appeler","partir","suivre","attendre","sentir","connaître","regarder","arriver","douter","hésiter","craindre","espérer","désirer","choisir","décider","résoudre","accepter","refuser","répondre","demander","questionner","discuter","argumenter","objecter","conclure","résumer",
    "affirmer","nier","démontrer","prouver","supposer","postuler","définir","concevoir","considérer","estimer","reconnaître","admettre","rejeter","contester","distinguer","opposer","comparer","expliquer","analyser","qualifier","constituer","former","produire","engendrer","causer","déterminer","conditionner","permettre","impliquer","suggérer","indiquer","révéler","signifier","désigner","nommer","appeler","identifier","représenter","symboliser","ressentir","éprouver","résister",
    # Formes conjuguées courantes (pour tagger rapide sans regex)
    "exister","existe","existent","existaient","pense","penses","pensons","pensez","pensent","pensait","pensaient",
    "trompe","trompes","trompons","trompez","trompent","trompait","trompaient",
    "donne","donnes","donnons","donnez","donnent","donnait",
    "parle","parles","parlons","parlez","parlent","parlait",
    "crois","croit","croyons","croyez","croient","croyait",
    "sens","sent","sentons","sentez","sentent","sentait",
    "trouve","trouves","trouvons","trouvez","trouvent","trouvait",
    "mange","manges","mangeons","mangez","mangent",
    "perd","perds","perdons","perdez","perdent","perdait",
    "finis","finit","finissons","finissez","finissent",
    "punis","punit","punissons","punissez","punissent",
    "réfléchis","réfléchit","réfléchissons","réfléchissez","réfléchissent",
    "agis","agit","agissons","agissez","agissent",
    "réussis","réussit","réussissons","réussissez","réussissent",
    "saisis","saisit","saisissons","saisissez","saisissent",
    "guéris","guérit","guérissons","guérissez","guérissent",
    "réponds","répond","répondons","répondez","répondent",
    "perds","perd","perdons","perdez","perdent",
    "vends","vend","vendons","vendez","vendent",
    "prends","prend","prenons","prenez","prennent",
    "apprends","apprend","apprenons","apprenez","apprennent",
    "comprends","comprend","comprenons","comprenez","comprennent",
    "surprends","surprend","surprenons","surprenez","surprennent",
    "attends","attend","attendons","attendez","attendent",
    "descends","descend","descendons","descendez","descendent",
    "entends","entend","entendons","entendez","entendent",
    "rends","rend","rendons","rendez","rendent",
    "tends","tend","tendons","tendez","tendent",
    "répands","répand","répandons","répandez","répandent",
    "mords","mord","mordons","mordez","mordent",
    "tords","tord","tordons","tordez","tordent",
    "crains","craint","craignons","craignez","craignent",
    "plains","plaint","plaignons","plaignez","plaignent",
    "joins","joint","joignons","joignez","joignent",
    "vaincs","vainc","vainquons","vainquez","vainquent",
    "convaincs","convainc","convainquons","convainquez","convainquent",
    "nais","naît","naissons","naissez","naissent",
    "pais","paît","paissons","passez","paissent",
    "crois","croit","croyons","croyez","croient",
    "vois","voit","voyons","voyez","voient",
    "fuir","fuis","fuit","fuyons","fuyez","fuient",
    "ouvre","ouvres","ouvrons","ouvrez","ouvrent",
    "couvre","couvres","couvrons","couvrez","couvrent",
    "offre","offres","offrons","offrez","offrent",
    "souffre","souffres","souffrons","souffrez","souffrent",
    "cueille","cueilles","cueillons","cueillez","cueillent",
    "assailli","assaillit","assaillissons","assaillissez","assaillissent",
    "dors","dort","dormons","dormez","dorment",
    "mens","ment","mentons","mentez","mentent",
    "pars","part","partons","partez","partent",
    "ris","rit","rions","riez","rient",
    "conclus","conclut","concluons","concluez","concluent",
    "cuis","cuit","cuirons","cuirez","cuiront",
    "plais","plaît","plaisons","plaisez","plaisent",
    "tais","tait","taisons","taisez","taisent",
    "vis","vit","vivons","vivez","vivent",
    "lis","lit","lisons","lisez","lisent",
    "soumet","soumets","soumettons","soumettez","soumettent",
    "admets","admet","admettons","admettez","admettent",
    "promets","promet","promettons","promettez","promettent",
    "permets","permet","permettons","permettez","permettent",
    "transmets","transmet","transmettons","transmettez","transmettent",
    "déçois","déçoit","déçoivons","décevez","déçoivent",
    "aperçois","aperçoit","apercevons","apercevez","aperçoivent",
    "conçois","conçoit","concevons","concevez","conçoivent",
    "reçois","reçoit","recevons","recevez","reçoivent",
    # Verbes fréquents en -er manquants
    "donner","donne","donnes","donnons","donnez","donnent",
    "passer","passe","passes","passons","passez","passent",
    "porter","porte","portes","portons","portez","portent",
    "montrer","montre","montres","montrons","montrez","montrent",
    "demander","demande","demandes","demandons","demandez","demandent",
    "répondre","réponds","répond","répondons","répondez","répondent",
    "parler","parle","parles","parlons","parlez","parlent",
    "trouver","trouve","trouves","trouvons","trouvez","trouvent",
    "laisser","laisse","laisses","laissons","laissez","laissent",
    "penser","pense","penses","pensons","pensez","pensent",
    "sembler","semble","sembles","semblons","semblez","semblent",
    "entrer","entre","entres","entrons","entrez","entrent",
    "rester","reste","restes","restons","restez","restent",
    "mener","mène","mènes","menons","menez","mènent",
    "lever","lève","lèves","levons","levez","lèvent",
    "manger","mange","manges","mangeons","mangez","mangent",
    "lancer","lance","lances","lançons","lancez","lancent",
    "commencer","commence","commences","commençons","commencez","commencent",
    "placer","place","places","plaçons","placez","placent",
    "payer","paie","paies","payons","payez","paient",
    "acheter","achète","achètes","achetons","achetez","achètent",
    "appeler","appelle","appelles","appelons","appelez","appellent",
    "jeter","jette","jettes","jetons","jetez","jettent",
    "rappeler","rappelle","rappelles","rappelons","rappelez","rappellent",
    "envoyer","envoie","envoies","envoyons","envoyez","envoient",
    "essayer","essaie","essaies","essayons","essayez","essaient",
    "employer","emploie","emploies","employons","employez","emploient",
    "nettoyer","nettoie","nettoies","nettoyons","nettoyez","nettoient",
    "nouer","noue","noues","nouons","nouez","nouent",
    "essuyer","essuie","essuies","essuyons","essuyez","essuient",
    "s’asseoir","assieds","assied","asseyons","asseyez","asseyent",
    "s'asseoir","assieds","assied","asseyons","asseyez","asseyent",
    "voir","vois","voit","voyons","voyez","voient","vis","vit","vîmes","vîtes","virent",
    "croire","crois","croit","croyons","croyez","croient",
    "boire","bois","boit","buvons","buvez","boivent",
    "dire","dis","dit","disons","dites","disent",
    "faire","fais","fait","faisons","faites","font",
    "savoir","sais","sait","savons","savez","savent",
    "pouvoir","peux","peut","pouvons","pouvez","peuvent",
    "devoir","dois","doit","devons","devez","doivent",
    "vouloir","veux","veut","voulons","voulez","veulent",
    "prendre","prends","prend","prenons","prenez","prennent",
    "apprendre","apprends","apprend","apprenons","apprenez","apprennent",
    "comprendre","comprends","comprend","comprenons","comprenez","comprennent",
    "surprendre","surprends","surprend","surprenons","surprenez","surprennent",
    "mettre","mets","met","mettons","mettez","mettent",
    "permettre","permets","permet","permettons","permettez","permettent",
    "soumettre","soumets","soumet","soumettons","soumettez","soumettent",
    "transmettre","transmets","transmet","transmettons","transmettez","transmettent",
    "admettre","admets","admet","admettons","admettez","admettent",
    "promettre","promets","promet","promettons","promettez","promettent",
    "répondre","réponds","répond","répondons","répondez","répondent",
    "perdre","perds","perd","perdons","perdez","perdent",
    "rendre","rends","rend","rendons","rendez","rendent",
    "vendre","vends","vend","vendons","vendez","vendent",
    "tendre","tends","tend","tendons","tendez","tendent",
    "répandre","répands","répand","répandons","répandez","répandent",
    "mordre","mords","mord","mordons","mordez","mordent",
    "tordre","tords","tord","tordons","tordez","tordent",
    "craindre","crains","craint","craignons","craignez","craignent",
    "plaindre","plains","plaint","plaignons","plaignez","plaignent",
    "feindre","feins","feint","feignons","feignez","feignent",
    "joindre","joins","joint","joignons","joignez","joignent",
    "poindre","poinds","poind","poignons","poignez","poignent",
    "atteindre","atteins","atteint","atteignons","atteignez","atteignent",
    "éteindre","éteins","éteint","éteignons","éteignez","éteignent",
    "peindre","peins","peint","peignons","peignez","peignent",
    "vaincre","vaincs","vainc","vainquons","vainquez","vainquent",
    "convaincre","convaincs","convainc","convainquons","convainquez","convainquent",
    "vivre","vis","vit","vivons","vivez","vivent",
    "suivre","suis","suit","suivons","suivez","suivent",
    "poursuivre","poursuis","poursuit","poursuivons","poursuivez","poursuivent",
    "ouvrir","ouvre","ouvres","ouvrons","ouvrez","ouvrent",
    "couvrir","couvre","couvres","couvrons","couvrez","couvrent",
    "offrir","offre","offres","offrons","offrez","offrent",
    "souffrir","souffre","souffres","souffrons","souffrez","souffrent",
    "cueillir","cueille","cueilles","cueillons","cueillez","cueillent",
    "assaillir","assaillis","assaillit","assaillissons","assaillissez","assaillissent",
    "fuir","fuis","fuit","fuyons","fuyez","fuient",
    "courir","cours","court","courons","courez","courent",
    "mourrir","meurs","meurt","mourons","mourez","meurent",
    "valoir","vaux","vaut","valons","valez","valent",
    "falloir","faut","faudra","faudrait",
    "chaloir","chaut",
    "échoir","échoit","échoyons","échoyez","échoient",
    "déchoir","déchoit",
    "choisir","choisis","choisit","choisissons","choisissez","choisissent",
    "finir","finis","finit","finissons","finissez","finissent",
    "réussir","réussis","réussit","réussissons","réussissez","réussissent",
    "guérir","guéris","guérit","guérissons","guérissez","guérissent",
    "pâlir","pâlis","pâlit","pâlissons","pâlissez","pâlissent",
    "rougir","rougis","rougit","rougissons","rougissez","rougissent",
    "maigrir","maigris","maigrit","maigrissons","maigrissez","maigrissent",
    "grandir","grandis","grandit","grandissons","grandissez","grandissent",
    "vieillir","vieillis","vieillit","vieillissons","vieillissez","vieillissent",
    "rajeunir","rajeunis","rajeunit","rajeunissons","rajeunissez","rajeunissent",
    "blanchir","blanchis","blanchit","blanchissons","blanchissez","blanchissent",
    "noircir","noircis","noircit","noircissons","noircissez","noircissent",
    "raccourcir","raccourcis","raccourcit","raccourcissons","raccourcissez","raccourcissent",
    "durcir","durcis","durcit","durcissons","durcissez","durcissent",
    "amollir","amollis","amollit","amollissons","amollissez","amollissent",
    "applaudir","applaudis","applaudit","applaudissons","applaudissez","applaudissent",
    "réagir","réagis","réagit","réagissons","réagissez","réagissent",
    "agir","agis","agit","agissons","agissez","agissent",
    "bénir","bénis","bénit","bénissons","bénissez","bénissent",
    "verdir","verdis","verdit","verdissons","verdissez","verdissent",
    "jaunir","jaunis","jaunit","jaunissons","jaunissez","jaunissent",
    "blêmir","blêmis","blêmit","blêmissons","blêmissez","blêmissent",
    "languir","languis","languit","languissons","languissez","languissent",
    "réfléchir","réfléchis","réfléchit","réfléchissons","réfléchissez","réfléchissent",
    "maudire","maudis","maudit","maudissons","maudissez","maudissent",
    "vêtir","vêts","vêt","vêtons","vêtez","vêtent",
    "tenir","tiens","tient","tenons","tenez","tiennent",
    "venir","viens","vient","venons","venez","viennent",
    "revenir","reviens","revient","revenons","revenez","reviennent",
    "devenir","deviens","devient","devenons","devenez","deviennent",
    "maintenir","maintiens","maintient","maintenons","maintenez","maintiennent",
    "soutenir","soutiens","soutient","soutenons","soutenez","soutiennent",
    "retenir","retiens","retient"," retenons","retenez","retiennent",
    "appartenir","appartiens","appartient","appartenons","appartenez","appartiennent",
    "convenir","conviens","convient","convenons","convenez","conviennent",
    "intévenir","interviens","intervient","intervenons","intervenez","interviennent",
    "prévenir","préviens","prévient","prévenons","prévenez","préviennent",
    "obtenir","obtiens","obtient","obtenons","obtenez","obtiennent",
    "recevoir","reçois","reçoit","recevons","recevez","reçoivent",
    "concevoir","conçois","conçoit","concevons","concevez","conçoivent",
    "apercevoir","aperçois","aperçoit","apercevons","apercevez","aperçoivent",
    "émouvoir","émeus","émeut","émouvons","émouvez","émeuvent",
    "promouvoir","promus","promut","promouvons","promouvez","promeuvent",
    "s'asseoir","assieds","assied","asseyons","asseyez","asseyent",
    "s'asseoir","assieds","assied","asseyons","asseyez","asseyent",
    "voir","vois","voit","voyons","voyez","voient","vis","vit","vîmes","vîtes","virent",
    "croire","crois","croit","croyons","croyez","croient",
    "boire","bois","boit","buvons","buvez","boivent",
    "croire","crois","croit","croyons","croyez","croient",
    "dire","dis","dit","disons","dites","disent",
    "faire","fais","fait","faisons","faites","font",
    "savoir","sais","sait","savons","savez","savent",
    "pouvoir","peux","peut","pouvons","pouvez","peuvent",
    "devoir","dois","doit","devons","devez","doivent",
    "vouloir","veux","veut","voulons","voulez","veulent",
    "prendre","prends","prend","prenons","prenez","prennent",
    "apprendre","apprends","apprend","apprenons","apprenez","apprennent",
    "comprendre","comprends","comprend","comprenons","comprenez","comprennent",
    "surprendre","surprends","surprend","surprenons","surprenez","surprennent",
    "mettre","mets","met","mettons","mettez","mettent",
    "permettre","permets","permet","permettons","permettez","permettent",
    "soumettre","soumets","soumet","soumettons","soumettez","soumettent",
    "transmettre","transmets","transmet","transmettons","transmettez","transmettent",
    "admettre","admets","admet","admettons","admettez","admettent",
    "promettre","promets","promet","promettons","promettez","promettent",
    "répondre","réponds","répond","répondons","répondez","répondent",
    "perdre","perds","perd","perdons","perdez","perdent",
    "rendre","rends","rend","rendons","rendez","rendent",
    "vendre","vends","vend","vendons","vendez","vendent",
    "tendre","tends","tend","tendons","tendez","tendent",
    "répandre","répands","répand","répandons","répandez","répandent",
    "mordre","mords","mord","mordons","mordez","mordent",
    "tordre","tords","tord","tordons","tordez","tordent",
    "craindre","crains","craint","craignons","craignez","craignent",
    "plaindre","plains","plaint","plaignons","plaignez","plaignent",
    "feindre","feins","feint","feignons","feignez","feignent",
    "joindre","joins","joint","joignons","joignez","joignent",
    "poindre","poinds","poind","poignons","poignez","poignent",
    "atteindre","atteins","atteint","atteignons","atteignez","atteignent",
    "éteindre","éteins","éteint","éteignons","éteignez","éteignent",
    "peindre","peins","peint","peignons","peignez","peignent",
    "vaincre","vaincs","vainc","vainquons","vainquez","vainquent",
    "convaincre","convaincs","convainc","convainquons","convainquez","convainquent",
    "vivre","vis","vit","vivons","vivez","vivent",
    "suivre","suis","suit","suivons","suivez","suivent",
    "poursuivre","poursuis","poursuit","poursuivons","poursuivez","poursuivent",
    "ouvrir","ouvre","ouvres","ouvrons","ouvrez","ouvrent",
    "couvrir","couvre","couvres","couvrons","couvrez","couvrent",
    "offrir","offre","offres","offrons","offrez","offrent",
    "souffrir","souffre","souffres","souffrons","souffrez","souffrent",
    "cueillir","cueille","cueilles","cueillons","cueillez","cueillent",
    "assaillir","assaillis","assaillit","assaillissons","assaillissez","assaillissent",
    "fuir","fuis","fuit","fuyons","fuyez","fuient",
    "courir","cours","court","courons","courez","courent",
    "mourrir","meurs","meurt","mourons","mourez","meurent",
    "valoir","vaux","vaut","valons","valez","valent",
    "falloir","faut","faudra","faudrait",
    "vouloir","veux","veut","voulons","voulez","veulent",
    "savoir","sais","sait","savons","savez","savent",
    "pouvoir","peux","peut","pouvons","pouvez","peuvent",
    "devoir","dois","doit","devons","devez","doivent",
    "mouvoir","meus","meut","mouvons","mouvez","meuvent",
    "promouvoir","promus","promut","promouvons","promouvez","promeuvent",
    "choisir","choisis","choisit","choisissons","choisissez","choisissent",
    "finir","finis","finit","finissons","finissez","finissent",
    "réussir","réussis","réussit","réussissons","réussissez","réussissent",
    "guérir","guéris","guérit","guérissons","guérissez","guérissent",
    "pâlir","pâlis","pâlit","pâlissons","pâlissez","pâlissent",
    "rougir","rougis","rougit","rougissons","rougissez","rougissent",
    "maigrir","maigris","maigrit","maigrissons","maigrissez","maigrissent",
    "grandir","grandis","grandit","grandissons","grandissez","grandissent",
    "vieillir","vieillis","vieillit","vieillissons","vieillissez","vieillissent",
    "rajeunir","rajeunis","rajeunit","rajeunissons","rajeunissez","rajeunissent",
    "blanchir","blanchis","blanchit","blanchissons","blanchissez","blanchissent",
    "noircir","noircis","noircit","noircissons","noircissez","noircissent",
    "raccourcir","raccourcis","raccourcit","raccourcissons","raccourcissez","raccourcissent",
    "durcir","durcis","durcit","durcissons","durcissez","durcissent",
    "amollir","amollis","amollit","amollissons","amollissez","amollissent",
    "applaudir","applaudis","applaudit","applaudissons","applaudissez","applaudissent",
    "réagir","réagis","réagit","réagissons","réagissez","réagissent",
    "agir","agis","agit","agissons","agissez","agissent",
    "bénir","bénis","bénit","bénissons","bénissez","bénissent",
    "finir","finis","finit","finissons","finissez","finissent",
    "pâlir","pâlis","pâlit","pâlissons","pâlissez","pâlissent",
    "verdir","verdis","verdit","verdissons","verdissez","verdissent",
    "jaunir","jaunis","jaunit","jaunissons","jaunissez","jaunissent",
    "blêmir","blêmis","blêmit","blêmissons","blêmissez","blêmissent",
    "languir","languis","languit","languissons","languissez","languissent",
    "réfléchir","réfléchis","réfléchit","réfléchissons","réfléchissez","réfléchissent",
    "maudire","maudis","maudit","maudissons","maudissez","maudissent",
    "vêtir","vêts","vêt","vêtons","vêtez","vêtent",
    "cueillir","cueille","cueilles","cueillons","cueillez","cueillent",
    "assaillir","assaillis","assaillit","assaillissons","assaillissez","assaillissent",
    "tenir","tiens","tient","tenons","tenez","tiennent",
    "venir","viens","vient","venons","venez","viennent",
    "revenir","reviens","revient","revenons","revenez","reviennent",
    "devenir","deviens","devient","devenons","devenez","deviennent",
    "maintenir","maintiens","maintient","maintenons","maintenez","maintiennent",
    "soutenir","soutiens","soutient","soutenons","soutenez","soutiennent",
    "retenir","retiens","retient"," retenons","retenez","retiennent",
    "appartenir","appartiens","appartient","appartenons","appartenez","appartiennent",
    "convenir","conviens","convient","convenons","convenez","conviennent",
    "intévenir","interviens","intervient","intervenons","intervenez","interviennent",
    "prévenir","préviens","prévient","prévenons","prévenez","préviennent",
    "obtenir","obtiens","obtient","obtenons","obtenez","obtiennent",
    "recevoir","reçois","reçoit","recevons","recevez","reçoivent",
    "concevoir","conçois","conçoit","concevons","concevez","conçoivent",
    "apercevoir","aperçois","aperçoit","apercevons","apercevez","aperçoivent",
    "apercevoir","aperçois","aperçoit","apercevons","apercevez","aperçoivent",
    "devoir","dois","doit","devons","devez","doivent",
    "mouvoir","meus","meut","mouvons","mouvez","meuvent",
    "émouvoir","émeus","émeut","émouvons","émouvez","émeuvent",
    "promouvoir","promus","promut","promouvons","promouvez","promeuvent",
    "falloir","faut","faudra","faudrait",
    "chaloir","chaut",
    "échoir","échoit","échoyons","échoyez","échoient",
    "déchoir","déchoit",
    "pouvoir","peux","peut","pouvons","pouvez","peuvent",
    "savoir","sais","sait","savons","savez","savent",
    "boire","bois","boit","buvons","buvez","boivent",
    "croire","crois","croit","croyons","croyez","croient",
    "voir","vois","voit","voyons","voyez","voient",
    "mouvoir","meus","meut","mouvons","mouvez","meuvent",
    "résister","résiste","résistes","résistons","résistez","résistent",
}

# ─── SUFFIXES DE CONJUGAISON ─────────────────────────────────────────────────
_CONJUG_SUFF = {
    "er":("e","es","e","ons","ez","ent","ais","ait","aient","ions","iez","ai","as","a","âmes","âtes","èrent","é","ée","és","ées","ant","ait"),
    "ir":("is","is","it","issons","issez","issent","issais","issait","issaient","issions","issiez","îmes","îtes","irent","issant"),
    "re":("s","s","t","ons","ez","ent","ais","ait","aient","ions","iez","us","ut","ûmes","ûtes","urent","ant"),
    "oir":("x","x","t","ons","ez","ent","ais","ait","aient","ions","iez"),
}

def _is_verb_form(w):
    w = w.lower()
    if w in _VERBS: return True
    for grp, suffs in _CONJUG_SUFF.items():
        for s in sorted(suffs, key=len, reverse=True):
            if w.endswith(s):
                root = w[:-len(s)]
                if len(root) >= 3:
                    candidate = root + grp
                    if candidate in _VERBS:
                        return True
    if re.search(r"(er|ir|re|oir|ire|aindre|endre|ondre|erdre|ertir|venir|tenir|iss|ifier|iser|ailler|iller|anner|asser|atter|ayer|uyer|eler|eter|iner|oner|urer|irer|cher|quer)$", w) and len(w) > 4:
        if w.endswith(("tion","ment","ité","eur","euse","rice","ique","isme","té","ence","ance","esse","oire","age")):
            return False
        return True
    return False

# ─── RESTE DU LEXIQUE ─────────────────────────────────────────────────────────
_DET = {"le","la","les","un","une","des","du","de","l","mon","ma","mes","ton","ta","tes","son","sa","ses","notre","nos","votre","vos","leur","leurs","ce","cet","cette","ces","quel","quelle","quels","quelles"}
_PREP = {"à","de","dans","pour","par","sur","avec","sans","sous","vers","chez","comme","entre","contre","devant","derrière","durant","après","avant","depuis","pendant","selon","dès","près","outre","parmi","malgré","concernant","suivant","grâce","faute","face","loin","au","aux","du","d'","l'"}
_CONJ_C = {"et","ou","ni","mais","or","donc","car"}
_CONJ_S = {"que","qu","quand","lorsque","puisque","comme","si","parce","parce que","afin que","bien que","quoique","pour que","de peur que","avant que","après que","tandis que","alors que","même si","tant que","dès que"}
_OPP = {"mais","cependant","pourtant","néanmoins","toutefois","au contraire","en revanche","malgré","bien que","quoique","alors que","tandis que","au lieu de","plutôt que","par contre","contrairement"}
_CAUS = {"car","parce","puisque","donc","ainsi","c'est pourquoi","en effet","de ce fait","par conséquent","d'où","grâce à","à cause de","suite à","en conséquence","par suite"}
_CONC = {"certes","il est vrai","admettons","sans doute"}
_THESIS = {"premièrement","tout d'abord","or","ainsi","j'affirme","je soutiens","en conclusion","finalement","bref","en somme","pour conclure","d'où"}
_POS_EMO = {"aimer","joie","bonheur","beau","bien","espoir","amour","confiance","liberté","lumière","vrai","juste","merci","douceur","tendresse","paix","sérénité","harmonie","réconfort","chaleur","enthousiasme","passion","curiosité","plaisir","sourire","rire","espérer","réussir","satisfait","heureux","ravi","merveilleux","extraordinaire","brillant","belle","bonne","doux","douce","généreux","noble","pur","clair"}
_NEG_EMO = {"mort","peur","haine","souffrance","mal","mauvais","impossible","terrible","horrible","injuste","violence","détresse","douleur","crainte","anxiété","tristesse","colère","refus","échec","erreur","abandon","deuil","frustration","agression","menace","catastrophe","désastre","chaos","vide","néant","angoisse","désespoir","culpabilité","honte","jalousie","envie","laid","sombre","froid","dur","cruel"}
_INTENS = {"très","extrêmement","totalement","absolument","complètement","profondément","vraiment","intensément","follement","terriblement","incroyablement","tellement","tant","si","trop","beaucoup","énormément","radicalement","parfaitement","strictement","pas du tout","nullement","aucunement"}
_NEGAT = {"pas","ne","non","jamais","rien","aucun","aucune","nul","nulle","sans","ni","pas du tout","nullement","aucunement","guère","plus","point"}
_PHILOS = {"bergson","kant","hegel","descartes","nietzsche","platon","aristote","spinoza","sartre","heidegger","wittgenstein","foucault","deleuze","derrida","leibniz","locke","hume","rousseau","voltaire","pascal","montaigne","merleau-ponty","épictète","marc aurèle","sénèque","marx","freud","jung","épicure"}
_GENERIC = {"trace","présence","continuité","doute","question","appui","lien","mouvement","rythme","mémoire","résonance","curiosité","friction","stabilité","page","fragment","pdf","livre","chose","fait","idée","notion","concept","sens","mot","terme","motif","aspect","façon","manière","forme","type","sorte","genre","exemple","cas","moment","temps","partie","côté","fond","raison","cause","effet","résultat","problème","solution","thème","sujet","texte","passage","contexte","base","point","part","fin","début","milieu","suite","ensemble"}

_CHALL = {"non","faux","tort","erreur","je ne suis pas","pas d'accord","contredis","conteste","mais tu","pourtant","cependant","en réalité","au contraire","je m'oppose","je refuse","inexact","incorrect","mensonge","trompe","tu te trompes","c'est faux","n'importe quoi","ridicule","absurde","tu mens","tu dis n'importe quoi"}
_CONF = {"sûr","certain","certaine","clairement","évidemment","bien sûr","absolument","forcément","indéniablement","manifestement","incontestable","assurément","définitivement"}
_DOUBT = {"peut-être","je ne sais","j'hésite","vraiment","doute","incertain","je doute","bizarre","étrange","hésiter","incertitude","hypothèse","supposer","probable","possible"}
_PERS = {"je ressens","j'éprouve","j'ai peur","je souffre","j'aime","je hais","ça me touche","je me sens","je vis","j'ai vécu","ma vie","mon expérience","moi je","pour moi","je pense que","je crois que","j'imagine","je sens que"}

# ─── UTILS ─────────────────────────────────────────────────────────────────
def _clamp(v, lo=0.0, hi=1.0):
    try:
        f=float(v)
        if math.isnan(f) or math.isinf(f): return lo
        return max(lo,min(hi,f))
    except: return lo

def _norm(t): return re.sub(r"\s+"," ",str(t or "").strip().lower())

# ─── TOKENIZER ─────────────────────────────────────────────────────────────
class Tok:
    __slots__ = ("surf","norm","pos","idx","is_stop","is_punct","chunk_id","dep","lem")
    def __init__(self,surf,idx):
        self.surf=surf; self.idx=idx; self.norm=surf.lower().strip("'\"")
        self.pos="X"; self.is_stop=False; self.is_punct=False
        self.chunk_id=-1; self.dep=""; self.lem=self.norm
    def __repr__(s): return f"Tok({s.surf}/{s.pos})"

def _tag(t):
    w=t.norm
    if w in _PRON_SUBJ|_PRON_OBJ|_PRON_DEM|_PRON_REL|_PRON_INT or w in _CONTRACTIONS: t.pos="PRON"; return
    if w in _DET: t.pos="DET"; return
    if w in _PREP: t.pos="ADP"; return
    if w in _CONJ_C|_CONJ_S: t.pos="CONJ"; return
    if w in _AUX_BE|_AUX_HAVE|_AUX_MODAL: t.pos="AUX"; return
    if w in _VERBS or _is_verb_form(w): t.pos="VERB"; return
    if w.endswith("ment") and len(w)>5: t.pos="ADV"; return
    if w.endswith(("if","ive","able","ible","ant","ent","ais","ois","ain","eur","eux","ieux","âtre")) and len(w)>4: t.pos="ADJ"; return
    if re.search(r"(tion|ment|age|ure|eur|iste|isme|té|ité|esse|ance|ence|ée|oire|eur)$",w) and len(w)>4: t.pos="NOUN"; return
    if len(w)>2: t.pos="NOUN"
    else: t.pos="X"

def _tok(text):
    text=re.sub(r"([.!?…,;:\(\)\[\]\"«»—–\-])",r" \1 ",text)
    text=re.sub(r"\b([ldnjmtsceçLNDNJMTSCEÇqu])'",r"\1' ",text)
    text=re.sub(r"\b(puisqu|lorsqu|quoiqu|jusqu|aujourd)'",r"\1' ",text)
    text=re.sub(r"\b(n)['’]([aeiouyéèêëàâôûù])",r"\1' \2",text)
    text=re.sub(r"\s+"," ",text)
    raw=text.strip().split()
    tokens=[]
    for i,s in enumerate(raw):
        t=Tok(s,i)
        if s in {'.',',',';','!',':','?','…','—','–','-','(',')','[',']','"','«','»'}: t.pos="PUNCT";t.is_punct=True
        elif re.match(r"^\d+([.,]\d+)?$",s): t.pos="NUM"
        else: _tag(t)
        tokens.append(t)
    return tokens

# ─── LEMMATISATION ───────────────────────────────────────────────────────────
def _lem_v(w):
    w=w.lower()
    if w in _VERBS: return w
    for grp,suffs in _CONJUG_SUFF.items():
        for s in sorted(suffs,key=len,reverse=True):
            if w.endswith(s):
                root=w[:-len(s)]
                if len(root)>=3:
                    cand=root+grp
                    if cand in _VERBS: return cand
    return w

def _lem_n(w):
    w=w.lower()
    # V2.3 : noms courts protégés
    if len(w)<=5: return w
    for s,r in [("tions","tion"),("ments","ment"),("ités","ité"),("eurs","eur"),("euses","euse"),("rices","rice"),("iques","ique"),("elles","elle"),("eaux","eau"),("aux","al"),("s","")]:
        if w.endswith(s) and len(w)>len(s)+2: return w[:-len(s)]+r
    return w

def _sent_split(text):
    text=re.sub(r"\b(M|Mme|Dr|Prof|etc|vol|p|pp|art|fig|cf|vs| M)\.",r"\1§",text)
    s=re.split(r"(?<=[.!?…])\s+(?=[A-ZÀÂÉÈÊËÎÏÔÙÛÜÇ])",text)
    return [x.replace("§",".").strip() for x in s if x.strip()]

# ─── CHUNKER ─────────────────────────────────────────────────────────────────
class Chunk:
    __slots__ = ("label","toks","head","idx","deps")
    def __init__(self,label,toks,idx): self.label=label;self.toks=toks;self.head=None;self.idx=idx;self.deps=[]
    def text(self): return " ".join(t.surf for t in self.toks)
    def __repr__(s): return f"Chunk({s.label}:{s.text()[:40]})"

def _chunk(tokens):
    chunks,i,n,ci=[],0,len(tokens),0
    while i<n:
        t=tokens[i]
        if t.is_punct: i+=1; continue
        # GN
        if t.pos in ("DET","PRON","NUM","ADJ","NOUN"):
            if t.pos=="PRON" and i+1<n and tokens[i+1].pos in ("VERB","AUX"):
                i+=1; continue
            st=i
            while i<n and tokens[i].pos in ("DET","PRON","NUM","ADJ","NOUN") and not tokens[i].is_punct: i+=1
            sub=tokens[st:i]
            hd=next((tt for tt in reversed(sub) if tt.pos=="NOUN"),None) or next((tt for tt in reversed(sub) if tt.pos in ("ADJ","PRON")),None) or sub[-1]
            hd.chunk_id=ci
            for tt in sub: tt.chunk_id=ci
            c=Chunk("GN",sub,ci);c.head=hd;chunks.append(c);ci+=1;continue
        # GV (absorbe clitiques PRON précédents par recul)
        if t.pos in ("VERB","AUX"):
            st=i
            while st>0 and tokens[st-1].pos=="PRON" and tokens[st-1].norm in _PRON_OBJ|_PRON_SUBJ|_CONTRACTIONS:
                st-=1
            while i<n and (tokens[i].pos in ("VERB","AUX","ADV","PRON") or (tokens[i].is_punct and tokens[i].surf in {"'","'"})) and not (tokens[i].is_punct and tokens[i].surf not in {"'","'"}):
                if tokens[i].pos=="PUNCT" and tokens[i].surf in {'.',',',';',':','!','?'}: break
                i+=1
            sub=tokens[st:i]
            hd=next((tt for tt in reversed(sub) if tt.pos=="VERB"),None) or next((tt for tt in reversed(sub) if tt.pos=="AUX"),None) or sub[-1]
            hd.chunk_id=ci
            for tt in sub: tt.chunk_id=ci
            c=Chunk("GV",sub,ci);c.head=hd;chunks.append(c);ci+=1;continue
        # GP
        if t.pos=="ADP" and t.norm in _PREP:
            st=i; i+=1
            while i<n and not tokens[i].is_punct and tokens[i].pos in ("DET","ADJ","NOUN","PRON","NUM","ADP"): i+=1
            if i>st+1:
                sub=tokens[st:i]; hd=sub[0]; hd.chunk_id=ci
                for tt in sub: tt.chunk_id=ci
                c=Chunk("GP",sub,ci);c.head=hd;chunks.append(c);ci+=1; continue
            else: i=st+1
        # seul
        t.chunk_id=ci; c=Chunk(t.pos,[t],ci);c.head=t;chunks.append(c);ci+=1;i+=1
    return chunks

# ─── DÉPENDANCES ─────────────────────────────────────────────────────────────
def _dep(chunks,tokens):
    gvs=[c for c in chunks if c.label=="GV"]
    gns=[c for c in chunks if c.label=="GN"]
    gps=[c for c in chunks if c.label=="GP"]
    for gv in gvs:
        vi=gv.head.idx if gv.head else -1
        sc=[gn for gn in gns if gn.head and gn.head.idx<vi and not (gn.head.pos=="PRON" and gn.head.norm in _PRON_OBJ and len(gn.toks)==1)]
        if sc:
            subj=min(sc,key=lambda gn:gn.head.idx)
            gv.deps.append(("nsubj",subj)); subj.deps.append(("head_verb",gv))
        oc=[gn for gn in gns if gn.head and gn.head.idx>vi and not any(gp.head and gp.head.idx<gn.head.idx and gp.head.idx>vi for gp in gps)]
        oc=[gn for gn in oc if not (gn.head.pos=="PRON" and gn.head.norm in _PRON_OBJ and len(gn.toks)==1)]
        if oc:
            obj=min(oc,key=lambda gn:gn.head.idx)
            gv.deps.append(("obj",obj))
        pc=[gp for gp in gps if gp.head and gp.head.idx>vi]
        if pc:
            p=min(pc,key=lambda gp:gp.head.idx)
            gv.deps.append(("obl",p))
        if gv.head and gv.head.norm in _COPULA:
            ac=[gn for gn in gns if gn.head and gn.head.idx>vi and not any(d[0]=="obj" and d[1]==gn for d in gv.deps)]
            if ac:
                attr=min(ac,key=lambda gn:gn.head.idx)
                gv.deps.append(("attr",attr))

# ─── ANAPHORES / DISCOURS ────────────────────────────────────────────────────
class DiscCtx:
    def __init__(self):
        self.recent_subj=deque(maxlen=5);self.recent_obj=deque(maxlen=5);self.recent_v=deque(maxlen=5);self.last_clause="";self.exchanges=0
    def update(self,tokens,chunks):
        self.exchanges+=1
        for c in chunks:
            if c.label=="GN" and c.head and c.head.pos in ("NOUN","PRON") and c.head.norm not in _PRON_OBJ:
                self.recent_subj.append(c.text())
            for rel,target in c.deps:
                if rel=="obj" and isinstance(target,Chunk) and target.label=="GN":
                    self.recent_obj.append(target.text())
            if c.label=="GV" and c.head: self.recent_v.append(c.head.norm)
        clause=" ".join(t.surf for t in tokens if not t.is_punct)
        if len(clause)>5: self.last_clause=clause[:200]

def _resolve_ana(tokens,ctx):
    if not ctx: return tokens
    for t in tokens:
        if t.pos!="PRON": continue
        if t.norm in {"il","elle","ils","elles","on"}:
            t.lem=f"[ref:{ctx.recent_subj[-1]}]" if ctx.recent_subj else "[ref:??]"
        elif t.norm in {"le","la","les","l'","l","lui","leur"}:
            t.lem=f"[ref:{ctx.recent_obj[-1]}]" if ctx.recent_obj else "[ref:??]"
        elif t.norm in _PRON_DEM or t.norm in {"ça","ca","cela","ceci"}:
            t.lem=f"[ref:ça→{ctx.last_clause[:60]}]"
    return tokens

def _resolve_ellip(utterance,chunks,ctx):
    if not ctx: return utterance
    has_v=any(c.label=="GV" for c in chunks)
    has_content=any(t.pos in ("NOUN","ADJ","ADV","PRON") and t.norm not in _STOP for t in _tok(utterance))
    if not has_v and has_content and ctx.recent_v:
        return f"[ellipsis:{ctx.recent_v[-1]}?] {utterance}"
    return utterance

# ─── POLARITÉ ────────────────────────────────────────────────────────────────
def _polarity(tokens):
    pol,scope=0.0,set(); i,n=0,len(tokens)
    while i<n:
        t=tokens[i]
        if t.norm in _NEGAT:
            j,sp=i+1,0
            while j<n and sp<10 and not (tokens[j].is_punct and tokens[j].surf in {'.',',',';',':','!','?'}):
                scope.add(j); sp+=1; j+=1
            scope.add(i); pol-=0.4
        if t.norm in _INTENS:
            j=i+1
            while j<n and j<i+4:
                if tokens[j].pos in ("ADJ","VERB","NOUN","ADV"):
                    pol*=1.5 if pol!=0 else (1.5 if tokens[j].norm in _POS_EMO else -1.5)
                    break
                j+=1
        if t.norm in _POS_EMO and t.idx not in scope: pol+=0.3
        elif t.norm in _NEG_EMO and t.idx not in scope: pol-=0.3
        elif t.norm in _POS_EMO and t.idx in scope: pol-=0.3
        elif t.norm in _NEG_EMO and t.idx in scope: pol+=0.3
        i+=1
    return _clamp(pol,-1,1),scope

def _emo_deep(tokens,scope):
    pos=sum(1 for t in tokens if t.norm in _POS_EMO and t.idx not in scope)
    neg=sum(1 for t in tokens if t.norm in _NEG_EMO and t.idx not in scope)
    pn=sum(1 for t in tokens if t.norm in _POS_EMO and t.idx in scope)
    np=sum(1 for t in tokens if t.norm in _NEG_EMO and t.idx in scope)
    tot=pos+neg+pn+np
    if tot==0: return 0.0
    return _clamp((pos-neg-pn+np)/tot,-1,1)

# ─── DISCOURS ────────────────────────────────────────────────────────────────
def _discourse(sentences):
    res,prev=[],0.0
    for i,sent in enumerate(sentences):
        st=" ".join(t.surf for t in sent if not t.is_punct).lower()
        _,scope=_polarity(sent)
        p=_emo_deep(sent,scope)
        dtype="neutre"
        if any(w in st for w in _THESIS): dtype="thèse"
        elif any(w in st for w in _CONC): dtype="concession"
        elif any(w in st for w in _OPP): dtype="antithèse"
        elif any(w in st for w in _CAUS): dtype="cause"
        elif p>0.3: dtype="positif"
        elif p<-0.3: dtype="négatif"
        r=abs(p-prev)>0.6
        res.append({"index":i,"polarity":round(p,3),"discourse_type":dtype,"rupture":r,"has_negation":len(scope)>0,"text":st[:120]})
        prev=p
    return res

# ─── PROPOSITIONS ────────────────────────────────────────────────────────────
class DProp:
    __slots__=("subj","subj_mod","rel","rel_mod","obj","obj_mod","neg","conf","conn","src","dsubj","dobj")
    def __init__(self):
        self.subj="";self.subj_mod=[];self.rel="";self.rel_mod=[];self.obj="";self.obj_mod=[]
        self.neg=False;self.conf=0.7;self.conn="";self.src="";self.dsubj="";self.dobj=""
    def to_dict(self):
        return {"subject":self.subj,"relation":self.rel,"object":self.obj,"negated":self.neg,"confidence":round(self.conf,3),"connector_type":self.conn,"deep_subject":self.dsubj,"deep_object":self.dobj}
    def __repr__(s):
        return f"({s.dsubj or s.subj}, {'¬' if s.neg else ''}{s.rel}, {s.dobj or s.obj})"

def _resolve_chunk(chk,tokens):
    return " ".join(t.lem if t.pos=="PRON" and t.lem.startswith("[ref:") else t.surf for t in chk.toks)

def _extract_props(tokens,chunks,scope):
    props=[]
    for gv in [c for c in chunks if c.label=="GV"]:
        p=DProp()
        p.neg=any(t.idx in scope for t in gv.toks)
        p.rel=gv.head.norm if gv.head else ""
        p.rel_mod=[t.norm for t in gv.toks if t.pos in ("ADV","AUX") and t!=gv.head]
        for rel,target in gv.deps:
            if rel=="nsubj" and isinstance(target,Chunk):
                p.subj=target.text(); p.subj_mod=[t.norm for t in target.toks if t.pos=="ADJ"]; p.dsubj=_resolve_chunk(target,tokens)
            if rel=="obj" and isinstance(target,Chunk):
                p.obj=target.text(); p.obj_mod=[t.norm for t in target.toks if t.pos=="ADJ"]; p.dobj=_resolve_chunk(target,tokens)
            if rel=="attr" and isinstance(target,Chunk) and not p.obj:
                p.obj=target.text(); p.dobj=_resolve_chunk(target,tokens)
            if rel=="obl" and isinstance(target,Chunk):
                if not p.obj: p.obj=target.text(); p.dobj=_resolve_chunk(target,tokens)
                else: p.obj+=f" ; {target.text()}"
        p.conf=0.85 if (p.subj and p.obj) else 0.55
        if p.neg: p.conf*=0.9
        if tokens and gv.toks:
            fi=min(t.idx for t in gv.toks)
            lb=[t for t in tokens if 0<=fi-t.idx<=5 and t.pos in ("CONJ","ADP","ADV")]
            lbt=" ".join(t.norm for t in lb)
            if any(w in lbt for w in _OPP): p.conn="opposition"
            elif any(w in lbt for w in _CAUS): p.conn="causal"
            elif any(w in lbt for w in _CONC): p.conn="concession"
        p.src=" ".join(t.surf for t in tokens[max(0,gv.toks[0].idx-3):min(len(tokens),gv.toks[-1].idx+3)] if not t.is_punct)
        if p.subj or p.obj: props.append(p)
    return props

# ─── ENTITÉS ─────────────────────────────────────────────────────────────────
class DEnt:
    __slots__=("text","label","conf","ctx")
    def __init__(self,text,label,conf,ctx): self.text=text;self.label=label;self.conf=conf;self.ctx=ctx
    def to_dict(self): return {"text":self.text,"label":self.label,"confidence":round(self.conf,2),"context":self.ctx}

def _ctx_around(tokens,idx,w=20):
    return " ".join(t.surf for t in tokens[max(0,idx-2):min(len(tokens),idx+w)] if not t.is_punct)

def _extract_ent(tokens,chunks):
    ent,seen=[],[]
    for c in chunks:
        if c.label=="GN":
            raw=[t.surf for t in c.toks if t.pos=="NOUN" and t.surf and t.surf[0].isupper()]
            if raw:
                name=" ".join(raw)
                if len(name)>2 and name.lower() not in seen:
                    seen.append(name.lower()); ent.append(DEnt(name,"PROPER",0.7,_ctx_around(tokens,c.toks[0].idx,20)))
    at=" ".join(t.surf for t in tokens)
    al=at.lower()
    for ph in _PHILOS:
        if ph in al and ph not in seen:
            seen.append(ph)
            try: idx=next(t.idx for t in tokens if ph in t.norm)
            except: idx=0
            ent.append(DEnt(ph.title(),"PERSON",0.95,_ctx_around(tokens,idx,25)))
    for pat in [r'"([^"]{3,60})"',r'«([^»]{3,60})»']:
        for m in re.finditer(pat,at):
            t=m.group(1)
            if t.lower() not in seen:
                seen.append(t.lower()); ent.append(DEnt(t,"WORK",0.75,t))
    return ent

# ─── SORTIES ─────────────────────────────────────────────────────────────────
@dataclass
class UtteranceAnalysis:
    intent:str="";stance:str="";modality:str=""
    subject:str="";verb_root:str="";obj:str=""
    deep_subject:str="";deep_object:str=""
    is_question:bool=False;is_negative:bool=False;is_personal:bool=False
    is_elliptical:bool=False;resolved_surface:str="";deep_structure:str=""
    focus_concepts:List[str]=field(default_factory=list)
    named_entities:List[DEnt]=field(default_factory=list)
    propositions:List[DProp]=field(default_factory=list)
    content_words:List[str]=field(default_factory=list)
    word_count:int=0;emotional_charge:float=0.0;polarity_scope:List[int]=field(default_factory=list)
    urgency:float=0.0;complexity:float=0.0;parser_used:str="deep_heuristic_v2.3"
    raw:str=""
    def to_dict(self):
        return {"intent":self.intent,"stance":self.stance,"modality":self.modality,"subject":self.subject,"verb_root":self.verb_root,"object":self.obj,
                "deep_subject":self.deep_subject,"deep_object":self.deep_object,"is_question":self.is_question,"is_negative":self.is_negative,
                "is_personal":self.is_personal,"is_elliptical":self.is_elliptical,"resolved_surface":self.resolved_surface,
                "deep_structure":self.deep_structure,"focus_concepts":self.focus_concepts[:8],
                "named_entities":[e.to_dict() for e in self.named_entities],"propositions":[p.to_dict() for p in self.propositions],
                "content_words":self.content_words[:15],"word_count":self.word_count,"emotional_charge":round(self.emotional_charge,3),
                "polarity_scope":self.polarity_scope,"urgency":round(self.urgency,3),"complexity":round(self.complexity,3),"parser_used":self.parser_used}

@dataclass
class TextAnalysis:
    key_concepts:List[str]=field(default_factory=list)
    named_entities:List[DEnt]=field(default_factory=list)
    propositions:List[DProp]=field(default_factory=list)
    themes:List[str]=field(default_factory=list)
    theses:List[str]=field(default_factory=list)
    objections:List[str]=field(default_factory=list)
    conclusions:List[str]=field(default_factory=list)
    discourse_structure:List[Dict]=field(default_factory=list)
    chunks:List[str]=field(default_factory=list)
    sentence_count:int=0;word_count:int=0;lexical_density:float=0.0
    dominant_modality:str="";source:str="";parser_used:str="deep_heuristic_v2.3"
    processed_at:float=field(default_factory=time.time)
    def to_dict(self):
        return {"key_concepts":self.key_concepts[:20],"named_entities":[e.to_dict() for e in self.named_entities[:30]],
                "propositions":[p.to_dict() for p in self.propositions[:40]],"themes":self.themes[:10],
                "theses":self.theses[:5],"objections":self.objections[:5],"conclusions":self.conclusions[:5],
                "discourse_structure":self.discourse_structure[:10],"sentence_count":self.sentence_count,
                "word_count":self.word_count,"lexical_density":round(self.lexical_density,3),
                "dominant_modality":self.dominant_modality,"source":self.source,"parser_used":self.parser_used}

# ─── MOTEUR CENTRAL ───────────────────────────────────────────────────────────
class LeiaSpaCyEngine:
    def __init__(self):
        self.disc=DiscCtx()
        self._times=deque(maxlen=100);self._n_u=0;self._n_t=0

    def analyze_utterance(self,text,use_context=True):
        if not text or not text.strip():
            return UtteranceAnalysis(raw=text or "",parser_used="none")
        t0=time.monotonic()
        text=text.strip(); low=_norm(text)
        tokens=_tok(text)
        for t in tokens:
            _tag(t)
            if t.pos in ("VERB","AUX"): t.lem=_lem_v(t.norm)
            elif t.pos=="NOUN": t.lem=_lem_n(t.norm)
        chunks=_chunk(tokens)
        _dep(chunks,tokens)
        if use_context: _resolve_ana(tokens,self.disc)
        pol,scope=_polarity(tokens)
        emo=_emo_deep(tokens,scope)
        resolved=_resolve_ellip(text,chunks,self.disc if use_context else None)
        props=_extract_props(tokens,chunks,scope)
        ents=_extract_ent(tokens,chunks)
        intent,stance,modality=self._cls_intent(low,tokens,chunks,props,scope)
        focus=self._focus(tokens,chunks)
        subj,verb,obj=self._svo_surf(chunks)
        deep=self._deep_str(props)
        words=[t for t in tokens if not t.is_punct]
        complexity=_clamp(len(set(t.lem for t in words if t.pos in ("NOUN","VERB","ADJ")))/max(len(words),1))
        urgency=_clamp((("!" in text)*0.3)+sum(0.15 for w in ["urgent","aide","vite","maintenant","problème","crise"] if w in low)+(len([t for t in tokens if t.norm in _INTENS])*0.1))
        if use_context: self.disc.update(tokens,chunks)
        self._times.append(time.monotonic()-t0);self._n_u+=1
        return UtteranceAnalysis(
            intent=intent,stance=stance,modality=modality,subject=subj,verb_root=verb,obj=obj,
            deep_subject=next((p.dsubj for p in props if p.dsubj),subj),
            deep_object=next((p.dobj for p in props if p.dobj),obj),
            is_question=("?" in text or intent.startswith("question")),
            is_negative=len(scope)>0,is_personal=bool(re.search(r"\b(je|mon|ma|mes|moi|j'|nous|notre)\b",low)),
            is_elliptical="[ellipsis:" in resolved,resolved_surface=resolved,deep_structure=deep,
            focus_concepts=focus[:10],named_entities=ents,propositions=props,
            content_words=[t.lem for t in words if t.pos in ("NOUN","VERB","ADJ") and t.norm not in _STOP][:20],
            word_count=len(words),emotional_charge=emo,polarity_scope=sorted(scope),urgency=urgency,
            complexity=complexity,raw=text)

    def analyze_text(self,text,source="",max_chars=100_000):
        if not text or not text.strip():
            return TextAnalysis(source=source,parser_used="none")
        text=text[:max_chars];t0=time.monotonic()
        sents=_sent_split(text)
        all_p,all_e=[],[]; cf=Counter(); theses,objec,conc=[],[],[]; tok_sents=[]
        for st in sents:
            if len(st.strip())<5: continue
            tokens=_tok(st)
            for t in tokens:
                _tag(t)
                if t.pos in ("VERB","AUX"): t.lem=_lem_v(t.norm)
                elif t.pos=="NOUN": t.lem=_lem_n(t.norm)
            tok_sents.append(tokens)
        disc=_discourse(tok_sents)
        for i,sent_tokens in enumerate(tok_sents):
            chunks=_chunk(sent_tokens); _dep(chunks,sent_tokens)
            _,scope=_polarity(sent_tokens)
            props=_extract_props(sent_tokens,chunks,scope)
            all_p.extend(props); all_e.extend(_extract_ent(sent_tokens,chunks))
            content=[t.lem for t in sent_tokens if t.pos in ("NOUN","VERB","ADJ") and t.norm not in _STOP and len(t.norm)>3]
            cf.update(content)
            s_txt=" ".join(t.surf for t in sent_tokens if not t.is_punct)
            sl=s_txt.lower()
            if any(w in sl for w in _THESIS) and len(s_txt)>20: theses.append(s_txt[:120])
            elif any(w in sl for w in _CONC): objec.append(s_txt[:120])
            elif any(w in sl for w in _OPP): objec.append(s_txt[:120])
            elif any(w in sl for w in {"en conclusion","finalement","bref","d'où"}): conc.append(s_txt[:120])
        kc=[w for w,_ in cf.most_common(40) if len(w)>3 and w not in _STOP and w not in _GENERIC]
        all_w=[t for sent in tok_sents for t in sent if not t.is_punct]
        tw=len(all_w)
        ld=len([t for t in all_w if t.norm not in _STOP])/max(tw,1)
        self._times.append(time.monotonic()-t0);self._n_t+=1
        return TextAnalysis(
            key_concepts=kc[:25],named_entities=self._dedup_e(all_e)[:30],propositions=all_p[:60],
            themes=kc[:10],theses=theses[:5],objections=objec[:5],conclusions=conc[:5],
            discourse_structure=disc[:15],chunks=[" ".join(t.surf for t in s if not t.is_punct)[:200] for s in tok_sents][:10],
            sentence_count=len(tok_sents),word_count=tw,lexical_density=ld,
            dominant_modality=self._mod_glob(text),source=source)

    def _cls_intent(self,low,tokens,chunks,props,scope):
        has_q="?" in " ".join(t.surf for t in tokens)
        if any(m in low for m in _CHALL): return "challenge","scepticisme","assertion"
        if has_q or low.startswith(("est-ce","quel","comment","pourquoi","où","qui","que","quoi","qu'est-ce")):
            if any(w in low for w in {"pourquoi","comment","qu'est-ce","qu est ce","a quoi bon"}): return "question_philosophique","doute","hypothèse"
            if any(w in low for w in {"n'est-ce pas","pas vrai","tu vois"}): return "question_rhétorique","certitude","assertion"
            return "question","neutre","assertion"
        mc=Counter()
        for t in tokens:
            if t.norm in _AUX_MODAL:
                if t.norm in {"peut","pourrait","possible"}: mc["possibilité"]+=1
                elif t.norm in {"doit","faut","nécessaire"}: mc["nécessité"]+=1
                elif t.norm in {"devrait","fallait","faudrait"}: mc["obligation_morale"]+=1
        if mc: return "affirmation_modale","certitude",mc.most_common(1)[0][0]
        if any(t.norm in {"je","mon","ma","mes","moi","j'"} for t in tokens):
            em=sum(1 for t in tokens if t.norm in _POS_EMO)-sum(1 for t in tokens if t.norm in _NEG_EMO)
            if em>0: return "confidence_personnelle","certitude","assertion"
            elif em<0: return "confidence_personnelle","doute","assertion"
            else: return "confidence_personnelle","neutre","assertion"
        if any(m in low for m in _DOUBT): return "expression_doute","doute","hypothèse"
        return "affirmation","neutre","assertion"

    def _focus(self,tokens,chunks):
        sc=defaultdict(float)
        for c in chunks:
            if c.label=="GN" and c.head:
                w=c.head.lem
                if w not in _STOP and w not in _GENERIC and len(w)>3: sc[w]+=2.0
                for t in c.toks:
                    if t.pos=="ADJ" and t.norm not in _STOP and len(t.norm)>3: sc[t.lem]+=1.0
            if c.label=="GV" and c.head and c.head.pos=="VERB" and len(c.head.norm)>3:
                sc[c.head.lem]+=1.5
            if c.label=="GN":
                for t in c.toks:
                    if t.surf and t.surf[0].isupper() and len(t.surf)>3:
                        sc[t.surf.lower()]+=2.5
        return [w for w,_ in sorted(sc.items(),key=lambda x:-x[1])[:12]]

    def _svo_surf(self,chunks):
        subj,verb,obj="","",""
        for c in chunks:
            if c.label=="GV" and c.head:
                verb=c.head.norm
                for rel,target in c.deps:
                    if rel=="nsubj" and isinstance(target,Chunk) and not subj: subj=target.text()
                    if rel=="obj" and isinstance(target,Chunk): obj=target.text()
                    if rel=="attr" and isinstance(target,Chunk) and not obj: obj=target.text()
        return subj,verb,obj

    def _deep_str(self,props):
        if not props: return ""
        return " ; ".join(f"({p.dsubj or p.subj} — {'¬' if p.neg else ''}{p.rel} — {p.dobj or p.obj})" for p in props[:3])

    def _mod_glob(self,text):
        low=_norm(text)
        scores=Counter()
        for mod,markers in {"assertion":{"est","sont","c'est","il y a","réalité","effectivement"},"hypothèse":{"si","peut-être","probablement","éventuellement","supposons"},"nécessité":{"doit","faut","obligatoire","nécessaire","indispensable"},"possibilité":{"peut","pourrait","serait","faisable"},"négation":{"ne","pas","non","jamais","rien","aucun"}}.items():
            for m in markers:
                if m in low: scores[mod]+=1
        return scores.most_common(1)[0][0] if scores else "assertion"

    def _dedup_e(self,ents):
        seen,res=set(),[]
        for e in ents:
            k=e.text.lower()
            if k not in seen: seen.add(k); res.append(e)
        return res

    def semantic_similarity(self,a,b):
        sa=set(t.norm for t in _tok(a) if t.norm not in _STOP)
        sb=set(t.norm for t in _tok(b) if t.norm not in _STOP)
        if not sa or not sb: return 0.0
        return len(sa&sb)/len(sa|sb)

    def segment_text(self,text,max_chars=1500):
        sents=_sent_split(text); out,cur=[],""
        for s in sents:
            if len(cur)+len(s)+1>max_chars and cur: out.append(cur.strip()); cur=s
            else: cur=(cur+" "+s).strip()
        if cur: out.append(cur.strip())
        return out

    def detect_meta_leak(self,text):
        internal={"pressure","payload","context","metadata","snapshot","field","label","token","score","weight","valence","engine","weaver","available","json","python","mapping","dict","source","pipeline","module","neurone","continuité","résonance","trace","axe","signal","consolidation","réactivation","_clamp","_normalize","_tokenize","heuristic","utteranceanalysis","textanalysis","deepproposition","chunk","discoursecontext"}
        low=text.lower()
        if "_" in text and any(w in low for w in {"self","dict","tuple","list"}): return True
        if re.search(r"[{}\\<>]",text): return True
        return any(w in low for w in internal)

    def stats(self):
        avg=(sum(self._times)/len(self._times)) if self._times else 0.0
        return {"engine":"LeiaSpaCyEngine_v2.3","dependencies":"none","total_utterances":self._n_u,"total_texts":self._n_t,"avg_parse_ms":round(avg*1000,2),"discourse_memory":self.disc.exchanges}

engine=LeiaSpaCyEngine()

# ─── DIAGNOSTIC ─────────────────────────────────────────────────────────────
if __name__=="__main__":
    print("="*70+"\n  LEIA NLP Engine V2.3 — Diagnostic (Deep Heuristic / Pure Python)\n"+"="*70)
    print("\n  Mode : pur Python, zéro dépendance.\n")
    tests=[
        "Est-ce que la liberté peut vraiment exister sans contrainte ?",
        "Je ne suis pas d'accord — la mémoire n'est pas un tiroir.",
        "Bergson affirme que la durée est irréductible à l'espace.",
        "J'ai peur que l'intelligence artificielle efface l'essentiel.",
        "Tu te trompes complètement sur ce point fondamental.",
        "Et la liberté, tu en penses quoi ?",
        "Ça me résiste, cette idée.",
    ]
    print("-"*70+"\n  TEST DIALOGUE\n"+"-"*70)
    # V2.3 : reset contexte entre tests
    engine.disc=DiscCtx()
    for utt in tests:
        ua=engine.analyze_utterance(utt)
        print(f"\n  > {utt[:65]}")
        print(f"    intent        : {ua.intent}  |  stance : {ua.stance}  |  modality : {ua.modality}")
        print(f"    SVO surface   : ({ua.subject}, {ua.verb_root}, {ua.obj})")
        print(f"    SVO profond   : ({ua.deep_subject}, {ua.verb_root}, {ua.deep_object})")
        print(f"    structure     : {ua.deep_structure[:90]}")
        if ua.propositions:
            for p in ua.propositions[:2]: print(f"      → {p}")
        print(f"    focus         : {ua.focus_concepts[:5]}")
        print(f"    émotion       : {ua.emotional_charge:+.2f}  |  négation : {ua.is_negative}  |  ellipse : {ua.is_elliptical}")
        print(f"    résolution    : {ua.resolved_surface[:75]}")
    print("\n"+"-"*70+"\n  TEST LECTURE (Bergson)\n"+"-"*70)
    sample=("La mémoire, selon Bergson, n'est pas un tiroir où l'on range des souvenirs. "
            "Elle est une durée vécue, une continuité vivante qui déborde la perception. "
            "Mais certains philosophes, comme Locke, considèrent au contraire que la mémoire "
            "est fondée sur des impressions passées, des traces fixes. "
            "Cette opposition révèle deux conceptions du temps : le temps mesuré et le temps vécu. "
            "On peut donc affirmer que la question de la mémoire engage nécessairement "
            "une philosophie du temps et de la conscience.")
    ta=engine.analyze_text(sample,source="Bergson test")
    print(f"\n  Phrases      : {ta.sentence_count}")
    print(f"  Concepts     : {ta.key_concepts[:8]}")
    print(f"  Entités      : {[e.text for e in ta.named_entities[:5]]}")
    print(f"  Propositions : {len(ta.propositions)}")
    for p in ta.propositions[:3]: print(f"    {p}")
    print(f"  Thèmes       : {ta.themes[:4]}")
    print(f"  Discours     : {ta.discourse_structure[:3]}")
    print(f"  Densité lex. : {ta.lexical_density:.3f}")
    print("\n"+"-"*70+"\n  TEST SIMILARITÉ\n"+"-"*70)
    for a,b in [("La liberté est une valeur essentielle.","La liberté suppose un choix réel."),
                ("La mémoire est une durée vécue.","L'oubli est une forme de liberté."),
                ("Le chat dort sur le canapé.","La philosophie du temps chez Bergson.")]:
        print(f"  sim={engine.semantic_similarity(a,b):.3f}  |  '{a[:40]}' ↔ '{b[:40]}'")
    print("\n"+"="*70)
    print(f"  Stats : {engine.stats()}")
    print("="*70)