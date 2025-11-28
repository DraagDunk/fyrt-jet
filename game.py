from paths import ChoicePath, LinearPath, LootPath, LinearChallengePath, EndPath, \
    HasItemLinearPath
from items import Item, Weapon
from character import Character

# Landevejen
landevejen = LinearPath(
    "",
    "Du kommer marcherende hen ad landevejen: én to, én to! "
    "Du har dit tornyster på ryggen, og en sabel ved siden, for du har været i krig. "
    "Nu skal du hjem. "
    "Så møder du en gammel heks på landevejen; "
    "Hun er så ækel, hendes underlæbe hænger lige ned på brystet."

)

heksens_hilsen = ChoicePath(
    "",
    "Hun siger: 'God aften, soldat! Hvor du har en pæn sabel og et stort tornyster, "
    "du er en rigtig soldat! Nu skal du få så mange penge, du vil eje!'"
)
landevejen.set_next(heksens_hilsen)

# Slå heksen ihjel

hug_ned = LinearChallengePath(
    "Hug den vederstyggelige heks ned.",
    "Du hugger hovedet af den klamme heks, og fortsætter hjem.",
    failed="Heksen losser dig durk i løgene.",
    failed_consequence=lambda c: c.take_damage(2),
    challenge=6,
    stat="body"
)

se_træet = LinearPath(
    "",
    "Du får øje på et besynderligt træ, som minsandten er hult! "
    "Du kommer i tanke om, at heksen vist nok nævnte noget, med nogle penge. "
    "Pengene kunne grangiveligt måske være gemt inde i det mærkværdige hule træ!",
)
hug_ned.set_next(se_træet)

få_klø = LinearPath(
    "",
    "'Den kan vi lige prøve at tage igen,' siger heksen surt."
)
hug_ned.set_next(se_træet)
hug_ned.set_failed_next(få_klø)
få_klø.set_next(heksens_hilsen)

# Sig tak

sig_tak = ChoicePath(
    "Sig: 'tak skal du have, din gamle heks!'",
    "'Kan du se det store træ?' siger heksen, og peger på et træ, der står ved siden af jer. "
    "'Det er ganske hult inden i! Der skal du krybe op i toppen, så ser du et hul, som du skal "
    "lade dig glide igennem og komme dybt i træet! Jeg skal binde dig en strikke om livet, "
    "for at jeg kan hejse dig op igen, når du råber på mig!'"
)

sig_hvad_skal_jeg = LinearPath(
    "Sig: 'Hvad skal jeg så nede i træet?'",
    "'Hente penge!' siger heksen."
)

sig_tak.add_choices(sig_hvad_skal_jeg)

heksen_forklaring = ChoicePath(
    "",
    "'Du skal vide, når du kommer ned på bunden af træet, så er du i en stor gang, der er ganske "
    "lyst, for der brænder over hundrede lamper. Så ser du tre døre, du kan lukke dem op, nøglen "
    "sidder i. Går du ind i det første kammer, da ser du midt på gulvet en stor kiste, oven på "
    "den sidder en hund; han har et par øjne så store som et par tekopper, men det skal du ikke "
    "bryde dig om! Jeg giver dig mit blåternede forklæde, det kan du brede ud på gulvet; gå så "
    "rask hen og tag hunden, sæt ham på mit forklæde, luk kisten op og tag lige så mange "
    "skillinger, du vil. De er alle sammen af kobber, men vil du hellere have sølv, så skal du "
    "gå ind i det næste værelse, men der sidder en hund, der har et par øjne, så store, som et "
    "møllehjul, men det skal du ikke bryde dig om, sæt ham på mit forklæde og tag du af pengene! "
    "Vil du derimod have guld, det kan du også få, og det så meget, du vil bære, når du går ind i "
    "det tredje kammer. Men hunden, som sidder på pengekisten, har her to øjne, hvert så stort "
    "som Rundetårn. Det er en rigtig hund, kan du tro! Men det skal du ikke bryde dig noget om! "
    "Sæt ham bare på mit forklæde, så gør han dig ikke noget, og tag du af kisten så meget guld, "
    "du vil!'"
)
sig_hvad_skal_jeg.set_next(heksen_forklaring)

sig_det_var_ikke_galt = LinearPath(
    "Sig: 'Det var ikke så galt. Men hvad skal jeg give dig, din gamle heks? For noget vil du vel "
    "have med, kan jeg tænke!'",
    "'Nej' siger heksen, 'ikke en eneste skilling vil jeg have! Du skal bare tage til mig et "
    "gammelt fyrtøj, som min bedstemoder glemte, da hun sidst var dernede!'"
)
heksen_forklaring.add_choices(sig_det_var_ikke_galt)

heksens_genstande = ChoicePath(
    "",
    "Heksen kigger afventende på dig. Hun trækker vejret dybt og rallende."
)
sig_det_var_ikke_galt.set_next(heksens_genstande)

forklæde = Item("heksens forklæde")
få_forklæde = LootPath(
    "Ræk hånden frem efter forklædet.",
    "'Her er mit blåternede forklæde,' siger heksen.",
    loot=forklæde,
    looted_consequence="Heksen kigger forvirret på din fremstrakte hånd. hun trækker på skuldrene."
)

strik = Item("strikken om livet")
få_strik = LootPath(
    "Sig: 'Nå! Lad mig få strikken om livet!'",
    "'Her er den!' sagde heksen.",
    loot=strik,
    looted_consequence="'Øh,' sagde heksen forvirret, 'jeg har bundet den om dig ...'"
)
sig_tak.add_choices(få_strik)

heksen_forklaring.add_choices(få_strik, få_forklæde)

ved_træet = ChoicePath(
    "Gå hen til træet.",
    "Du står foran det store hule træ."
)
se_træet.set_next(ved_træet)

heksens_genstande.add_choices(få_forklæde, få_strik, ved_træet)

ignorer_træet = LinearPath(
    "Ignorér træet og gå hjem.",
    "'Næ,' tænker du for dig selv. 'Det er garanteret løgn og latin.'"
)

undersøg_træet = LinearChallengePath(
    "Undersøg træet nærmere.",
    "Træet er hult, og åbningen ser ud til at være dyb og mørk.",
    challenge=2,
    stat="mind",
    failed="Træet ser ud til at være på nippet til at falde sammen om ørene på dig. Det virker "
    "ikke sikkert.",
)
undersøg_træet.set_next(ved_træet)
undersøg_træet.set_failed_next(ved_træet)

kravl_ind = LinearChallengePath(
    "Kravl ind i træet.",
    "Så kryber du op i træet, lader dig dumpe ned i hullet.",
    challenge=3,
    stat="spirit",
    failed="Du snubler på vej ned i træet, og falder det sidste stykke.",
    failed_consequence=lambda c: c.take_damage(1),
)
ved_træet.add_choices(ignorer_træet, undersøg_træet, kravl_ind)

# Nede i træet

stor_gang = ChoicePath(
    "Gå ud på gangen.",
    "Du står nede i en stor gang, hvor mange hundrede lamper brænder. Der er tre døre."
)
kravl_ind.set_next(stor_gang)
kravl_ind.set_failed_next(stor_gang)

kravl_op = HasItemLinearPath(
    "Kravl op",
    "Du råber 'hejs mig nu op, du gamle heks!'",
    required_item=strik,
    failed="Du prøver at klatre op."
)

fyrtøj = Item("fyrtøj")
tag_fyrtøj = LootPath(
    "Tag fyrtøjet.",
    "Du går og tager det.",
    loot=fyrtøj,
    looted_consequence="Du har allerede gået og taget det."
)

dør1 = LinearPath(
    "Åbn dør 1.",
    "Nu lukker du den første dør op. Uh! Dér sidder en hund med øjne, så store som tekopper og "
    "glor på dig."
)

dør2 = LinearPath(
    "Åbn dør 2.",
    "Du går ind i det andet værelse. Eja! Dér sidder en hund med øjne så store, som et møllehjul."
)

dør3 = LinearPath(
    "Åbn dør 3.",
    "Du går ind i det tredje kammer! Nej det var ækelt! Hunden derinde har virkeligt to øjne så "
    "store som Rundetårn! Og de løber rundt i hovedet lige som hjul."
)
stor_gang.add_choices(dør1, dør2, dør3, tag_fyrtøj, kravl_op)


klatr_op = LinearChallengePath(
    "Prøv at klatre op",
    "Du klatrer op, og det er let som en leg!",
    failed="Du prøver at klatre op, men falder ned.",
    failed_consequence=lambda c: c.take_damage(1),
    challenge=6,
    stat="spirit"
)
kravl_op.set_failed_next(klatr_op)
klatr_op.set_next(ved_træet)

# Rum 1

rum1 = ChoicePath(
    "",
    "Du står i et rum med en hund med øjne så store som tekopper."
)
dør1.set_next(rum1)

kobber = Item("kobberskillinger")
tag_kobber = LootPath(
    "Tag kobberskillinger.",
    "Du tager lige så mange kobberskillinger, du kan have i din lomme, lukker så kisten.",
    loot=kobber,
    looted_consequence="Kisten med kobbermønter er tom.",
)

sig_du_er_net = HasItemLinearPath(
    "Sig: 'Du er en net fyr!'",
    "Du sætter hunden på heksens forklæde.",
    failed="'Tak,' siger hunden og blinker med øjnene så store som tekopper.",
    success_consequence=lambda c: rum1.add_choices(tag_kobber)
)


def slå_hund_1_sc(char):
    rum1.add_choices(tag_kobber)
    rum1.rem_choices(sig_du_er_net)
    rum1.consequence = "Du står i et rum med en død hund med øjne så store som tekopper."
    dør1.consequence = "Nu lukker du den første dør op. Uh! Dér ligger en hund med øjne, så store "
    "som tekopper og er død på jorden."


slå_hund_1 = LinearChallengePath(
    "Slå hunden ihjel.",
    "Du hugger hovedet af hunden med øjne så store som tekopper.",
    failed="Hunden med øjne så store som tekopper bider dig i hånden.",
    failed_consequence=lambda c: c.take_damage(1),
    challenge=3,
    stat="body",
    success_consequence=slå_hund_1_sc,
    succeeded_consequence="Du har allerede slået hunden med øjne så store som tekopper ihjel."
)

slå_hund_1.set_failed_next(rum1)
slå_hund_1.set_next(rum1)
rum1.add_choices(sig_du_er_net, slå_hund_1, stor_gang)


# Rum 2


rum2 = ChoicePath(
    "",
    "Du står i et rum med en hund med øjne så store som møllehjul."
)
dør2.set_next(rum2)

sølv = Item("sølvskillinger")
tag_sølv = LootPath(
    "Tag sølvskillinger.",
    "Du fylder lommen og dit tornyster med det bare sølv.",
    loot=sølv,
    looted_consequence="Kisten med sølvskillinger er tom.",
)

sig_du_skal_ikke_se = HasItemLinearPath(
    "Sig: 'Du skulle ikke se så meget på mig! Du kunne få ondt i øjnene!'",
    "Du sætter hunden på heksens forklæde.",
    failed="Hunden spærrer øjnene yderligere op på provokerende vis.",
    success_consequence=lambda c: rum1.add_choices(tag_sølv)
)


def slå_hund_2_sc(char):
    rum2.add_choices(tag_sølv)
    rum2.rem_choices(sig_du_skal_ikke_se)
    rum2.consequence = "Du står i et rum med en død hund med øjne så store som møllehjul."
    dør2.consequence = "Nu lukker du den første dør op. Eja! Dér ligger en hund med øjne, så store "
    "som møllehjul og er død på jorden."


slå_hund_2 = LinearChallengePath(
    "Slå hunden ihjel.",
    "Du hugger hovedet af hunden med øjne så store som møllehjul.",
    failed="Hunden med øjne så store som møllehjul bider dig i foden.",
    failed_consequence=lambda c: c.take_damage(1),
    challenge=4,
    stat="body",
    success_consequence=slå_hund_2_sc,
    succeeded_consequence="Du har allerede slået hunden med øjne så store som møllehjul ihjel."
)

slå_hund_2.set_failed_next(rum2)
slå_hund_2.set_next(rum2)
rum2.add_choices(sig_du_skal_ikke_se, slå_hund_2, stor_gang)


# Rum 3

rum3 = ChoicePath(
    "",
    "Du står i et rum med en hund med øjne så store som Rundetårn."
)
dør3.set_next(rum3)

guld = Item("guldskillinger")
tag_guld = LootPath(
    "Tag guldmønter",
    "Du tager guld. Ja alle lommer, tornystret, kasketten og støvlerne, bliver fyldte, så du knapt "
    "kan gå! Nu har du penge!",
    loot=guld,
    looted_consequence="Kisten med guldmønter er tom.",
)

sig_godaften = HasItemLinearPath(
    "tag til kasketten og sig: 'God aften!'",
    "Sådan en hund har du aldrig set før; Men da du nu så lidt på ham, tænker du, nu kan det jo "
    "være nok. Du løfter ham ned på gulvet, og sætter ham på heksens forklæde.",
    failed="'Godaften,' siger hunden høfligt.",
    success_consequence=lambda c: rum3.add_choices(tag_guld)
)


def slå_hund_3_sc(char):
    rum3.add_choices(tag_guld)
    rum3.rem_choices(sig_godaften)
    rum3.consequence = "Du står i et rum med en død hund med øjne så store som Rundetårn."
    dør3.consequence = "Du går ind i det tredje kammer! Nej det var ækelt! Den døde hund derinde "
    "har virkeligt to øjne så store som Rundetårn!"


slå_hund_3 = LinearChallengePath(
    "Slå hunden ihjel.",
    "Du hugger hovedet af hunden med øjne så store som Rundetårn.",
    failed="Hunden med øjne så store som tekopper bider dig i to stykker.",
    failed_consequence=lambda c: c.take_damage(100),
    challenge=5,
    stat="body",
    success_consequence=slå_hund_3_sc,
    succeeded_consequence="Du har allerede slået hunden med øjne så store som Rundetårn ihjel."
)

slå_hund_3.set_failed_next(rum3)
slå_hund_3.set_next(rum3)
rum3.add_choices(sig_godaften, slå_hund_3, stor_gang)

# Kravl op

heksen_spørger = HasItemLinearPath(
    "",
    "Heksen hejser dig op, og du står igen på landevejen.",
    failed="'Har du fyrtøjet med?' spørger heksen. 'Det er sandt!' siger du, 'det havde jeg rent "
    "glemt.'",
    required_item=fyrtøj
)
kravl_op.set_next(heksen_spørger)
heksen_spørger.set_failed_next(stor_gang)

fyldt_med_penge = HasItemLinearPath(
    "",
    "Du har lommer, støvler, tornyster og kasket fulde af penge.",
    required_item=guld
)
heksen_spørger.set_next(fyldt_med_penge)

ved_heksen = ChoicePath(
    "",
    "Du står foran den afskyelige heks, som rækker hånden frem."
)
fyldt_med_penge.set_failed_next(ved_heksen)
fyldt_med_penge.set_next(ved_heksen)


def giv_fyrtøj_after(char):
    char.remove_item(fyrtøj)
    ved_træet.rem_choices(kravl_ind)


giv_fyrtøj = LinearPath(
    "Giv fyrtøjet til den ildelugtende heks.",
    "Du giver den frastødende heks fyrtøjet. 'Tak,' siger hun. Hun går.",
    after=giv_fyrtøj_after
)
giv_fyrtøj.set_next(ved_træet)

spørg_om_fyrtøj = LinearPath(
    "Spørg: 'Hvad vil du nu med det fyrtøj?'",
    "'Det kommer ikke dig ved!' siger heksen, 'nu har du jo fået penge! Giv mig bare fyrtøjet!'"
)

tru_heksen = LinearChallengePath(
    "Sig: 'Vil du straks sige mig, hvad du vil med fyrtøjet, eller jeg trækker min sabel ud og "
    "hugger dit hoved af!'",
    "'Jeg skal tænde op med det,' mumler heksen.",
    failed="'Nej,' siger heksen.",
    challenge=6,
    stat="spirit"
)

dræb_heksen = LinearChallengePath(
    "Hug hovedet af heksen.",
    "Du hugger hovedet af heksen.",
    failed="Heksen løber skrigende og skrålende væk.",
    challenge=4,
    stat="body",
    after=lambda c: ved_træet.rem_choices(kravl_ind)
)
ved_heksen.add_choices(giv_fyrtøj, spørg_om_fyrtøj, tru_heksen, dræb_heksen)
dræb_heksen.set_next(ved_træet)
dræb_heksen.set_failed_next(ved_træet)

# Gå hjem

ignorer_heksen = LinearChallengePath(
    "Ignorér heksen og gå hjem.",
    "Du går uden om den gennemført afskyelige heks, og fortsætter ad landevejen.",
    failed="Du forsøger at gå uden om heksen, men hun træder ind foran dig, og får øjenkontakt. "
    "'Undskyld,' siger hun, 'hørte du ikke hvad jeg sagde?'",
    challenge=4,
    stat="mind",
    failed_consequence=lambda c: heksens_hilsen.set_choices(sig_tak, hug_ned)
)
ignorer_heksen.set_failed_next(heksens_hilsen)
heksens_hilsen.add_choices(sig_tak, hug_ned, ignorer_heksen)

gå_hjem = EndPath(
    "",
    "Du fortsætter ad landevejen, og går hjem.",
    credits=["Jesper", "Nikolaj", "H. C. Andersen"]
)
ignorer_heksen.set_next(gå_hjem)
ignorer_træet.set_next(gå_hjem)

# Character creation
sabel = Weapon("sabel", value=2)
tornyster = Item("tornyster")

char = Character(input("Hvad er dit navn?: "))
char.add_item(sabel)
char.add_item(tornyster)

# Initialization
landevejen.choose(char)
