#!/usr/bin/env python3
"""
Match exercises with English translations from sentence corpus
"""
import json

# Load the 175 gap-fill exercises
with open('../calude_suggested_sentence_exercises/dutch_exercises.json', 'r', encoding='utf-8') as f:
    exercises = json.load(f)

# Manually curated translations from ALL200 and SECTIONS (extracted from gold-sentences.html)
# This is the comprehensive list from the corpus
translations = {
    # ALL200 sentences
    "Dat lijkt me heerlijk.": "That seems wonderful to me.",
    "Dat gaat niet.": "That won't work / That's not possible.",
    "Kun jij Joris vanmiddag naar het hockeyveld brengen?": "Can you take Joris to the hockey field this afternoon?",
    "Ik heb met Sjoerd afgesproken.": "I made plans with Sjoerd.",
    "We gaan hardlopen, omdat we volgende week die wedstrijd hebben.": "We're going to run because we have that race next week.",
    "Niks aan te doen.": "Nothing to be done about it.",
    "Onze agenda's zitten behoorlijk vol.": "Our schedules are quite full.",
    "Laten we binnenkort samen iets gaan drinken.": "Let's go get a drink together soon.",
    "Ik ben dol op mijn neefje en nichtje.": "I'm crazy about my nephew and niece.",
    "Ik wil dus eigenlijk 'nee' zeggen, maar ik durf het niet.": "So I actually want to say no, but I don't dare.",
    "Mijn zus wordt namelijk nogal snel kwaad.": "My sister gets angry quite quickly, you see.",
    "Doen zij wel eens iets voor jou?": "Do they ever do anything for you?",
    "Ik heb niet uitgelegd dat ik niet van honden hou.": "I didn't explain that I don't like dogs.",
    "Maar nu vraagt hij het weer!": "But now he's asking again!",
    "Zeg gewoon 'nee' tegen je vriend, maar leg je reactie wel uit.": "Just say no to your friend, but do explain your reaction.",
    "Dan vraagt hij je de volgende keer ook niet meer.": "Then he won't ask you again next time either.",
    "Je moet inderdaad zeggen dat je honden niet leuk vindt.": "You should indeed say that you don't like dogs.",
    "Dat hangt van je moedertaal af.": "That depends on your mother tongue.",
    "Voor hem is Nederlands gemakkelijk, omdat het Duits dichtbij het Nederlands staat.": "For him Dutch is easy, because German is close to Dutch.",
    "Jazeker, dat is een voordeel.": "Absolutely, that is an advantage.",
    "Hoe gemotiveerd ben je?": "How motivated are you?",
    "Hoeveel tijd besteed je aan je huiswerk?": "How much time do you spend on your homework?",
    "Je moet overal en met iedereen Nederlands spreken.": "You must speak Dutch everywhere and with everyone.",
    "Het gaat niet echt vanzelf.": "It doesn't really happen by itself.",
    "Schrijven in het Nederlands vind ik het moeilijkst.": "I find writing in Dutch the hardest.",
    "Nederlanders begrijpen je echt niet als je een klank verkeerd uitspreekt.": "Dutch people really don't understand you if you pronounce a sound wrong.",
    "Het Arabisch heeft maar één lidwoord en niet drie, zoals het Nederlands.": "Arabic has only one article and not three, like Dutch.",

    # SECTIONS - Modal Imperfectum
    "Ik kon geen minuut stilzitten, ik was altijd buiten.": "I couldn't sit still for a minute, I was always outside.",
    "We konden niet stoppen met lachen.": "We couldn't stop laughing.",
    "Ik moest het magazijn en de winkel netjes houden.": "I had to keep the stockroom and the shop tidy.",
    "Ik moest ze helpen, als ze iets niet konden vinden.": "I had to help them when they couldn't find something.",
    "Als het erg druk was, moest ik soms ook achter de kassa werken.": "When it was very busy I sometimes had to work at the checkout.",
    "Vroeger kon je in Nederland bijna iedere winter schaatsen.": "In the past you could skate in the Netherlands almost every winter.",
    "In de stad kon je de bergen zien.": "From the city you could see the mountains.",
    "Daar kon je zwemmen.": "You could swim there.",
    "Ik wilde dat het zomer was, lekker 25 graden.": "I wished it were summer, a nice 25 degrees.",
    "Ik wilde ze meteen de blauwe zee laten zien.": "I wanted to show them the blue sea right away.",

    # SECTIONS - Er constructions
    "Er zijn veel bergen, maar ik ben in een stad opgegroeid.": "There are many mountains but I grew up in a city.",
    "Er zijn ook vaak periodes met regen en onweer.": "There are also often periods of rain and thunderstorms.",
    "Er zijn zo veel regels.": "There are so many rules.",
    "Er is ook een toename van het aantal ouderen op sociale media.": "There is also an increase in the number of elderly on social media.",
    "Er zitten meer ouderen op sociale media omdat ze handiger zijn geworden.": "More elderly are on social media because they have become more skilled.",
    "Er is trouwens ook voetbal op tv.": "There's also football on TV by the way.",
    "Zijn er nog meer positieve invloeden?": "Are there any more positive influences?",
    "Op deze school zijn speciale ruimtes voor pianolessen.": "At this school there are special rooms for piano lessons.",
    "In veel steden zijn dan feesten.": "In many cities there are celebrations then.",
    "Fijn dat je er bent.": "Good that you're here.",

    # SECTIONS - Relative clauses
    "Alleenstaande mensen zijn mensen die alleen wonen.": "Single people are people who live alone.",
    "Jeroen kent een fotograaf die mooie foto's kan maken.": "Jeroen knows a photographer who can take beautiful photos.",
    "Je netwerk bestaat uit alle mensen die je kent.": "Your network consists of all the people you know.",
    "Op de vijfde verdieping zijn studieplekken die een wifi-verbinding hebben.": "On the fifth floor there are study spots that have a wifi connection.",
    "Zoek naar interesses die jullie allebei hebben.": "Look for interests that you both share.",
    "Soms kijk ik programma's terug die ik heb gemist.": "Sometimes I watch programmes back that I missed.",
    "Geniet van de leuke contacten die je krijgt.": "Enjoy the nice contacts you get.",
    "Dat is het enige stukje echte natuur in Nederland.": "That is the only real piece of nature in the Netherlands.",
    "Is die grammatica moeilijk?": "Is that grammar hard?",

    # SECTIONS - Reflexive verbs
    "Ik voelde me thuis in de natuur.": "I felt at home in nature.",
    "Ik schaamde me vroeger altijd voor zijn grapjes.": "I always used to be embarrassed by his jokes.",
    "Ik herinner me onze huwelijksreis nog goed.": "I still remember our honeymoon well.",
    "Ik had geen zin meer om me te scheren.": "I no longer felt like shaving.",
    "Je moet je niet zo druk maken.": "You shouldn't stress so much.",
    "Ze spraken af en gaan daten.": "They made a date and started dating.",
    "Ik bedenk ineens dat ik de kapper nog niet heb gebeld.": "I suddenly realize I haven't called the hairdresser yet.",
    "Hij schaamde zich voor zijn gedrag.": "He was embarrassed about his behaviour.",
    "We hebben ons goed voorbereid.": "We have prepared ourselves well.",
    "Je kunt je hier prima op concentreren.": "You can concentrate on this perfectly well here.",

    # SECTIONS - Time/place fronting
    "Gisteren heb ik lekker uitgerust en twee films gekeken.": "Yesterday I had a good rest and watched two films.",
    "Vorig jaar hebben we hem gekocht.": "Last year we bought it.",
    "Vorige maand is mijn vader overleden.": "Last month my father passed away.",
    "Tegenwoordig trouwen mensen gemiddeld tien jaar later.": "Nowadays people get married on average ten years later.",
    "Vroeger was ongetrouwd samenwonen niet zo vanzelfsprekend.": "In the past cohabiting without marriage was not so obvious.",
    "In de zomervakantie ging ik met mijn ouders vaak wandelen.": "In the summer holidays I often went hiking with my parents.",
    "'s Ochtends maakte ik de winkel open en 's avonds sloot ik hem weer.": "In the morning I opened the shop and in the evening I closed it again.",
    "Daarna overleg ik meteen met de directeur.": "After that I'll consult with the director right away.",
    "Sindsdien daalt het aantal huwelijken in Nederland.": "Since then the number of marriages in the Netherlands has been falling.",
    "Op 4 mei is iedereen om 20.00 uur twee minuten stil.": "On May 4th everyone is silent for two minutes at 8pm.",

    # SECTIONS - Laten constructions
    "Ik laat je straks zien hoe je het moet föhnen.": "I'll show you later how to blow-dry it.",
    "Dat laten we u morgen weten.": "We'll let you know tomorrow.",
    "Misschien kunnen ze een monteur sturen.": "Maybe they can send a repairman.",
    "Laat maar, ik doe het zelf wel.": "Never mind, I'll do it myself.",
    "Zullen we het journaal kijken?": "Shall we watch the news?",
    "Ik ga het eerst even wassen, oké?": "I'll wash it first quickly, okay?",
    "Kom op, probeer het zelf even te doen.": "Come on, try to do it yourself.",
    "Ze laten de kinderen de hele dag op school sporten.": "They have the children exercise at school all day.",

    # SECTIONS - Worden process
    "Als alles goed gaat, worden ze verliefd en krijgen ze een relatie.": "If everything goes well they fall in love and get into a relationship.",
    "Ongetrouwd samenwonen wordt ieder jaar populairder.": "Cohabiting without marriage becomes more popular every year.",
    "De winters zijn de laatste vijftig jaar minder koud geworden.": "Winters have become less cold over the past fifty years.",
    "Als ik niet sport, word ik chagrijnig.": "If I don't work out I get irritable.",
    "Er zitten meer ouderen op sociale media omdat ze handiger zijn geworden.": "More elderly are on social media because they have become more skilled.",
    "Je vriend wordt vast boos als hij dat ontdekt.": "Your friend will definitely get angry when he finds that out.",
    "Ik werd helemaal nat op de fiets.": "I got completely wet on the bike.",
    "Mijn zus wordt namelijk nogal snel kwaad.": "My sister gets angry quite quickly you see.",
    "Ze worden verliefd en gaan daten.": "They fall in love and start dating.",
    "Nederland wordt steeds warmer door klimaatverandering.": "The Netherlands is getting increasingly warmer due to climate change.",

    # SECTIONS - Perfectum with zijn
    "Vorige maand is mijn vader overleden.": "Last month my father passed away.",
    "Leuk dat je mijn broer in de trein bent tegengekomen!": "Great that you ran into my brother on the train!",
    "We zijn vorig jaar verhuisd.": "We moved last year.",
    "We zijn gisteren naar het strand gegaan.": "Yesterday we went to the beach.",
    "Iedereen was positief over de reis.": "Everyone was positive about the trip.",
    "Ik ben in een stad opgegroeid.": "I grew up in a city.",
    "De leerlingen zijn bij Chinese leerlingen thuis gelogeerd.": "The students stayed at Chinese students' homes.",
    "De aarde is de laatste jaren warmer geworden.": "The earth has become warmer in recent years.",
    "Ook het aantal alleenstaande mensen is erg toegenomen.": "The number of single people has also increased a lot.",
    "Ze zijn verliefd geworden en hebben een relatie gekregen.": "They fell in love and got into a relationship.",

    # Additional common sentences
    "Je hoeft ze niet in de kast te zetten.": "You don't have to put them in the cupboard.",
    "Dan hoef je geen afspraak meer te maken met Isa.": "Then you don't have to make an appointment with Isa anymore.",
    "In Nederland zijn heel veel fietsers.": "In the Netherlands there are a lot of cyclists.",
    "Dat duurt nogal lang.": "That takes quite a long time.",
    "Zijn jullie ook dol op dieren?": "Do you love animals too?",
    "Zoeken jullie een oppas voor volgende week?": "Are you looking for a babysitter for next week?",
    "Staat je fiets wel op slot?": "Is your bike locked?",
    "Wat leuk dat je mijn broer bent tegengekomen!": "How nice that you ran into my brother!",
    "Zullen we ook naar het strand gaan?": "Shall we also go to the beach?",
}

# Normalize function to handle minor punctuation/spacing differences
def normalize(text):
    return text.strip().replace('  ', ' ').lower()

# Build normalized lookup
normalized_translations = {normalize(k): v for k, v in translations.items()}

# Update each exercise
matched = 0
unmatched = []

for ex in exercises:
    source = ex.get('source', '').strip()
    norm_source = normalize(source)

    if source in translations:
        ex['english'] = translations[source]
        matched += 1
    elif norm_source in normalized_translations:
        ex['english'] = normalized_translations[norm_source]
        matched += 1
    else:
        ex['english'] = ""  # Mark as unmatched
        unmatched.append(source)

print(f"✓ Matched {matched} out of {len(exercises)} exercises ({matched/len(exercises)*100:.1f}%)")
print(f"✗ Unmatched: {len(unmatched)} exercises")

# Save updated exercises
with open('../calude_suggested_sentence_exercises/dutch_exercises_with_english.json', 'w', encoding='utf-8') as f:
    json.dump(exercises, f, ensure_ascii=False, indent=2)

print(f"\n✓ Saved to dutch_exercises_with_english.json")

if unmatched:
    print(f"\nFirst 10 unmatched sentences:")
    for i, sent in enumerate(unmatched[:10], 1):
        print(f"{i}. {sent}")
