same="VICTINI MUNNA ZORUA ZOROARK EMOLGA RESHIRAM ZEKROM KYUREM KELDEO MELOETTA GENESECT FLOETTE FLORGES DEDENNE XERNEAS YVELTAL ZYGARDE DIANCIE HOOPA VOLCANION CRABOMINABLE TOGEDEMARU COSMOG SOLGALEO LUNALA NECROZMA MAGEARNA MARSHADOW ZERAORA MELTAN MELMETAL MORPEKO ZACIAN ZAMAZENTA ZARUDE REGIELEKI REGIDRAGO ARBOLIVA KORAIDON MIRAIDON POLTCHAGEIST OGERPON TERAPAGOS FARIGIRAF MEW".split()
import json
o=json.load(open('/tmp/a_trad.json'))
T={}
for i,x in enumerate(o):
    if x['id'] in same: T[i]=x['id']
    if x['id']=='FLABéBé': T[i]='FLABÉBÉ'
forms={'RATICATE':'RATTATAC','RAICHU':'RAICHU','SANDSLASH':'SABLAIREAU','NINETALES':'FEUNARD','MEOWTH':'MIAOUSS','PERSIAN':'PERSIAN','ARCANINE':'ARCANIN','GOLEM':'GROLEM','RAPIDASH':'GALOPA','SLOWPOKE':'RAMOLOSS','SLOWBRO':'FLAGADOSS','SLOWKING':'ROIGADA',"FARFETCH'D":'CANARTICHO','MUK':'GROTADMORV','VOLTORB':'VOLTORBE','ELECTRODE':'ÉLECTRODE','MAROWAK':'OSSATUEUR','WEEZING':'SMOGOGO','MR. MIME':'M. MIME','TAUROS':'TAUROS','WOOPER':'AXOLOTO','QWILFISH':'QWILFISH','SNEASEL':'FARFURET','CORSOLA':'CORAYON','ZIGZAGOON':'ZIGZATON','ZORUA':'ZORUA','ZOROARK':'ZOROARK'}
import re
for i,x in enumerate(o):
    m=re.fullmatch(r"(.+)-([A-Z])",x['id'])
    if m and m.group(1) in forms: T[i]=forms[m.group(1)]+'-'+m.group(2)
cat={'Unique Horn':'Unicorne','Royal':'Royal','Hexpert':'Sorcier','Bivalve':'Bivalve','Sphere':'Sphère','Strong Legs':'Grand-Pied','Malevolent':'Malveillant','Ghost Flame':'Flamme Spectre','Poison Fish':'Poison-Poisson','Big Boss':'Grand Patron','Patient':'Patient','Jet':'Jet','Bouquet':'Bouquet','Cactus':'Cactus','Fruit':'Fruit','Face':'Visage','Iceberg':'Iceberg','Continent':'Continent','Hippo':'Hippo','Gratitude':'Gratitude','Judo':'Judo','Spinning':'Tournoyant','Spiteful Fox':'Renard Hargneux','Baneful Fox':'Renard Néfaste','Chinchilla':'Chinchilla','Battle Cry':'Cri de Guerre','Shell Bunker':'Bunker','Parasite':'Parasite','Punk':'Punk','Jujitsu':'Jujitsu','Couple':'Couple','Matcha':'Matcha'}
for i,x in enumerate(o):
    if x['id'] in cat and 'species_info' in x['src']: T[i]=cat[x['id']]
M={
721:"SAUTILLEMENTS",722:"SÉPIA",
723:"Pokémon Talk du Prof. Chen",724:"Émission Pokédex",725:"Chantons tous!",726:"Son de Hoenn",
727:"Une mélodie Pokémon d’une",728:"lointaine région: HOENN!",729:"pourrait apparaître!",730:"ÉMISSION POKéDEX DE CHEN!",
731:"CHEN: Le Pokémon du jour: ",732:"CHEN: ",733:"se trouve vers",734:"BEN: CHAÎNE MUSIQUE POKéMON!",
735:"Aujourd’hui ",736:"alors swinguons sur",737:"alors détendez-vous sur",738:"la Marche Pokémon!",739:"la Berceuse Pokémon!",
740:"ROSIN: Youhou! Comment ça va",741:"tout le monde? Que vous soyez",742:"LOTO-NUMÉRO!",743:"Le numéro de la semaine est",
744:"Je répète!",745:"S’il correspond, allez à",746:"la Tour Radio!",747:"…Me répéter, ça",748:"devient lassant…",
749:"présenté par moi, DJ LILY!",750:"… …Hum, nous sommes",751:"Après trois années",752:"de préparation, nous",
753:"renaissons de nos cendres!",754:"GIOVANNI!",755:"Vous m’entendez?",756:"BUENA: Ici BUENA!",
757:"Le mot de passe du jour!",758:"Voyons voir… C’est",
759:"M. NIDO",760:"une capacité",761:"une capacité ???",
762:"On vous propose d’échanger votre\\nPokémon N. {DYNAMIC 0} {DYNAMIC 1}\\pcontre un\\nN. {DYNAMIC 2} {DYNAMIC 3}.\\pAccepter cette offre d’échange?",
764:("{DPAD_UPDOWN}CHOISIR {A_BUTTON}REJOINDRE {B_BUTTON}ANNULER",),
765:("NOM{CLEAR_TO 60}CHERCHE{CLEAR_TO 110}OFFRE{CLEAR_TO 198}N.",),
766:("Voici la Carte Dresseur de\\n{DYNAMIC 0} {DYNAMIC 1}…\\l{DYNAMIC 2}\\pPOKéDEX: {DYNAMIC 3}\\nDURÉE:   {DYNAMIC 4}:{DYNAMIC 5}\\p",),
767:("COMBATS: VICT.: {DYNAMIC 0}  DÉF.: {DYNAMIC 2}\\nÉCHANGES: {DYNAMIC 3}\\p“{DYNAMIC 4} {DYNAMIC 5}\\n{DYNAMIC 6} {DYNAMIC 7}”\\p",),
768:"{DYNAMIC 1}: Ravi de t’avoir vu!{PAUSE 60}",769:"{DYNAMIC 1}: Ravi de te rencontrer!{PAUSE 60}",
770:"Fin de la lecture de la Carte\\nDresseur de {DYNAMIC 1}.{PAUSE 60}",
771:"CAT: ",
772:"TEAM AQUA",773:"TEAM MAGMA",774:"EXPERT",775:"TRIATHLETE",776:"RANGER {PKMN}",777:"INGÉNIEUR",778:"CRÂNE CHAUVE",
779:"JOUEUR",780:"ROCKEUR",781:"BOSS",782:"MEDIUM",783:"COUPLE BRANCHÉ",784:"TANDEM",785:"FILLE TANDEM",786:"PEINTRE",
787:"AGENT",788:"ADMIN. ROCKET",789:"ROCKET",790:"DÉVELOPPEUR",
791:("{PALETTE 5}{COLOR_HIGHLIGHT_SHADOW 13 14 15}BALL{CLEAR_TO 56}APPÂT\\nCAILLOU{CLEAR_TO 56}FUITE",),
792:"SAFARI BALLS",793:"Marnga",794:" a été fabriqué!",
795:"MIXEUR À BAIES\\nRECORD DE VITESSE!",796:"m découverte. Très sucrée.",
797:"ORIGINAL",798:"GÉN. 3",799:"GÉN. 7",800:"GÉN. 1",801:"Aller à la page suivante.",802:"Sauver et continuer…",
803:"GÉN. 1-9",804:"GÉN. 1-3",805:"CHAOS",806:"RTC",807:"Aller aux options aléatoires.",808:"Aller aux options Nuzlocke.",
809:"ÉVOLUTIONS",810:"Aller aux options de difficulté.",811:"NUZLOCKE",812:"Aller aux options de défi.",
814:"{STR_VAR_1} est troublé par\\nla météo anormale!",
815:("Enregistrer cet\\nobjet en touchant ou\\nen maintenant SELECT?",),
816:"Trier les objets comment?",817:"Objets triés par {STR_VAR_1}!",
820:"LA FAMILLE STRATÈGE",
824:("Lecture de la Carte\\nannulée.",),
825:"NOM DU RIVAL?",
827:"KRIS",828:"STÉRÉO",829:"IMPÉRIAL",830:"GÉN. 4",831:"B{RIGHT_ARROW}A",
832:"Choisissez le cadre qui entoure\\nles fenêtres.",
833:"ZONE INCONNUE",
834:"MINÉRAL",835:"Inconnu",836:"Att < Déf",837:"aléatoire %",838:"{UP_ARROW_2}sang-froid",839:"{UP_ARROW_2}intelligence",
840:"échangé avec ",841:" dans l’équipe",842:"sur ",843:"Kanto",844:"Johto",845:"Kalos",846:"Galar",847:"Sinjoh",848:"Paldea",
849:"natures Amplifiées",850:" dégâts actuels",851:" coups critiques",
856:"{DYNAMIC 0} est sélectionné.",857:"{DYNAMIC 0} a été déposé.",858:"{DYNAMIC 0} a été relâché.",
859:"Bye bye, {DYNAMIC 0}!",860:"{DYNAMIC 0} est revenu!",861:"{DYNAMIC 0} est tenu.",862:"Changé en {DYNAMIC 0}.",
863:"Nº {DYNAMIC 0}",864:"RUBANS {DYNAMIC 0}",865:"ROUTE 49",866:"ROUTE 50",
868:"Pokémon ?????",869:"???,? kg",872:"Nº ID /",
873:("Nature {DYNAMIC 0}{DYNAMIC 2}{DYNAMIC 1}{DYNAMIC 5}{DYNAMIC 6}{DYNAMIC 7},\\nrencontré au {LV_2}{DYNAMIC 0}{DYNAMIC 3}{DYNAMIC 1},\\n{DYNAMIC 0}{DYNAMIC 4}{DYNAMIC 1}.",),
874:("Nature {DYNAMIC 0}{DYNAMIC 2}{DYNAMIC 1}{DYNAMIC 5}{DYNAMIC 6}{DYNAMIC 7},\\néclos au {LV_2}{DYNAMIC 0}{DYNAMIC 3}{DYNAMIC 1},\\n{DYNAMIC 0}{DYNAMIC 4}{DYNAMIC 1}.",),
875:("Nature {DYNAMIC 0}{DYNAMIC 2}{DYNAMIC 1}{DYNAMIC 5}{DYNAMIC 6}{DYNAMIC 7},\\nobtenu lors d’un échange.",),
876:("Nature {DYNAMIC 0}{DYNAMIC 2}{DYNAMIC 1}{DYNAMIC 5}{DYNAMIC 6}{DYNAMIC 7},\\nobtenu lors d’une rencontre\\nfatidique au {LV_2}{DYNAMIC 0}{DYNAMIC 3}{DYNAMIC 1}.",),
877:("Nature {DYNAMIC 0}{DYNAMIC 2}{DYNAMIC 1}{DYNAMIC 5}{DYNAMIC 6}{DYNAMIC 7},\\nsans doute rencontré au {LV_2}{DYNAMIC 0}{DYNAMIC 3}{DYNAMIC 1},\\n{DYNAMIC 0}{DYNAMIC 4}{DYNAMIC 1}.",),
878:("Nature {DYNAMIC 0}{DYNAMIC 2}{DYNAMIC 1}{DYNAMIC 5}{DYNAMIC 6}{DYNAMIC 7}",),
879:("Nature {DYNAMIC 0}{DYNAMIC 2}{DYNAMIC 1}{DYNAMIC 5}{DYNAMIC 6}{DYNAMIC 7},\\nrencontré quelque part au {LV_2}{DYNAMIC 0}{DYNAMIC 3}{DYNAMIC 1}.",),
880:("Nature {DYNAMIC 0}{DYNAMIC 2}{DYNAMIC 1}{DYNAMIC 5}{DYNAMIC 6}{DYNAMIC 7},\\néclos quelque part au {LV_2}{DYNAMIC 0}{DYNAMIC 3}{DYNAMIC 1}.",),
881:"HYPER",882:"MULTI",883:"MULTI-LINK",884:"Interview",885:"Quiz de {DYNAMIC 0}",886:"{STR_VAR_1} MULTI",887:"{STR_VAR_1} LINK",
888:"{DYNAMIC 0} a rejoint le chat!",889:"{DYNAMIC 0} a quitté le chat.",
890:"Le chef, {DYNAMIC 0}, est parti.\\nFin du chat.",891:"{DYNAMIC 0} a sauvegardé.",
892:"Le gagnant reçoit ce\\n{DYNAMIC 0}!",893:"Super score! Vous avez\\ngagné {DYNAMIC 1} {DYNAMIC 0}!",
894:"POKeMON",895:("{STR_VAR_1}/{STR_VAR_2}\\nBALLS  {STR_VAR_3}",),896:"KANTO",897:"JOHTO ET KANTO",
898:"{DYNAMIC 0} joueurs",899:"{DYNAMIC 1} joueurs",900:"{DYNAMIC 2} joueurs",901:"{DYNAMIC 3} joueurs",
909:"QUIZ",
910:"Voici la liste de vos Pokémon,\\n{PLAYER}.\\pOuvrez-la pour voir les talents et\\ncapacités de vos Pokémon.\\pC’est aussi ici que vous choisissez un\\nPokémon pour utiliser un objet.{PAUSE_UNTIL_PRESS}",
912:"KOGA",
}
T.update(M)
for k,v in list(T.items()):
    if isinstance(v,str) and 'DYNAMIC' in v: T[k]=(v,)
