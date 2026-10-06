// Vogelstimmen München – Datenbasis
// present / sings: Monate 1–12 (Anwesenheit bzw. Hauptgesangszeit, grobe Richtwerte für Südbayern)
// hab: garten | park | wasser | feld | nacht
const ALL = [1,2,3,4,5,6,7,8,9,10,11,12];
const R = (a,b) => { const r=[]; for(let i=a;i<=b;i++) r.push(i); return r; };

window.BIRDS = [
{
  id:"amsel", de:"Amsel", lat:"Turdus merula", hab:["garten","park"],
  present:ALL, sings:R(2,7),
  lautbild:"Tiefe, gelassene Flötenstrophen mit Pausen – oft ausklingend mit leisem Gezwitscher.",
  gesang:"Melodisch, flötend, tief und ohne Eile. Jede Strophe ist etwas anders, häufig mit einem leiseren, ‚zerdrückten‘ Schluss. Singt von Dachfirsten und Antennen, besonders in der Morgen- und Abenddämmerung.",
  ruf:"Warnruf ein hartes „tix-tix“ oder tiefes „duck-duck“. Beim abendlichen Schlafplatzbezug und bei Katzen ein lautes, sich überschlagendes Zetern „tschink-tschink-tschink“.",
  merk:"Der Vogel, der klingt, als hätte er Zeit.",
  verw:"Singdrossel (wiederholt jedes Motiv 2–4×), Mönchsgrasmücke (kürzer, mit hellem ‚Überschlag‘).",
  wo:"Überall: Hinterhöfe, Friedhöfe, Englischer Garten, jeder Garten mit Rasen.",
  fakt:"Ursprünglich ein scheuer Waldvogel; die Verstädterung der Amsel begann im 19. Jahrhundert."
},
{
  id:"kohlmeise", de:"Kohlmeise", lat:"Parus major", hab:["garten","park"],
  present:ALL, sings:[1,2,3,4,5,6,9,10],
  lautbild:"Metallisch wiederholtes „zi-zi-bä“ – wie eine Fahrradpumpe.",
  gesang:"Zwei- bis dreisilbige, metallische Motive, viele Male wiederholt: „zi-zi-bä“, „zi-dä zi-dä“, „titu-titu“. Beginnt schon an milden Januartagen.",
  ruf:"Finkenähnliches „pink“, zeterndes „tsche-tsche-tsche“ und ein riesiges Repertoire weiterer Laute.",
  merk:"„Zi-zi-bä“ – die Fahrradpumpe im Gebüsch.",
  verw:"Fast alles. Faustregel der Vogelkundler: Ein unbekannter Ruf im Park ist zuerst einmal eine Kohlmeise.",
  wo:"Jeder Park, jeder Garten, jedes Futterhaus.",
  fakt:"Einzelne Männchen beherrschen mehrere Strophentypen und wechseln zwischen ihnen."
},
{
  id:"blaumeise", de:"Blaumeise", lat:"Cyanistes caeruleus", hab:["garten","park"],
  present:ALL, sings:R(2,6),
  lautbild:"Zwei, drei hohe Töne, dann ein perlender Triller: „zi-zi-sirrrr“.",
  gesang:"Kurze Strophe: hohe, dünne Einleitungstöne, gefolgt von einem schnellen Triller „zi-zi-sirrrrr“.",
  ruf:"Schimpfendes, schnarrendes „zerretetet“, dazu feine „tsi-tsi“-Laute.",
  merk:"Erst Anlauf, dann Rolle.",
  verw:"Kohlmeise (metallischer, ohne Triller), Tannenmeise.",
  wo:"Gärten, Parks, Alleen – gern an Nistkästen.",
  fakt:"Für Menschen fast unsichtbar: Blaumeisen reflektieren UV-Licht am Scheitel, das bei der Partnerwahl eine Rolle spielt."
},
{
  id:"buchfink", de:"Buchfink", lat:"Fringilla coelebs", hab:["park","garten"],
  present:ALL, sings:R(2,7),
  lautbild:"Schmetternde, abwärts rollende Strophe mit Schnörkel am Ende – der „Finkenschlag“.",
  gesang:"Laut, temperamentvoll, abfallend, mit einem betonten Endschnörkel. Ein Männchen hat meist ein bis mehrere Strophentypen.",
  ruf:"„Pink“ oder „fink“; dazu der regional verschiedene „Regenruf“ (z. B. „rüüt“ oder „hüit“), im Flug „jüpp“.",
  merk:"„Bin, bin, bin ich nicht ein schöner Feld-mar-schall?“ (Volksmund, Varianten)",
  verw:"Fitis (weicher, melancholisch), Gartenrotschwanz.",
  wo:"Englischer Garten, Nymphenburger Park, Perlacher Forst – häufigster Waldvogel.",
  fakt:"Buchfinken haben regionale Dialekte: Endschnörkel und Regenruf klingen in verschiedenen Gegenden verschieden."
},
{
  id:"haussperling", de:"Haussperling (Spatz)", lat:"Passer domesticus", hab:["garten"],
  present:ALL, sings:ALL,
  lautbild:"Unermüdliches „tschilp-tschilp“, gemeinschaftliches Geschwätz aus Hecken.",
  gesang:"Kein eigentlicher Gesang: Das Männchen reiht „tschilp“-Laute aneinander. In Gruppen entsteht ein lautes Schwatzkonzert.",
  ruf:"„Tschilp“, im Flug „tschuw“, Warnruf ein schnarrendes „terrr“.",
  merk:"Der Biergarten-Soundtrack.",
  verw:"Feldsperling (höher, ‚tschettet‘, eher am Stadtrand).",
  wo:"Biergärten, Viktualienmarkt, dichte Hecken in Wohnvierteln.",
  fakt:"In vielen europäischen Städten seit Jahrzehnten rückläufig – fehlende Nischen an sanierten Gebäuden gelten als ein Grund."
},
{
  id:"rotkehlchen", de:"Rotkehlchen", lat:"Erithacus rubecula", hab:["garten","park"],
  present:ALL, sings:[1,2,3,4,5,6,9,10,11,12],
  lautbild:"Perlende, wehmütige Kaskaden – hohe Töne, die wie Tropfen herabfallen.",
  gesang:"Fein, perlend, abwechslungsreich, mit langen, hohen Tönen und plötzlichen Tempowechseln. Singt auch im Herbst und Winter – dann klingt es besonders melancholisch.",
  ruf:"Hartes „tick“ oder „zick“, oft zu „tikikik“ gereiht; dazu ein dünnes, hohes „ziieh“.",
  merk:"Der Herbstsänger: Wer im Oktober eine zarte, traurige Weise hört, hört meist ihn.",
  verw:"Heckenbraunelle (gleichförmiger), Zaunkönig (viel lauter, mit Triller).",
  wo:"Unterholz in Parks und Friedhöfen, Isarauen, jeder Garten mit Gebüsch.",
  fakt:"Im Herbst verteidigen Männchen UND Weibchen eigene Winterreviere – deshalb singen beide. Unter Straßenlaternen singt es auch nachts. Vogel des Jahres 2021."
},
{
  id:"zilpzalp", de:"Zilpzalp", lat:"Phylloscopus collybita", hab:["park","garten"],
  present:R(3,10), sings:R(3,9),
  lautbild:"Er sagt seinen Namen: „zilp-zalp-zilp-zelp-zalp“.",
  gesang:"Unregelmäßige Folge zweier Tonhöhen, wie ein Pendel, das stolpert. Einer der ersten Rückkehrer im März.",
  ruf:"Weiches, fragendes „hüit“.",
  merk:"Lautmalerischer Name – einfacher wird’s nicht.",
  verw:"Fitis (abfallende, weiche Strophe), Kohlmeise (metallischer, regelmäßiger).",
  wo:"Isarauen, Englischer Garten, Gehölzränder.",
  fakt:"Einzelne Zilpzalpe überwintern inzwischen in Mitteleuropa, statt ans Mittelmeer zu ziehen."
},
{
  id:"moenchsgrasmuecke", de:"Mönchsgrasmücke", lat:"Sylvia atricapilla", hab:["park","garten"],
  present:R(4,9), sings:R(4,7),
  lautbild:"Erst leises Plaudern, dann ein lauter, jubelnder Flöten-„Überschlag“.",
  gesang:"Beginnt mit schnellem, leisem Gezwitscher und bricht dann in klare, laute Flötentöne aus – der typische ‚Überschlag‘.",
  ruf:"Hartes „tack-tack“, wie zwei aneinandergeschlagene Kiesel.",
  merk:"Erst murmeln, dann jubeln.",
  verw:"Gartengrasmücke (lange, gleichmäßige Strophe ohne Überschlag), Amsel.",
  wo:"Hecken, Parks, Gärten mit dichtem Gebüsch, Isarauen.",
  fakt:"Ein Teil der mitteleuropäischen Population zieht im Herbst nach Nordwesten (Britische Inseln) statt nach Süden."
},
{
  id:"singdrossel", de:"Singdrossel", lat:"Turdus philomelos", hab:["park"],
  present:R(3,10), sings:R(3,7),
  lautbild:"Laute Motive, jedes zwei- bis viermal wiederholt.",
  gesang:"Kraftvoll, klar, abwechslungsreich – aber jedes Motiv wird zwei- bis viermal wiederholt, bevor das nächste kommt. Singt gern hoch von Baumspitzen.",
  ruf:"Kurzes, scharfes „zipp“ – im Oktober nachts von ziehenden Drosseln über der Stadt zu hören.",
  merk:"„Philipp, Philipp, Philipp – komm her, komm her – Tee trinken, Tee trinken“ (Volksmund).",
  verw:"Amsel (wiederholt nicht), Misteldrossel.",
  wo:"Parks mit altem Baumbestand, Waldfriedhof, Isarauen, Perlacher Forst.",
  fakt:"Zerschlägt Schneckenhäuser auf einem festen Stein – solche ‚Drosselschmieden‘ erkennt man an den Scherben."
},
{
  id:"zaunkoenig", de:"Zaunkönig", lat:"Troglodytes troglodytes", hab:["park","wasser"],
  present:ALL, sings:[1,2,3,4,5,6,7,9,10,11,12],
  lautbild:"Winzig, aber ohrenbetäubend: schmetternde Strophe mit schnurrendem Triller.",
  gesang:"Sehr laut, schnell, schmetternd, mit einem oder mehreren eingebauten Trillern. Singt fast das ganze Jahr, auch im Winter.",
  ruf:"Hartes „teck-teck“, schnarrendes „zerrr“.",
  merk:"Zehn Gramm Vogel, Weckerlautstärke.",
  verw:"Rotkehlchen (leiser, ohne Triller), Heckenbraunelle.",
  wo:"Isarauen, Bachufer, dichtes Unterholz in jedem größeren Park.",
  fakt:"Das Männchen baut mehrere Nester; das Weibchen wählt eines davon aus."
},
{
  id:"hausrotschwanz", de:"Hausrotschwanz", lat:"Phoenicurus ochruros", hab:["garten"],
  present:R(3,10), sings:[3,4,5,6,7,9,10],
  lautbild:"Kurze Strophe mit einem knirschenden Teil – wie zerknülltes Papier.",
  gesang:"Kurze, gepresste Pfeiftöne, dazwischen ein unverwechselbares Knirschen oder Kratzen. Oft der allererste Sänger, lange vor Sonnenaufgang.",
  ruf:"„Hüid“, dazu ein schnalzendes „tek-tek“.",
  merk:"Der Morgen beginnt mit Papierknüllen auf dem Dach.",
  verw:"Gartenrotschwanz (melodischer, ohne Knirschen).",
  wo:"Dachfirste, Baustellen, Industriegebiete, Altstadt – ursprünglich ein Felsenvogel.",
  fakt:"Bleibt oft bis in den Oktober oder November und singt im Herbst noch einmal."
},
{
  id:"gruenfink", de:"Grünfink (Grünling)", lat:"Chloris chloris", hab:["garten"],
  present:ALL, sings:R(3,7),
  lautbild:"Klingelnde Triller und ein gedehntes, nasales „dschwuiiih“.",
  gesang:"Abwechselnd klingelnde Triller und das gedehnte, gequetschte „dschwuiiih“. Im Frühling oft im flatternden Singflug.",
  ruf:"Im Flug ein klingelndes „gigigig“.",
  merk:"„Dschwuiiih“ – der Seufzer aus der Thuja-Hecke.",
  verw:"Girlitz (höher, klirrend), Bergfink im Winter.",
  wo:"Gärten, Alleen, Wohnviertel mit Hecken.",
  fakt:"Die Bestände sind seit etwa 2009 deutlich eingebrochen – Hauptursache ist eine Parasitenerkrankung (Trichomonose), die sich an verschmutzten Futterstellen ausbreitet."
},
{
  id:"stieglitz", de:"Stieglitz (Distelfink)", lat:"Carduelis carduelis", hab:["feld","garten"],
  present:ALL, sings:R(3,8),
  lautbild:"Hastiges, perlendes Gezwitscher mit eingestreutem „stiglitt“.",
  gesang:"Flinkes, munteres Zwitschern und Trillern, durchsetzt mit dem namensgebenden Ruf.",
  ruf:"„Stiglitt“ oder „didlit“ – daher der Name.",
  merk:"Ruft seinen Namen beim Losfliegen.",
  verw:"Girlitz, Erlenzeisig.",
  wo:"Brachen, Bahndämme, Fröttmaninger Heide, Gärten mit Disteln oder Sonnenblumen.",
  fakt:"Frisst mit seinem spitzen Schnabel Samen aus Distel- und Kardenköpfen. Vogel des Jahres 2016."
},
{
  id:"star", de:"Star", lat:"Sturnus vulgaris", hab:["park","garten"],
  present:R(2,11), sings:[2,3,4,5,6,9,10],
  lautbild:"Pfeifen, Schnalzen, Knarren – und Imitationen von allem Möglichen.",
  gesang:"Ein buntes Durcheinander aus Pfiffen, Klicken und Knarren, dazu nachgeahmte Laute anderer Vögel (z. B. Bussard, Pirol) und Alltagsgeräusche. Typisch ein abfallender Pfiff „wiuuu“. Singt mit flatternden Flügeln.",
  ruf:"Raues „rrää“, im Flug ein kurzes „tschurr“.",
  merk:"Das Mixtape der Vogelwelt.",
  verw:"Kaum zu verwechseln, aber seine Imitationen führen in die Irre.",
  wo:"Parkwiesen, Englischer Garten, Kleingärten; im Herbst große Schwärme an Schlafplätzen.",
  fakt:"Einzelne Stare imitieren sogar Handyklingeltöne oder Autoalarmanlagen. Vogel des Jahres 2018."
},
{
  id:"ringeltaube", de:"Ringeltaube", lat:"Columba palumbus", hab:["garten","park"],
  present:ALL, sings:R(3,9),
  lautbild:"Dumpfes, fünfsilbiges Gurren, betont auf der zweiten Silbe, endet abrupt.",
  gesang:"Tiefes Gurren in fünfsilbigen Strophen (etwa „gru-GRUUU-gru, gru-gru“), mehrmals wiederholt, oft mit einem abgehackten Schlusston. Beim Balzflug klatschen die Flügel laut.",
  ruf:"Beim Auffliegen lautes Flügelklatschen.",
  merk:"Fünf Silben = Ringeltaube, drei Silben = Türkentaube.",
  verw:"Türkentaube (dreisilbig), Straßentaube (rollendes ‚gurr‘).",
  wo:"Überall – Parks, Straßenbäume, Hausdächer.",
  fakt:"Größte heimische Taube; erkennbar am weißen Halsfleck."
},
{
  id:"tuerkentaube", de:"Türkentaube", lat:"Streptopelia decaocto", hab:["garten"],
  present:ALL, sings:R(2,10),
  lautbild:"Dreisilbiges „gu-GUUU-gu“, endlos wiederholt.",
  gesang:"Hohles, dreisilbiges Gurren mit Betonung in der Mitte, monoton wiederholt – oft von Antennen und Dachkanten.",
  ruf:"Beim Landen ein nasales, gequetschtes „chwäää“.",
  merk:"Drei Silben – die Taube auf der Antenne.",
  verw:"Ringeltaube (fünfsilbig).",
  wo:"Wohnviertel, Dächer, Antennen, Gärten.",
  fakt:"Kam erst im 20. Jahrhundert vom Balkan her nach Mitteleuropa – eine der spektakulärsten Ausbreitungen eines Vogels in Europa."
},
{
  id:"rabenkraehe", de:"Rabenkrähe", lat:"Corvus corone", hab:["garten","park","feld"],
  present:ALL, sings:ALL,
  lautbild:"Raues, hartes „krah-krah-krah“.",
  gesang:"Kein Gesang im engeren Sinn; selten leises Gemurmel.",
  ruf:"Lautes, heiseres „krah“, meist drei- bis viermal gereiht.",
  merk:"Das Krächzen über der Theresienwiese.",
  verw:"Saatkrähe (Wintergast, nasaler „gaah“, in großen Trupps), Kolkrabe (tief „korrk“).",
  wo:"Überall, besonders auf großen Wiesen und Plätzen.",
  fakt:"Rabenvögel gehören zu den intelligentesten Vögeln überhaupt – sie erkennen einzelne Menschen wieder."
},
{
  id:"elster", de:"Elster", lat:"Pica pica", hab:["garten","park"],
  present:ALL, sings:ALL,
  lautbild:"Ratterndes „schak-schak-schak“ wie ein Maschinengewehr.",
  gesang:"Leises, plauderndes Schwatzen, selten wahrgenommen.",
  ruf:"Laut ratterndes „schäckern“ – besonders bei Katzen, Greifvögeln oder Eulen.",
  merk:"Die Klapper der Nachbarschaft.",
  verw:"Wacholderdrossel (ähnlich ratternd, heller), Eichelhäher.",
  wo:"Wohnviertel, Parks, Straßenbäume.",
  fakt:"Eines der wenigen Nicht-Säugetiere, die im Spiegeltest Hinweise auf Selbsterkennen zeigten."
},
{
  id:"eichelhaeher", de:"Eichelhäher", lat:"Garrulus glandarius", hab:["park"],
  present:ALL, sings:ALL,
  lautbild:"Heiseres, kreischendes „rätsch“ – der Alarm des Waldes.",
  gesang:"Leises, vielseitiges Schwatzen mit Imitationen.",
  ruf:"Lautes, reißendes „rätsch“. Imitiert täuschend echt den Ruf des Mäusebussards.",
  merk:"„Rätsch!“ – jemand reißt ein Tuch entzwei.",
  verw:"Mäusebussard (den er nachahmt), Elster.",
  wo:"Parks mit Eichen: Nymphenburger Park, Hirschgarten, Perlacher Forst, Englischer Garten.",
  fakt:"Im Herbst versteckt ein Häher tausende Eicheln – vergessene keimen. So pflanzt er Eichenwälder."
},
{
  id:"mauersegler", de:"Mauersegler", lat:"Apus apus", hab:["garten","feld"],
  present:R(5,8), sings:R(5,8),
  lautbild:"Schrilles „srieh-srieh“ – Gruppen jagen kreischend um die Dächer.",
  gesang:"Kein Gesang; die gemeinsamen Schreiflüge sind ihr Sommerlied.",
  ruf:"Hohes, schrilles „srieeh“, in Gruppen im rasanten Flug.",
  merk:"Der Klang des Münchner Hochsommers über den Altbauten.",
  verw:"Schwalben (zwitschernd, nicht schrill).",
  wo:"Altbauviertel: Schwabing, Haidhausen, Maxvorstadt, Altstadt.",
  fakt:"Verbringt außerhalb der Brutzeit bis zu zehn Monate ununterbrochen in der Luft – schläft und frisst im Flug."
},
{
  id:"buntspecht", de:"Buntspecht", lat:"Dendrocopos major", hab:["park","garten"],
  present:ALL, sings:R(1,5),
  lautbild:"Kurzer, schneller Trommelwirbel – und ein hartes „kick“.",
  gesang:"Statt Gesang: Trommeln. Ein sehr kurzer, schneller Wirbel (unter einer Sekunde), der abrupt endet. Hauptzeit Januar bis April.",
  ruf:"Hartes, einzelnes „kick“ oder „tschick“, das ganze Jahr.",
  merk:"Kurzes Trommeln, hartes „kick“.",
  verw:"Kleinspecht, Mittelspecht; Trommeln anderer Spechte (länger oder langsamer).",
  wo:"Jeder Park mit alten Bäumen, auch Futterhäuser im Winter.",
  fakt:"Trommeln ist Revieranzeige, keine Futtersuche – gern auf resonanten Ästen oder sogar Blechdächern."
},
{
  id:"gruenspecht", de:"Grünspecht", lat:"Picus viridis", hab:["park"],
  present:ALL, sings:R(2,6),
  lautbild:"Lautes Lachen: „klü-klü-klü-klü-klü“.",
  gesang:"Lauter, gleichmäßiger, leicht abfallender Ruf, der wie Gelächter klingt. Trommelt selten.",
  ruf:"Im Flug ein scharfes „kjück“.",
  merk:"Der lachende Specht auf der Parkwiese.",
  verw:"Grauspecht (langsamer, stärker abfallend, melancholisch).",
  wo:"Parkwiesen mit alten Bäumen: Englischer Garten, Olympiapark, Friedhöfe.",
  fakt:"Sucht seine Nahrung am Boden – vor allem Ameisen, die er mit einer sehr langen, klebrigen Zunge aus dem Nest holt."
},
{
  id:"kleiber", de:"Kleiber", lat:"Sitta europaea", hab:["park"],
  present:ALL, sings:[1,2,3,4,5,6,9,10,11,12],
  lautbild:"Laute, klare Pfiffe „wi-wi-wi-wi“ – als ob jemand seinen Hund ruft.",
  gesang:"Reihen lauter Pfiffe, mal schnell trillernd „wiwiwiwi“, mal langsam „tüi – tüi – tüi“.",
  ruf:"Kräftiges „twit-twit“ oder „sit“.",
  merk:"Pfeift wie ein Hundehalter im Park.",
  verw:"Kohlmeise, Gimpel – wird oft für einen viel größeren Vogel gehalten.",
  wo:"Alte Laubbäume: Hofgarten, Englischer Garten, Nymphenburger Park.",
  fakt:"Klettert als einziger heimischer Vogel kopfüber den Stamm hinab und verkleinert den Eingang seiner Bruthöhle mit Lehm."
},
{
  id:"gartenbaumlaeufer", de:"Gartenbaumläufer", lat:"Certhia brachydactyla", hab:["park","garten"],
  present:ALL, sings:R(2,6),
  lautbild:"Kurze, rhythmische Strophe: „tüt-tüt-teroi-tit“.",
  gesang:"Kurze, hohe, rhythmische Strophe mit festem Muster, oft mehrmals pro Minute.",
  ruf:"Hohes, durchdringendes „tiit“.",
  merk:"„Tüt-tüt-teroi-tit“ – ein kleiner Morsecode am Baumstamm.",
  verw:"Waldbaumläufer (abfallender Triller) – optisch fast identisch, am Gesang sicher zu trennen.",
  wo:"Parks und Alleen mit alten Bäumen, Friedhöfe.",
  fakt:"Klettert spiralig den Stamm hinauf, fliegt zum Fuß des nächsten Baums und beginnt von vorn."
},
{
  id:"dohle", de:"Dohle", lat:"Coloeus monedula", hab:["garten","feld"],
  present:ALL, sings:ALL,
  lautbild:"Helles, kurzes „kjack“ – fröhlicher als jede Krähe.",
  gesang:"Kein Gesang im engeren Sinn.",
  ruf:"Kurzes, helles „kjack“ oder „tschjak“, oft im Chor aus fliegenden Trupps.",
  merk:"Die Krähe mit der hellen Stimme und den hellen Augen.",
  verw:"Saatkrähe, Rabenkrähe (beide tiefer und rauer).",
  wo:"Gebäude mit Nischen (Kirchtürme, Altbauten), Parks; im Winter gemeinsam mit Saatkrähen auf Feldern.",
  fakt:"Dohlen leben in lebenslanger Partnerschaft – Paare fliegen dicht nebeneinander."
},
{
  id:"stockente", de:"Stockente", lat:"Anas platyrhynchos", hab:["wasser"],
  present:ALL, sings:ALL,
  lautbild:"Das klassische, absteigende „Quak-quak-quak-quak“.",
  gesang:"Kein Gesang. Bei der Balz pfeifen die Erpel leise.",
  ruf:"Weibchen: lautes, absteigendes „quaak-quak-quak“. Erpel: leises, gequetschtes „räb“.",
  merk:"Laut quakt nur die Ente – der Erpel räbbelt.",
  verw:"Kaum möglich.",
  wo:"Isar, Eisbach, Kleinhesseloher See, Nymphenburger Kanal, jeder Teich.",
  fakt:"Das berühmte laute Quaken stammt ausschließlich von den Weibchen."
},
{
  id:"blaesshuhn", de:"Blässhuhn", lat:"Fulica atra", hab:["wasser"],
  present:ALL, sings:ALL,
  lautbild:"Kurzes, explosives „pix!“ oder „kött“ vom Wasser.",
  gesang:"Kein Gesang.",
  ruf:"Laute, kurze Rufe: „pix“, „pitz“, „kött“; auch nachts.",
  merk:"Ein Knall mit weißer Stirn.",
  verw:"Teichhuhn (gurgelndes „kürrk“).",
  wo:"Kleinhesseloher See, Nymphenburger Kanal, Feringasee, Isar-Staustufen.",
  fakt:"Die weiße Stirnplatte – die ‚Blässe‘ – gibt dem Vogel seinen Namen."
},
{
  id:"maeusebussard", de:"Mäusebussard", lat:"Buteo buteo", hab:["feld"],
  present:ALL, sings:R(2,6),
  lautbild:"Miauendes „hiääh“ aus großer Höhe.",
  gesang:"Kein Gesang; im Frühjahr ruft er bei Balzflügen besonders oft.",
  ruf:"Gedehntes, katzenartiges „hiääh“, oft im kreisenden Segelflug.",
  merk:"Die Katze am Himmel.",
  verw:"Eichelhäher (imitiert ihn täuschend echt!).",
  wo:"Stadtrand, Felder im Münchner Norden und Osten, Fröttmaninger Heide, Autobahnränder.",
  fakt:"Der häufigste Greifvogel Mitteleuropas – sitzt gern auf Pfählen am Straßenrand."
},
{
  id:"waldkauz", de:"Waldkauz", lat:"Strix aluco", hab:["park","nacht"],
  present:ALL, sings:[1,2,3,4,10,11,12],
  lautbild:"Nachts: das klassische „huu – hu-hu-huuuu“.",
  gesang:"Das Männchen ruft ein langes „huu“, eine Pause, dann ein bebendes „hu-hu-hu-huuu“ – der Eulenruf aus jedem Film.",
  ruf:"Weibchen: scharfes „kuwitt“. Jungvögel im Frühsommer: heiser bettelndes „psii“.",
  merk:"„Huu – hu-hu-huuu“ und „kuwitt“ – oft im Duett.",
  verw:"Waldohreule (dumpfes, einzelnes „huh“).",
  wo:"Englischer Garten, Nymphenburger Park, Waldfriedhof, Nordfriedhof, Perlacher Forst.",
  fakt:"Im Oktober und November ruft er besonders oft – es ist die Herbstbalz. Der „kuwitt“-Ruf (v. a. beim Steinkauz) wurde im Volksglauben als „Komm mit!“ gedeutet. Vogel des Jahres 2017."
},
{
  id:"goldammer", de:"Goldammer", lat:"Emberiza citrinella", hab:["feld"],
  present:ALL, sings:R(2,8),
  lautbild:"Sechs bis acht schnelle Töne, dann ein gedehnter Schluss: „zi-zi-zi-zi-zi-düüüh“.",
  gesang:"Eine Reihe gleicher, schneller Töne mit einem langen, oft tieferen Endton. Singt unermüdlich, bis in den Hochsommer.",
  ruf:"„Zick“ oder ein rauschendes „tsrik“.",
  merk:"„Wie, wie, wie, wie hab ich dich liiieb!“",
  verw:"Zippammer, Grauammer (klirrend).",
  wo:"Hecken und Feldränder am Stadtrand: Fröttmaninger Heide, Münchner Norden und Osten.",
  fakt:"Einer Legende nach soll das Motiv von Beethovens 5. Sinfonie auf den Goldammerruf zurückgehen – belegt ist das nicht."
}
];

window.HABITATS = {
  garten:{label:"Garten & Stadt", icon:"🏘️"},
  park:{label:"Park & Wald", icon:"🌳"},
  wasser:{label:"Wasser", icon:"💧"},
  feld:{label:"Feld & Himmel", icon:"🌾"},
  nacht:{label:"Nacht", icon:"🌙"}
};
