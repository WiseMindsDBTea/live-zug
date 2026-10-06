#!/usr/bin/env python3
"""Quelle der Artentexte. Erzeugt ../data/birds.js (window.BIRDS = [...])."""
import json, os

def M(spec):
    out = []
    for part in str(spec).split(","):
        part = part.strip()
        if not part: continue
        if "-" in part:
            a, b = map(int, part.split("-"))
            if a <= b: out += list(range(a, b + 1))
            else: out += list(range(a, 13)) + list(range(1, b + 1))
        else:
            out.append(int(part))
    return sorted(set(out))

B = []
def bird(id, de, lat, grp, hab, freq, present, sings, snd, laut, gesang, ruf, merk, verw, wo, fakt,
         kultur=None, kid=None, dawn=None, night=False, reg=None, alias=None):
    B.append({k: v for k, v in dict(
        id=id, de=de, lat=lat, grp=grp, hab=hab, freq=freq, present=M(present), sings=M(sings) if sings else [],
        snd=snd, laut=laut, gesang=gesang, ruf=ruf, merk=merk, verw=verw, wo=wo, fakt=fakt,
        kultur=kultur, kid=kid, dawn=dawn, night=night or None, reg=reg, alias=alias).items() if v not in (None, [], "")})

# freq: 1 sehr häufig · 2 häufig · 3 verbreitet/regional · 4 selten
# hab: garten · wald · wasser · feld · berge · kueste
# snd: floete · zwitscher · motiv · name · kraechz · tief · wasser · trommel · schrill · lach

# ============================================================ Drosseln & Schmätzer
bird("amsel","Amsel","Turdus merula","Drosseln",["garten","wald"],1,"1-12","2-7",["floete"],
 "Tiefe, gelassene Flötenstrophen mit Pausen – oft mit leisem Gezwitscher am Schluss.",
 "Melodisch, flötend, ohne Eile; jede Strophe ein wenig anders, häufig mit einem leiseren, „zerdrückten“ Ende. Singt von Dachfirsten und Antennen, besonders in der Morgen- und Abenddämmerung.",
 "Warnruf hartes „tix-tix“ oder tiefes „duck-duck“; abends beim Schlafplatzbezug und bei Katzen ein lautes, sich überschlagendes Zetern.",
 "Der Vogel, der klingt, als hätte er Zeit.",
 ["singdrossel","misteldrossel","moenchsgrasmuecke"],
 "Überall von der Großstadt bis zur Almhütte: Hinterhöfe, Friedhöfe, Parks, Gärten mit Rasen.",
 "Ursprünglich ein scheuer Waldvogel – die Verstädterung begann im 19. Jahrhundert. Stadtamseln singen früher, länger und höher als Waldamseln.",
 kultur="In der „Vogelhochzeit“ ist die Amsel die Braut. Und „Alle Vögel sind schon da“ zählt sie zuerst auf: „Amsel, Drossel, Fink und Star“.",
 kid=["Tü-dü-lü-lüü","Die Amsel flötet abends auf dem Dach."], dawn=55)

bird("singdrossel","Singdrossel","Turdus philomelos","Drosseln",["wald","garten"],2,"3-10","3-7",["floete","motiv"],
 "Laute, klare Motive – jedes zwei- bis viermal wiederholt.",
 "Kraftvoll und abwechslungsreich, aber jedes Motiv wird zwei- bis viermal wiederholt, bevor das nächste kommt. Singt hoch von Baumspitzen, oft bis tief in die Dämmerung.",
 "Kurzes, scharfes „zipp“ – im Oktober nachts von ziehenden Drosseln über den Städten zu hören.",
 "„Philipp, Philipp, Philipp – komm her, komm her – Tee trinken, Tee trinken“ (Volksmund).",
 ["amsel","misteldrossel","star"],
 "Wälder, Parks mit altem Baumbestand, große Gärten; im Gebirge bis zur Waldgrenze.",
 "Zerschlägt Schneckenhäuser auf einem festen Stein – solche „Drosselschmieden“ erkennt man an den Scherben.",
 kultur="In der „Vogelhochzeit“ ist die Drossel der Bräutigam: „Die Drossel war der Bräutigam, die Amsel war die Braute.“")

bird("misteldrossel","Misteldrossel","Turdus viscivorus","Drosseln",["wald","berge"],3,"1-12","1-6",["floete"],
 "Wie eine Amsel in Eile: kurze, wehmütige Strophen, oft schon im Januar.",
 "Amselähnlich, aber kürzere, raue, schneller aufeinanderfolgende Strophen ohne Ruhe dazwischen. Singt schon im Spätwinter, gern bei Wind und Regen von der höchsten Baumspitze – auf Englisch heißt sie deshalb „Stormcock“.",
 "Schnarrendes „zerrrr“ wie eine hölzerne Ratsche.",
 "Amsel mit Sturmwarnung.",
 ["amsel","singdrossel"],
 "Hohe Bäume in Parks und Wäldern, Streuobstwiesen; Nadelwälder im Bergland.",
 "Ihr Name kommt von der Mistel: Sie frisst die Beeren, die klebrigen Samen bleiben an Ästen haften – und keimen dort neu.")

bird("wacholderdrossel","Wacholderdrossel","Turdus pilaris","Drosseln",["feld","garten","wald"],2,"1-12","4-6",["kraechz"],
 "Ratterndes „schack-schack-schack“ aus Obstbäumen und Feldgehölzen.",
 "Unscheinbar: gequetschtes, schwatzendes Gezwitscher, oft im Flug vorgetragen.",
 "Laut ratterndes „schack-schack-schack“; im Flug ein gedehntes „gih“.",
 "Die Drossel, die schimpft wie eine Elster.",
 ["elster","misteldrossel"],
 "Feldgehölze, Streuobst, Parks; im Winter Trupps aus dem Norden an Ebereschen und auf Wiesen.",
 "Brütet in Kolonien und wehrt Krähen und Elstern gemeinsam ab – mit gezielten Kotattacken im Sturzflug.")

bird("rotkehlchen","Rotkehlchen","Erithacus rubecula","Schmätzer",["garten","wald"],1,"1-12","1-6,9-12",["zwitscher"],
 "Perlende, wehmütige Kaskaden – hohe Töne, die wie Tropfen herabfallen.",
 "Fein, perlend, abwechslungsreich, mit langen hohen Tönen und plötzlichen Tempowechseln. Singt auch im Herbst und Winter – dann besonders melancholisch.",
 "Hartes „tick“ oder „zick“, oft zu „tikikik“ gereiht; dazu ein dünnes, hohes „ziieh“.",
 "Der Herbstsänger: Wer im Oktober eine zarte, traurige Weise hört, hört meist ihn.",
 ["heckenbraunelle","zaunkoenig","hausrotschwanz"],
 "Unterholz in Wäldern, Parks, Friedhöfen und jedem Garten mit Gebüsch – bis hinauf in die Bergwälder.",
 "Im Herbst verteidigen Männchen und Weibchen eigene Winterreviere – deshalb singen beide. Unter Straßenlaternen singt es auch nachts.",
 kultur="In Großbritannien der Weihnachtsvogel schlechthin. Eine Legende erzählt, es habe Christus einen Dorn aus der Krone gezogen und sich dabei die Brust rot gefärbt.",
 kid=["Tick, tick!","Das Rotkehlchen singt sogar im Winter."], dawn=60)

bird("nachtigall","Nachtigall","Luscinia megarhynchos","Schmätzer",["wald","garten","wasser"],3,"4-8","4-6",["floete","zwitscher"],
 "Schluchzende, anschwellende „lü-lü-lü“-Reihen – mitten in der Nacht.",
 "Laut, enorm abwechslungsreich: schmetternde Triller, harte „tschuk“-Reihen und vor allem die berühmten, langsam anschwellenden Flötentöne „lü-lü-lü-lü“. Unverpaarte Männchen singen die ganze Nacht.",
 "Weiches „huit“ und knarrendes „karr“.",
 "Wer im Mai nachts ein Konzert im Gebüsch hört, hört sie.",
 ["singdrossel","moenchsgrasmuecke"],
 "Dichte Gebüsche in Auwäldern, Parks und an Flussufern im Tiefland. Berlin ist berühmt für seine vielen Nachtigallen, ebenso die Donau-Auen bei Wien.",
 "Nachts singen die Männchen vor allem für Weibchen, die auf dem Zug vorbeifliegen; tagsüber gilt der Gesang den Rivalen.",
 kultur="Andersens Märchen „Die Nachtigall“: Der Kaiser von China zieht einen mechanischen Vogel vor – bis nur die echte Nachtigall ihn retten kann. Bei Shakespeare streiten Romeo und Julia: „Es war die Nachtigall und nicht die Lerche.“ Auch in Grimms „Jorinde und Joringel“ wird Jorinde in eine Nachtigall verwandelt.",
 kid=["Lü-lü-lü-lü!","Die Nachtigall singt mitten in der Nacht."], night=True)

bird("hausrotschwanz","Hausrotschwanz","Phoenicurus ochruros","Schmätzer",["garten","berge"],1,"3-10","3-7,9-10",["zwitscher"],
 "Kurze Strophe mit einem knirschenden Teil – wie zerknülltes Papier.",
 "Gepresste Pfeiftöne, dazwischen ein unverwechselbares Knirschen oder Kratzen. Oft der allererste Sänger, lange vor Sonnenaufgang.",
 "„Hüid“ und ein schnalzendes „tek-tek“.",
 "Der Morgen beginnt mit Papierknüllen auf dem Dach.",
 ["gartenrotschwanz","rotkehlchen"],
 "Dachfirste, Baustellen, Industriegebiete, Altstädte – und ursprünglich Felsen im Gebirge, bis über 3000 m.",
 "Bleibt oft bis in den November und singt im Herbst noch einmal. Einzelne überwintern inzwischen.",
 dawn=70)

bird("gartenrotschwanz","Gartenrotschwanz","Phoenicurus phoenicurus","Schmätzer",["garten","wald"],3,"4-9","4-6",["zwitscher"],
 "Wehmütiger Einstieg „hüit – tüi-tüi-tüi“, dann ein wechselnder Schnörkel.",
 "Kurze Strophe: ein gedehnter Anfangston, zwei, drei gleiche Silben, dann ein jedes Mal anderes Ende – oft mit Imitationen anderer Vögel.",
 "„Huit“ und „tek-tek“, ähnlich dem Hausrotschwanz.",
 "Der Frühaufsteher unter den Frühaufstehern.",
 ["hausrotschwanz","rotkehlchen"],
 "Streuobstwiesen, Kleingärten und Parks mit alten Bäumen, lichte Wälder.",
 "Vogel des Jahres 2011. Zieht im Winter bis in die Savannen südlich der Sahara.",
 dawn=80)

# ============================================================ Meisen & Co.
bird("kohlmeise","Kohlmeise","Parus major","Meisen",["garten","wald"],1,"1-12","1-6,9-10",["motiv"],
 "Metallisch wiederholtes „zi-zi-bä“ – wie eine Fahrradpumpe.",
 "Zwei- bis dreisilbige, metallische Motive, viele Male wiederholt: „zi-zi-bä“, „zi-dä zi-dä“, „titu-titu“. Beginnt schon an milden Januartagen.",
 "Finkenartiges „pink“, zeterndes „tsche-tsche-tsche“ und ein riesiges Repertoire weiterer Laute.",
 "„Zi-zi-bä“ – die Fahrradpumpe im Gebüsch.",
 ["tannenmeise","blaumeise","zilpzalp","buchfink"],
 "Jeder Park, jeder Garten, jeder Wald, jedes Futterhaus.",
 "Faustregel der Vogelkundler: Ein unbekannter Ruf im Park ist zuerst einmal eine Kohlmeise. Einzelne Männchen beherrschen mehrere Strophentypen.",
 kid=["Zi-zi-bä!","Die Meise klingt wie eine Fahrradpumpe."], dawn=35)

bird("blaumeise","Blaumeise","Cyanistes caeruleus","Meisen",["garten","wald"],1,"1-12","2-6",["zwitscher"],
 "Zwei, drei hohe Töne, dann ein perlender Triller: „zi-zi-sirrrr“.",
 "Kurze Strophe: hohe, dünne Einleitungstöne, gefolgt von einem schnellen Triller.",
 "Schimpfendes, schnarrendes „zerretetet“ und feine „tsi-tsi“-Laute.",
 "Erst Anlauf, dann Rolle.",
 ["kohlmeise","tannenmeise"],
 "Gärten, Parks, Alleen und Laubwälder – gern an Nistkästen.",
 "Blaumeisen reflektieren am Scheitel UV-Licht, das für uns unsichtbar ist – bei der Partnerwahl spielt es eine Rolle.",
 kid=["Zi-zi-sirrr!","Die kleine blaue Meise trillert."])

bird("tannenmeise","Tannenmeise","Periparus ater","Meisen",["wald","berge","garten"],2,"1-12","1-6,9-10",["motiv"],
 "Schnelles, helles „sitühe-sitühe-sitühe“ aus Fichten.",
 "Zweisilbige, schnelle Motive, höher und weicher als bei der Kohlmeise, oft von der Spitze eines Nadelbaums.",
 "Feines „sit“ und klagendes „tüh“.",
 "Die Kohlmeise in Eile – und im Nadelwald.",
 ["kohlmeise","wintergoldhaehnchen"],
 "Nadelwälder bis zur Baumgrenze, Friedhöfe und Gärten mit Fichten und Kiefern.",
 "Die kleinste heimische Meise legt im Herbst Wintervorräte an: Samen, versteckt in Rindenritzen.")

bird("schwanzmeise","Schwanzmeise","Aegithalos caudatus","Meisen",["wald","garten"],2,"1-12","2-5",["zwitscher","schrill"],
 "Feines „sri-sri-sri“ und ein schnurrendes „zerrr“ – ein Trupp zieht vorbei.",
 "Selten zu hören: leises, zwitscherndes Plaudern.",
 "Hohe, dünne „sri-sri-sri“-Reihen und kurze, schnurrende „trrr“-Laute – der Kontaktruf eines umherziehenden Trupps.",
 "Ein Wollknäuel mit Stiel, das immer in Gesellschaft reist.",
 ["wintergoldhaehnchen","blaumeise"],
 "Laub- und Mischwälder, Parks, Gärten mit Hecken; im Winter in gemischten Meisentrupps.",
 "Baut ein kunstvolles, beutelförmiges Nest aus Moos, Spinnweben und Flechten, ausgepolstert mit hunderten bis über tausend Federn. Im Winter schlafen die Tiere eng aneinandergekuschelt in einer Reihe.")

bird("wintergoldhaehnchen","Wintergoldhähnchen","Regulus regulus","Goldhähnchen",["wald","berge","garten"],2,"1-12","3-7,9-10",["schrill","zwitscher"],
 "Die höchste Stimme im Wald: rhythmisches „si-si-sisi-sisi-sisirissi“.",
 "Sehr hoch, rhythmisch auf- und abschwingend, mit einem kleinen Schnörkel am Ende.",
 "Extrem hohes „srii-srii-srii“.",
 "Ein Hörtest: Wer es nicht mehr hört, hört keine hohen Töne mehr.",
 ["schwanzmeise","tannenmeise","gartenbaumlaeufer"],
 "Fichten- und Tannenwälder bis zur Baumgrenze, Friedhöfe und Parks mit Nadelbäumen.",
 "Mit rund 5–6 Gramm zusammen mit dem Sommergoldhähnchen der kleinste Vogel Europas. Viele ältere Menschen hören seinen Gesang nicht mehr.")

bird("zaunkoenig","Zaunkönig","Troglodytes troglodytes","Weitere Singvögel",["wald","garten","wasser"],1,"1-12","1-7,9-12",["zwitscher"],
 "Winzig, aber ohrenbetäubend: schmetternde Strophe mit schnurrendem Triller.",
 "Sehr laut, schnell, schmetternd, mit einem oder mehreren eingebauten Trillern. Singt fast das ganze Jahr, auch im Winter.",
 "Hartes „teck-teck“ und schnarrendes „zerrr“.",
 "Zehn Gramm Vogel, Weckerlautstärke.",
 ["rotkehlchen","heckenbraunelle"],
 "Unterholz, Bachufer, Gärten mit dichtem Gebüsch – vom Tiefland bis ins Gebirge.",
 "Das Männchen baut mehrere Nester; das Weibchen wählt eines davon aus.",
 kultur="Bei den Brüdern Grimm („Der Zaunkönig“) wollen die Vögel den König wählen: Wer am höchsten fliegt. Der Adler gewinnt – doch der kleine Vogel hat sich in seinem Gefieder versteckt und flattert zuletzt noch ein Stück höher. Daher sein Name. In „Der Zaunkönig und der Bär“ führt er sogar Krieg gegen den Bären.",
 kid=["Tirili-trrrr!","Der kleinste Vogel singt so laut wie ein Wecker."], dawn=40)

bird("heckenbraunelle","Heckenbraunelle","Prunella modularis","Weitere Singvögel",["garten","wald","berge"],2,"1-12","2-7",["zwitscher"],
 "Hohes, gleichförmig klirrendes Plätschern – ohne Höhepunkt.",
 "Eilige, etwa zwei bis drei Sekunden lange Strophe, die wie ein Rinnsal klirrt; oft von einer Buschspitze.",
 "Hohes „tiih“.",
 "Rotkehlchen ohne Gefühl.",
 ["rotkehlchen","zaunkoenig","haussperling"],
 "Hecken, Gärten, Parks, Waldränder, Fichtenschonungen – bis ins Gebirge.",
 "Wirkt unscheinbar wie ein Spatz, führt aber ein kompliziertes Liebesleben: Ein Weibchen hat oft mehrere Partner.")

# ============================================================ Finken & Sperlinge
bird("buchfink","Buchfink","Fringilla coelebs","Finken",["wald","garten"],1,"1-12","2-7",["zwitscher"],
 "Schmetternde, abwärts rollende Strophe mit Schnörkel am Ende – der „Finkenschlag“.",
 "Laut, temperamentvoll, abfallend, mit betontem Endschnörkel. Ein Männchen hat meist ein bis mehrere Strophentypen.",
 "„Pink“ oder „fink“; dazu der regional verschiedene „Regenruf“ (z. B. „rüüt“ oder „hüit“), im Flug „jüpp“.",
 "„Bin, bin, bin ich nicht ein schöner Feld-mar-schall?“ (Volksmund)",
 ["fitis","kohlmeise","bergfink"],
 "Häufigster Waldvogel: Laub- und Nadelwälder, Parks, Gärten, bis zur Baumgrenze.",
 "Buchfinken haben regionale Dialekte: Endschnörkel und Regenruf klingen in verschiedenen Gegenden verschieden.",
 kultur="„Amsel, Drossel, Fink und Star …“ aus „Alle Vögel sind schon da“. Im Harz wird beim „Finkenmanöver“ seit Generationen der schönste Finkenschlag prämiert.",
 kid=["Pink, pink!","Der Fink ruft „pink“ und schmettert sein Lied."], dawn=25)

bird("bergfink","Bergfink","Fringilla montifringilla","Finken",["wald","garten"],3,"10-3",None,["kraechz"],
 "Quäkendes, gedehntes „wäääh“ aus Buchenkronen im Winter.",
 "Bei uns kaum zu hören – im Norden ein schnarrendes, gedehntes „dsäää“.",
 "Nasales „kwääk“ und im Flug ein hartes „jäck“.",
 "Der Wintergast, der wie ein quengelnder Buchfink klingt.",
 ["buchfink","gruenfink"],
 "Wintergast aus Skandinavien: Buchenwälder in Mastjahren, Futterstellen, Felder.",
 "In Buchenmast-Wintern sammeln sich an einzelnen Schlafplätzen teils Millionen Bergfinken – ein Naturschauspiel.",
 reg="Wintergast")

bird("gruenfink","Grünfink","Chloris chloris","Finken",["garten"],2,"1-12","3-7",["zwitscher"],
 "Klingelnde Triller und ein gedehntes, nasales „dschwuiiih“.",
 "Abwechselnd klingelnde Triller und das gequetschte „dschwuiiih“; im Frühling oft im flatternden Singflug.",
 "Im Flug ein klingelndes „gigigig“.",
 "„Dschwuiiih“ – der Seufzer aus der Thuja-Hecke.",
 ["girlitz","bergfink","stieglitz"],
 "Gärten, Alleen, Friedhöfe, Wohnviertel mit Hecken.",
 "Die Bestände sind seit etwa 2009 stark eingebrochen – vor allem durch eine Parasitenkrankheit (Trichomonaden), die sich an verschmutzten Futterstellen ausbreitet. Futterhäuser deshalb sauber halten!",
 alias=["Grünling"])

bird("stieglitz","Stieglitz","Carduelis carduelis","Finken",["feld","garten"],2,"1-12","3-8",["zwitscher","name"],
 "Hastiges, perlendes Gezwitscher mit eingestreutem „stiglitt“.",
 "Flinkes, munteres Zwitschern und Trillern, durchsetzt mit dem namensgebenden Ruf.",
 "„Stiglitt“ oder „didlit“ – daher der Name.",
 "Ruft seinen Namen beim Losfliegen.",
 ["girlitz","erlenzeisig"],
 "Brachen, Bahndämme, Wegränder, Gärten mit Disteln oder Sonnenblumen.",
 "Zieht mit seinem spitzen Schnabel Samen aus Disteln und Karden. Vogel des Jahres 2016.",
 kultur="Auf Renaissance-Gemälden hält das Jesuskind oft einen Stieglitz – ein Symbol der Passion. Carel Fabritius malte 1654 „Der Distelfink“, der später einem berühmten Roman den Namen gab.",
 kid=["Stiglitt!","Der bunte Distelfink ruft seinen Namen."], alias=["Distelfink"])

bird("girlitz","Girlitz","Serinus serinus","Finken",["garten"],3,"3-10","3-8",["zwitscher","schrill"],
 "Sehr schnelles, hohes Klirren – wie aneinanderreibende Glasscherben.",
 "Hastiges, sirrendes, klirrendes Gezwitscher, oft im fledermausartigen Singflug.",
 "Trillerndes „girrlitt“.",
 "Ein Schlüsselbund, der singt.",
 ["gruenfink","stieglitz","erlenzeisig"],
 "Gärten, Friedhöfe, Parks und Ortsränder mit Nadelbäumen – wärmeliebend.",
 "Kleinster Fink Mitteleuropas. Kam erst im 19. Jahrhundert aus dem Mittelmeerraum zu uns.")

bird("gimpel","Gimpel","Pyrrhula pyrrhula","Finken",["wald","garten","berge"],2,"1-12","3-6",["floete"],
 "Ein leises, wehmütiges „djü“ – wie ein kleines Seufzen.",
 "Leise, knirschend und flötend, selten bemerkt.",
 "Weiches, melancholisches „djü“ oder „büh“.",
 "Der Vogel mit dem roten Bauch und der traurigen Pfeife.",
 ["kernbeisser"],
 "Wälder mit Unterholz, Parks, Gärten; im Winter an Knospen und Futterstellen.",
 "Der zweite Name „Dompfaff“ kommt von der roten Brust und der schwarzen Kappe – wie bei einem Domherrn. Früher brachte man Gimpeln ganze Melodien bei.",
 kultur="„Gimpel“ wurde zum Schimpfwort für einfältige Menschen, weil die Vögel sich leicht fangen ließen.",
 alias=["Dompfaff"])

bird("kernbeisser","Kernbeißer","Coccothraustes coccothraustes","Finken",["wald","garten"],3,"1-12","3-5",["schrill"],
 "Scharfes, kurzes „zicks“ aus den Baumkronen.",
 "Leise und stockend, kaum bekannt.",
 "Explosives, hartes „zicks“ oder „tsik“.",
 "Ein Nussknacker mit Flügeln.",
 ["gimpel","kleiber"],
 "Laubwälder, Parks und Friedhöfe mit Hainbuchen, Kirschen und Ahorn – meist hoch oben.",
 "Sein riesiger Schnabel knackt Kirsch- und sogar Olivenkerne; dabei wirken enorme Kräfte.")

bird("erlenzeisig","Erlenzeisig","Spinus spinus","Finken",["wald","berge","wasser"],2,"1-12","2-6",["zwitscher"],
 "Plapperndes Gezwitscher mit gequetschtem „dziii“ und knarrendem Schluss.",
 "Schnelles, schwatzendes Zwitschern, eingestreut gedehnte, gequetschte Töne, oft mit knarrendem Endlaut.",
 "Klagendes „tsüje“ oder „dlüi“.",
 "Ein Girlitz mit Schnupfen.",
 ["girlitz","stieglitz"],
 "Nadelwälder im Bergland; im Winter in Trupps an Erlen und Birken an Gewässern.",
 "Hängt beim Fressen kopfüber an den Erlenzapfen wie eine kleine Meise.",
 alias=["Zeisig"])

bird("kreuzschnabel","Fichtenkreuzschnabel","Loxia curvirostra","Finken",["wald","berge"],3,"1-12","1-12",["schrill"],
 "Hartes, metallisches „kip-kip-kip“ im Überflug über Fichtenwäldern.",
 "Mischung aus Rufen, Trillern und knarrenden Tönen.",
 "Lautes „kip“ oder „glipp“, meist im Flug in Trupps.",
 "Der Vogel mit dem Dosenöffner-Schnabel.",
 ["gimpel"],
 "Fichtenwälder, vor allem im Gebirge und in den Mittelgebirgen.",
 "Mit dem gekreuzten Schnabel spreizt er Zapfenschuppen auf. Wenn genug Zapfen da sind, brütet er sogar mitten im Winter.",
 kultur="Eine alte Legende erzählt, er habe versucht, die Nägel aus dem Kreuz Christi zu ziehen – dabei habe sich sein Schnabel verbogen und seine Brust rot gefärbt.")

bird("haussperling","Haussperling","Passer domesticus","Sperlinge",["garten"],1,"1-12","1-12",["kraechz","zwitscher"],
 "Unermüdliches „tschilp-tschilp“ – gemeinschaftliches Geschwätz aus Hecken.",
 "Kein echter Gesang: Das Männchen reiht „tschilp“-Laute aneinander; in Gruppen entsteht ein lautes Schwatzkonzert.",
 "„Tschilp“, im Flug „tschuw“, Warnruf ein schnarrendes „terrr“.",
 "Der Biergarten-Soundtrack.",
 ["feldsperling","heckenbraunelle"],
 "Dörfer und Städte: Biergärten, Bauernhöfe, dichte Hecken, Nischen an Gebäuden.",
 "In vielen Städten seit Jahrzehnten rückläufig – sanierte Fassaden ohne Nischen gelten als ein Grund.",
 kultur="„Der Sperling, der Sperling, der bringt der Braut den Trauring“ (Vogelhochzeit). Und: „Lieber den Spatz in der Hand als die Taube auf dem Dach.“",
 kid=["Tschilp, tschilp!","Die Spatzen schwatzen in der Hecke."], dawn=15, alias=["Spatz"])

bird("feldsperling","Feldsperling","Passer montanus","Sperlinge",["feld","garten"],2,"1-12","2-7",["kraechz"],
 "Heller als der Spatz: „tschett-tettet“.",
 "Ähnlich dem Haussperling, aber heller und rhythmischer.",
 "„Tschett“, „tettet“, im Flug ein hartes „tek“.",
 "Der Spatz vom Land – mit schwarzem Wangenfleck.",
 ["haussperling"],
 "Dorfränder, Kleingärten, Streuobstwiesen, Feldgehölze.",
 "Männchen und Weibchen sehen gleich aus: brauner Scheitel, schwarzer Wangenfleck.")

# ============================================================ Stare & Rabenvögel
bird("star","Star","Sturnus vulgaris","Stare",["garten","feld"],1,"2-11","2-6,9-10",["zwitscher","kraechz"],
 "Pfeifen, Schnalzen, Knarren – und Imitationen von allem Möglichen.",
 "Ein buntes Durcheinander aus Pfiffen, Klicken und Knarren, dazu nachgeahmte Laute anderer Vögel und des Alltags. Typisch ein abfallender Pfiff „wiuuu“. Singt mit flatternden Flügeln.",
 "Raues „rrää“, im Flug ein kurzes „tschurr“.",
 "Das Mixtape der Vogelwelt.",
 ["pirol","maeusebussard"],
 "Parkwiesen, Gärten, Weiden, Obstplantagen; im Herbst riesige Schwärme an Schlafplätzen.",
 "Einzelne Stare imitieren Handyklingeltöne oder Autoalarmanlagen. Vogel des Jahres 2018.",
 kultur="Mozart kaufte 1784 einen Star, der ein Thema aus seinem Klavierkonzert G-Dur pfiff – Mozart notierte die Melodie in sein Ausgabenbuch. Und natürlich: „Amsel, Drossel, Fink und Star“.",
 dawn=20)

bird("elster","Elster","Pica pica","Rabenvögel",["garten"],1,"1-12","1-12",["kraechz"],
 "Ratterndes „schak-schak-schak“ wie ein Maschinengewehr.",
 "Leises, plauderndes Schwatzen, selten wahrgenommen.",
 "Laut ratterndes „Schäckern“ – besonders bei Katzen, Greifvögeln oder Eulen.",
 "Die Klapper der Nachbarschaft.",
 ["wacholderdrossel","eichelhaeher"],
 "Wohnviertel, Parks, Gärten, Feldgehölze.",
 "Eines der wenigen Nicht-Säugetiere, die im Spiegeltest Hinweise auf Selbsterkennen zeigten.",
 kultur="Rossinis Oper „Die diebische Elster“ machte sie zur Diebin – ein Mythos: In Versuchen mieden Elstern glänzende Gegenstände eher.",
 kid=["Schak-schak-schak!","Die Elster schimpft laut."])

bird("eichelhaeher","Eichelhäher","Garrulus glandarius","Rabenvögel",["wald","garten"],2,"1-12","1-12",["kraechz"],
 "Heiseres, kreischendes „rätsch“ – der Alarm des Waldes.",
 "Leises, vielseitiges Schwatzen mit Imitationen.",
 "Lautes, reißendes „rätsch“. Imitiert täuschend echt den Mäusebussard.",
 "„Rätsch!“ – jemand reißt ein Tuch entzwei.",
 ["maeusebussard","elster","tannenhaeher"],
 "Wälder, Parks mit Eichen, große Gärten.",
 "Im Herbst versteckt ein Häher tausende Eicheln – vergessene keimen. So pflanzt er ganze Eichenwälder.",
 kultur="Im Volksmund die „Polizei des Waldes“: Sein Warnruf verrät jeden Fuchs und jeden Spaziergänger.")

bird("tannenhaeher","Tannenhäher","Nucifraga caryocatactes","Rabenvögel",["berge","wald"],3,"1-12","1-12",["kraechz"],
 "Raues, schnarrendes „rrrää“ aus Zirben- und Fichtenwäldern.",
 "Leises Schwatzen, selten gehört.",
 "Heiseres, gedehntes „krrrä“, oft mehrfach gereiht.",
 "Der Eichelhäher der Berge – mit Sommersprossen.",
 ["eichelhaeher","kolkrabe"],
 "Bergwälder der Alpen mit Zirbe und Hasel; Fichtenwälder der Mittelgebirge.",
 "Versteckt im Herbst zehntausende Zirbennüsse und findet einen Großteil davon selbst unter Schnee wieder – der wichtigste „Förster“ der Zirbe.",
 reg="Alpen & Mittelgebirge", alias=["Zirbengratsch"])

bird("rabenkraehe","Rabenkrähe","Corvus corone","Rabenvögel",["garten","feld"],1,"1-12","1-12",["kraechz"],
 "Raues, hartes „krah-krah-krah“.",
 "Kein Gesang im engeren Sinn; selten leises Gemurmel.",
 "Lautes, heiseres „krah“, meist drei- bis viermal gereiht.",
 "Das Krächzen über jeder großen Wiese.",
 ["saatkraehe","kolkrabe","dohle"],
 "Überall, besonders auf Wiesen, Feldern und Plätzen. Im Osten Deutschlands und Österreichs lebt die grau-schwarze Nebelkrähe – gleiche Stimme.",
 "Krähen erkennen einzelne Menschen wieder und merken sich jahrelang, wer ihnen schadet.",
 kultur="„Eine Krähe hackt der anderen kein Auge aus.“",
 kid=["Krah, krah!","Die Krähe ruft „Krah“."], alias=["Krähe","Nebelkrähe"])

bird("saatkraehe","Saatkrähe","Corvus frugilegus","Rabenvögel",["feld","garten"],2,"1-12","1-12",["kraechz"],
 "Tieferes, weicheres „gaah“ – oft hundertfach aus einer Kolonie.",
 "Kein Gesang; in Kolonien ein dauerndes Stimmengewirr.",
 "Nasales „gaah“ oder „korr“.",
 "Die Krähe mit der hellen Gesichtsmaske – und dem Chor.",
 ["rabenkraehe","dohle"],
 "Brütet in Kolonien in Stadtparks und Alleen; im Winter riesige Trupps aus Osteuropa auf Feldern und an Schlafplätzen.",
 "Erkennbar am nackten, hellgrauen Schnabelgrund. Winterliche Schlafplätze können zehntausende Vögel umfassen.")

bird("kolkrabe","Kolkrabe","Corvus corax","Rabenvögel",["berge","wald","feld"],3,"1-12","1-12",["kraechz","tief"],
 "Tiefes, sonores „korrk“ – und klonkende Glockentöne.",
 "Leises, vielseitiges Plaudern mit Klick- und Glockenlauten.",
 "Weit hörbares, tiefes „korrk“ oder „krok“.",
 "Wenn die Krähe im Keller ruft, ist es ein Rabe.",
 ["rabenkraehe","saatkraehe"],
 "Alpen, Mittelgebirge und zunehmend auch das Flachland.",
 "Der größte Singvogel der Welt, mit über einem Meter Spannweite. Raben spielen – etwa, indem sie Schneehänge hinabrutschen.",
 kultur="Odins Raben Hugin und Munin bringen ihm die Nachrichten der Welt. Grimms „Die sieben Raben“, Wilhelm Buschs „Hans Huckebein, der Unglücksrabe“, Abraxas, der sprechende Rabe der „kleinen Hexe“ (Otfried Preußler), und der kleine Rabe Socke aus den Kinderbüchern.",
 kid=["Korr, korr!","Der Rabe ist groß, schwarz und sehr schlau."], alias=["Rabe"])

bird("dohle","Dohle","Coloeus monedula","Rabenvögel",["garten","feld","berge"],2,"1-12","1-12",["kraechz","name"],
 "Helles, kurzes „kjack“ – fröhlicher als jede Krähe.",
 "Kein Gesang im engeren Sinn.",
 "Kurzes, helles „kjack“ oder „tschjak“, oft im Chor aus fliegenden Trupps.",
 "Die kleine Krähe mit den hellen Augen und der hellen Stimme.",
 ["rabenkraehe","saatkraehe","alpendohle"],
 "Kirchtürme, Altbauten, Burgen, Felswände, alte Parks.",
 "Dohlen leben in lebenslanger Partnerschaft – Paare fliegen dicht nebeneinander.",
 kultur="Konrad Lorenz beobachtete jahrelang zahme Dohlen und beschrieb ihre Rangordnung in „Er redete mit dem Vieh, den Vögeln und den Fischen“.")

bird("alpendohle","Alpendohle","Pyrrhocorax graculus","Rabenvögel",["berge"],2,"1-12","1-12",["schrill"],
 "Rollende, schrille Pfiffe „zirrr“ über Gipfeln.",
 "Kein Gesang im engeren Sinn.",
 "Hohe, rollende, fast trillernde „zirr“- und „srieh“-Rufe.",
 "Der Gipfelbegleiter mit dem gelben Schnabel.",
 ["dohle"],
 "Hochgebirge der Alpen: Felswände, Gipfelstationen, Hütten; im Winter auch in Tälern und Skigebieten.",
 "Akrobatische Flieger, die in Aufwinden segeln – und sich gern Brotkrumen von Wanderern holen.",
 reg="Alpen")

# ============================================================ Tauben & Kuckuck
bird("ringeltaube","Ringeltaube","Columba palumbus","Tauben",["garten","wald"],1,"1-12","3-9",["tief","motiv"],
 "Dumpfes, fünfsilbiges Gurren – betont auf der zweiten Silbe, endet abrupt.",
 "Tiefes Gurren in fünfsilbigen Strophen („gru-GRUUU-gru, gru-gru“), mehrmals wiederholt. Beim Balzflug klatschen die Flügel laut.",
 "Lautes Flügelklatschen beim Auffliegen.",
 "Fünf Silben = Ringeltaube, drei Silben = Türkentaube.",
 ["tuerkentaube","strassentaube","turteltaube"],
 "Überall – Wälder, Parks, Straßenbäume, Hausdächer.",
 "Größte heimische Taube; erkennbar am weißen Halsfleck.",
 kid=["Gru-gruuu-gru!","Die Taube gurrt im Baum."])

bird("tuerkentaube","Türkentaube","Streptopelia decaocto","Tauben",["garten"],1,"1-12","2-10",["tief","motiv"],
 "Dreisilbiges „gu-GUUU-gu“, endlos wiederholt.",
 "Hohles, dreisilbiges Gurren mit Betonung in der Mitte, monoton von Antennen und Dachkanten.",
 "Beim Landen ein nasales, gequetschtes „chwääh“.",
 "Drei Silben – die Taube auf der Antenne.",
 ["ringeltaube","turteltaube"],
 "Wohnviertel, Dörfer, Gärten, Dächer.",
 "Kam erst im 20. Jahrhundert vom Balkan nach Mitteleuropa – eine der spektakulärsten Ausbreitungen eines Vogels in Europa.")

bird("strassentaube","Straßentaube","Columba livia","Tauben",["garten"],1,"1-12","1-12",["tief"],
 "Rollendes, schwellendes „gurr-gu-guuh“ auf Plätzen und Simsen.",
 "Gurrende Balzstrophen, bei denen das Männchen sich aufplustert und im Kreis dreht.",
 "Leises Gurren; lautes Flügelklatschen beim Auffliegen.",
 "Der Klang jedes Bahnhofs.",
 ["ringeltaube","tuerkentaube"],
 "Städte: Bahnhöfe, Plätze, Brücken, Dachböden.",
 "Nachfahren verwilderter Haustauben, die von der Felsentaube abstammen. Brieftauben finden über hunderte Kilometer heim.",
 kultur="In Grimms „Aschenputtel“ helfen die Täubchen beim Linsenlesen und gurren: „Rucke di guh, rucke di guh, Blut ist im Schuh.“ Die Taube mit dem Ölzweig kehrt zu Noahs Arche zurück; Picassos Friedenstaube wurde weltberühmt.",
 kid=["Gurr, gurr!","Die Taube gurrt auf dem Platz."], alias=["Stadttaube","Taube"])

bird("turteltaube","Turteltaube","Streptopelia turtur","Tauben",["feld","wald"],4,"5-9","5-7",["tief","name"],
 "Sanftes, schnurrendes „turrr-turrr“ – daher der Name.",
 "Weiches, schnurrendes Gurren in Reihen, das fast wie ein Katzenschnurren klingt.",
 "Leises „turr“.",
 "Turrt wie verliebt.",
 ["tuerkentaube","ringeltaube"],
 "Halboffene Landschaften mit Feldgehölzen, Auwälder, warme Waldränder – heute selten geworden.",
 "Vogel des Jahres 2020. Die Bestände sind in Europa dramatisch eingebrochen – durch Lebensraumverlust und Jagd auf dem Zug.",
 kultur="„Turteltauben“ steht für verliebte Paare. Schon im Hohelied der Bibel heißt es: „Die Stimme der Turteltaube lässt sich hören in unserem Lande.“")

bird("kuckuck","Kuckuck","Cuculus canorus","Kuckucke",["wald","feld","wasser","berge"],2,"4-9","4-6",["name","tief"],
 "„Ku-kuck!“ – er ruft seinen eigenen Namen.",
 "Das Männchen ruft weithin hörbar „ku-kuck“, oft in langen Reihen. Das Weibchen antwortet mit einem kichernden, sprudelnden Triller.",
 "Das blubbernde „kwikwikwik“ des Weibchens; das Männchen auch heiser „chach-chach“.",
 "Lautmalerischer Name – und die Uhr ist nach ihm benannt.",
 ["tuerkentaube"],
 "Auen, Moore, Waldränder und Hecken, im Gebirge bis zur Baumgrenze.",
 "Brutparasit: Das Weibchen legt seine Eier in Nester von Teichrohrsänger, Bachstelze, Rotkehlchen und anderen. Der junge Kuckuck wirft die Eier seiner Pflegeeltern aus dem Nest.",
 kultur="„Kuckuck, Kuckuck, ruft's aus dem Wald“ und „Der Kuckuck und der Esel, die hatten einen Streit“ – beide Lieder textete Hoffmann von Fallersleben. Ein alter Brauch: Wer den ersten Kuckuck hört, soll mit dem Geld klimpern – dann geht es das ganze Jahr nicht aus. Die Kuckucksuhr kommt aus dem Schwarzwald.",
 kid=["Kuckuck! Kuckuck!","Der Kuckuck ruft seinen eigenen Namen."], dawn=50)

# ============================================================ Segler, Schwalben, Stelzen, Lerchen
bird("mauersegler","Mauersegler","Apus apus","Segler & Schwalben",["garten"],1,"5-8","5-8",["schrill"],
 "Schrilles „srieh-srieh“ – Gruppen jagen kreischend um die Dächer.",
 "Kein Gesang; die gemeinsamen Schreiflüge sind ihr Sommerlied.",
 "Hohes, schrilles „srieeh“, in Gruppen im rasanten Flug.",
 "Der Klang des Hochsommers über den Altbauten.",
 ["mehlschwalbe","rauchschwalbe"],
 "Altstädte und Altbauviertel, Kirchtürme, hohe Gebäude mit Nischen.",
 "Verbringt außerhalb der Brutzeit bis zu zehn Monate ununterbrochen in der Luft – er schläft und frisst im Flug.",
 kid=["Srieh, srieh!","Der Mauersegler fliegt schreiend ums Haus."])

bird("mehlschwalbe","Mehlschwalbe","Delichon urbicum","Segler & Schwalben",["garten"],2,"4-9","4-8",["zwitscher"],
 "Weiches, trockenes „prrit“ unter der Dachtraufe.",
 "Leises, zwitscherndes Plaudern aus Rufen.",
 "Kurzes, trockenes „prrit“ oder „trr“.",
 "Die Schwalbe mit der weißen Unterhose.",
 ["rauchschwalbe","mauersegler"],
 "Dörfer und Städte: Kugelnester aus Lehm außen unter Dachvorsprüngen, oft in Kolonien.",
 "Ein Nest besteht aus über tausend Lehmklümpchen, die das Paar im Schnabel heranträgt. Unverkennbar: der leuchtend weiße Bürzel.")

bird("rauchschwalbe","Rauchschwalbe","Hirundo rustica","Segler & Schwalben",["feld","garten"],2,"4-9","4-8",["zwitscher"],
 "Lebhaftes Zwitschern mit eingebautem schnarrendem „zerrr“.",
 "Plapperndes, zwitscherndes Geplauder mit einem eingeschobenen, schnarrenden Triller.",
 "„Witt-witt“; Warnruf scharfes „flitt“.",
 "Plaudert im Kuhstall.",
 ["mehlschwalbe","mauersegler"],
 "Bauernhöfe und Ställe (Nest innen), jagt über Wiesen und Gewässern.",
 "Lange Schwanzspieße; überwintert bis ins südliche Afrika.",
 kultur="„Eine Schwalbe macht noch keinen Sommer“ geht auf Aristoteles zurück. In Andersens „Däumelinchen“ trägt eine Schwalbe das kleine Mädchen in den warmen Süden.",
 kid=["Witt-witt!","Die Schwalbe wohnt im Stall und fliegt im Winter bis nach Afrika."])

bird("bachstelze","Bachstelze","Motacilla alba","Stelzen & Lerchen",["garten","wasser","feld","berge"],1,"3-11","3-7",["schrill","zwitscher"],
 "Helles, zweisilbiges „zi-litt“ – im wellenförmigen Flug.",
 "Zwitschernde Reihen aus Rufen, eher unauffällig.",
 "Klares „zi-litt“ oder „zwitt“.",
 "Wippt mit dem Schwanz – und ruft „zi-litt“ beim Abheben.",
 ["gebirgsstelze"],
 "Offene Landschaft, besonders am Wasser, auf Höfen, Parkplätzen und Dächern – bis ins Hochgebirge.",
 "Der ständig wippende Schwanz hat ihr regional Namen wie „Wippsterz“ eingebracht.",
 alias=["Wippsterz"])

bird("gebirgsstelze","Gebirgsstelze","Motacilla cinerea","Stelzen & Lerchen",["wasser","berge"],2,"1-12","3-6",["schrill"],
 "Scharfes, metallisches „zississ“ über rauschendem Wasser.",
 "Kurze, hohe Strophen aus Rufen und Trillern.",
 "Hohes, metallisches „zit-zit“ – schärfer als bei der Bachstelze.",
 "Gelber Bauch, grauer Rücken, immer am Wildwasser.",
 ["bachstelze","wasseramsel"],
 "Schnell fließende Bäche und Flüsse, Wehre und Mühlen – auch mitten in Städten.",
 "Trotz des Namens nicht nur im Gebirge, sondern an fast jedem schnellen Bach.")

bird("feldlerche","Feldlerche","Alauda arvensis","Stelzen & Lerchen",["feld","berge"],2,"2-10","2-7",["zwitscher"],
 "Minutenlanger, jubilierender Triller hoch oben am Himmel.",
 "Ein endloser, trillernder, sprudelnder Fluss, vorgetragen im Singflug: Die Lerche steigt steil auf, „steht“ am Himmel und singt minutenlang.",
 "„Trlit“ oder „prrit“.",
 "Der Punkt am Himmel, der singt.",
 ["stieglitz"],
 "Äcker, Wiesen, Heiden, Almen.",
 "Durch die intensive Landwirtschaft stark zurückgegangen. Vogel des Jahres 1998 und 2019.",
 kultur="„Die Lerche, die Lerche, die führt die Braut zur Kerche“ (Vogelhochzeit). Bei Shakespeare ist sie die Botin des Morgens – darum heißen Frühaufsteher „Lerchen“.",
 kid=["Tirili-tirili!","Die Lerche singt hoch oben am Himmel."], dawn=90)

# ============================================================ Laubsänger & Grasmücken & Rohrsänger
bird("zilpzalp","Zilpzalp","Phylloscopus collybita","Laubsänger & Grasmücken",["wald","garten"],1,"3-10","3-9",["name","motiv"],
 "Er sagt seinen Namen: „zilp-zalp-zilp-zelp-zalp“.",
 "Unregelmäßige Folge zweier Tonhöhen, wie ein Pendel, das stolpert. Einer der ersten Rückkehrer im März.",
 "Weiches, fragendes „hüit“.",
 "Lautmalerischer Name – einfacher wird’s nicht.",
 ["fitis","kohlmeise"],
 "Wälder, Parks, Gärten, Auen – fast überall mit Bäumen und Gebüsch.",
 "Einzelne Zilpzalpe überwintern inzwischen in Mitteleuropa, statt ans Mittelmeer zu ziehen.",
 kid=["Zilp-zalp!","Der Zilpzalp ruft seinen Namen."])

bird("fitis","Fitis","Phylloscopus trochilus","Laubsänger & Grasmücken",["wald"],2,"4-9","4-7",["floete"],
 "Weiche, abfallende, wehmütige Strophe – wie ein kleiner Seufzer.",
 "Sanft beginnend, dann in weichen Tönen tonleiterartig absteigend und leise endend.",
 "Zweisilbiges „hu-iit“.",
 "Ein Buchfink, der traurig geworden ist.",
 ["zilpzalp","buchfink"],
 "Lichte Wälder, Birken, Moore, Gebüschland.",
 "Optisch fast identisch mit dem Zilpzalp – am Gesang aber sofort zu trennen. Zieht bis ins tropische Afrika.")

bird("moenchsgrasmuecke","Mönchsgrasmücke","Sylvia atricapilla","Laubsänger & Grasmücken",["wald","garten"],1,"3-10","4-7",["zwitscher","floete"],
 "Erst leises Plaudern, dann ein lauter, jubelnder Flöten-„Überschlag“.",
 "Beginnt mit schnellem, leisem Gezwitscher und bricht dann in klare, laute Flötentöne aus.",
 "Hartes „tack-tack“, wie zwei aneinandergeschlagene Kiesel.",
 "Erst murmeln, dann jubeln.",
 ["gartengrasmuecke","amsel","nachtigall"],
 "Hecken, Wälder mit Unterholz, Parks und Gärten.",
 "Ein Teil der mitteleuropäischen Population überwintert inzwischen auf den Britischen Inseln statt im Mittelmeerraum – Evolution im Zeitraffer.")

bird("gartengrasmuecke","Gartengrasmücke","Sylvia borin","Laubsänger & Grasmücken",["wald","garten"],3,"5-9","5-7",["zwitscher"],
 "Langes, gleichmäßig plätscherndes „Orgeln“ ohne Höhepunkt.",
 "Tiefe, gleichmäßig dahinplätschernde Strophen, oft über zehn Sekunden lang – ohne den Überschlag der Mönchsgrasmücke.",
 "„Tschek-tschek“.",
 "Ihr Merkmal ist, dass sie keine Merkmale hat.",
 ["moenchsgrasmuecke"],
 "Gebüschreiche Waldränder, Auen, verwilderte Gärten.",
 "Gilt als der unscheinbarste Vogel Europas – graubraun ohne jede Zeichnung.")

bird("teichrohrsaenger","Teichrohrsänger","Acrocephalus scirpaceus","Rohrsänger",["wasser"],2,"5-9","5-7",["motiv","kraechz"],
 "Rhythmisches Knarren aus dem Schilf – wie eine Nähmaschine.",
 "Gleichmäßiges, rhythmisches Schwatzen: „tiri-tiri-tiri tschä-tschä-tschä zerr-zerr“, jede Silbe zwei- bis dreimal.",
 "„Tsch“ und schnarrendes „krrr“.",
 "Die Nähmaschine im Röhricht.",
 ["drosselrohrsaenger"],
 "Schilfgürtel an Seen, Teichen und Gräben.",
 "Einer der häufigsten Wirte des Kuckucks.")

bird("drosselrohrsaenger","Drosselrohrsänger","Acrocephalus arundinaceus","Rohrsänger",["wasser"],4,"5-8","5-7",["kraechz","motiv"],
 "Lautes, knarrendes „karre-karre-kiet-kiet“ – Froschkonzert mit Flügeln.",
 "Sehr laut, rau und knarrend, mit quietschenden Einlagen.",
 "Raues „krrr“.",
 "Klingt wie ein Frosch, ist aber ein Vogel.",
 ["teichrohrsaenger"],
 "Große Schilfgebiete an Seen, z. B. am Neusiedler See und Bodensee.",
 "Der größte Rohrsänger Europas – fast drosselgroß, daher der Name.")

# ============================================================ Baumkletterer & Spechte
bird("kleiber","Kleiber","Sitta europaea","Baumkletterer",["wald","garten"],2,"1-12","1-6,9-12",["motiv","floete"],
 "Laute, klare Pfiffe „wi-wi-wi-wi“ – als ob jemand seinen Hund ruft.",
 "Reihen lauter Pfiffe, mal schnell trillernd, mal langsam „tüi – tüi – tüi“.",
 "Kräftiges „twit-twit“ oder „sit“.",
 "Pfeift wie ein Hundehalter im Park.",
 ["kohlmeise","gimpel"],
 "Alte Laubbäume in Wäldern, Parks und Gärten.",
 "Klettert als einziger heimischer Vogel kopfüber den Stamm hinab – und verkleinert den Eingang seiner Bruthöhle mit Lehm.")

bird("gartenbaumlaeufer","Gartenbaumläufer","Certhia brachydactyla","Baumkletterer",["wald","garten"],2,"1-12","2-6",["motiv","schrill"],
 "Kurze, rhythmische Strophe: „tüt-tüt-teroi-tit“.",
 "Hohe, kurze Strophe mit festem Muster, mehrmals pro Minute.",
 "Hohes, durchdringendes „tiit“.",
 "Ein kleiner Morsecode am Baumstamm.",
 ["wintergoldhaehnchen","kleiber"],
 "Parks, Alleen, Friedhöfe, Laubwälder. Sein Zwilling, der Waldbaumläufer, lebt eher im Nadelwald und singt einen abfallenden Triller.",
 "Klettert spiralig den Stamm hinauf, fliegt zum Fuß des nächsten Baums und beginnt von vorn.")

bird("buntspecht","Buntspecht","Dendrocopos major","Spechte",["wald","garten"],1,"1-12","1-5",["trommel","schrill"],
 "Kurzer, schneller Trommelwirbel – und ein hartes „kick“.",
 "Statt Gesang: Trommeln. Ein sehr kurzer, schneller Wirbel (unter einer Sekunde), der abrupt endet.",
 "Hartes, einzelnes „kick“ – das ganze Jahr.",
 "Kurzes Trommeln, hartes „kick“.",
 ["schwarzspecht","gruenspecht"],
 "Jeder Wald und Park mit alten Bäumen, Futterhäuser im Winter.",
 "Trommeln ist Revieranzeige, keine Futtersuche – gern auf hohlen Ästen oder sogar Blechdächern.",
 kid=["Tock-tock-trrrr!","Der Specht klopft an den Baum."], alias=["Specht"])

bird("gruenspecht","Grünspecht","Picus viridis","Spechte",["garten","wald","feld"],2,"1-12","2-6",["lach"],
 "Lautes Lachen: „klü-klü-klü-klü-klü“.",
 "Lauter, gleichmäßiger, leicht abfallender Ruf, der wie Gelächter klingt. Trommelt selten.",
 "Im Flug ein scharfes „kjück“.",
 "Der lachende Specht auf der Parkwiese.",
 ["schwarzspecht","buntspecht"],
 "Parks, Streuobstwiesen, Friedhöfe, Waldränder mit Wiesen.",
 "Sucht seine Nahrung am Boden – vor allem Ameisen, die er mit einer sehr langen, klebrigen Zunge aus dem Nest holt.",
 kid=["Klü-klü-klü!","Der grüne Specht lacht."])

bird("schwarzspecht","Schwarzspecht","Dryocopus martius","Spechte",["wald","berge"],3,"1-12","2-5",["lach","trommel","schrill"],
 "Im Flug „krrü-krrü-krrü“, im Sitzen ein klagendes „kliööh“.",
 "Laute „kwi-kwi-kwi“-Reihen; trommelt laut und lang (zwei bis drei Sekunden).",
 "Klagendes, gedehntes „kliöh“ – weit hörbar.",
 "Ein krähengroßer Specht mit roter Kappe und dem lautesten Trommelwirbel.",
 ["gruenspecht","buntspecht"],
 "Alte Buchen- und Nadelwälder bis in die Bergwälder.",
 "Europas größter Specht. Seine Höhlen ziehen später Hohltauben, Käuze, Dohlen und Fledermäuse ein – der Baumeister des Waldes.")

# ============================================================ Feldvögel & Hühnervögel
bird("kiebitz","Kiebitz","Vanellus vanellus","Watvögel & Möwen",["feld","wasser"],3,"2-10","3-5",["name","schrill"],
 "„Kiu-witt!“ – und wummernde Flügel im Gaukelflug.",
 "Balzflug mit wilden Sturzflügen, wummernden Flügelschlägen und dem gequetschten Ruf.",
 "Gequetschtes „kiu-witt“ oder „chä-witt“ – daher der Name.",
 "Ruft seinen Namen und fliegt dabei Purzelbäume.",
 ["austernfischer"],
 "Feuchte Wiesen, Äcker, Moore.",
 "Einst überall häufig, heute stark gefährdet. Vogel des Jahres 1996 und 2024.",
 kultur="Wer beim Kartenspiel zuschaut und mitredet, „kiebitzt“ – wie der neugierige Vogel, der alles laut kommentiert.",
 kid=["Kiwitt!","Der Kiebitz ruft seinen Namen."])

bird("rebhuhn","Rebhuhn","Perdix perdix","Hühnervögel",["feld"],4,"1-12","2-5",["kraechz"],
 "Rostiges, kratzendes „kirr-ek“ in der Abenddämmerung.",
 "Der Ruf des Hahns ist sein Gesang: ein kratzendes „girrhäk“.",
 "Beim Auffliegen schnurrende Flügel und „pitt-pitt-pitt“.",
 "Ein rostiges Tor auf dem Acker.",
 ["fasan","wachtel"],
 "Felder mit Hecken, Brachen und Feldrainen.",
 "Stark gefährdet. Im Herbst leben Familien als „Ketten“ zusammen.")

bird("wachtel","Wachtel","Coturnix coturnix","Hühnervögel",["feld"],3,"5-9","5-7",["motiv"],
 "Dreisilbiges „pick-wer-wick“ aus dem Getreide, oft nachts.",
 "Der „Wachtelschlag“: ein dreisilbiges, hartes „pick-wer-wick“, mehrmals wiederholt.",
 "Leises „wrüä“ des Weibchens.",
 "„Bück den Rück!“ – man hört sie, sieht sie aber nie.",
 ["rebhuhn"],
 "Getreidefelder und Wiesen in offener Landschaft.",
 "Der einzige echte Zugvogel unter den Hühnervögeln Europas – sie fliegt bis nach Afrika.",
 night=True)

bird("fasan","Fasan","Phasianus colchicus","Hühnervögel",["feld"],2,"1-12","3-6",["kraechz"],
 "Lautes, zweisilbiges „gö-gock!“ mit anschließendem Flügelschwirren.",
 "Der Hahn ruft ein heiseres „gö-gock“ und schlägt danach rasselnd mit den Flügeln.",
 "Beim Auffliegen ein lautes „kotok-kotok-kotok“.",
 "Ein Wecker mit Federschwanz.",
 ["rebhuhn","pfau","haushuhn"],
 "Feldflur mit Hecken, Schilf und Waldrändern.",
 "Stammt aus Asien und wurde schon von den Römern eingeführt; die heutigen Bestände gehen vor allem auf Aussetzungen zurück.")

bird("haushuhn","Haushuhn","Gallus gallus domesticus","Hühnervögel",["garten","feld"],1,"1-12","1-12",["kraechz"],
 "„Kikeriki!“ – der Hahn. „Gock-gock-gock-gooock“ – die Henne.",
 "Der Hahn kräht, besonders frühmorgens, aber auch tagsüber.",
 "Hennen gackern laut nach dem Eierlegen und glucken leise mit den Küken.",
 "Der älteste Wecker der Welt.",
 ["fasan","pfau"],
 "Bauernhöfe, Gärten, Kinderbauernhöfe.",
 "Alle Haushühner stammen vom Bankivahuhn aus Südostasien ab. Hähne krähen nach einer inneren Uhr – auch ohne Sonnenaufgang.",
 kultur="In den „Bremer Stadtmusikanten“ kräht der Hahn mit. In „Frau Holle“ ruft er: „Kikeriki, unsere goldene Jungfrau ist wieder hie!“ Max und Moritz stibitzen die Hühner der Witwe Bolte, und bei Pettersson und Findus wohnen sie im Hühnerhaus.",
 kid=["Kikeriki!","Der Hahn kräht am Morgen."], alias=["Hahn","Huhn","Henne"])

bird("auerhuhn","Auerhuhn","Tetrao urogallus","Hühnervögel",["berge","wald"],4,"1-12","3-5",["tief","trommel"],
 "Klicken, ein Korkenknall und leises Wetzen – die Balz im Morgengrauen.",
 "Der Hahn balzt mit einer seltsamen Abfolge: „Knappen“ (Klicklaute), ein Triller, der „Hauptschlag“ (wie ein Korkenknall) und das „Schleifen“ (wie Messerwetzen).",
 "Henne: gackerndes „gock-gock“.",
 "Ein Sektkorken im Bergwald.",
 ["fasan"],
 "Lichte, alte Bergwälder der Alpen, des Schwarzwalds und des Bayerischen Waldes.",
 "Größter Hühnervogel Europas. Jäger erzählten, der Hahn sei beim „Schleifen“ für einen Moment taub.",
 kultur="„Der Auerhahn, der Auerhahn, der war der würd'ge Herr Kaplan“ (Vogelhochzeit).",
 reg="Alpen & Mittelgebirge", alias=["Auerhahn"])

bird("alpenschneehuhn","Alpenschneehuhn","Lagopus muta","Hühnervögel",["berge"],4,"1-12","3-6",["kraechz"],
 "Schnarrendes, knarrendes „arrr-ka-ka“ über Geröllhalden.",
 "Der Hahn balzt mit knarrenden Rufen im Singflug.",
 "Tiefes, schnarrendes „gerrr“.",
 "Im Sommer ein Stein, im Winter ein Schneeball.",
 ["auerhuhn"],
 "Alpen oberhalb der Baumgrenze.",
 "Wechselt das Gefieder: im Sommer graubraun, im Winter schneeweiß. Befiederte Füße dienen als Schneeschuhe, bei Sturm gräbt es sich in den Schnee.",
 reg="Alpen")

# ============================================================ Störche, Reiher, Kraniche
bird("weissstorch","Weißstorch","Ciconia ciconia","Störche & Reiher",["feld","wasser"],3,"2-9","3-6",["trommel"],
 "Hölzernes Schnabelklappern vom Kirchturm.",
 "Fast stumm. Statt zu singen, klappern die Partner mit dem Schnabel, den Kopf weit in den Nacken gelegt.",
 "Junge Störche betteln mit miauenden Lauten.",
 "Der Vogel, der klappert statt singt.",
 ["kranich","graureiher"],
 "Dörfer mit Nestern auf Kirchtürmen, Masten und Schornsteinen; Feuchtwiesen und Flussauen. Hochburgen sind Elbtal, Oberrhein, Bodensee und das Burgenland.",
 "Die Bestände erholen sich. Viele Störche überwintern inzwischen in Spanien statt in Afrika.",
 kultur="Der Klapperstorch bringt die Babys. Wilhelm Hauffs Märchen „Kalif Storch“ erzählt von einem Kalifen, der sich in einen Storch verwandelt und das Zauberwort „Mutabor“ vergisst.",
 kid=["Klapper-klapper!","Der Storch klappert mit dem Schnabel."], alias=["Storch","Klapperstorch"])

bird("graureiher","Graureiher","Ardea cinerea","Störche & Reiher",["wasser","feld"],2,"1-12","1-12",["kraechz"],
 "Heiseres, raues „kräik“ im Flug.",
 "Kein Gesang; in Kolonien lautes Schnabelklappern und Krächzen.",
 "Rau, heiser und laut: „kräik“ oder „chräik“.",
 "Ein Pterodaktylus mit Halsweh.",
 ["weissstorch","kranich"],
 "Flüsse, Seen, Teiche, Wiesen (Mäusejagd) und Stadtparks.",
 "Steht minutenlang reglos im Wasser – und frisst auch viele Mäuse auf Wiesen.",
 alias=["Fischreiher"])

bird("kranich","Kranich","Grus grus","Kraniche",["feld","wasser"],3,"2-11","3-5,9-11",["tief","wasser"],
 "Lautes, trompetendes „krruuu“ von Keilformationen am Himmel.",
 "Paare rufen im Duett, weit hörbar und tief trompetend.",
 "Trompetendes „krru“ oder „grüi“, auf dem Zug unablässig.",
 "Trompeten am Herbsthimmel – der Zug ist da.",
 ["graugans","graureiher"],
 "Brütet in Mooren und Bruchwäldern Nord- und Ostdeutschlands. Im Herbst rasten zehntausende etwa im Havelland, an der Ostsee und im Diepholzer Moor; der Zug führt über ganz Deutschland.",
 "Im Oktober und November ziehen große Kranich-Keile über Deutschland, oft auch nachts hörbar.",
 kultur="Schillers Ballade „Die Kraniche des Ibykus“: Ein Kranichschwarm verrät die Mörder eines Dichters. In Japan gilt der Kranich als Glücksvogel – tausend gefaltete Papierkraniche sollen einen Wunsch erfüllen.",
 kid=["Krruu, krruu!","Die Kraniche fliegen wie ein großes V."])

# ============================================================ Wasservögel
bird("hoeckerschwan","Höckerschwan","Cygnus olor","Entenvögel",["wasser"],1,"1-12","1-12",["wasser"],
 "Meist still – doch seine Flügel singen: „wium-wium-wium“.",
 "Kein Gesang. Im Flug erzeugen die Schwingen ein weithin hörbares, rhythmisches Singen.",
 "Zischen und Schnauben bei Bedrohung.",
 "Der Vogel, dessen Musik aus den Flügeln kommt.",
 ["graugans"],
 "Seen, Flüsse, Stadtgewässer.",
 "Mit über zehn Kilogramm einer der schwersten flugfähigen Vögel. Paare bleiben oft ein Leben lang zusammen.",
 kultur="Andersens „Das hässliche Entlein“ wird zum schönsten Schwan. Grimms „Die sechs Schwäne“, Wagners „Lohengrin“ mit dem Schwanenritter und Tschaikowskys „Schwanensee“.",
 kid=["Wium-wium-wium!","Der Schwan ist still, aber seine Flügel singen."], alias=["Schwan"])

bird("graugans","Graugans","Anser anser","Entenvögel",["wasser","feld"],2,"1-12","1-12",["wasser","kraechz"],
 "Lautes Trompeten und Schnattern: „ga-ga-ga“.",
 "Kein Gesang; Familien und Trupps sind ständig im lauten Gespräch.",
 "Laute, nasale „gang-gang-gang“-Rufe und Schnattern; Zischen bei Gefahr.",
 "Das Original der Hausgans.",
 ["nilgans","kranich","hoeckerschwan"],
 "Seen, Feuchtgebiete und Stadtparks, im Winter auf Feldern.",
 "Stammform der Hausgans. Konrad Lorenz zog Gänseküken auf, die ihn für ihre Mutter hielten – berühmt wurde die Gans Martina.",
 kultur="Nils Holgersson reist auf dem Hausgänserich Martin mit den Wildgänsen – ihre Anführerin Akka von Kebnekaise ist eine Graugans. Dazu „Fuchs, du hast die Gans gestohlen“ und Grimms „Die Gänsemagd“.",
 kid=["Gak, gak, gak!","Die Gänse schnattern laut."], alias=["Gans","Wildgans","Hausgans"])

bird("nilgans","Nilgans","Alopochen aegyptiaca","Entenvögel",["wasser","garten"],2,"1-12","1-12",["wasser","kraechz"],
 "Heiseres Fauchen und lautes, gackerndes „hää-hää-hää“.",
 "Kein Gesang. Das Männchen faucht heiser, das Weibchen gackert laut – oft im Duett.",
 "Heisere Zisch- und Gackerlaute.",
 "Die Gans mit der Sonnenbrille.",
 ["graugans","stockente"],
 "Flüsse, Seen, Parkteiche, Freibäder – vor allem entlang des Rheins, zunehmend überall.",
 "Stammt aus Afrika, entkam aus Ziergeflügelhaltungen und breitet sich seit den 1980er-Jahren in Deutschland aus. Brütet sogar auf Bäumen und Gebäuden.")

bird("stockente","Stockente","Anas platyrhynchos","Entenvögel",["wasser"],1,"1-12","1-12",["wasser"],
 "Das klassische, absteigende „Quaak-quak-quak-quak“.",
 "Kein Gesang. Bei der Balz pfeifen und grunzen die Erpel leise.",
 "Weibchen: lautes, absteigendes „quaak-quak-quak“. Erpel: leises, gequetschtes „räb“.",
 "Laut quakt nur die Ente – der Erpel räbbelt.",
 ["nilgans","blaesshuhn"],
 "Jeder Fluss, Bach, See und Teich, auch mitten in der Stadt.",
 "Das berühmte laute Quaken stammt ausschließlich von den Weibchen.",
 kultur="„Alle meine Entchen schwimmen auf dem See.“ In Prokofjews „Peter und der Wolf“ spielt die Oboe die Ente.",
 kid=["Quak, quak!","Die Ente quakt auf dem Teich."], alias=["Ente","Wildente"])

bird("blaesshuhn","Blässhuhn","Fulica atra","Rallen",["wasser"],1,"1-12","1-12",["wasser","schrill"],
 "Kurzes, explosives „pix!“ oder „kött“ vom Wasser.",
 "Kein Gesang.",
 "Laute, kurze Rufe: „pix“, „pitz“, „kött“ – auch nachts.",
 "Ein Knall mit weißer Stirn.",
 ["teichhuhn","stockente"],
 "Seen, Teiche, langsame Flüsse, Parkgewässer.",
 "Die weiße Stirnplatte – die „Blässe“ – gibt ihm den Namen. Statt Schwimmhäuten hat es Lappen an den Zehen.")

bird("teichhuhn","Teichhuhn","Gallinula chloropus","Rallen",["wasser"],2,"1-12","3-8",["wasser","kraechz"],
 "Gurgelndes „kürrk“ aus dem Uferdickicht.",
 "Kein Gesang.",
 "Blubberndes „krrük“ und scharfes „kick“.",
 "Das Blässhuhn mit dem roten Schnabel.",
 ["blaesshuhn"],
 "Kleine, dicht bewachsene Teiche, Gräben, Parkweiher.",
 "Läuft mit seinen langen Zehen über Seerosenblätter und wippt dabei ständig mit dem Schwanz.")

bird("haubentaucher","Haubentaucher","Podiceps cristatus","Lappentaucher",["wasser"],2,"1-12","2-7",["kraechz","wasser"],
 "Raues, lautes „kroa-kroa“ über dem See.",
 "Kein Gesang; im Frühjahr laute, schnarrende Balzrufe.",
 "Rau „gräh“ und „kroa“; die Jungen betteln pfeifend.",
 "Der Punk mit der Halskrause.",
 ["blaesshuhn"],
 "Größere Seen und Stauseen.",
 "Berühmt für den Balztanz, bei dem sich die Partner mit Wasserpflanzen im Schnabel aufrichten. Die Küken reisen auf dem Rücken der Eltern.")

bird("eisvogel","Eisvogel","Alcedo atthis","Eisvögel",["wasser"],3,"1-12","3-6",["schrill"],
 "Scharfer, hoher Pfiff „tiiit“ – ein blauer Blitz über dem Wasser.",
 "Kein auffälliger Gesang.",
 "Durchdringendes, hohes „tiiet“ im pfeilschnellen Flug knapp über dem Wasser.",
 "Erst hört man ihn, dann sieht man einen blauen Strich.",
 ["gebirgsstelze"],
 "Klare Bäche, Flüsse und Seen mit Steilufern zum Brüten.",
 "Stoßtaucht nach kleinen Fischen. Seine Bruthöhle gräbt er bis zu einem Meter tief in Steilwände. Vogel des Jahres 1973 und 2009.",
 kultur="In der griechischen Sage wird Alkyone in einen Eisvogel verwandelt – davon stammen der lateinische Name „Alcedo“ und die „halkyonischen Tage“ der Windstille.",
 kid=["Tiiit!","Der blaue Eisvogel fängt Fische."])

bird("wasseramsel","Wasseramsel","Cinclus cinclus","Weitere Singvögel",["wasser","berge"],3,"1-12","1-5,10-12",["zwitscher"],
 "Zwitschernder, kratzender Gesang über Wildwasserrauschen – auch im Winter.",
 "Plätschernd, zwitschernd und kratzend; Männchen und Weibchen singen, sogar bei Frost.",
 "Scharfes „zrits“ im schnellen Flug über das Wasser.",
 "Der Vogel, der unter Wasser spazieren geht.",
 ["gebirgsstelze","zaunkoenig"],
 "Schnell fließende, klare Bäche und Flüsse im Bergland und in den Alpen.",
 "Der einzige Singvogel, der tauchen und am Bachgrund laufen kann.")

bird("lachmoewe","Lachmöwe","Chroicocephalus ridibundus","Watvögel & Möwen",["wasser","feld","kueste"],1,"1-12","1-12",["kraechz","schrill"],
 "Rau kreischendes „kriääh“ über Seen und Flüssen.",
 "Kein Gesang; in Kolonien ein lautes Kreischen.",
 "Rau und schnarrend: „kriää“, „kwärr“.",
 "Die Möwe, die man auch weit weg vom Meer trifft.",
 ["silbermoewe"],
 "Seen, Flüsse, Städte im Winter, frisch gepflügte Felder – und die Küsten.",
 "Im Sommer trägt sie eine schokoladenbraune (nicht schwarze) Kapuze, im Winter nur einen dunklen Ohrfleck. Der lateinische Name „ridibundus“ heißt „lachend“.",
 alias=["Möwe"])

bird("silbermoewe","Silbermöwe","Larus argentatus","Watvögel & Möwen",["kueste","wasser"],2,"1-12","1-12",["schrill","lach"],
 "„Kiau!“ – und das „Jauchzen“: eine lachende Rufreihe mit zurückgeworfenem Kopf.",
 "Das „Jauchzen“: Kopf nach hinten, dann eine laute, lachende Serie „kiau-kau-kau-kau“.",
 "Lautes „kiau“ und gackerndes „ga-ga-ga“.",
 "Der Klang der Nordsee.",
 ["lachmoewe","austernfischer"],
 "Nord- und Ostseeküste, Häfen, Inseln; im Winter auch an großen Seen.",
 "Der rote Fleck am Schnabel ist ein Signal: Die Küken picken darauf, damit die Eltern Futter hervorwürgen. Niko Tinbergen erforschte das und erhielt 1973 den Nobelpreis.",
 kid=["Kiau, kiau!","Die Möwe ruft am Meer."], reg="Küste")

bird("austernfischer","Austernfischer","Haematopus ostralegus","Watvögel & Möwen",["kueste","wasser"],3,"1-12","3-7",["schrill"],
 "Schrilles, lautes „kliep-kliep-kliep“ am Strand.",
 "Laute, trillernde Rufreihen, oft von mehreren Vögeln gleichzeitig.",
 "Gellendes „kliep“ oder „kwiep“.",
 "Schwarz-weiß, mit Möhrenschnabel – und laut.",
 ["silbermoewe","kiebitz"],
 "Wattenmeer, Strände und Salzwiesen an Nord- und Ostsee; zunehmend auch an Flüssen im Binnenland.",
 "Frisst kaum Austern, sondern Muscheln, Schnecken und Würmer, die er mit dem Schnabel aufhebelt.",
 reg="Küste")

bird("kormoran","Kormoran","Phalacrocorax carbo","Weitere Wasservögel",["wasser","kueste"],2,"1-12","2-6",["tief","kraechz"],
 "Tiefe, kehlige „ko-ko-ko“-Laute aus Brutkolonien.",
 "Kein Gesang.",
 "Tief und gutural „chrro“; abseits der Kolonien meist stumm.",
 "Der Vogel, der seine Flügel zum Trocknen aufhängt.",
 ["haubentaucher","graureiher"],
 "Seen, Flüsse, Küsten; Kolonien in Bäumen.",
 "Sein Gefieder ist nicht ganz wasserdicht – darum sitzt er nach dem Tauchen mit ausgebreiteten Flügeln da.")

bird("rohrdommel","Rohrdommel","Botaurus stellaris","Störche & Reiher",["wasser"],4,"1-12","3-6",["tief"],
 "Tiefes, nebelhornartiges „uh-prumb“ – kilometerweit hörbar.",
 "Das Männchen „brüllt“: nach einigen Einatemlauten ein dumpfes, tiefes „uh-prumb“, oft nachts.",
 "Im Flug ein heiseres „kau“.",
 "Wenn nachts ein Ochse im Schilf brüllt.",
 ["kormoran"],
 "Große, nasse Schilfgebiete.",
 "Bei Gefahr erstarrt sie in der „Pfahlstellung“: Schnabel senkrecht nach oben, perfekt getarnt im Schilf.",
 kultur="Alte Namen wie „Moorochse“ oder „Mooskuh“ kommen von ihrem Ruf. In Moorsagen hielt man ihn für einen Geist.",
 night=True, alias=["Moorochse"])

# ============================================================ Greifvögel
bird("maeusebussard","Mäusebussard","Buteo buteo","Greifvögel",["feld","wald"],1,"1-12","2-6",["schrill"],
 "Miauendes „hiääh“ aus großer Höhe.",
 "Kein Gesang; im Frühjahr ruft er bei den Balzflügen besonders oft.",
 "Gedehntes, katzenartiges „hiääh“, oft im kreisenden Segelflug.",
 "Die Katze am Himmel.",
 ["eichelhaeher","rotmilan","steinadler"],
 "Feldflur mit Waldstücken, Autobahnränder, Stadtränder – sitzt gern auf Pfählen.",
 "Der häufigste Greifvogel Mitteleuropas.",
 kid=["Hiääh!","Der Bussard kreist am Himmel und miaut."], alias=["Bussard"])

bird("rotmilan","Rotmilan","Milvus milvus","Greifvögel",["feld"],3,"2-11","2-6",["schrill"],
 "Hohes, wieherndes „hiiä-hiä-hiä“ über offener Landschaft.",
 "Kein Gesang.",
 "Trillernd-wiehernde Rufreihen.",
 "Der Greifvogel mit dem Schwalbenschwanz.",
 ["maeusebussard"],
 "Offene Agrarlandschaft mit Wäldchen, besonders in der Mitte Deutschlands.",
 "Mehr als die Hälfte aller Rotmilane weltweit brütet in Deutschland – eine besondere Verantwortung.",
 alias=["Gabelweihe"])

bird("sperber","Sperber","Accipiter nisus","Greifvögel",["wald","garten"],2,"1-12","3-6",["schrill"],
 "Schnelles, keckerndes „kjekjekje“ am Horst – sonst stumm.",
 "Kein Gesang.",
 "Hohes, schnelles „kekeke“.",
 "Ein Schatten am Futterhaus.",
 ["turmfalke"],
 "Wälder, Parks und Gärten – jagt Kleinvögel im Überraschungsangriff.",
 "Die Weibchen sind fast doppelt so schwer wie die Männchen.")

bird("turmfalke","Turmfalke","Falco tinnunculus","Greifvögel",["feld","garten"],2,"1-12","3-7",["schrill"],
 "Schrilles „kikikiki“ von Kirchtürmen.",
 "Kein Gesang.",
 "Hohes, gellendes „kikikiki“.",
 "Der Falke, der in der Luft stehen kann.",
 ["sperber","wanderfalke"],
 "Kirchtürme, Hochhäuser, Brücken, Feldränder.",
 "Im „Rüttelflug“ steht er auf der Stelle in der Luft und späht nach Mäusen.",
 alias=["Falke"])

bird("wanderfalke","Wanderfalke","Falco peregrinus","Greifvögel",["berge","garten"],3,"1-12","2-6",["kraechz","schrill"],
 "Raues, schnelles „kek-kek-kek“ an Felsen und Türmen.",
 "Kein Gesang.",
 "Rau und laut „kräk-kräk-kräk“.",
 "Das schnellste Tier der Welt.",
 ["turmfalke"],
 "Felswände, Kirchtürme, Kraftwerke und Hochhäuser in Städten.",
 "Im Sturzflug wurden über 300 km/h gemessen. In den 1970er-Jahren war er durch das Insektengift DDT fast verschwunden – heute hat er sich erholt.")

bird("steinadler","Steinadler","Aquila chrysaetos","Greifvögel",["berge"],4,"1-12","1-4",["schrill"],
 "Selten zu hören: hohe Pfiffe und bellende „kja“-Rufe.",
 "Kein Gesang.",
 "Gelegentlich bellendes „kjäk“ oder hohes Pfeifen.",
 "Der König der Lüfte – meist schweigsam.",
 ["maeusebussard","bartgeier"],
 "Alpen; jagt über Almen und Felsen.",
 "Spannweite über zwei Meter. Die Paare besetzen riesige Reviere.",
 kultur="Bei Grimms „Zaunkönig“ fliegt der Adler am höchsten – fast. Adler zieren die Wappen von Deutschland, Österreich und vieler Schweizer Kantone.",
 kid=["Kjä!","Der Adler fliegt hoch über den Bergen."], reg="Alpen", alias=["Adler"])

bird("seeadler","Seeadler","Haliaeetus albicilla","Greifvögel",["wasser","kueste"],4,"1-12","1-4",["schrill"],
 "Hohes, kläffendes „kja-kja-kja“ – Paare im Duett.",
 "Kein Gesang; Paare rufen gemeinsam.",
 "Lange, abfallende Rufreihen.",
 "Ein fliegendes Scheunentor mit weißem Schwanz.",
 ["steinadler"],
 "Seen und Küsten Norddeutschlands, Donau-Auen in Österreich, zunehmend auch im Süden.",
 "Der größte Greifvogel Mitteleuropas – bis zu 2,4 Meter Spannweite. Fast ausgerottet, heute wieder auf dem Vormarsch.")

bird("bartgeier","Bartgeier","Gypaetus barbatus","Greifvögel",["berge"],4,"1-12",None,["schrill"],
 "Fast stumm – nur selten hohe Pfiffe.",
 "Kein Gesang.",
 "Selten hohe, pfeifende Laute.",
 "Der Knochenbrecher der Alpen.",
 ["steinadler"],
 "Alpen; seit 1986 werden Bartgeier wieder angesiedelt, in Österreich, der Schweiz und seit 2021 auch in Berchtesgaden.",
 "Ernährt sich fast nur von Knochen. Große Knochen lässt er aus der Luft auf Felsen fallen, bis sie zerbrechen.",
 kultur="Der alte Name „Lämmergeier“ beruht auf einem Irrtum: Bartgeier rauben weder Lämmer noch Kinder.",
 reg="Alpen", alias=["Lämmergeier"])

# ============================================================ Eulen
bird("uhu","Uhu","Bubo bubo","Eulen",["berge","wald","garten"],3,"1-12","1-4,9-11",["tief","name"],
 "Tiefes, weittragendes „buhu“ in der Dämmerung.",
 "Das Männchen ruft ein tiefes „u-hu“ mit Betonung auf der ersten Silbe, das Weibchen antwortet höher. Hauptzeit im Spätwinter.",
 "Weibchen und Junge: heisere, kreischende „chräh“-Laute.",
 "Er ruft seinen Namen – im tiefsten Bass.",
 ["waldkauz","waldohreule"],
 "Felswände, Steinbrüche, Schluchten – zunehmend auch in Städten an Gebäuden und Friedhöfen.",
 "Eine der größten Eulen der Welt. Die „Ohren“ sind nur Federbüschel.",
 kultur="„Der Uhu, der Uhu, der macht die Fensterläden zu“ (Vogelhochzeit). Bei den Grimms gibt es das Märchen „Die Eule“, in dem ein Uhu eine ganze Stadt in Aufruhr versetzt.",
 kid=["Uhu! Uhu!","Der Uhu ruft „Uhu“ in der Nacht."], night=True)

bird("waldkauz","Waldkauz","Strix aluco","Eulen",["wald","garten"],2,"1-12","1-4,9-12",["tief"],
 "Nachts das klassische „huu – hu-hu-huuu“.",
 "Das Männchen ruft ein langes „huu“, dann nach einer Pause ein bebendes „hu-hu-hu-huuu“ – der Eulenruf aus jedem Film.",
 "Weibchen: scharfes „ku-witt“. Jungvögel im Frühsommer: heiser bettelndes „psii“.",
 "„Huu – hu-hu-huuu“ und „ku-witt“ – oft im Duett.",
 ["waldohreule","uhu","steinkauz"],
 "Wälder, große Parks, Friedhöfe und Alleen, auch mitten in Städten.",
 "Im Oktober und November ruft er besonders oft – das ist die Herbstbalz. Vogel des Jahres 2017.",
 kultur="Die typische Kinderbuch-Eule mit „Huhu“ ist meist ein Waldkauz.",
 kid=["Huu, hu-hu-huuu!","Die Eule ruft nachts im Wald."], night=True, alias=["Eule","Kauz"])

bird("waldohreule","Waldohreule","Asio otus","Eulen",["wald","feld","garten"],3,"1-12","2-4",["tief"],
 "Dumpfes, gleichmäßiges „huh … huh … huh“ – und quietschende Junge.",
 "Das Männchen ruft alle zwei bis drei Sekunden ein leises, tiefes „huh“.",
 "Die Jungen betteln im Frühsommer mit einem hohen „pfiieh“ – wie ein ungeöltes Gartentor.",
 "Ein quietschendes Gartentor in der Juninacht.",
 ["waldkauz","uhu"],
 "Feldgehölze, Waldränder, Parks und Friedhöfe; im Winter Schlafplätze in Nadelbäumen mitten in Ortschaften.",
 "Im Winter sitzen oft dutzende Waldohreulen gemeinsam in einem Baum.",
 night=True)

bird("schleiereule","Schleiereule","Tyto alba","Eulen",["feld","garten"],3,"1-12","3-7",["kraechz"],
 "Schauriges, heiseres Kreischen „chrrrüüh“ aus Kirchtürmen.",
 "Kein Gesang; das Männchen kreischt im Flug.",
 "Rau zischendes Kreischen; die Jungen „schnarchen“ zischend.",
 "Die Eule, die nicht „huhu“ macht.",
 ["waldkauz"],
 "Scheunen, Kirchtürme und Dörfer in offener Feldflur.",
 "Der herzförmige Gesichtsschleier bündelt den Schall wie ein Parabolspiegel – sie fängt Mäuse in völliger Dunkelheit nach Gehör.",
 kultur="Ihr Kreischen aus Kirchtürmen nährte Gespenstergeschichten; früher nagelte man Eulen sogar an Scheunentore, um Unheil abzuwehren.",
 night=True)

bird("steinkauz","Steinkauz","Athene noctua","Eulen",["feld","garten"],4,"1-12","2-5",["schrill"],
 "Klagendes „kuwitt“ und ein ansteigendes „guhk“.",
 "Das Männchen ruft ein gedehntes, ansteigendes „guhk“.",
 "Bellendes „kuwitt“ und „kja“.",
 "Die kleine Eule mit den zornigen Augenbrauen.",
 ["waldkauz"],
 "Streuobstwiesen, Kopfweiden, Dörfer mit Weiden.",
 "Jagt oft am Boden, läuft dabei sogar Regenwürmern hinterher.",
 kultur="Die Eule der Göttin Athene – daher „Athene noctua“ und die Redewendung „Eulen nach Athen tragen“. Den Ruf „kuwitt“ deutete der Aberglaube als „Komm mit!“ – darum galt er als Totenvogel.",
 night=True)

# ============================================================ Weitere Bekannte
bird("pirol","Pirol","Oriolus oriolus","Weitere Singvögel",["wald","wasser"],3,"5-8","5-7",["floete"],
 "Flötendes, sonniges „düdlio“ aus Baumkronen.",
 "Klare, volle Flötentöne: „dü-dü-dlio“ – fast tropisch.",
 "Raues, katzenartiges „kräh“.",
 "Ein goldgelber Vogel, den man hört, aber kaum sieht.",
 ["amsel","star"],
 "Auwälder, Laubwälder mit hohen Pappeln und Eichen, Parks.",
 "Kommt erst Anfang Mai aus Afrika zurück und heißt deshalb im Volksmund „Pfingstvogel“.",
 kultur="„Loriot“ ist französisch für Pirol – Vicco von Bülow wählte den Namen als Künstlernamen, weil der Pirol das Wappentier seiner Familie ist.",
 alias=["Pfingstvogel"])

bird("wiedehopf","Wiedehopf","Upupa epops","Weitere Vögel",["feld"],4,"4-9","4-6",["tief","motiv"],
 "Dumpfes, dreisilbiges „hup-hup-hup“.",
 "Weich, hohl und dumpf, drei- bis viersilbig, oft lange wiederholt.",
 "Raues „schähr“.",
 "Er ruft, wie sein lateinischer Name klingt: „Upupa“.",
 ["kuckuck","tuerkentaube"],
 "Warme, offene Landschaften: Weinberge, Streuobst, Weiden – etwa am Kaiserstuhl, im Wallis und im Osten Österreichs.",
 "Junge und brütende Weibchen verteidigen sich mit einem übel riechenden Sekret – daher der Spitzname „Stinkhahn“. Vogel des Jahres 2022.",
 kultur="„Der Wiedehopf, der Wiedehopf, der bringt der Braut 'nen Blumentopf“ (Vogelhochzeit). Seit 2008 ist er Nationalvogel Israels.",
 kid=["Hup-hup-hup!","Der Wiedehopf hat eine Krone aus Federn."])

bird("neuntoeter","Neuntöter","Lanius collurio","Weitere Singvögel",["feld"],3,"5-9","5-7",["kraechz"],
 "Hartes „tschek“ aus der Dornenhecke.",
 "Leises, gepresstes Schwätzen mit Imitationen anderer Vögel.",
 "Hartes „tschek“ oder „gäk“.",
 "Der Räuber mit der Zorro-Maske.",
 ["haussperling"],
 "Hecken und Dornbüsche in offener, insektenreicher Landschaft.",
 "Spießt Insekten und Mäuse als Vorrat auf Dornen. Der Volksglaube sagte, er töte erst neun Tiere, bevor er eines frisst – daher der Name.",
 alias=["Rotrückenwürger"])

bird("halsbandsittich","Halsbandsittich","Psittacula krameri","Papageien",["garten"],3,"1-12","1-12",["schrill","kraechz"],
 "Schrilles, lautes Kreischen „kii-ak“ aus Platanen.",
 "Kein Gesang im engeren Sinn.",
 "Durchdringendes Kreischen, oft im Flug in Trupps.",
 "Ein Stück Tropen über dem Rhein.",
 ["star"],
 "Städte am Rhein: Köln, Düsseldorf, Bonn, Wiesbaden, Mannheim, Heidelberg – in Parks mit alten Bäumen.",
 "Ursprünglich aus Afrika und Südasien; seit den 1960er-Jahren leben entflogene Vögel frei und überstehen die Winter problemlos.",
 reg="Rheinschiene", alias=["Papagei","Sittich"])

bird("pfau","Pfau","Pavo cristatus","Hühnervögel",["garten"],3,"1-12","3-7",["schrill"],
 "Lauter, katzenhafter Schrei „mi-ääu!“ aus dem Schlosspark.",
 "Der Hahn schreit vor allem in der Balzzeit, laut und weit hörbar.",
 "Gellendes „kie-aah“ und hupende Laute.",
 "Schön anzusehen, laut anzuhören.",
 ["maeusebussard","fasan"],
 "Schlossparks, Tiergärten, Gutshöfe – frei laufend, etwa auf der Berliner Pfaueninsel.",
 "Das „Rad“ besteht nicht aus Schwanzfedern, sondern aus verlängerten Oberschwanzdecken. Ursprünglich aus Indien.",
 kultur="„Der Pfau mit seinem bunten Schwanz macht mit der Braut den ersten Tanz“ (Vogelhochzeit). „Stolz wie ein Pfau.“",
 kid=["Mi-ääu!","Der Pfau schlägt ein buntes Rad."])

bird("seidenschwanz","Seidenschwanz","Bombycilla garrulus","Weitere Singvögel",["garten"],4,"11-3",None,["zwitscher","schrill"],
 "Glöckchenhelles, sirrendes Trillern „sirrrr“ aus Beerensträuchern.",
 "Bei uns kaum Gesang.",
 "Hohes, klingelndes „sirrr“, im Trupp wie ein Glockenspiel.",
 "Der Punk aus dem Norden – mit Wachsflügeln.",
 ["star"],
 "Wintergast in manchen Jahren: an Ebereschen, Misteln und Ziersträuchern in Städten, oft auf Supermarkt-Parkplätzen.",
 "Kommt nur in manchen Wintern in großen Zahlen aus Skandinavien und Russland. Im Mittelalter hielt man sein Erscheinen für ein Vorzeichen der Pest.",
 reg="Wintergast")

bird("mauerlaeufer","Mauerläufer","Tichodroma muraria","Weitere Singvögel",["berge"],4,"1-12","4-7",["schrill","floete"],
 "Hohe, gedehnte, ansteigende Pfiffe „ti-tüü-zrüih“ an Felswänden.",
 "Hohe, pfeifende, ansteigende Töne – leicht im Rauschen von Wasserfällen zu überhören.",
 "Dünnes „tüi“.",
 "Ein Schmetterling, der Felsen klettert.",
 ["alpendohle"],
 "Steile Felswände der Alpen; im Winter auch an Burgmauern und Steinbrüchen tiefer unten.",
 "Mit seinen leuchtend roten Flügeln flattert er wie ein Schmetterling – Vogelkundler nennen ihn den „Alpenschmetterling“.",
 reg="Alpen")

bird("goldammer","Goldammer","Emberiza citrinella","Ammern",["feld"],2,"1-12","2-8",["motiv"],
 "Sechs bis acht schnelle Töne, dann ein gedehnter Schluss: „zi-zi-zi-zi-zi-düüh“.",
 "Eine Reihe gleicher, schneller Töne mit langem, oft tieferem Endton. Singt unermüdlich bis in den Hochsommer.",
 "„Zick“ oder ein rauschendes „tsrik“.",
 "„Wie, wie, wie, wie hab ich dich liiieb!“",
 ["girlitz","zilpzalp"],
 "Hecken und Feldränder in offener Landschaft, Waldränder, Kahlschläge.",
 "Leuchtend gelber Kopf. Im Winter in Trupps auf Stoppelfeldern.",
 kultur="Eine Legende erzählt, das Anfangsmotiv von Beethovens 5. Sinfonie gehe auf den Goldammer-Ruf zurück – belegt ist das nicht.")


# ============================================================ Ausgabe
ids = {b["id"] for b in B}
for b in B:
    for v in b.get("verw", []):
        assert v in ids, (b["id"], v)
assert len(ids) == len(B)
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "birds.js")
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, "w") as fh:
    fh.write("/* generiert aus tools/birds_src.py */\nwindow.BIRDS = " + json.dumps(B, ensure_ascii=False, separators=(",", ":")) + ";\n")
print(len(B), "Arten ->", out)
