"""
Seed script — populates the SQLite database with:
  • All 20 Rougon-Macquart novels
  • ~58 characters (major protagonists + key family members + important secondaries)
  • Character relations
  • Character ↔ novel appearances
  • Key locations

Run with:  python data/seed.py
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.database import engine, init_db, SessionLocal
from app.models import (
    Novel, Character, CharacterRelation,
    CharacterAppearance, Location, Event, EventCharacter, Quote
)


def run():
    init_db()
    db = SessionLocal()

    # ── Wipe existing data (idempotent re-seed) ─────────────────────────────
    for Model in [EventCharacter, Quote, CharacterAppearance, CharacterRelation,
                  Event, Character, Novel, Location]:
        db.query(Model).delete()
    db.commit()

    # ── NOVELS ──────────────────────────────────────────────────────────────
    novels_data = [
        (1,  "la-fortune-des-rougon",      "La Fortune des Rougon",           "The Fortune of the Rougons",          1871, "Plassans",
         "The founding novel of the cycle, set in the fictional Provençal town of Plassans during the coup d'état of 2 December 1851. Two narratives run in counterpoint: the young lovers Silvère Mouret and Miette Chantegreil join a column of Republican insurgents marching to resist the coup, while Pierre and Félicité Rougon scheme in their 'yellow drawing room' to seize local power by backing the winning side. Zola interrupts the action to trace the dynasty's origins — the neurotic matriarch Adélaïde Fouque, whose marriage to Rougon and passion for the smuggler Macquart create the two great branches of the family, and whose hereditary instability (la fêlure — the crack) will haunt every descendant across all twenty novels. Miette, thirteen years old, carries the red flag at the head of the insurgent column, convinced she is bearing the Virgin's banner in a Corpus Christi procession. Silvère is executed by a gendarme beside the tombstone where he and Miette used to meet. The Rougons triumph; the Republic dies with its children. The cycle's moral architecture is set in its closing pages: Second Empire respectability is built on fraud, betrayal, and the blood of those who actually believed in something.",
         "Roman fondateur du cycle, se déroulant à Plassans lors du coup d'État du 2 décembre 1851. Silvère Mouret et Miette Chantegreil rejoignent les insurgés républicains tandis que Pierre et Félicité Rougon manœuvrent dans leur salon jaune pour s'emparer du pouvoir. Zola retrace les origines de la dynastie : la matriarche névrotique Adélaïde Fouque, dont la fêlure héréditaire hantera tous ses descendants. Miette, treize ans, porte le drapeau rouge en croyant marcher à une procession de la Fête-Dieu. Silvère est fusillé. Les Rougon triomphent."),
        (2,  "la-curee",                   "La Curée",                        "The Kill",                            1871, "Paris",
         "The title comes from the hunting term for the entrails thrown to the hounds after the kill — Zola's image for the speculative frenzy of Haussmann's Paris. Aristide Saccard, born Aristide Rougon, arrives in Paris after the coup and within a few years has transformed himself into one of the city's great property speculators, making a fortune by buying up land in the path of Haussmann's new boulevards before the expropriations are announced. The novel is set in the heart of this world: a lavish hôtel particulier with a tropical hothouse, carriages, jewels, and dinners whose cost would keep a working family for a year. Against this backdrop of artificial excess, Aristide's second wife Renée — a bored, beautiful woman of good family whom he married to cover a scandal — drifts into an affair with his own son Maxime. The incest at the novel's heart is less a moral failure than a symptom: Renée has nothing real to live for, Maxime is incapable of genuine feeling, and Aristide treats both of them — his wife and his son — as assets to be managed. When Renée realises this, it is too late. Zola's Paris in La Curée is pure spectacle, a city that has been demolished and rebuilt as a stage-set for the making and losing of fortunes, and the human lives within it are as disposable as the old houses Saccard buys and tears down.",
         "Le titre renvoie aux entrailles jetées aux chiens après la chasse — image de la spéculation effrénée du Paris haussmannien. Aristide Saccard s'y enrichit en achetant des terrains avant les expropriations. Sa femme Renée, belle et désœuvrée, glisse dans une liaison avec Maxime, le fils d'Aristide. La curée : hommes et femmes traités comme des actifs à gérer, dans un Paris démoli et reconstruit comme décor de fortune."),
        (3,  "le-ventre-de-paris",         "Le Ventre de Paris",              "The Belly of Paris",                  1873, "Paris — Les Halles",
         "Le Ventre de Paris is built on one of Zola's most brilliant structural oppositions: les gras against les maigres — the fat against the thin. Florent Quenu is the thin man, a gentle, idealistic Republican who was swept up in the mass arrests following Napoleon III's coup of 1851 and transported to the penal colony of Cayenne on false evidence. After years of brutal imprisonment he escapes and returns to Paris clandestinely, half-starved, in rags, and barely recognisable. He makes his way to the only family he has: his half-brother Quenu and Quenu's wife Lisa, who run a thriving charcuterie on the edge of Les Halles. The contrast is immediately physical: Quenu is magnificently prosperous, Lisa is white-skinned and opulent behind her marble counter, and the market they live beside is a monument to abundance — Baltard's great iron-and-glass pavilions heaped with every food Paris consumes, Zola's prose luxuriating in page-length inventories of fish, meat, cheese, vegetables, butter, and charcuterie. Into this overwhelming fecundity Florent inserts his angular, fevered, politically inconvenient self. He is given work as a fish inspector — an official role that the market women resent instantly. The artist Claude Lantier — a minor character who will become the tragic hero of L'Œuvre — is present throughout as an observer, the only person who genuinely sees and enjoys the spectacle of the market for what it is, and who introduces Florent to its social layers. The market has its own politics: the fish stalls, the cheese pavilion, the charcuterie — each is a closed world of petty wars, alliances, and gossip. La Normande, a magnificent and arrogant fish seller, becomes Florent's reluctant attraction; her rivalry with Lisa Quenu is one of the novel's running comedies. Florent, characteristically, is too abstracted by Republican dreams to manage either his professional position or his personal life competently. He meets with a small group of other dissidents — their conspiracy amounts to almost nothing, a few heated conversations in back rooms — and Lisa Quenu becomes convinced that his presence in her shop is a threat to everything she has built. She denounces him to the authorities without visible guilt, framing it as her civic duty. Florent is re-arrested and transported again. The fat people have won. The market continues. The closing note belongs to Claude Lantier, who looks at it all and mutters that these comfortable, well-fed people make him sick — then goes back to trying to paint it.",
         "Construit sur l'opposition des gras contre les maigres. Florent, républicain idéaliste revenu du bagne de Cayenne, se retrouve chez son demi-frère Quenu et sa femme Lisa, charcutiers prospères aux Halles. L'abondance écrasante du marché — inventaires minutieux de poissons, viandes, fromages — contraste avec sa maigreur et sa marginalité politique. Lisa le dénonce aux autorités pour préserver leur confort bourgeois. Les gras ont gagné. Claude Lantier observe tout et dégoûté, continue à peindre."),
        (4,  "la-conquete-de-plassans",    "La Conquête de Plassans",         "The Conquest of Plassans",            1874, "Plassans",
         "Abbé Faujas arrives in Plassans with a concealed political mission: the Empire's managers want the traditionally legitimist town to return government-approved deputies at the next elections. His method is a masterpiece of patience — he lodges with the Mouret family (François Mouret and his wife Marthe Rougon, daughter of Pierre and Félicité) under the guise of a humble, pious priest of modest means, then gradually cultivates the religious women of the town through his ostentatious devotion, builds a network of obligation and gratitude that covers the entire social fabric of Plassans, and delivers the vote. He accomplishes his mission. The human cost is the Mouret family. François — a quiet, methodical man whose entire happiness rests on domestic order — finds himself dispossessed room by room of his own house, his wife Marthe drawn away from him into a religious mania that Faujas deliberately intensifies because it is useful to him. She dies broken by what she has been made into. François, committed to the asylum at Les Tulettes (where his grandmother Adélaïde also lives), escapes and burns down the house with Faujas and his sister inside. Félicité Rougon, hearing of the fire from a safe distance, considers the political outcome satisfactory.",
         "L'abbé Faujas arrive à Plassans chargé d'une mission politique secrète : livrer la ville à l'Empire. Il s'installe chez les Mouret, exploite méthodiquement la dévotion de Marthe Rougon jusqu'à la briser, dépossède François Mouret de sa maison et de sa raison. Mission accomplie : Plassans vote pour l'Empire. Prix humain : Marthe meurt, François incendie la maison avec Faujas à l'intérieur. Félicité Rougon juge le bilan politique satisfaisant."),
        (5,  "la-faute-de-labbe-mouret",   "La Faute de l'Abbé Mouret",       "Abbé Mouret's Sin",                   1875, "Provence",
         "La Faute de l'Abbé Mouret is the most lyrical and mythologically ambitious of the twenty novels — a full-scale reimagining of the Fall, Edenic innocence, and the war between flesh and spirit. The novel opens in a state of religious transport: Serge Mouret, the young priest of a sun-baked Provençal village, is conducting mass in an ecstasy of Marian devotion. His faith has the character of an erotic fixation — he is in love with the Virgin with an intensity that Zola explicitly diagnoses as the redirection of suppressed sexual energy. Two characters flank him: Désirée, his simple-minded younger sister, who raises farm animals with pure, unselfconscious delight and represents the body's untroubled relationship with nature; and Frère Archangias, a brutal lay brother of the Brotherhood of the Holy Spirit, who loathes women and sexuality with a violence that is the dark mirror of Serge's sublimation. Serge collapses in a brain fever — caused, in Zola's terms, by the extreme repression of the flesh — and Dr Pascal Rougon is called from Plassans to treat him. Pascal sends him to recover at the home of the old recluse Jeanbernat, who lives at the edge of the vast, overgrown garden called Le Paradou. The Paradou is the novel's great imaginative creation — a seventeenth-century formal garden run entirely wild over a hundred years, so dense with vegetation that it has become a private world. Here Serge recovers without memory of his name, his vows, or his God. Albine — Jeanbernat's niece, who has grown up alone in the Paradou like a creature of the garden itself — nurses him back to health, and the two fall into an Edenic love, living outside of time, gradually discovering the garden's spaces and each other. Zola renders this idyll with extraordinary tenderness and sensory richness: it is, he suggests, what human beings were before the Church made them ashamed of their bodies. The idyll is disrupted when Archangias tracks them down; Serge's memory returns; he is retrieved by his ecclesiastical superior and restored to his parish. What follows is agonising: Serge, now fully restored to his vows, has re-consecrated himself to the Virgin, whom he now treats quite consciously as a substitute for the woman he has renounced. Albine comes to him at the rectory and he turns her away — one of the novel's most painful scenes. She returns to the Paradou and dies there, lying in a sealed room choked with the flowers she has gathered, willing her own death in a manner Zola renders as both mythological and devastatingly human. The final scene reprises the opening exactly: Serge conducting mass in religious transport, the circle closed — at the cost of Albine's life, and at no cost at all to the Church.",
         "Roman lyrique et mythologique du cycle — réécriture de la Chute et de l'Eden. Serge Mouret, prêtre en transport mystique, s'effondre d'une fièvre cérébrale diagnostiquée par le docteur Pascal comme la conséquence du refoulement charnel. Envoyé en convalescence au Paradou — immense jardin sauvage — il se rétablit sans mémoire de ses vœux et tombe amoureux d'Albine, sauvage et lumineuse. Leur idylle edénique est brisée par Frère Archangias ; Serge retrouve la mémoire et renonce à Albine. Elle revient le voir ; il la renvoie. Elle retourne au Paradou et se tue parmi ses fleurs. La dernière scène reprend la première exactement : Serge en transport mystique disant la messe, le cercle refermé."),
        (6,  "son-excellence-eugene-rougon", "Son Excellence Eugène Rougon",  "His Excellency Eugène Rougon",        1876, "Paris",
         "The Rougon-Macquart cycle's great novel of political power, and one of Zola's most analytically precise. Eugène Rougon — eldest Rougon son, now president of the Council of State under Napoleon III — is surrounded by a 'bande' of clients and followers: ambitious provincials, scheming lawyers, social climbers, all hoping proximity to power will yield personal benefits. When he refuses to play the patronage game and bend his office to their private ends, they combine to engineer his fall. When the Emperor needs him back, he returns on his own terms, more powerful than before. Running through the novel as his equal and antagonist is Clorinde Balbi, an Italian adventuress who matches him strategy for strategy — the one person in his world he cannot dismiss. Zola is systematic about how Second Empire political machinery actually works: appointments, honours, favours, the constant performance of loyalty, the cynical distance between public principles and private calculation. Eugène is not corrupt in the simple sense — he does not steal money — but his devotion to power for its own sake makes him, in Zola's moral universe, the most complete expression of the Empire's values. The novel ends with him back in his ministerial chair, his followers reinstated, nothing changed. It is one of Zola's most controlled and purposefully cold books.",
         "Roman du pouvoir politique pur. Eugène Rougon, président du Conseil d'État, voit sa 'bande' de fidèles le trahir quand il refuse de faire jouer ses relations en leur faveur. Il tombe, puis revient au pouvoir plus fort qu'avant. Face à lui, Clorinde Balbi, aventurière italienne, son égale en ambition et en intelligence. Zola dissèque les mécanismes du Second Empire avec une froideur analytique implacable."),
        (7,  "lassommoir",                 "L'Assommoir",                     "The Dram Shop",                       1877, "Paris — Goutte d'Or",
         "L'Assommoir is the masterpiece of French Naturalism and one of the great novels of any language about poverty, alcoholism, and the mechanics of moral collapse. Gervaise Macquart arrives in Paris from Plassans as a young woman with her partner Lantier and their two small sons Claude and Étienne, lodging in a cheap hotel in the Goutte d'Or district of northern Paris. When Lantier abandons her for another woman, she is left alone with no money and two children, and proceeds — without drama, steadily, simply by working hard — to build a decent life. She finds work in a laundry; she falls in love with the roofer Coupeau, a good-natured man with steady habits; she marries him. For a few years it works: she opens her own laundry in the Rue Neuve de la Goutte d'Or, she has credit, friends, and the brief, real happiness of a working-class person who has achieved what she wanted. The famous birthday feast — a roast goose, the laundry table crowded with neighbours — is the novel's high-water mark and, in retrospect, the beginning of the end. The turning point is Coupeau's fall from a rooftop. He survives, but the long convalescence — during which Gervaise works double to support them, and Coupeau drinks to manage the boredom and the pain — starts the process that will kill them both. Lantier reappears, with his terrible ease and his endless appetite, and installs himself in their apartment as a lodger who pays nothing and costs everything. The laundry fails. Gervaise begins to drink. Coupeau's alcoholism deepens into something physical and then terminal — his death in the Sainte-Anne asylum from delirium tremens is one of Zola's greatest pieces of controlled horror: the body betraying itself, the room full of voices. Gervaise's death is worse: she starves and deteriorates by inches, ending her days in the stairwell of the same building where she once had a prosperous shop, living under the stairs like vermin. The novel was revolutionary not only in subject but in style — written largely in the slang and register of the working class, a formal choice that scandalized literary Paris and made Zola rich. Nana is a child in the background: the next generation already in formation.",
         "Chef-d'œuvre du naturalisme français. Gervaise Macquart construit patiemment une vie honnête à la Goutte d'Or après l'abandon de Lantier — launderie, mariage avec Coupeau, bonheur ouvrier réel. La chute de Coupeau d'un toit commence la descente : alcoolisme, retour de Lantier parasite, faillite de la boutique, misère progressive. Coupeau meurt de delirium tremens à Sainte-Anne dans une scène d'horreur physique contrôlée. Gervaise meurt de faim dans la cage d'escalier de son immeuble. Roman écrit en argot ouvrier — choix formel révolutionnaire. Nana grandit dans le fond du tableau."),
        (8,  "une-page-damour",            "Une Page d'amour",                "A Love Episode",                      1878, "Paris",
         "Une Page d'amour is the most formally elegant of the twenty novels — a precisely constructed study in how a single contained passion, long suppressed, can undo a carefully built life. The novel is structured around five panoramic views of Paris seen from the heights of Passy, one at the opening of each of the five sections, in different seasons and at different times of day. Paris is not metaphor here so much as witness: the city watches what is happening to Hélène with the magnificent indifference of a permanent backdrop. Hélène Grandjean — née Mouret, daughter of Ursule Macquart — is a widow of thirty, living with her daughter Jeanne in a quiet apartment in Passy. She has an enormous capacity for self-containment. She is not cold: she is disciplined. Her whole life is ordered around Jeanne, a sensitive and somewhat sickly child who loves her mother with a jealous intensity that borders on the erotic. The love affair develops slowly, against Hélène's will, with her neighbour Dr Henri Deberle — a fashionable, charming, ultimately rather superficial Paris physician. She resists for most of the novel; her fall, when it comes, is therefore all the more devastating. The crisis arrives in a single night: Jeanne has fallen acutely ill; Dr Deberle's wife is absent; Hélène and Deberle are alone in the apartment above Jeanne's sickroom. Hélène abandons her daughter's bedside and goes to him. What follows is never described directly — Zola leaves the hours of the night unmarked. But Jeanne, downstairs, is left in the care of a servant; the cold she contracts that night, and the emotional abandonment she intuits from her mother (Jeanne understands things she should not be old enough to understand), begins the process that kills her. Jeanne dies weeks later — in a scene of great formal beauty and complete moral devastation, as Hélène holds the child she has destroyed by the one act of self-abandonment in an otherwise impeccably controlled life. Deberle, faced with the consequences of what has passed between them, retreats smoothly into his ordinary life. Hélène leaves Paris, marries a respectable widower in a provincial town, and settles into an existence that is entirely without interior life. Zola appends a final scene — she returns to Paris once, years later, looks at it from the heights of Passy, and turns away.",
         "Roman formellement élaboré : cinq panoramas de Paris — un par partie — regardent la passion d'Hélène avec une indifférence de témoin éternel. Hélène Grandjean, veuve disciplinée de Passy, résiste longtemps à l'amour du docteur Deberle. La nuit décisive : Jeanne est gravement malade, Hélène abandonne son chevet pour Deberle. Jeanne meurt — du froid contracté ce soir-là et de l'abandon qu'elle a compris. Hélène quitte Paris, se remarie convenablement, vit sans vie intérieure. Elle revient une fois, regarde Paris de loin, et repart."),
        (9,  "nana",                       "Nana",                            "Nana",                                1880, "Paris — theatre world",
         "Nana opens with one of the great theatrical set-pieces in French fiction: Anna Coupeau, eighteen years old and entirely without talent, appears on stage at the Théâtre des Variétés as the Golden Venus in a mythological revue. She cannot act, cannot sing, and the audience knows it — but her body electrifies every man in the house, and Zola makes clear that what is happening in the theatre is a collective experience of desire that bypasses reason entirely. From this beginning, the novel follows Nana through eight years of the Second Empire's demi-monde: the succession of apartments (each grander than the last, until the mansion on the Avenue de Villiers), the succession of men, the succession of fortunes devoured. The novel's great male victim is Count Muffat de Beuville, the rigidly moral court chamberlain and devout Catholic who becomes Nana's most thoroughly destroyed admirer — Zola's central political allegory: the Empire's governing class, outwardly virtuous and inwardly rotten, hollowed out by the very licence it publicly condemns. Nana does not hate Muffat; she is curious about him, bored by him, occasionally cruel without malice. She has no particular philosophy of destruction — she simply takes what is offered, and men offer themselves. The exception to this passivity is Fontan — a rough, unsuccessful actor she falls for and lives with in a tiny apartment in a moment of genuine feeling; he beats her, she stays; the relationship illuminates what desire costs her as opposed to what it costs her patrons. Count de Vandeuvres, another ruin, burns himself alive after a race-track fraud. Georges Hugon, a boy she is genuinely fond of, stabs himself when she refuses him. She barely notices her son Louiset, who dies while she is abroad. In the final pages, Nana returns to Paris to visit the child who is already dead; she contracts smallpox from him; she is locked in a hotel room and dies there — the magnificent face destroyed, the body reduced to something her admirers cannot look at. The last thing heard in the novel is the crowd in the street below chanting 'À Berlin! À Berlin!' — the Second Empire plunging into the war that will end it. The connection is not metaphor; it is Zola's thesis: Nana is what this civilisation grew.",
         "Nana s'ouvre sur un triomphe théâtral paradoxal : Anna Coupeau, sans talent, électrise la salle par son seul corps. Suit sa trajectoire à travers la demi-mondaine du Second Empire : appartements de plus en plus luxueux, hommes de plus en plus ruinés. Le comte Muffat, chambellan moral et rigide, est sa victime centrale — allégorie de la classe dirigeante impériale creusée par le vice qu'elle condamne. Fontan, acteur raté, est l'exception : Nana l'aime et il la bat. Vandeuvres se suicide, Hugon se poignarde. Nana meurt de la variole dans une chambre fermée, le visage détruit, tandis que la foule crie 'À Berlin !' — l'Empire s'effondre avec elle."),
        (10, "pot-bouille",                "Pot-Bouille",                     "Pot Luck",                            1882, "Paris — bourgeois apartment",
         "Octave Mouret — son of François and Marthe Mouret, arriving from the south with provincial charm and undisguised ambition — takes a room in a gleaming bourgeois apartment building on the Rue de Choiseul. The building's white marble staircase and impeccable facade present the image of respectable middle-class life; behind every door, Zola systematically reveals, there is adultery, hypocrisy, cupidity, and cruelty that its occupants would die rather than acknowledge. Octave both observes and participates: he pursues several of the building's wives (Berthe Josserand, the feckless daughter of an ambitious bourgeois family, becomes his main entanglement), edges his way upward professionally through the drapery shop on the ground floor, and ultimately emerges ready to take over the shop across the street that will become Au Bonheur des Dames. Zola's satire of the bourgeoisie in Pot-Bouille is without mercy: these families are, in his view, no better morally than the working-class characters of L'Assommoir — they simply cover their identical vices with a veneer of respectability and call it virtue. The servants who gather in the internal courtyard — who hear everything through the walls, see everything on the stairs — provide the novel's darkest and funniest commentary.",
         "Octave Mouret arrive à Paris du Midi et s'installe dans un immeuble bourgeois de la rue de Choiseul. La façade blanche cache un monde d'adultères, d'hypocrisies et de calculs sordides. Octave observe et participe — plusieurs liaisons, ascension professionnelle — et en sort prêt à bâtir Au Bonheur des Dames. Satire impitoyable : la bourgeoisie cache exactement les mêmes vices que les ouvriers de L'Assommoir, mais les appelle vertu."),
        (11, "au-bonheur-des-dames",       "Au Bonheur des Dames",            "The Ladies' Delight",                 1883, "Paris — department store",
         "Au Bonheur des Dames is Zola's great novel of modern capitalism, and also — unexpectedly — one of the most generously ambivalent books he wrote. Octave Mouret, having served his apprenticeship in the bourgeois apartment building of Pot-Bouille, has taken over and transformed the department store he inherited from his first wife. What he is building is something genuinely new: the first modern mass-market retail operation in Paris, inspired by Le Bon Marché and the Grands Magasins du Louvre, but expanded beyond anything that has existed before. Mouret is a genius of consumption. He understands female desire — he says so, and Zola does not entirely disagree — and he builds the store as a machine for exploiting it: fixed prices (the end of haggling, the democratisation of luxury), seasonal sales engineered to manufacture desire and urgency, goods arranged to create temptation at every turn, the pleasure of spending raised to an aesthetic experience. The store expands relentlessly through the novel, buying up and demolishing the surrounding buildings, including eventually the old linen shop of Denise Baudu's uncle, who watches his livelihood disappear across the street in real time. Zola is not simple about this: he does not pretend the old world of the small draper was admirable. Baudu is rigid, paternalistic, and doomed not only by Mouret but by time itself. The store's working conditions are another matter — employees are surveilled, underpaid relative to their effort, dismissed for the slightest infraction, housed in dormitories, their private lives controlled. Into this world arrives Denise Baudu, from Valognes in Normandy, with no connections and two younger brothers to support. She is taken on without enthusiasm, fired for a minor infraction, scrapes through a desperate period, and comes back. She rises on merit alone — not beauty (she is not considered beautiful), not manipulation, not the use of her sex. Mouret offers her everything: a director's position, money, his desire. She refuses all of it until he can offer something he has never offered any woman: genuine love and marriage. Bourdoncle — Mouret's cold, brilliant business partner — advises against her throughout, seeing sentiment as a fatal weakness. He is not entirely wrong. The novel ends with the store at its most triumphant expansion, Denise promoted to a directorship and about to marry Mouret — a conclusion that Zola renders with genuine warmth and without irony. The store has ruined Baudu. It will ruin others. But the old ways were not better; progress is real, even when its mechanism is merciless.",
         "Grand roman du capitalisme moderne. Octave Mouret bâtit un magasin-machine à exploiter le désir féminin : prix fixes, soldes manufacturés, séduction systématique. Le magasin s'agrandit et écrase les petits commerçants, dont l'oncle Baudu de Denise Baudu. Denise, vendeuse normande sans protection, monte par son seul mérite. Mouret lui offre argent, poste, désir — elle refuse tout jusqu'à ce qu'il lui offre un amour sincère. Bourdoncle, associé rationnel, déconseille tout sentiment. Zola n'est pas simple : les vieux commerces n'étaient pas admirables, le progrès est réel même quand il est impitoyable. Fin heureuse, ambivalente."),
        (12, "la-joie-de-vivre",           "La Joie de vivre",                "The Bright Side of Life",             1884, "Normandy coast",
         "La Joie de vivre is the most philosophically explicit of the twenty novels — a sustained confrontation between two worldviews set on the edge of the sea in a Norman fishing village. Pauline Quenu, the daughter of Lisa Quenu the charcutière, arrives at the Chanteau household in Bonneville as an orphan of ten, bringing her inheritance — some 85,000 francs — and an instinctive, unkillable generosity. The Chanteau household needs money and gets it: old Chanteau is immobilised by gout, one of Zola's most carefully rendered depictions of chronic physical suffering; his wife Véronique is avaricious and calculating, steadily finding ways to redirect Pauline's money to family uses. Lazare — the Chanteaus' son, Pauline's age, brilliant and restless — is the novel's great study in Schopenhauerian pessimism. He has read Schopenhauer and adopted the philosopher's worldview with the wholehearted enthusiasm of a young man who has found an intellectual framework for his anxiety: life is suffering, the will is the source of misery, annihilation is the only release. He is genuinely terrified of death — the terror visits him in the night, physical and specific — and his philosophy, rather than providing comfort, provides merely a language for the terror. He conceives grand schemes: a chemical factory to process seaweed into industrial products; a great timber seawall to protect Bonneville from the sea's storms. Each scheme collapses. The money spent on them is largely Pauline's. She watches, understands, and continues to give — not from weakness or illusion but from a clear-eyed choice that this is what she is for. Lazare eventually marries Louise Thibaudier, a conventional, pretty girl with no money: Pauline watches this too, accepts it, and raises Lazare's child when Louise dies in childbirth. The novel ends quietly: the sea still batters the unprotected village, the seawall has long since collapsed, Lazare leaves for Paris with his son, old Chanteau still suffers — and Pauline, stripped of most of what she had, is still there, still choosing life. Zola's answer to Schopenhauer is not argument but example.",
         "Roman le plus philosophiquement explicite du cycle : confrontation entre le pessimisme schopenhauerien de Lazare et la joie de vivre instinctive de Pauline. Bonneville, village normand au bord d'une mer qui bat sans cesse. Pauline, héritière généreuse, soutient les Chanteau alors qu'ils dilapident ses fonds. Lazare construit des projets qui échouent tous, épouse Louise, laisse Pauline élever son enfant. Pauline reste — dépouillée de presque tout, toujours vivante. La réponse de Zola à Schopenhauer n'est pas un argument mais un exemple."),
        (13, "germinal",                   "Germinal",                        "Germinal",                            1885, "Northern coalfields",
         "Étienne Lantier arrives at the Voreux mine and leads the miners in a great strike against the Company. The most politically powerful novel in the series — and one of the greatest novels ever written about class and labour.",
         "Étienne Lantier mène les mineurs de Voreux dans une grande grève. L'œuvre la plus politiquement puissante de la série."),
        (14, "loeuvre",                    "L'Œuvre",                         "The Masterpiece",                     1886, "Paris — art world",
         "L'Œuvre is a novel of artistic failure — the most painful subject Zola could have chosen, given his lifelong friendship with the generation it portrays. Claude Lantier, the painter-son of Gervaise Macquart, is clearly modelled on Paul Cézanne, with elements of Édouard Manet and others; his friends are equally recognisable to anyone who knows the period: Sandoz the novelist is Zola himself, Dubuche the architect, Fagerolles the painter who succeeds by compromising. The novel opens with Claude in his studio on the Île de la Cité, working on a vast canvas of Paris seen from the Seine, centred on a reclining female nude — the figure that becomes his obsession and his destruction. He meets Christine Halleguen, she poses for him, they fall in love, they marry, they have a son. Claude's inability to finish the central painting does not diminish; it worsens. Every revision leaves the canvas more charged with his need and less coherent as a work of art. The nude at its centre becomes increasingly abstract, increasingly his, increasingly divorced from any woman, including Christine. Their son Jacques dies — an event Zola renders in close parallel to Claude's relationship with the painting: the dead child as failed creation, the artist who cannot give life to either. Christine watches Claude choose the painting over everything, including her, and eventually their marriage becomes a practical pretense. Claude hangs himself before the canvas — found dead by Christine in the morning, the painting behind him still unfinished. Sandoz speaks the novel's closing words: a farewell to Claude that is also a reckoning with what ambition of this kind costs. The novel permanently damaged Zola's friendship with Cézanne, who read it as a verdict on his own failure and never forgave it.",
         "Roman de l'échec artistique. Claude Lantier, peintre fils de Gervaise, poursuit une toile géante — Paris depuis la Seine, nu central — qui ne se laisse jamais finir. La toile absorbe tout : Christine sa femme, leur fils Jacques mort en bas âge, sa propre santé mentale. Sandoz — l'alter ego de Zola — assiste à la destruction de son ami. Claude se pend devant la toile inachevée. Le roman blessa définitivement l'amitié de Zola avec Cézanne."),
        (15, "la-terre",                   "La Terre",                        "The Earth",                           1887, "Beauce — wheat country",
         "Jean Macquart, working as a farm labourer in the Beauce, witnesses the brutal, elemental life of the French peasantry — a world of land-hunger, violence, lust, and an almost geological attachment to the soil.",
         "Jean Macquart, ouvrier agricole en Beauce, observe la vie brutale et élémentaire des paysans français."),
        (16, "le-reve",                    "Le Rêve",                         "The Dream",                           1888, "Cathedral town",
         "The most deliberately gentle of the twenty novels — Zola wrote it as a conscious respite after the violence of Germinal. Angélique is an orphan of obscure birth (she is, though the novel does not stress it, a Rougon by blood) who has been taken in by Hubert and Hubertine, elderly embroiderers living in the shadow of a great Gothic cathedral in a provincial town. She grows up entirely on a diet of hagiographies — the Légende Dorée, the lives of the saints — and constructs her inner world from them, overlaying everything she sees with the luminous imagery of the books she loves. When the handsome, aristocratic Félicien de Hautecœur appears — the son of the local bishop Monseigneur de Hautecœur — she falls in love with a figure who seems to have stepped directly out of her legends. Zola traces with great delicacy the collision between the world of religious dream and the world of material fact: the bishop refuses to consent to their marriage (Angélique's obscure birth makes it impossible in his view); she falls dangerously ill; in the end the bishop relents and blesses her, she recovers, they marry — and she dies on the church steps immediately after the ceremony, as if the dream, once made real in the material world, has no further substance. Le Rêve is the cycle's one unambiguously happy ending, which is also an ending.",
         "Le roman le plus tendre du cycle, écrit comme respiration après Germinal. Angélique, orpheline recueillie par des brodeurs au pied d'une cathédrale, grandit dans la Légende Dorée et les vies de saints. Elle tombe amoureuse de Félicien de Hautecœur, fils du monseigneur local, qui semble sorti de ses lectures. Son père refuse le mariage, Angélique dépérit, mais finit par être bénie et épouse Félicien — et meurt sur les marches de l'église, comme si le rêve réalisé n'avait plus de substance. La seule fin heureuse du cycle."),
        (17, "la-bete-humaine",            "La Bête humaine",                 "The Beast Within",                    1890, "Paris–Le Havre railway",
         "Jacques Lantier, train driver on the Paris-Le Havre line, harbours a murderous impulse towards women that he can barely control. Love, murder, and the thundering locomotive on the iron road.",
         "Jacques Lantier, mécanicien de locomotive, lutte contre son désir meurtrier envers les femmes. Amour, meurtre et train."),
        (18, "largent",                    "L'Argent",                        "Money",                               1891, "Paris — the Bourse",
         "Zola's great novel of financial capitalism. Aristide Saccard — having lost his first fortune in the ruins of La Curée — returns to Paris and founds the Universal Bank on the basis of his engineer friend Georges Hamelin's genuine projects: railways into the Ottoman Empire, agricultural schemes in the Levant, a Catholic establishment in the Holy Land. The projects are real; the problem is that Saccard inflates the stock far beyond any rational valuation, manipulating the price upward through planted rumour and engineered confidence, attracting tens of thousands of small investors — widows, working women, retired tradespeople — whose savings he pours into a machine designed to enrich himself. The bank soars, then collapses with devastating violence, ruining its shareholders. Caroline Hamelin, who has become Saccard's mistress while watching his operation with lucid moral disquiet, survives the disaster with her dignity and most of her judgment intact; her brother Hamelin returns from the Orient to find his genuine work buried under rubble. Saccard is arrested and eventually escapes consequences almost entirely. Zola does not make it simple: the novel holds a genuine paradox — Saccard's own argument that speculation is the engine of progress, that without fever nothing great would be built, is given enough force that it cannot be simply dismissed. It is one of Zola's most intellectually demanding novels.",
         "Roman du capitalisme financier. Saccard, ayant perdu sa première fortune, fonde la Banque universelle sur les vrais projets de l'ingénieur Hamelin : chemins de fer ottomans, établissements en Orient. Il en fait une machine spéculative, attire des milliers de petits épargnants, fait monter le cours artificiellement, puis tout s'effondre. Caroline Hamelin, sa maîtresse et conscience morale du roman, s'en sort intacte. Saccard échappe aux conséquences. Zola pose la question : la spéculation est-elle la condition du progrès ?"),
        (19, "la-debacle",                 "La Débâcle",                      "The Debacle",                         1892, "Franco-Prussian War",
         "Jean Macquart and Maurice Levasseur fight together in the catastrophic Franco-Prussian War of 1870 — Sedan, the siege of Paris, the Commune. The destruction of the Second Empire witnessed from the trenches.",
         "Jean Macquart combat dans la désastreuse guerre franco-prussienne de 1870 — Sedan, le siège de Paris, la Commune."),
        (20, "le-docteur-pascal",          "Le Docteur Pascal",               "Doctor Pascal",                       1893, "Plassans",
         "Dr Pascal Rougon, the scientific conscience of the series, has spent his life cataloguing the family's hereditary history. In his last years he falls in love with his niece Clotilde. The final summing-up of the entire cycle.",
         "Le docteur Pascal Rougon a consacré sa vie à cataloguer l'hérédité familiale. Bilan final de tout le cycle."),
    ]

    novels = {}
    for row in novels_data:
        n = Novel(
            number=row[0], slug=row[1], title_fr=row[2], title_en=row[3],
            year=row[4], setting=row[5], summary_en=row[6], summary_fr=row[7]
        )
        db.add(n)
        db.flush()
        novels[row[1]] = n

    # Novel illustrations (local static files)
    novels["la-fortune-des-rougon"].image_url = "/static/images/novels/la-fortune-des-rougon.png"
    novels["la-fortune-des-rougon"].image_credit = "Engraving from the Vizetelly English translation (1886) — Public domain"

    # ── CHARACTERS ──────────────────────────────────────────────────────────
    # Dict keys: slug, name, birth_name, occupation, branch, generation,
    #            description_en, description_fr, physical_en,
    #            featured_on_landing, tree_x, tree_y, image_url, image_credit
    chars_data = [

        # ── GENERATION 0 ────────────────────────────────────────────────────
        {
            "slug": "adelaide-fouque",
            "name": "Adélaïde Fouque",
            "occupation": "Matriarch / 'Tante Dide'",
            "branch": "macquart",
            "generation": 0,
            "image_url": "/static/images/characters/adelaide.jpg",
            "image_credit": "Théodore Géricault, 'La monomane de l'envie' (c. 1820) — Public domain",
            "description_en": "The neurotic, visionary matriarch of the entire dynasty, born in 1768. Her marriage to the peasant Rougon produces one legitimate son, Pierre; her passionate liaison with the smuggler Macquart produces Antoine and Ursule, creating the two great branches of the family. What Zola calls la fêlure — the crack — runs from Adélaïde through every one of her descendants: a hereditary nervous instability that manifests as madness in some, alcoholism in others, violent passion or artistic obsession in others still. She raises her grandson Silvère after his mother Ursule's death, and it is she who witnesses his execution during the 1851 coup — raving 'le prix du sang!' (the price of blood!) as he is shot. She is immediately committed to the lunatic asylum at Les Tulettes near Plassans, where she lives on for more than twenty years in a deepening stupor, visited occasionally by Dr Pascal and others. She is still alive in Le Docteur Pascal, over a hundred years old, a hollow-eyed relic of the dynasty's founding sin.",
            "description_fr": "Matriarche névrotique née en 1768. Son mariage avec Rougon et sa liaison avec Macquart créent les deux branches familiales. La fêlure héréditaire qu'elle transmet se manifeste différemment chez chacun de ses descendants. Elle assiste à l'exécution de son petit-fils Silvère en 1851 et est aussitôt internée aux Tulettes, où elle vivra plus de vingt ans dans un état de stupeur croissante.",
            "physical_en": "Gaunt, pallid, with wide staring eyes and a fixed, otherworldly expression — the family's mark of nervous instability made visible in its source. In her extreme old age she sits motionless for hours, then erupts without warning into a fit of shuddering that seems to pass through her whole body.",
            "featured_on_landing": True, "tree_x": 550, "tree_y": 80,
        },

        # ── GENERATION 1 ────────────────────────────────────────────────────
        {
            "slug": "pierre-rougon",
            "name": "Pierre Rougon",
            "occupation": "Bourgeois landowner, politician",
            "branch": "rougon",
            "generation": 1,
            "description_en": "The legitimate son of Adélaïde. Cunning, cold, and entirely self-interested, Pierre had already cheated his mother and half-siblings out of their inheritance before the events of La Fortune des Rougon begin. During the coup of December 1851 he manoeuvres himself into political power in Plassans — rallying a token band of forty-one men, seizing the empty town hall, and presenting himself as the city's saviour after the real fighting is already over. The 'yellow drawing room' that he and Félicité keep is the nerve centre of Plassans's conservative establishment. He is rewarded with the Legion of Honour and a promise of preferment from Paris. He is the founder of the respectable Rougon line — a man who has always known exactly what he wants and has never had a scruple about how he gets it.",
            "description_fr": "Fils légitime d'Adélaïde. Après avoir floué sa mère et ses demi-frères de leur héritage, Pierre s'empare du pouvoir politique à Plassans lors du coup d'État de 1851 avec quarante et un hommes. Récompensé par la Légion d'honneur, il incarne l'opportunisme bourgeois triomphant.",
            "physical_en": "Heavy-set, ruddy complexion, with the calculating eyes of a man who has never acted without self-interest.",
            "featured_on_landing": True, "tree_x": 280, "tree_y": 210,
        },
        {
            "slug": "felicite-rougon",
            "name": "Félicité Rougon",
            "birth_name": "Félicité Puech",
            "occupation": "Bourgeoise, social climber",
            "branch": "rougon",
            "generation": 1,
            "description_en": "Pierre's sharp, energetic wife — and the real intelligence behind the Rougon ascent. It is Félicité who understands that in provincial France, reputation and timing matter more than courage or talent; who cultivates the right connections in the yellow drawing room; who engineers the story that reaches Paris after the coup. From a modest enough background herself (daughter of a small-time oil merchant), she has made the family's ambition entirely her own. More than any other character in the cycle she survives: she outlives almost everyone, witnesses the whole drama from Plassans across twenty years of Second Empire, and in Le Docteur Pascal she is still there — still scheming, still enjoying the triumphs of her children and grandchildren.",
            "description_fr": "Femme de Pierre et véritable architecte de l'ascension Rougon. C'est elle qui comprend que dans la province française, la réputation et le moment comptent plus que le courage. Elle cultive les bonnes relations dans leur salon jaune et survit à presque tous les membres de la saga.",
            "physical_en": "Small, dark, quick-eyed, with the restless energy of someone who is always scheming.",
            "featured_on_landing": True, "tree_x": 160, "tree_y": 210,
        },
        {
            "slug": "ursule-macquart",
            "name": "Ursule Macquart",
            "occupation": "Seamstress",
            "branch": "mouret",
            "generation": 1,
            "description_en": "The younger illegitimate daughter of Adélaïde by Macquart. She inherited her mother's nervous temperament but also a gentler, artistic strain. She married a hatter named Mouret and died young, leaving three children — François, Hélène, and Silvère — who carry the Mouret name and the family's hereditary burden into a third branch of the dynasty.",
            "description_fr": "Fille illégitime cadette d'Adélaïde et de Macquart. Elle épousa un chapelier nommé Mouret et mourut jeune, laissant trois enfants qui fondèrent la branche Mouret.",
            "physical_en": "Gentle-looking, with her mother's pallor softened into something almost luminous, and the family's nervous hands.",
            "featured_on_landing": False, "tree_x": 630, "tree_y": 210,
        },
        {
            "slug": "antoine-macquart",
            "name": "Antoine Macquart",
            "occupation": "Drunkard, small trader, former soldier",
            "branch": "macquart",
            "generation": 1,
            "image_url": "/static/images/characters/antoine-macquart.png",
            "image_credit": "Engraving from the Vizetelly English translation of La Fortune des Rougon (1886) — Public domain",
            "description_en": "The illegitimate son of Adélaïde by the smuggler Macquart. Bitter, idle, and alcoholic, he embodies the hereditary vice of the Macquart line — the same tainted blood that produces genius in one descendant and madness in another here producing mere rancour and dissolution. He served in the army and came back with nothing except a sense of grievance against the Rougons, who have inherited the family property while he has inherited only his father's vices. Father of Lisa, Gervaise, and Jean, he treats his family as a resource to be exploited and abuses his long-suffering wife Joséphine for decades. His resentment of Pierre Rougon's prosperity is one of the cycle's persistent bass notes. He dies a gruesome but darkly comic death in La Terre — spontaneously combusting after a life of near-pure alcohol.",
            "description_fr": "Fils illégitime d'Adélaïde et du braconnier Macquart. Alcoolique et rancunier, il incarne le vice héréditaire. Père de Lisa, Gervaise et Jean, il meurt d'une combustion spontanée dans La Terre.",
            "physical_en": "Slouching, sallow, with reddened nose and the loose gestures of a habitual drinker.",
            "featured_on_landing": True, "tree_x": 820, "tree_y": 210,
        },
        {
            "slug": "josephine-macquart",
            "name": "Joséphine Macquart",
            "birth_name": "Joséphine Gavaudan",
            "occupation": "Laundress",
            "branch": "macquart",
            "generation": 1,
            "description_en": "Wife of Antoine Macquart. A hard-working, long-suffering laundress who bears Antoine's abuse and alcoholism with stoic endurance, raising their three children largely alone. She is the quiet, decent counterweight to Antoine's chaos.",
            "description_fr": "Épouse d'Antoine Macquart. Lingère courageuse et patiente, elle endure les violences de son mari et élève leurs trois enfants.",
            "physical_en": "Worn, patient-faced, with strong hands roughened by years of washing.",
            "featured_on_landing": False, "tree_x": 950, "tree_y": 210,
        },

        # ── GENERATION 2 — Rougon children ──────────────────────────────────
        {
            "slug": "eugene-rougon",
            "name": "Eugène Rougon",
            "occupation": "Minister of State, politician",
            "branch": "rougon",
            "generation": 2,
            "description_en": "The eldest Rougon son and the most purely political animal in the cycle. Where his brother Aristide craves money and his brother Pascal craves knowledge, Eugène craves power — and power only. He has no programme, no ideology, no convictions: he wants to govern because governing is the one activity in which his exceptional temperament finds full expression. He was in Paris manoeuvring from the very night of the 1851 coup, having orchestrated his family's provincial triumph in Plassans from a distance. He rises to become president of the Council of State and then a minister — one of the most powerful men in Napoleon III's empire — surrounded by a 'bande' of clients who need his favour and whom he regards with contemptuous clarity. He falls from office when he refuses to bend his position to their private ends, then returns more powerful than before. His most worthy opponent is Clorinde Balbi, the Italian adventuress whom he almost loves and who consistently outmanoeuvres him at the moments that matter. He reappears in Le Docteur Pascal still in office, still untouched, a monument to the proposition that the machinery of power outlasts every individual who operates it.",
            "description_fr": "Fils aîné des Rougon, il n'aspire qu'au pouvoir pour lui-même, sans idéologie ni conviction. Montant à Paris dès le coup d'État de 1851, il devient président du Conseil d'État puis ministre. Sa bande de clients — qu'il méprise avec lucidité — le trahit quand il refuse de leur accorder des faveurs. Il tombe, revient plus puissant. Face à lui, Clorinde Balbi, son égale qu'il n'arrive jamais à dominer complètement.",
            "physical_en": "Tall, massive, with a large head and the slow, deliberate movements of a man accustomed to dominating every room he enters. His bulk is itself a political instrument — he speaks rarely, moves slowly, and lets his physical presence do the work that lesser men do with words.",
            "featured_on_landing": True, "tree_x": 120, "tree_y": 370,
        },
        {
            "slug": "aristide-saccard",
            "name": "Aristide Saccard",
            "birth_name": "Aristide Rougon",
            "occupation": "Speculator, financier",
            "branch": "rougon",
            "generation": 2,
            "description_en": "Born Aristide Rougon, he changed his name to Saccard — a name that suggests 'sac d'or', a bag of gold — to shed his provincial origins and reinvent himself. He is the cycle's great capitalist: feverish, brilliant, amoral, and capable of rising from every ruin he creates. His first great fortune comes from speculating on property in the path of Haussmann's demolitions, buying condemned buildings at low prices just before the expropriations are announced. He treats his second wife Renée as he treats his properties — as an asset whose value he has calculated and whose eventual depreciation he has already planned for. His son Maxime he treats similarly. In L'Argent he returns for a second round of speculation, building the vast Universal Bank almost from nothing, inflating it to extraordinary heights, and crashing it in a ruin that takes thousands of investors with him. He escapes. He always escapes. Zola renders him with something close to fascinated horror: Saccard is destructive, dishonest, and ruinous to everyone around him, and yet there is an energy in him — a sheer animal vitality — that makes him one of the most compelling presences in the cycle.",
            "description_fr": "Né Aristide Rougon, il se rebaptise Saccard pour effacer ses origines. Spéculateur génial et amoral, il fait sa première fortune sur les expropriations haussmanniennes, traite sa femme Renée comme un actif, puis reconstruit une immense banque dans L'Argent avant de la couler. Il sort toujours des ruines qu'il crée — personnage fascinant d'énergie destructrice.",
            "physical_en": "Small, wiry, with quick gestures and bright, feverish eyes always scanning for the next opportunity. He has the electric restlessness of a man for whom stillness is physically painful.",
            "featured_on_landing": True, "tree_x": 270, "tree_y": 370,
        },
        {
            "slug": "pascal-rougon",
            "name": "Dr Pascal Rougon",
            "occupation": "Physician, scientist",
            "branch": "rougon",
            "generation": 2,
            "description_en": "The humane, idealistic scientist of the family. Pascal spends his life studying heredity and compiling secret dossiers on every family member. He is the moral conscience of the cycle — a man of science who believes in progress, love, and life. His final novel, told in part through his eyes, is the cycle's summation.",
            "description_fr": "Savant idéaliste de la famille. Pascal consacre sa vie à étudier l'hérédité et à compiler des dossiers sur chaque membre de la famille. Conscience morale du cycle.",
            "physical_en": "White-haired, gentle-eyed, with the absorbed look of a man perpetually lost in thought and the warm hands of a good doctor.",
            "featured_on_landing": True, "tree_x": 400, "tree_y": 370,
        },
        {
            "slug": "sidonie-rougon",
            "name": "Sidonie Rougon",
            "occupation": "Commission agent, go-between",
            "branch": "rougon",
            "generation": 2,
            "description_en": "A shadowy, androgynous figure who acts as a fixer and go-between across Paris society. She facilitates dubious arrangements for her brothers' ambitions, disappears from the narrative as quietly as she enters it, and eventually ends up running a convent school in a distant city.",
            "description_fr": "Figure androgyne et énigmatique qui sert d'intermédiaire dans la société parisienne. Elle facilite les arrangements douteux de ses frères.",
            "physical_en": "Thin, colourless, dressed in black, with the discreet manner of someone who moves through society unseen.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },
        {
            "slug": "marthe-rougon",
            "name": "Marthe Rougon",
            "occupation": "Housewife, religious devotee",
            "branch": "rougon",
            "generation": 2,
            "description_en": "Daughter of Pierre and Félicité Rougon, married to her cousin François Mouret. She carries the family's hereditary nervous instability — the fêlure from Adélaïde — in the form of an intense, slightly uncontrollable religious temperament. Before her marriage she was genuinely devout but manageable; her life with François, quiet and domestic, has suppressed it. Abbé Faujas recognises immediately what she is and what use can be made of it: he cultivates her religious devotion systematically, drawing her into his circle of good works, giving her religious feeling the outlet it has been denied. Marthe is not manipulated against her will — she goes willingly toward Faujas because what he offers her is real to her — and this is what makes her story so painful. She loses her husband's trust, her household, her children's respect, and finally her health; she dies broken, near the novel's end, a casualty of what she was shaped into. Zola treats her with sympathy even as he is precise about how she was used.",
            "description_fr": "Fille de Pierre et Félicité Rougon, mariée à son cousin François Mouret. Elle porte la fêlure héréditaire d'Adélaïde sous forme d'un tempérament religieux intense. Faujas reconnaît immédiatement ce qu'elle est et ce qu'il peut en faire : il cultive sa dévotion, l'absorbe dans ses œuvres, la transforme en instrument. Elle y va volontairement, ce qui rend son histoire d'autant plus tragique. Elle meurt brisée, avant la fin du roman.",
            "physical_en": "Pale, gentle, with the distracted look of someone whose inner religious life has become more vivid than the outer world — a look that deepens over the course of the novel into something closer to absence.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },

        # ── GENERATION 2 — Macquart children ────────────────────────────────
        {
            "slug": "lisa-quenu",
            "name": "Lisa Quenu",
            "birth_name": "Lisa Macquart",
            "occupation": "Charcutière",
            "branch": "macquart",
            "generation": 2,
            "description_en": "Antoine Macquart's eldest daughter. Respectable, prosperous, and satisfied with herself and her shop, she and her husband Quenu run a thriving charcuterie in Les Halles. She represents the well-fed complacency and moral conformism of the Second Empire bourgeoisie — ultimately she betrays her own brother-in-law Florent to preserve her comfort.",
            "description_fr": "Fille aînée d'Antoine, charcutière prospère et satisfaite d'elle-même. Elle représente la bourgeoisie repue du Second Empire.",
            "physical_en": "Plump, white-skinned, magnificent in her way — a Rubens-esque figure of comfortable prosperity, always immaculate behind her marble counter.",
            "featured_on_landing": True, "tree_x": 680, "tree_y": 370,
        },
        {
            "slug": "gervaise-macquart",
            "name": "Gervaise Macquart",
            "occupation": "Laundress",
            "branch": "macquart",
            "generation": 2,
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Gervaise_demandant_l%27aum%C3%B4ne.jpg/500px-Gervaise_demandant_l%27aum%C3%B4ne.jpg",
            "image_credit": "Alfred Richard Kemplen, 'Gervaise demandant l'aumône' (1878) — Public domain, BnF",
            "description_en": "The tragic heroine of L'Assommoir and mother of Nana, Étienne, Claude, and Jacques Lantier. Daughter of Antoine Macquart and his common-law wife Josephine, Gervaise leaves Plassans as a teenager with Lantier, her brutal first companion, who abandons her in a Paris hotel with their two boys and no money. She does not collapse — she works, she survives, she builds. Her brief period of prosperity — her own laundry in the Rue Neuve de la Goutte d'Or, a respectable marriage to Coupeau, the famous birthday feast — is one of Zola's most genuinely warm passages of writing: the reader is given time to love her, because the fall must earn the grief it will cause. Coupeau's fall from a rooftop changes everything. The long convalescence, the return of Lantier as an intolerable lodger, the accumulated exhaustion of running a business alone while managing two damaged men — these are the specific mechanisms of her destruction, and Zola renders each one with documentary precision. She begins to drink. The laundry fails. The descent is inexorable and without dramatic rupture: there is no single moment when Gervaise chooses ruin; she simply makes the next slightly worse decision, and the next, and the next, until the decisions are no longer hers to make. She dies of starvation and cold in the passage under the staircase of the building where she once had a shop — found by the concierge in the morning. She is not quite fifty. She is one of the most fully realised characters in nineteenth-century literature, and her fall is heartbreaking precisely because her goodness is never in question.",
            "description_fr": "Héroïne tragique de L'Assommoir. Fille d'Antoine Macquart, elle part de Plassans avec Lantier qui l'abandonne à Paris. Elle construit une vie honnête — blanchisserie, mariage avec Coupeau, bonheur ouvrier — puis voit tout se défaire : chute de Coupeau, retour de Lantier parasite, alcoolisme progressif, faillite, misère. Elle meurt de faim et de froid sous l'escalier d'un immeuble où elle avait eu boutique. L'une des grandes figures du roman français.",
            "physical_en": "A slight limp from a childhood accident (her drunk father dropped her); pretty in youth with large, clear eyes and a quality of direct warmth; worn down year by year — the deterioration rendered by Zola with the same precision as everything else, so that her last appearance is almost unrecognisable from her first.",
            "featured_on_landing": True, "tree_x": 820, "tree_y": 370,
        },
        {
            "slug": "jean-macquart",
            "name": "Jean Macquart",
            "occupation": "Carpenter, soldier, farm labourer",
            "branch": "macquart",
            "generation": 2,
            "description_en": "The youngest Macquart child and one of the few to escape the family curse. A simple, decent, honourable man who appears in both La Terre (as a farm worker in the Beauce) and La Débâcle (as a soldier in the Franco-Prussian War). He is the ordinary Frenchman, battered by history but stubbornly surviving.",
            "description_fr": "Le plus jeune des Macquart, un homme simple et honnête. Il apparaît dans La Terre et La Débâcle comme le Français ordinaire battu par l'histoire.",
            "physical_en": "Solidly built, slow-spoken, with the patient strength of a man used to physical labour and the honest eyes of someone without guile.",
            "featured_on_landing": True, "tree_x": 970, "tree_y": 370,
        },
        {
            "slug": "florent-quenu",
            "name": "Florent Quenu",
            "occupation": "Political exile, fish inspector",
            "branch": "other",
            "generation": 2,
            "description_en": "Half-brother of Quenu (Lisa's husband) — thus Lisa's brother-in-law. A gentle idealist and political prisoner who returns from the penal colony of Cayenne to find himself in the suffocating abundance of Les Halles. His Republican idealism is utterly out of place among the comfortable shopkeepers, and Lisa eventually denounces him.",
            "description_fr": "Demi-frère de Quenu, idéaliste doux revenu du bagne de Cayenne. Sa conscience républicaine est étouffée par l'abondance des Halles.",
            "physical_en": "Thin to the point of gauntness, with large dark eyes and the haunted look of a man who has suffered greatly and forgiven everyone.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },

        # ── GENERATION 2 — Mouret branch (children of Ursule) ───────────────
        {
            "slug": "francois-mouret",
            "name": "François Mouret",
            "occupation": "Landowner, Plassans bourgeois",
            "branch": "mouret",
            "generation": 2,
            "description_en": "Son of Ursule Macquart and Mouret the hatter. A quiet, orderly man — the kind who keeps meticulous accounts, takes the same walk at the same time each day, and whose deepest happiness is domestic tranquillity. He is not unintelligent; he sees, eventually, what Faujas is doing. But by the time he sees it clearly, his wife has been taken, his children have drifted away, his house is occupied by people he cannot remove, and his own protests make him look like the unstable one. He is committed to the asylum at Les Tulettes — where his grandmother Adélaïde lives — in a cruel irony of hereditary appearance. He escapes from the asylum and returns to the house at night, setting fire to it with Faujas and Faujas's sister inside, and dying in the flames himself. His destruction is the cycle's most detailed portrait of how a fundamentally decent, unexceptional man is erased by someone who is willing to use every tool he is not.",
            "description_fr": "Fils d'Ursule Macquart, homme tranquille et méthodique dont toute la vie repose sur l'ordre domestique. Il voit progressivement Faujas dépossèder sa maison, éloigner sa femme, et s'établir en maître. Quand il comprend pleinement ce qui s'est passé, c'est trop tard : ses protestations le font passer pour déséquilibré. Interné aux Tulettes — où vit aussi Adélaïde — il s'échappe et met le feu à la maison avec Faujas à l'intérieur.",
            "physical_en": "Neat, careful in dress, with the methodical bearing of a man who values order above all things — and the progressive look, as the novel advances, of someone watching his world dissolve and finding no words for it.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },
        {
            "slug": "helene-grandjean",
            "name": "Hélène Grandjean",
            "birth_name": "Hélène Mouret",
            "occupation": "Widow, seamstress",
            "branch": "mouret",
            "generation": 2,
            "description_en": "Daughter of Ursule Macquart and granddaughter of Adélaïde Fouque. The sole subject of Une Page d'amour — the cycle's most formally austere novel. Hélène is a widow of thirty living in Passy with her daughter Jeanne, and she is in every way the product of intense self-discipline: her apartment is orderly, her dress is modest, her daily routines are carefully maintained, and her entire emotional life is organised around Jeanne. She is not a woman who represses feeling from coldness; she represses it because she has understood, early, that feeling is dangerous — and she has been right. The love affair with Dr Henri Deberle develops against her will and contrary to her every judgement of him (he is charming, shallow, and not worthy of her). She falls anyway. The decisive night — leaving Jeanne's sickbed for Deberle while Jeanne is gravely ill — is the pivot of the novel: she does not plan it, cannot explain it, and cannot take it back. Jeanne dies. Hélène leaves Paris and remarries a respectable official: a life without interior content, but stable. She is not destroyed in the spectacular fashion of Renée Saccard or Gervaise Macquart; she is simply diminished, sealed off, the catastrophe internalised and carried quietly. Zola gives her the cycle's most muted tragedy.",
            "description_fr": "Fille d'Ursule Macquart. Veuve rigoureusement disciplinée de Passy, dont toute la vie émotionnelle est organisée autour de sa fille Jeanne. La liaison avec le docteur Deberle se développe contre sa volonté. La nuit décisive — elle abandonne le chevet de Jeanne gravement malade — est le pivot du roman. Jeanne meurt. Hélène repart à la province, remariée convenablement, vie sans contenu intérieur : la tragédie la plus sobre du cycle.",
            "physical_en": "Tall, dark, with a composed, almost statuesque beauty and a reserve that conceals deep feeling — the kind of woman who is most striking not in animation but in stillness.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },
        {
            "slug": "silvere-mouret",
            "name": "Silvère Mouret",
            "occupation": "Blacksmith's apprentice, Republican",
            "branch": "mouret",
            "generation": 2,
            "image_url": "/static/images/characters/silvere-mouret.png",
            "image_credit": "Engraving from the Vizetelly English translation of La Fortune des Rougon (1886) — Public domain",
            "description_en": "Grandson of Adélaïde, raised by her after his mother Ursule's early death. He is apprenticed to a blacksmith and has educated himself on Republican ideals — he worships the idea of the Republic with the same fervour that a more conventional boy of his time might have given to religion. When the insurgent column forms to resist Napoleon III's coup, he joins without hesitation, and it is he who procures the red flag that Miette will carry. His love for Miette — stolen meetings at the old cemetery, an innocence that Zola describes with genuine tenderness — is one of the cycle's most affecting relationships. He is shot and killed by the gendarme Rengade (whose eye he had accidentally injured earlier) beside the tombstone at the aire Saint-Mittre, the very stone inscribed 'Ci-gît Marie' where he and Miette had met. He is seventeen. His death is the cycle's founding tragedy: the one character in La Fortune des Rougon who acts from pure conviction dies for it, while the opportunists inherit everything.",
            "description_fr": "Petit-fils d'Adélaïde, apprenti forgeron et républicain convaincu. Il rejoint la colonne insurgée lors du coup d'État de 1851. Son amour pour Miette, décrit avec une tendresse rare, est l'une des relations les plus touchantes du cycle. Fusillé à dix-sept ans par le gendarme Rengade.",
            "physical_en": "Young, handsome, with the open face of someone who has not yet learned to hide what he thinks or feels — and the nervous, burning energy inherited from Adélaïde.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },

        # ── GENERATION 2 — Key non-family characters ─────────────────────────
        {
            "slug": "coupeau",
            "name": "Coupeau",
            "occupation": "Zinc roofer (zingueur)",
            "branch": "other",
            "generation": 2,
            "description_en": "Gervaise's husband in L'Assommoir. A decent, hard-working roofer when she marries him, Coupeau falls from a rooftop and never truly recovers — physically or morally. He slides into alcoholism and drags Gervaise with him. His death from delirium tremens in the Sainte-Anne asylum is one of Zola's most harrowing scenes.",
            "description_fr": "Mari de Gervaise dans L'Assommoir. Zingueur honnête au départ, il sombre dans l'alcoolisme après une chute et entraîne Gervaise avec lui.",
            "physical_en": "Good-natured and broad-shouldered in his youth; later slack-faced and trembling, the alcohol consuming him visibly.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },
        {
            "slug": "lantier",
            "name": "Auguste Lantier",
            "occupation": "Hatter (chapelier), idler",
            "branch": "other",
            "generation": 2,
            "description_en": "Gervaise's first partner and the father of Étienne, Claude, and Jacques. He abandons Gervaise at the start of L'Assommoir, but later insinuates himself back into her life — and into her home — with insolent ease, living off her and Coupeau while doing no work. His idle, sensual presence is one of the forces that destroys her.",
            "description_fr": "Premier compagnon de Gervaise et père d'Étienne, Claude et Jacques. Il abandonne Gervaise puis se réinstalle chez elle en parasite.",
            "physical_en": "Dark, handsome, with the easy manner of a man who has always relied on his looks and charm and rarely been disappointed.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },
        {
            "slug": "quenu",
            "name": "Quenu",
            "occupation": "Pork butcher (charcutier)",
            "branch": "other",
            "generation": 2,
            "description_en": "Lisa's husband and co-owner of the flourishing charcuterie in Les Halles. A good-natured, plump, contented man who lives for his pork products and his comfortable life, and who does whatever Lisa tells him. His half-brother Florent's Republican politics are entirely beyond his comprehension.",
            "description_fr": "Mari de Lisa, charcutier prospère et bonhomme des Halles. Il vit pour sa boutique et fait ce que Lisa lui dit.",
            "physical_en": "Round-faced, florid, with the prosperous girth of a man who tastes his own wares frequently and contentedly.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },
        {
            "slug": "goujet",
            "name": "Goujet",
            "occupation": "Blacksmith (forgeron)",
            "branch": "other",
            "generation": 2,
            "description_en": "The gentle giant blacksmith of L'Assommoir — the novel's one unambiguously good man. He is silently, faithfully in love with Gervaise for years, lending her money when she needs it and expecting nothing in return. His nobility makes the surrounding degradation all the more painful.",
            "description_fr": "Le doux géant forgeron de L'Assommoir — l'homme le plus honnête du roman. Secrètement amoureux de Gervaise, il lui prête de l'argent sans rien attendre.",
            "physical_en": "Enormous, fair-haired, with the gentle eyes of a man whose great physical strength coexists with a child-like tenderness.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },
        {
            "slug": "virginie-poisson",
            "name": "Virginie Poisson",
            "occupation": "Laundress, shop keeper",
            "branch": "other",
            "generation": 2,
            "description_en": "Gervaise's great rival in L'Assommoir. She and Gervaise fight spectacularly in the laundry at the novel's opening, over Lantier. She later marries a policeman, insinuates herself back into Gervaise's life as a friend, and ultimately takes over Gervaise's laundry shop when Gervaise loses it to debt.",
            "description_fr": "Rivale acharnée de Gervaise dans L'Assommoir. Après leur bagarre mémorable, elle s'infiltre de nouveau dans sa vie et finit par lui voler sa boutique.",
            "physical_en": "Tall, dark, handsome, with a malicious wit and a long memory for slights.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },
        {
            "slug": "abbe-faujas",
            "name": "Abbé Faujas",
            "occupation": "Catholic priest",
            "branch": "other",
            "generation": 2,
            "description_en": "The antagonist of La Conquête de Plassans — a priest of genuine piety and iron will sent by the Empire's political managers to secure Plassans for the government. His method is impeccable: he presents himself as poor and humble, lodges with the Mouret family at a modest rate, never appears to scheme, and works through the social fabric of the town's religious women rather than through any direct political action. He identifies Marthe Rougon's religious temperament immediately and uses it as his primary instrument, drawing her into his network of charitable works, shaping her devotion to his ends. He brings his sister Olympe and eventually her whole family to lodge in the Mouret house, displacing its original occupants room by room. He is not a hypocrite in the simple sense: his faith may well be genuine, and his political mission he regards as serving the Church's interests. This is what makes him so dangerous — he does not see himself as an agent of destruction. He delivers the vote. He dies in the fire François Mouret sets.",
            "description_fr": "Antagoniste de La Conquête de Plassans. Prêtre envoyé par les managers politiques impériaux pour livrer Plassans au gouvernement. Sa méthode : se présenter comme humble et pauvre, s'installer chez les Mouret, travailler à travers le réseau des femmes dévotes plutôt que par action politique directe. Il reconnaît la dévotion de Marthe Rougon et s'en sert comme instrument principal. Mission accomplie — il est mort dans l'incendie que provoque François Mouret.",
            "physical_en": "Tall, square-shouldered, with a hard jaw and impenetrable dark eyes — a man of iron will dressed in priestly black, who has the disconcerting quality of never seeming to want anything for himself.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },
        {
            "slug": "roubaud",
            "name": "Roubaud",
            "occupation": "Railway deputy stationmaster",
            "branch": "other",
            "generation": 2,
            "description_en": "Séverine's jealous, violent husband in La Bête humaine. When he discovers a secret from Séverine's past, he forces her to help him commit a murder — and in doing so destroys them both. A study in how jealousy and wounded pride can turn an ordinary man into a killer.",
            "description_fr": "Mari jaloux et violent de Séverine dans La Bête humaine. En découvrant un secret du passé de sa femme, il l'entraîne dans un meurtre qui les détruira tous les deux.",
            "physical_en": "Stocky, strong, with the ruddy face of a man who works outdoors and the tightly clenched jaw of one who never forgets an injury.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },
        {
            "slug": "renee-saccard",
            "name": "Renée Saccard",
            "birth_name": "Renée Béraud du Châtel",
            "occupation": "Bourgeoise, socialite",
            "branch": "rougon",
            "generation": 2,
            "description_en": "Aristide Saccard's second wife — a woman of good family (née Béraud du Châtel) whom he married primarily to cover a social embarrassment, settling her inheritance debts in exchange for the respectability of her name. She is beautiful, intelligent, and utterly without occupation: Aristide provides everything except a reason to live. In the tropical hothouse of the Saccard mansion — its overheated air thick with exotic plants and artificial perfume — she drifts into an affair with Maxime, her stepson, who is nearly her own age. Zola renders the affair with unflinching clarity: it is not passion, exactly, but the boredom of a woman who has been given everything except genuine feeling. When she finally understands that Aristide has known about the affair and simply calculated its usefulness — that she is no different from the properties he buys and sells — her recognition is the novel's moral centre, and one of Zola's most pitiless endings. She dies shortly after the novel closes, undone not by scandal but by the simple realisation of what she has been worth to the people around her.",
            "description_fr": "Née Béraud du Châtel, elle épouse Aristide Saccard qui rachète ses dettes en échange de sa respectabilité. Belle et désœuvrée dans leur hôtel particulier, elle glisse dans une liaison avec Maxime, son beau-fils. Quand elle comprend qu'Aristide connaissait cette liaison et l'a tolérée par calcul — qu'elle n'est qu'un actif parmi d'autres — sa prise de conscience est l'un des moments les plus implacables du cycle.",
            "physical_en": "Magnificent, extravagantly dressed, with the glittering eyes of a woman on the permanent edge of nervous collapse — and, increasingly, the look of someone who suspects she is the only person in her world who feels anything genuinely.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },

        # ── Son Excellence — key non-family character ────────────────────────────
        {
            "slug": "clorinde-balbi",
            "name": "Clorinde Balbi",
            "occupation": "Italian adventuress, diplomat's wife",
            "branch": "other",
            "generation": 2,
            "description_en": "The most formidable figure in Son Excellence Eugène Rougon, and arguably the cycle's most purely political female character. An Italian of uncertain means, she arrives in Paris with her mother and attaches herself to Rougon's circle of followers — though 'follower' is far too weak a word for someone who is his equal in intelligence and will. She is as ambitious as Rougon himself, and she operates where he cannot: through charm, physical magnetism, and the social skills of someone who has learned to work through men in a world that offers women no direct path to power. She and Rougon are fascinated by each other — a mutual recognition of exceptional temperaments that is as close as either of them can come to respect. He might have loved her, in another life; instead she marries the Italian diplomat Cav. Luigi Rusconi, securing a position that gives her real leverage, and uses it to outmanoeuvre Rougon at the moments that count. Zola renders her as magnificently, almost dangerously alive: one of his great portraits of a woman who has taken the limited instruments available to her and made herself, against the odds, genuinely powerful.",
            "description_fr": "Figure centrale de Son Excellence Eugène Rougon et l'une des personnages féminins les plus politiquement formidables du cycle. Aventurière italienne qui s'attache à l'entourage de Rougon tout en étant son égale en ambition et en intelligence. Elle épouse le diplomate Cav. Rusconi pour obtenir un vrai levier d'action, et s'en sert pour contrecarrer Rougon aux moments décisifs.",
            "physical_en": "Tall, dark, magnificent, with the absolute ease of movement of someone who has never been afraid of anything — a quality Zola renders as almost feline. She takes up space in a room the way Rougon does: as a matter of right.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },

        # ── GENERATION 2 — Germinal characters ──────────────────────────────
        {
            "slug": "bonnemort",
            "name": "Bonnemort",
            "birth_name": "Vincent Maheu",
            "occupation": "Retired coal miner",
            "branch": "other",
            "generation": 1,
            "description_en": "The ancient patriarch of the Maheu mining family in Germinal. His nickname — 'good death' — is darkly ironic: he has survived fifty years underground when most men are killed or broken in twenty. He sits at the novel's opening in a kind of stupor, coughing black coal dust, a monument to what the mine does to men. His shocking act of violence late in the novel is one of Germinal's most unforgettable moments.",
            "description_fr": "Ancien patriarche mineur dans Germinal. Son surnom 'Bonnemort' est ironique : il a survécu cinquante ans sous terre. Sa violence finale est l'un des moments les plus marquants du roman.",
            "physical_en": "Enormous, slow, with a face the colour of ash and the vacant look of a man whose mind has returned underground. His legs are swollen, his cough constant and black.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },
        {
            "slug": "toussaint-maheu",
            "name": "Toussaint Maheu",
            "occupation": "Coal miner",
            "branch": "other",
            "generation": 2,
            "description_en": "The father of the Maheu family and one of Germinal's central characters. A good man worn to the bone by decades underground, he represents the dignity and endurance of the working class. He initially resists Étienne's strike call, then commits to it fully. He dies when soldiers fire on the strikers — shot from behind while trying to flee.",
            "description_fr": "Père de la famille Maheu dans Germinal. Homme juste et usé par des décennies sous terre. Il rejoint finalement la grève et meurt sous les balles de la troupe.",
            "physical_en": "Lean, hollow-cheeked, with the stooped posture of a man who has spent his life bent double underground, and the steady eyes of a man who has never complained.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },
        {
            "slug": "la-maheude",
            "name": "La Maheude",
            "occupation": "Miner's wife, later surface worker",
            "branch": "other",
            "generation": 2,
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/Stupide_La_Maheude_se_baissa_illustration_from_Germinal_by_Emile_Zola%EF%BC%88Drawing_by_Jules_F%C3%A9rat%EF%BC%89.jpg/500px-Stupide_La_Maheude_se_baissa_illustration_from_Germinal_by_Emile_Zola%EF%BC%88Drawing_by_Jules_F%C3%A9rat%EF%BC%89.jpg",
            "image_credit": "Jules Férat, 'La Maheude se baissa', illustration for Germinal (1886) — Public domain",
            "description_en": "Toussaint Maheu's wife and one of Germinal's most powerful characters. She runs the household with fierce love and practicality, feeding seven children on a miner's wages. When the strike ruins her family — killing her husband, her son Zacharie, and her daughter Alzire — she continues to live, with a bitterness that Zola renders as one of the novel's most sustained acts of moral witness.",
            "description_fr": "Femme de Toussaint Maheu dans Germinal. Elle nourrit sept enfants avec un salaire de mineur et survit à la grève qui détruit sa famille.",
            "physical_en": "Raw-boned, large-handed, with the permanent lines of exhaustion in her face and the indestructible stubbornness of a woman who has never stopped fighting.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },
        {
            "slug": "hennebeau",
            "name": "M. Hennebeau",
            "occupation": "Mine company director",
            "branch": "other",
            "generation": 2,
            "description_en": "The director of the Montsou mining company in Germinal. Outwardly the face of corporate power — the man who refuses the strikers' demands — he is privately miserable: his wife is having an affair with his nephew, and he envies the miners their simple, physical loves. Zola's portrait of him is unexpectedly sympathetic.",
            "description_fr": "Directeur de la Compagnie minière dans Germinal. Derrière son pouvoir apparent, il est misérable : sa femme le trompe et il envie les mineurs de leur simplicité.",
            "physical_en": "Well-dressed, controlled, with the careful bearing of a bureaucrat and something haunted behind his eyes.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },
        {
            "slug": "deneulin",
            "name": "Deneulin",
            "occupation": "Mine owner (Jean-Bart)",
            "branch": "other",
            "generation": 2,
            "description_en": "The owner of the smaller Jean-Bart mine in Germinal, and Hennebeau's brother-in-law. An honest, energetic man who genuinely cares for his workers but cannot survive the strike — he is forced to sell his mine to the Company at a ruinous price. His ruin illustrates Zola's point about the inevitable triumph of corporate capital over individual enterprise.",
            "description_fr": "Propriétaire de la fosse Jean-Bart dans Germinal, beau-frère d'Hennebeau. Homme honnête ruiné par la grève, contraint de vendre sa mine à la Compagnie.",
            "physical_en": "Vigorous, broad, with a red face and the direct manner of a man who built something himself and is proud of it.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },
        {
            "slug": "rasseneur",
            "name": "Rasseneur",
            "occupation": "Innkeeper, former miner",
            "branch": "other",
            "generation": 2,
            "description_en": "A former miner turned innkeeper in Germinal, Rasseneur runs the Avantage bar where the strikers meet. He is a moderate — a reformist rather than a revolutionary — and when the strike radicalises under Étienne's leadership, he loses his influence and his audience. He represents the older, gradualist tradition of French labour politics.",
            "description_fr": "Ancien mineur devenu cabaretier dans Germinal. Réformiste modéré, il perd son influence lorsque la grève se radicalise sous Étienne.",
            "physical_en": "Round-bellied, genial, with the easy warmth of a man who has spent years behind a bar, and the careful eyes of someone who has survived by never going too far.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },

        # ── GENERATION 3 — Rougon-Macquart ──────────────────────────────────
        {
            "slug": "nana",
            "name": "Nana",
            "birth_name": "Anna Coupeau",
            "occupation": "Courtesan, actress",
            "branch": "macquart",
            "generation": 3,
            "description_en": "Anna Coupeau — Nana — is the most famous character in the Rougon-Macquart cycle, and one of the great figures of nineteenth-century literature. Daughter of Gervaise Macquart and the roofer Coupeau, she grew up in the degradation of L'Assommoir — barely noticed by her parents as their lives fell apart — and taught herself, by the age of fifteen, that her body was her one resource. She appears first in L'Assommoir as a child, already sharp-eyed and half-feral; the novel Nana begins with her at eighteen, appearing on stage as the Golden Venus at the Théâtre des Variétés, technically incompetent and already irresistible. Zola does not allow Nana to be simply a predator. She is not intelligent, exactly, but she is shrewd; she is not cruel, exactly, but she is indifferent to suffering she cannot see directly; she is not calculating, exactly, but she instinctively understands what men want and uses that understanding without guilt, because guilt would require the ability to imagine herself as the men imagine her. Her relationship with Fontan — the coarse, violent actor with whom she lives in a moment of something like genuine feeling — is the one crack in this: she chooses to be with him, is beaten by him, and stays. With everyone else, she is the one who receives. Count Muffat de Beuville, the rigidly Catholic chamberlain who becomes her most destroyed admirer, is the novel's central case study: a man whose entire public identity is built on propriety and moral authority, dismantled piece by piece by his own desire. Nana does not engineer this — she barely understands it. She is hereditary ruin made beautiful: the accumulated damage of the Macquart line expressing itself through the most total instrument available, the one commodity the Second Empire values above all others. She dies of smallpox in a locked hotel room, the beautiful face obliterated, as the crowd outside chants 'À Berlin!'",
            "description_fr": "Anna Coupeau — Nana — est la figure la plus célèbre du cycle. Fille de Gervaise et de Coupeau, grandie dans la dégradation de L'Assommoir, elle fait de son corps son unique ressource. Pas vraiment prédatrice, pas vraiment cruelle — indifférente au mal qu'elle fait parce qu'elle ne peut pas le voir. Le comte Muffat, chamberllan rigidement catholique, est sa victime centrale. Fontan, l'acteur raté qui la bat, est son seul amour vrai. Elle meurt de la variole, le visage détruit, tandis que Paris crie 'À Berlin !'",
            "physical_en": "Blonde, magnificent, with the heavy golden beauty of a goddess risen from the gutter — a beauty that is not elegant but overwhelming, that bypasses aesthetic judgement entirely and operates directly on the body.",
            "featured_on_landing": True, "tree_x": 700, "tree_y": 530,
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/1877_Manet_Nana_anagoria.jpg/500px-1877_Manet_Nana_anagoria.jpg",
            "image_credit": "Édouard Manet, Nana (1877), Hamburger Kunsthalle — Public domain",
        },
        {
            "slug": "etienne-lantier",
            "name": "Étienne Lantier",
            "occupation": "Miner, socialist organiser",
            "branch": "macquart",
            "generation": 3,
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Front_cover_illustration_of_Germinal_by_Emile_Zola%EF%BC%88Drawing_by_Jules_F%C3%A9rat%EF%BC%89.jpg/500px-Front_cover_illustration_of_Germinal_by_Emile_Zola%EF%BC%88Drawing_by_Jules_F%C3%A9rat%EF%BC%89.jpg",
            "image_credit": "Jules Férat, frontispiece illustration for Germinal (1886) — Public domain",
            "description_en": "Son of Gervaise and Lantier. The young, idealistic miner who arrives at the Voreux pit in Germinal and organises the great strike against the Company. Educated by his own reading, passionate, and genuinely selfless, he is one of the cycle's great heroes — though the family's hereditary darkness haunts him too, surfacing as a murderous impulse he barely controls.",
            "description_fr": "Fils de Gervaise et Lantier. Jeune mineur idéaliste qui mène la grande grève dans Germinal, hanté par le germe héréditaire de la famille.",
            "physical_en": "Slender, dark, with the restless intelligence of a self-educated working man and his mother's clear, expressive eyes.",
            "featured_on_landing": True, "tree_x": 850, "tree_y": 530,
        },
        {
            "slug": "claude-lantier",
            "name": "Claude Lantier",
            "occupation": "Painter",
            "branch": "macquart",
            "generation": 3,
            "description_en": "Son of Gervaise, brother of Étienne and Jacques. The tormented genius painter who pursues an impossible masterpiece, sacrificing his marriage, his child's life, and finally his own sanity to his art. A barely veiled portrait of Paul Cézanne — and of the Impressionist generation's struggles. He ends by hanging himself before his unfinished canvas.",
            "description_fr": "Fils de Gervaise, peintre génial et torturé qui poursuit un chef-d'œuvre impossible. Portrait voilé de Cézanne.",
            "physical_en": "Unkempt, large-handed, with burning eyes and paint-stained clothes — an unmistakable figure of the consumed, bohemian artist.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },
        {
            "slug": "jacques-lantier",
            "name": "Jacques Lantier",
            "occupation": "Train driver (mécanicien)",
            "branch": "macquart",
            "generation": 3,
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/Geo_Dupuis_-_Bete_humaine_frontispice.jpeg/500px-Geo_Dupuis_-_Bete_humaine_frontispice.jpeg",
            "image_credit": "Géo Dupuis, frontispiece for La Bête humaine (Mornay edition, 1924) — Public domain",
            "description_en": "Son of Gervaise, brother of Étienne and Claude. The tragic hero of La Bête humaine — a locomotive driver haunted by an uncontrollable murderous impulse towards women, the most extreme expression of the family's hereditary curse. He loves his locomotive Lison as he cannot love any human being, and his story ends in darkness on the iron road.",
            "description_fr": "Fils de Gervaise, mécanicien de locomotive hanté par une pulsion meurtrière envers les femmes. Héros tragique de La Bête humaine.",
            "physical_en": "Strong, handsome, with something rigid and clenched about him — a man fighting constantly against himself.",
            "featured_on_landing": True, "tree_x": 1000, "tree_y": 530,
        },
        {
            "slug": "octave-mouret",
            "name": "Octave Mouret",
            "occupation": "Entrepreneur, department store magnate",
            "branch": "mouret",
            "generation": 3,
            "description_en": "Son of François Mouret and Marthe Rougon, arriving in Paris from Plassans with southern charm and unashamed ambition. His education in Pot-Bouille — the bourgeois apartment building on the Rue de Choiseul where he lodges — is an immersion in the hypocrisies and hidden lives of the Parisian middle class, in which he both participates and observes. He uses women as instruments of social advancement without compunction, while working his way up through the drapery trade. In Au Bonheur des Dames he reaches his full expression: the great department store he builds, one of the first of its kind, is an engine for understanding and exploiting female desire — cheaper goods in greater variety, temptation on every counter, the thrill of spending made irresistible. He is enormously successful and largely unscrupulous about the small traders he ruins. His one genuine surprise is Denise Baudu — the shop girl who refuses to be dazzled by him, who sees through his methods and will not yield to them, and whom he ends by genuinely loving. She is the only thing he cannot buy or manipulate his way to obtaining.",
            "description_fr": "Fils de François Mouret et de Marthe Rougon, il arrive à Paris du Midi avec charme et ambition. Son passage dans l'immeuble de Pot-Bouille lui donne son éducation parisienne — hypocrisies bourgeoises, liaisons instrumentalisées, ascension professionnelle. Dans Au Bonheur des Dames il bâtit un grand magasin comme machine à exploiter le désir féminin. Il réussit tout — jusqu'à Denise Baudu, la seule qu'il ne puisse ni acheter ni manipuler.",
            "physical_en": "Handsome, charming, with the easy confidence of a man who has always succeeded with women and with business — and who has never, until Denise, had reason to doubt that confidence.",
            "featured_on_landing": True, "tree_x": 550, "tree_y": 530,
        },
        {
            "slug": "serge-mouret",
            "name": "Abbé Serge Mouret",
            "occupation": "Catholic priest",
            "branch": "mouret",
            "generation": 3,
            "description_en": "The mystic, ascetic priest at the centre of La Faute de l'Abbé Mouret. Struck by a brain fever, he recovers in the paradisiacal garden of Le Paradou without memory of his vows, and falls passionately in love with the wild Albine. When his memory returns, he must choose between flesh and faith — one of Zola's most lyrical and philosophically daring explorations.",
            "description_fr": "Prêtre mystique et ascète. Sa chute amoureuse pour Albine dans le jardin du Paradou, et le retour déchirant de sa vocation, sont l'un des passages les plus lyriques de Zola.",
            "physical_en": "Pale, thin, luminous-eyed — a man whose physical presence seems almost to dissolve into the spiritual.",
            "featured_on_landing": True, "tree_x": 400, "tree_y": 530,
        },
        {
            "slug": "maxime-saccard",
            "name": "Maxime Saccard",
            "occupation": "Dandy, man of leisure",
            "branch": "rougon",
            "generation": 3,
            "description_en": "Son of Aristide Saccard by his first wife Rose. A beautiful, languid, and essentially empty young man who embodies the Second Empire's gilded generation — the children of new money who have grown up with every luxury and developed no capacity for feeling anything deeply. His affair with his stepmother Renée is not passion but boredom: he drifts into it and drifts out again with equal indifference. What makes him chilling is not malice but vacancy — he is not cruel to Renée, he simply cannot conceive that she feels things he does not. He survives everything: La Curée, Nana (where he appears as one of her ruined admirers), L'Argent. By the final novel, he is older and richer, having outlasted his father's first catastrophe. He has his father's talent for self-preservation with none of the energy that makes Aristide almost admirable.",
            "description_fr": "Fils d'Aristide par sa première femme Rose. Beau dandy langoureux et moralement vide, il représente la génération dorée du Second Empire — enfants de la richesse nouvelle incapables de sentiment profond. Sa liaison avec Renée n'est que désœuvrement. Il survit à tout : La Curée, Nana, L'Argent — plus riche et toujours aussi creux.",
            "physical_en": "Exquisitely dressed, languid, with a cold, perfect beauty that conceals complete moral nullity — the face of a man who has never been denied anything and has consequently never wanted anything very much.",
            "featured_on_landing": True, "tree_x": 260, "tree_y": 530,
        },
        {
            "slug": "pauline-quenu",
            "name": "Pauline Quenu",
            "occupation": "Independent woman, caregiver",
            "branch": "macquart",
            "generation": 3,
            "description_en": "Daughter of Lisa Quenu. An extraordinarily generous, life-affirming young woman who supports the Chanteau family with her inheritance while they take advantage of her. She loves Lazare Chanteau, watches him marry someone else, and raises his child. Her will to live and her clear-eyed acceptance of pain make her one of Zola's most admirable creations.",
            "description_fr": "Fille de Lisa Quenu, jeune femme d'une générosité extraordinaire qui soutient la famille Chanteau de son héritage.",
            "physical_en": "Sturdy, rosy, full of physical vitality — a young woman who seems to radiate health and goodwill even in the face of everything that diminishes her.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },
        {
            "slug": "angelique-rougon",
            "name": "Angélique",
            "birth_name": "Angélique Rougon",
            "occupation": "Embroiderer",
            "branch": "rougon",
            "generation": 3,
            "description_en": "The most ethereal character in the cycle — a Rougon by blood (her obscure origins are hinted at but never fully established in the novel itself) who has been abandoned as an infant on the steps of a Gothic cathedral and taken in by the elderly embroiderers Hubert and Hubertine. She grows up in the shadow of the cathedral, her entire inner world formed by the hagiographies she reads obsessively — above all Voragine's Légende Dorée. She does not distinguish sharply between the material world and the world of the legends; saints and miracles feel as real to her as the embroidery frame before her. When Félicien de Hautecœur appears — young, beautiful, the son of the local bishop — he seems to her quite literally to have stepped out of her books. The bishop refuses consent to their marriage; she falls gravely ill (psychosomatic, in Zola's view, but also willed — she is willing herself toward death as a saint might). The bishop comes to her bedside, blesses her, and she recovers. She marries Félicien in the cathedral — and dies on the steps after the ceremony, as if the dream, once made fully real, has exhausted its substance.",
            "description_fr": "La plus éthérée du cycle — une Rougon aux origines obscures, abandonnée bébé sur les marches d'une cathédrale et recueillie par des brodeurs. Elle grandit dans la Légende Dorée, dont elle ne distingue pas nettement la réalité de la vie concrète. Félicien de Hautecœur lui semble sorti de ses légendes. Refus du père, maladie, bénédiction épiscopale, guérison miraculeuse — elle épouse Félicien et meurt sur les marches de l'église, comme si le rêve réalisé n'avait plus de raison d'être.",
            "physical_en": "Fair, delicate, with an almost translucent quality — she seems lit from within by her own luminous inner world, a quality that becomes the more marked as her illness advances.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },
        {
            "slug": "clotilde-rougon",
            "name": "Clotilde Rougon",
            "occupation": "Pascal's niece and companion",
            "branch": "rougon",
            "generation": 3,
            "description_en": "Pascal Rougon's niece. She assists him in his scientific work, sharing his laboratory and his life. In the final novel she becomes his lover — a controversial relationship that Zola frames as life-affirming, the cycle's last act of defiance against death and endings. She carries his child as the novel closes.",
            "description_fr": "Nièce du docteur Pascal. Elle l'assiste dans ses travaux et devient sa compagne dans le dernier roman, portant son enfant comme acte final de vie.",
            "physical_en": "Young, fair, with a luminous quality and the calm of someone who has found her purpose.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },
        {
            "slug": "desiree-mouret",
            "name": "Désirée Mouret",
            "occupation": "Farmer's helper",
            "branch": "mouret",
            "generation": 3,
            "description_en": "Serge Mouret's younger sister in La Faute de l'Abbé Mouret. Simple-minded but radiantly happy, she raises her animals — chickens, rabbits, a cow — with pure, unselfconscious delight. She represents nature's joy as a counterpoint to the anguish of her brother's spiritual and erotic struggle. Her contentment is among Zola's most unusual passages.",
            "description_fr": "Sœur de Serge Mouret, simple d'esprit mais radieusement heureuse. Elle incarne la joie naturelle face à la souffrance spirituelle de son frère.",
            "physical_en": "Round-faced, rosy, with an animal ease of movement and a smile of pure, uncomplicated joy.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },
        {
            "slug": "denise-baudu",
            "name": "Denise Baudu",
            "occupation": "Shop girl, then department director",
            "branch": "other",
            "generation": 3,
            "description_en": "Not a Rougon-Macquart by blood, but the moral and narrative centre of Au Bonheur des Dames. Denise arrives in Paris from Valognes in Normandy with her two younger brothers and no connections, hoping to find work in her uncle Baudu's drapery shop — only to discover that the great department store across the street has already made the shop unviable. She takes a position in Au Bonheur des Dames without enthusiasm and without expectation; she is taken on without enthusiasm either. She is not beautiful in the conventional sense, not charming, not socially skilled. She is competent, honest, and apparently impervious to intimidation. She is fired for a minor infraction and spends a desperate period in furnished rooms, taking in sewing to survive, before returning to the store. Her ascent is entirely meritocratic — she is promoted because she is genuinely good at what she does. Octave Mouret notices her first as an irritant (she keeps filing complaints about working conditions that he would rather ignore), then as a puzzle, then as the one woman who will not be dazzled by him. He offers her everything, progressively: a private dinner, a directorship, money, his desire. She refuses all of it with the same quiet, implacable courtesy. She will accept none of it on those terms. She will accept marriage — genuine commitment — or nothing. He loves her eventually for this, and marries her, and she becomes the department store's humane conscience. Zola does not make her a saint; she is practical, occasionally naive, always clear about what she will and will not do. She is the only character in the cycle who faces Octave Mouret at full strength and does not blink.",
            "description_fr": "Héroïne morale d'Au Bonheur des Dames. Vendeuse normande arrivée à Paris sans relations et sans atouts conventionnels, elle monte par son seul mérite malgré les licenciements et la misère. Mouret lui propose argent, poste et désir ; elle refuse tout avec une courtoisie implacable jusqu'à ce qu'il lui offre un mariage sincère. Unique personnage du cycle à affronter Mouret à pleine force sans céder.",
            "physical_en": "Plain in feature but with a natural dignity and quiet strength that makes her beautiful to those who look carefully — which Octave Mouret, eventually, does.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },
        {
            "slug": "victor-saccard",
            "name": "Victor Saccard",
            "occupation": "Man of leisure",
            "branch": "rougon",
            "generation": 3,
            "description_en": "Aristide Saccard's illegitimate son, revealed in L'Argent. Raised in poverty, he is violently feral when Saccard finally acknowledges him — a dark echo of his father's destructive energy without any of the father's brilliance or charm. He represents the worst of hereditary transmission: corruption without talent.",
            "description_fr": "Fils illégitime d'Aristide Saccard, révélé dans L'Argent. Élevé dans la misère, il est violent et sauvage — écho sombre de son père sans son éclat.",
            "physical_en": "Swarthy, quick-eyed, with the watchful look of someone who grew up without safety.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },

        # ── GENERATION 3 — Key non-family characters ─────────────────────────
        {
            "slug": "miette",
            "name": "Miette",
            "birth_name": "Marie-Jeanne Chantegreil",
            "occupation": "Labourer's helper",
            "branch": "other",
            "generation": 3,
            "image_url": "/static/images/characters/miette.png",
            "image_credit": "Engraving from the Vizetelly English translation of La Fortune des Rougon (1886) — Public domain",
            "description_en": "Silvère's beloved in La Fortune des Rougon — and one of the cycle's most purely tragic figures. Born Marie-Jeanne Chantegreil, she is thirteen or fourteen years old, orphaned after her father was imprisoned for poaching a rabbit, and left to be exploited as an unpaid servant by a brutal uncle. She and Silvère meet secretly at the old cemetery of the aire Saint-Mittre and fall into the tender, half-understood love of adolescence. When the insurgent column forms she insists on marching with Silvère, turning her cloak inside-out to show its red lining and taking up the flag as the column's standard-bearer. Zola renders her at this moment as 'la vierge Liberté' — the virgin Liberty — an allegorical figure out of Delacroix. She tells Silvère that it feels like carrying the Virgin's banner in a Corpus Christi procession: she is a child playing at revolution, with no real understanding of what she is in the middle of. She is shot near Orchères and dies in Silvère's arms, clutching the flag. Dr Pascal, who will become the cycle's scientific conscience, pronounces her dead.",
            "description_fr": "Bien-aimée de Silvère, treize ou quatorze ans, orpheline exploitée par un oncle brutal. Elle marche avec les insurgés, le manteau retourné pour montrer sa doublure rouge, portant le drapeau dont Zola fait un symbole de la Liberté. Elle croit porter la bannière de la Vierge. Abattue près d'Orchères, elle meurt dans les bras de Silvère.",
            "physical_en": "Wild-haired, dark-eyed, with the tanned face of a girl who has spent her whole life outdoors and the fierce, unselfconscious beauty of someone who has never been told she is beautiful.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },
        {
            "slug": "albine",
            "name": "Albine",
            "occupation": "Wild girl of Le Paradou",
            "branch": "other",
            "generation": 3,
            "description_en": "The untamed young woman at the heart of La Faute de l'Abbé Mouret. She has grown up alone in the vast overgrown garden of Le Paradou, half-wild and half-mythological. She nurses the amnesiac Serge back to health, falls in love with him in an Edenic idyll, and when he returns to his vows and leaves her, she dies among her flowers — one of the cycle's most beautiful and tragic figures.",
            "description_fr": "La jeune femme sauvage au cœur de La Faute de l'Abbé Mouret. Elle grandit seule dans le jardin du Paradou et meurt parmi ses fleurs quand Serge la quitte.",
            "physical_en": "Sunburnt, loose-limbed, with flowers always in her hair — a figure who seems to belong to the garden itself rather than to human society.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },
        {
            "slug": "souvarine",
            "name": "Souvarine",
            "occupation": "Mechanic, nihilist revolutionary",
            "branch": "other",
            "generation": 3,
            "description_en": "The Russian nihilist in Germinal — one of literature's great portraits of the anarchist revolutionary. He has loved a woman executed in Russia and nothing has meaning for him since. Cold, intelligent, absolute, he ultimately sabotages the Voreux mine's pumps, causing the catastrophic flooding that kills dozens. He walks away afterwards into the darkness without a backward glance.",
            "description_fr": "Nihiliste russe dans Germinal, l'un des plus grands portraits du révolutionnaire anarchiste dans la littérature. Il sabote la mine du Voreux, provoquant l'inondation catastrophique.",
            "physical_en": "Slight, fair, almost girlishly handsome, with the pale, steady eyes of a man who has decided that nothing in the world has value.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },
        {
            "slug": "catherine-maheu",
            "name": "Catherine Maheu",
            "occupation": "Coal hewer (herscheuse)",
            "branch": "other",
            "generation": 3,
            "description_en": "Toussaint Maheu's daughter and Étienne Lantier's great love in Germinal. She works underground alongside the men, has been Chaval's unwilling companion since she was fifteen, and loves Étienne but cannot break free of Chaval's hold. She and Étienne finally come together in the flooded mine — and die there together. Her fate is the novel's most harrowing personal tragedy.",
            "description_fr": "Fille de Maheu et amour d'Étienne dans Germinal. Mineure de charbon, retenue par Chaval, elle retrouve Étienne dans la mine inondée où ils meurent ensemble.",
            "physical_en": "Small, slight, pale as chalk from years underground, with the quiet eyes of someone who has learned not to expect much.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },
        {
            "slug": "chaval",
            "name": "Chaval",
            "occupation": "Coal miner",
            "branch": "other",
            "generation": 3,
            "description_en": "Catherine Maheu's bullying, possessive partner in Germinal. He seduced her when she was fifteen and has dominated her through intimidation ever since. Vain, violent, and cowardly at root, he is Étienne's great rival — for Catherine's love and for the miners' political allegiance. He dies in the flooded mine, killed by Étienne.",
            "description_fr": "Compagnon brutal de Catherine dans Germinal. Dominant Catherine depuis ses quinze ans, il est le rival d'Étienne et meurt dans la mine inondée.",
            "physical_en": "Tall, dark, with an arrogant swagger and the sort of coarse handsomeness that intimidates the timid.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },
        {
            "slug": "jeanlin-maheu",
            "name": "Jeanlin Maheu",
            "occupation": "Child miner, thief",
            "branch": "other",
            "generation": 3,
            "description_en": "The youngest Maheu son in Germinal — a ten-year-old who is already morally feral. Injured underground and left with a limp, he builds a private world of small thefts and cruelties in the old tunnels. He commits a murder for no clear reason, almost as an animal might. He is Zola's most disturbing portrait of what poverty and the mine do to children.",
            "description_fr": "Le plus jeune fils Maheu dans Germinal — enfant déjà moral dévoyé par la mine. Il commet un meurtre inexpliqué, portrait glaçant de ce que la pauvreté fait aux enfants.",
            "physical_en": "Small, simian, always darting and grinning — a child who has skipped childhood entirely.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },
        {
            "slug": "christine-halleguen",
            "name": "Christine Halleguen",
            "occupation": "Artist's model and wife",
            "branch": "other",
            "generation": 3,
            "description_en": "Claude Lantier's devoted wife in L'Œuvre. She posed for his first great canvas and has loved him ever since with a total, self-sacrificing love. As Claude becomes increasingly obsessed with his impossible painting, she watches him destroy himself, their son, and their marriage — a witness to artistic mania rendered with great tenderness.",
            "description_fr": "Femme dévouée de Claude Lantier dans L'Œuvre. Elle l'aime d'un amour total et assiste impuissante à sa destruction par son œuvre impossible.",
            "physical_en": "Dark-haired, fine-featured, with the worn patience of a woman who has given everything and knows it.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },
        {
            "slug": "severine-roubaud",
            "name": "Séverine Roubaud",
            "occupation": "Railway official's wife",
            "branch": "other",
            "generation": 3,
            "description_en": "The femme fatale of La Bête humaine — though Zola's portrait of her is more sympathetic than that label suggests. Beautiful and passive, she was shaped by a much older man's influence in her youth, and has been trapped since by secrets she cannot escape. She falls in love with Jacques Lantier, but both of them are caught in the machinery of violence.",
            "description_fr": "Femme fatale de La Bête humaine — portrait plus nuancé que son rôle apparent. Elle tombe amoureuse de Jacques Lantier mais tous deux sont pris dans l'engrenage de la violence.",
            "physical_en": "Dark, with large violet eyes and a quality of stillness that men find irresistible, and that conceals a troubled, haunted interior.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },
        {
            "slug": "flore",
            "name": "Flore",
            "occupation": "Level-crossing keeper",
            "branch": "other",
            "generation": 3,
            "description_en": "A level-crossing keeper on the Paris-Le Havre railway line in La Bête humaine. Wild, strong, and passionately in love with Jacques Lantier, she cannot accept that he loves Séverine instead. Her response — causing a catastrophic train crash — is one of the novel's most terrifying moments, and her subsequent suicide is oddly magnificent.",
            "description_fr": "Gardienne de passage à niveau dans La Bête humaine. Amoureuse de Jacques, elle provoque un accident ferroviaire catastrophique avant de se suicider.",
            "physical_en": "Tall, sun-browned, with the free stride of someone who spends her days in the open air and the untamed look of a woman who has never been socialised.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },
        {
            "slug": "lazare-chanteau",
            "name": "Lazare Chanteau",
            "occupation": "Failed engineer, musician, author",
            "branch": "other",
            "generation": 3,
            "description_en": "The hypochondriac anti-hero of La Joie de Vivre. Pauline Quenu's childhood companion and the object of her love, he is a walking study in Schopenhauerian pessimism — brilliant, restless, terrified of death, and incapable of finishing anything he starts. He lives off Pauline's inheritance, marries someone else, and remains sustained by her goodwill he does not deserve.",
            "description_fr": "Hypocondriaque anti-héros de La Joie de Vivre. Brillant et inconstant, hanté par la mort, il dilapide l'héritage de Pauline et épouse une autre.",
            "physical_en": "Tall, energetic in bursts, with the restless eyes of someone always looking for the next enthusiasm and the next escape.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },
        {
            "slug": "maurice-levasseur",
            "name": "Maurice Levasseur",
            "occupation": "Soldier",
            "branch": "other",
            "generation": 3,
            "description_en": "Jean Macquart's closest friend and comrade in La Débâcle. An educated, idealistic young Parisian who enlists with Jean's regiment and shares the catastrophic retreat from Sedan. He becomes a Communard during the Paris Commune, and Jean — fighting with the Versaillais — kills him without knowing who he is in the final battle. His death is the cycle's last great tragedy of war.",
            "description_fr": "Ami et camarade de Jean Macquart dans La Débâcle. Communard idéaliste, il est tué par Jean lui-même lors des combats de la Commune.",
            "physical_en": "Fair, slight, with the earnest face of an educated young man who still believes in what France might be.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },
        {
            "slug": "caroline-hamelin",
            "name": "Caroline Hamelin",
            "occupation": "Engineer's sister, banker's partner",
            "branch": "other",
            "generation": 3,
            "description_en": "The moral conscience of L'Argent, and one of the most fully realised women in the cycle. She accompanies her brother Georges Hamelin in his dealings with Saccard and watches the Universal Bank's rise with growing disquiet — she knows Saccard is not honest, she knows the stock price is manipulated, and yet she stays, partly out of genuine affection for him and partly because her brother's real projects (which are genuinely valuable) are bound up in the enterprise. She travels to the Orient with Hamelin as the bank's ostensible projects take shape there, observing the genuine work being done even as the speculation in Paris grows monstrous. When the crash comes she is not ruined; when Saccard is arrested she does not abandon him entirely. What distinguishes her is not innocence — she is never innocent — but a lucidity that somehow coexists with continued engagement. Zola uses her to explore the question of how a decent person relates to a corrupt world: whether watching is complicity, whether love for a scoundrel is a moral failure, whether dignity can be maintained in contact with dishonesty.",
            "description_fr": "Conscience morale de L'Argent. Elle accompagne son frère Hamelin dans ses dealings avec Saccard, observe la montée frauduleuse de la Banque universelle avec un malaise lucide, reste malgré tout — par affection pour Saccard et attachement aux vrais projets de son frère. Elle survit au désastre sans être ruinée. Zola l'utilise pour explorer comment un être honnête se comporte dans un monde corrompu.",
            "physical_en": "Dark, handsome, with the intelligent eyes of a woman who understands men well and has decided, after weighing the evidence, not to be destroyed by them.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },
        {
            "slug": "hamelin",
            "name": "Georges Hamelin",
            "occupation": "Engineer, financial visionary",
            "branch": "other",
            "generation": 3,
            "description_en": "Caroline Hamelin's brother and the moral foil to Saccard's speculative genius in L'Argent. Hamelin is a genuine engineer with real plans for productive enterprise in the Orient — railways across the Ottoman Empire, agricultural projects in the Levant, a shipping company for the eastern Mediterranean. His projects are technically sound and humanly valuable. He is also entirely unsuited to the world of finance: when Saccard takes his plans as the basis for the Universal Bank, Hamelin departs for the Orient to actually begin building, blissfully unaware that back in Paris the stock price is being manipulated into the stratosphere. He returns to find his genuine work buried under the rubble of Saccard's fraud, his name attached to a catastrophe he did not cause. Zola uses him to represent productive capital — the thing that speculation claims to serve but systematically devours.",
            "description_fr": "Frère de Caroline Hamelin et pendant moral de Saccard dans L'Argent. Ingénieur aux vrais projets en Orient — chemins de fer ottomans, agriculture levanine — il part construire pendant que Saccard manipule le cours de la Banque universelle. Il revient pour trouver son travail honnête enterré sous la fraude. Zola l'utilise pour incarner le capital productif que la spéculation prétend servir mais dévore en réalité.",
            "physical_en": "Quiet, precise, with the focused air of an engineer who thinks in structures and forces — a man more at ease with blueprints than with boardrooms.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },
        {
            "slug": "jeanne-grandjean",
            "name": "Jeanne Grandjean",
            "occupation": "Child",
            "branch": "mouret",
            "generation": 3,
            "description_en": "Hélène Grandjean's daughter in Une Page d'Amour. A sensitive, somewhat sickly child who worships her mother with an almost jealous intensity. When she senses her mother's love affair with Dr Deberle, she sickens and dies — as though her love itself is a kind of consumption. Her death is the price Hélène pays for her passion.",
            "description_fr": "Fille d'Hélène dans Une Page d'Amour. Enfant sensible et jalouse de l'amour de sa mère, elle dépérit et meurt comme conséquence de la liaison de celle-ci.",
            "physical_en": "Pale, dark-eyed, with her mother's beauty in miniature and an intensity of feeling quite out of proportion to her small body.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },
        {
            "slug": "dr-deberle",
            "name": "Dr Henri Deberle",
            "occupation": "Physician",
            "branch": "other",
            "generation": 2,
            "description_en": "Hélène Grandjean's neighbour and lover in Une Page d'Amour. A fashionable Paris doctor — charming, elegant, somewhat superficial. He and Hélène fall into a love affair that neither can quite sustain, and his ultimate inadequacy as a partner makes her sacrifice of her daughter's happiness all the more bitter.",
            "description_fr": "Voisin et amant d'Hélène dans Une Page d'Amour. Médecin parisien charmant mais un peu superficiel dont la liaison avec Hélène coûte cher à tous les deux.",
            "physical_en": "Well-dressed, pleasant-faced, with the assured manner of a successful Paris doctor.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },
        {
            "slug": "felicien-de-hautecoeur",
            "name": "Félicien de Hautecœur",
            "occupation": "Young nobleman",
            "branch": "other",
            "generation": 3,
            "description_en": "The young man at the centre of Le Rêve — the living embodiment of Angélique's hagiographic dreams. Son of Monseigneur de Hautecœur, the local bishop and head of a family of ancient piety and aristocratic descent, he has grown up in the shadow of the cathedral as Angélique has grown up in its literal shadow, and the two seem almost predestined to find each other. Zola treats him with unusual sympathy and without irony: he is precisely what he appears to be — genuinely noble, genuinely in love, genuinely troubled by his father's refusal to consent to their marriage. He fights for Angélique, brings his father to her bedside when she is dying, and Monseigneur's blessing is what saves her. They marry in the cathedral. She dies immediately after. Félicien is one of the very few Zola male characters who is not in some sense a predator, a failure, or a fraud.",
            "description_fr": "Le jeune homme central du Rêve — incarnation vivante des rêves hagiographiques d'Angélique. Fils de Monseigneur de Hautecœur, il grandit dans l'ombre de la cathédrale comme elle l'a fait. Zola le traite avec une sympathie inhabituelle et sans ironie : il est exactement ce qu'il paraît être — noblement amoureux, sincèrement éprouvé par le refus de son père. Il obtient la bénédiction paternelle ; ils se marient ; Angélique meurt sur les marches.",
            "physical_en": "Young, fine-featured, with the luminous quality that Angélique associates with the figures in her saints' lives — beautiful enough to seem fictional.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },

        # ── Nana — key characters ────────────────────────────────────────────
        {
            "slug": "count-muffat",
            "name": "Count Muffat de Beuville",
            "occupation": "Court chamberlain",
            "branch": "other",
            "generation": 2,
            "description_en": "The central male figure of Nana and Zola's most detailed portrait of an establishment destroyed by its own suppressed desires. Count Muffat de Beuville is a rigidly devout Catholic, a court chamberlain under Napoleon III, a man of impeccable moral reputation — whose encounter with Nana at the Théâtre des Variétés undoes him completely. Zola renders his fall with clinical precision and without scorn: Muffat is not a hypocrite who secretly wants what he publicly condemns; he genuinely believes in everything he has built his life on, and the desire he feels for Nana is to him not a temptation but a catastrophe. He becomes her most devoted patron, most thorough ruin, and most pitiable victim — enduring humiliations that would drive a man of less rigid principle to leave immediately, because the alternative (giving up Nana) is more intolerable than any humiliation. His wife, the Countess Muffat, is simultaneously involved with other men — the sexual disorder radiates through the Empire's governing class. His destruction is Zola's political allegory made flesh: the Second Empire hollow at its moral centre.",
            "description_fr": "Figure masculine centrale de Nana. Chambellan impérial rigidement catholique et moralement irréprochable — dont la rencontre avec Nana le détruit entièrement. Zola rend sa chute avec une précision clinique et sans mépris : Muffat ne désire pas secrètement ce qu'il condamne ; le désir lui arrive comme une catastrophe. Sa destruction est l'allégorie politique du cycle : la classe dirigeante impériale creuse à son centre moral.",
            "physical_en": "Stiff, formal, with the precisely maintained bearing of a man for whom self-control has been the primary discipline of a lifetime — and the increasingly ravaged look, as the novel progresses, of someone losing that control irreversibly.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },
        {
            "slug": "fontan",
            "name": "Fontan",
            "occupation": "Actor",
            "branch": "other",
            "generation": 2,
            "description_en": "The coarse, unsuccessful actor in Nana — Nana's one genuine attachment. Fontan is the anomaly in the novel's scheme: among all the wealthy, well-connected men Nana takes as patrons, he is the only one she chooses freely, the only one she pursues rather than receives. He is not rich, not powerful, not even particularly good-looking — he is rough, loud, casually cruel, and a failure at his trade. She lives with him in a tiny apartment on an ordinary street; he beats her; she stays. Zola never fully explains this (it may not be fully explicable), but the relationship illuminates what desire costs Nana as opposed to what it costs her patrons: with the others, she gives nothing. With Fontan, she gives everything and gets beaten for it. He eventually tires of her and throws her out. She returns without apparent grievance to the professional life of the courtesan — but the Fontan episode remains the novel's strangest and most humanising passage.",
            "description_fr": "L'acteur raté dans Nana — seul homme que Nana choisit librement. Elle l'aime, vit avec lui dans un petit appartement, le laisse la battre, et reste. Parmi tous ses admirateurs riches et puissants, il est celui à qui elle donne tout sans rien recevoir. Zola ne l'explique pas entièrement, et c'est le passage le plus humanisant du roman.",
            "physical_en": "Stocky, loud-voiced, with an actor's exaggerated face and gestures even in private — a man who performs all the time, whether the audience is there or not.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },

        # ── L'Œuvre — key character ───────────────────────────────────────────
        {
            "slug": "sandoz",
            "name": "Pierre Sandoz",
            "occupation": "Novelist",
            "branch": "other",
            "generation": 3,
            "description_en": "Claude Lantier's closest friend in L'Œuvre and Zola's most explicit self-portrait. Sandoz is a novelist who, like Claude, came to Paris from the south as a young man, shared the early idealism of the Impressionist generation, and has decided to write a vast cycle of novels documenting French society in scientific terms — an ambition the reader recognises immediately as the Rougon-Macquart project itself. Unlike Claude, Sandoz succeeds: he works with discipline, delivers what he promises, accepts the limitations of the possible, and builds something durable. His success is not without cost — it isolates him from Claude, who begins to regard the measured achiever with a mixture of envy and contempt that neither can fully articulate. Sandoz watches Claude's destruction from inside: he is the one who finds him, visits him through the years of obsession, and is present in the closing pages to say the farewell the novel ends on. The self-portrait is honest to the point of harshness: Zola does not exempt Sandoz from the accusation that choosing to be the survivor is also a choice.",
            "description_fr": "Meilleur ami de Claude Lantier dans L'Œuvre et autoportrait le plus explicite de Zola. Romancier qui conçoit un vaste cycle sur la société française — le projet Rougon-Macquart lui-même. Il réussit là où Claude échoue : par la discipline, l'acceptation des limites, le travail méthodique. Il assiste à la destruction de Claude depuis l'intérieur, et prononce les derniers mots du roman. L'autoportrait est d'une honnêteté implacable : choisir de survivre est aussi un choix.",
            "physical_en": "Solid, energetic, with the particular quality of a man who has decided exactly what he is doing and is doing it — a contrast to Claude's consuming, unresolved energy.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },

        # ── La Faute de l'Abbé Mouret — key character ────────────────────────
        {
            "slug": "frere-archangias",
            "name": "Frère Archangias",
            "occupation": "Lay brother, Brotherhood of the Holy Spirit",
            "branch": "other",
            "generation": 2,
            "description_en": "The most violently anti-flesh figure in La Faute de l'Abbé Mouret — the lay brother of the Brotherhood of the Holy Spirit who is Serge Mouret's closest colleague and the instrument of his retrieval from Le Paradou. Archangias is a study in the dark underside of religious asceticism: he hates women with a rage that is barely distinguishable from desire, regarding them as the devil's primary instrument; he treats the village children he teaches with a brutality that he calls discipline; and he storms through the Provençal countryside as though the flesh itself were his enemy. He is not a hypocrite — he genuinely believes everything he preaches, which makes him more frightening than a simple bigot. When he realises that Serge has been living with Albine in the Paradou, he moves with cold efficiency to destroy it. He drags Serge back to the Church; he finds Albine and drives her off with a contempt that combines theology and personal revulsion. He is present at the novel's ending, unmoved by Albine's death — which he regards as the just consequence of sin. Zola gives him enough intelligence and consistency to make him genuinely disturbing rather than merely grotesque.",
            "description_fr": "Frère laïque de la confrérie du Saint-Esprit et collègue de Serge Mouret dans La Faute. Il hait les femmes avec une intensité indissociable du désir refoulé, traite les enfants du catéchisme avec brutalité, et stoppe l'idylle du Paradou avec une froideur efficace. Sa présence à la fin du roman, indifférent à la mort d'Albine, est parmi les moments les plus glaçants du cycle.",
            "physical_en": "Large-framed, thick-necked, with enormous hairy hands and a jaw like a door — a man whose physical presence suggests suppressed animal force.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },

        # ── Le Ventre de Paris — key character ───────────────────────────────
        {
            "slug": "la-normande",
            "name": "La Normande",
            "birth_name": "Louise Méhudin",
            "occupation": "Fish stall holder",
            "branch": "other",
            "generation": 2,
            "description_en": "The magnificent, arrogant fish seller of Le Ventre de Paris — Florent's reluctant attraction and Lisa Quenu's great rival in the social politics of Les Halles. Louise Méhudin is known throughout the market as La Normande: tall, superb, with the kind of beauty that belongs to a woman completely at home in her body and her trade. She runs her stall with absolute authority, and the fish she sells are an extension of her own particular presence — vivid, cold, gleaming. Her relationship with Florent is the novel's one moment of something like tenderness: she is curious about him (a thin, idealistic man unlike anything she has encountered in the market), briefly drawn to him, and ultimately frightened by his politics. Her rivalry with Lisa Quenu — over custom, over status, over the sexual dynamics of the market — is one of the novel's running energies, and Zola renders the market women's wars with an anthropological precision he clearly enjoyed.",
            "description_fr": "Marchande de poissons magnifique et souveraine des Halles — attraction réticente de Florent et grande rivale de Lisa Quenu. Louise Méhudin — la Normande — règne sur son étal avec l'autorité d'une femme entièrement chez elle dans son corps et son métier. Sa brève attirance pour Florent est le moment le plus tendre du roman, vite étouffé par la peur de ses idées politiques.",
            "physical_en": "Tall, fair, with the particular radiant health of a woman who has worked in the open air all her life — a queen of her quarter, and fully aware of it.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },

        # ── Au Bonheur des Dames — key character ─────────────────────────────
        {
            "slug": "bourdoncle",
            "name": "Bourdoncle",
            "occupation": "Department store director",
            "branch": "other",
            "generation": 2,
            "description_en": "Octave Mouret's chief business partner and the cold intelligence behind Au Bonheur des Dames's commercial operations. Bourdoncle does not share Mouret's charm or his genius for understanding desire, but he has an absolute clarity about what a business requires: efficiency, discipline, the ruthless subordination of sentiment to profit. From the first, he distrusts Denise Baudu — not because she is incompetent (he can see she is not) but because he understands that Mouret is becoming dangerously interested in her, and sentiment is, in his view, the only thing that can destroy what they have built together. He advises Mouret against her at every stage. He is not villainous; he is simply a man of pure economic rationality, and the novel's implicit question is whether that is compatible with being fully human. When Mouret chooses Denise over the logic Bourdoncle represents, Bourdoncle's position in the store becomes, in a sense, permanently subordinate — he was right about everything except what mattered most.",
            "description_fr": "Associé principal de Mouret et intelligence froide du Bonheur des Dames. Bourdoncle n'a pas le génie de Mouret pour le désir mais possède une clarté absolue sur ce que les affaires exigent. Il se méfie de Denise dès le début — non par incompétence de sa part, mais parce qu'il voit Mouret la regarder avec des yeux dangereux. Il conseille contre elle à chaque étape. Rationnel pur, il a raison de tout sauf de l'essentiel.",
            "physical_en": "Neat, precise, with watchful eyes and the particular stillness of a man who is always calculating — handsome in a cold, orderly way.",
            "featured_on_landing": False, "tree_x": None, "tree_y": None,
        },
    ]

    chars = {}
    for c_data in chars_data:
        c = Character(
            slug=c_data["slug"],
            name=c_data["name"],
            birth_name=c_data.get("birth_name"),
            occupation=c_data.get("occupation"),
            branch=c_data.get("branch", "other"),
            generation=c_data.get("generation", 2),
            description_en=c_data.get("description_en"),
            description_fr=c_data.get("description_fr"),
            physical_en=c_data.get("physical_en"),
            image_url=c_data.get("image_url"),
            image_credit=c_data.get("image_credit"),
            featured_on_landing=c_data.get("featured_on_landing", False),
            tree_x=c_data.get("tree_x"),
            tree_y=c_data.get("tree_y"),
        )
        db.add(c)
        db.flush()
        chars[c_data["slug"]] = c

    # ── RELATIONS ────────────────────────────────────────────────────────────
    def relate(a, b, rtype, desc=None):
        if a in chars and b in chars:
            db.add(CharacterRelation(
                character_a_id=chars[a].id,
                character_b_id=chars[b].id,
                relation_type=rtype,
                description=desc
            ))

    # ── Adélaïde's children ──────────────────────────────────────────────────
    for child in ["pierre-rougon", "antoine-macquart", "ursule-macquart"]:
        relate("adelaide-fouque", child, "parent")
        relate(child, "adelaide-fouque", "child")
    # Silvère is Ursule's son, not Adélaïde's direct child
    relate("adelaide-fouque", "silvere-mouret", "grandchild",
           "She raised Silvère after Ursule's death.")
    relate("silvere-mouret", "adelaide-fouque", "grandparent")

    # ── Pierre & Félicité's children ─────────────────────────────────────────
    for child in ["eugene-rougon", "aristide-saccard", "pascal-rougon",
                  "sidonie-rougon", "marthe-rougon"]:
        relate("pierre-rougon", child, "parent")
        relate("felicite-rougon", child, "parent")
        relate(child, "pierre-rougon", "child")
        relate(child, "felicite-rougon", "child")

    # ── Antoine's children ───────────────────────────────────────────────────
    for child in ["lisa-quenu", "gervaise-macquart", "jean-macquart"]:
        relate("antoine-macquart", child, "parent")
        relate(child, "antoine-macquart", "child")

    # ── Ursule's children ────────────────────────────────────────────────────
    for child in ["francois-mouret", "helene-grandjean", "silvere-mouret"]:
        relate("ursule-macquart", child, "parent")
        relate(child, "ursule-macquart", "child")

    # ── François & Marthe's children ─────────────────────────────────────────
    for child in ["octave-mouret", "serge-mouret", "desiree-mouret"]:
        relate("francois-mouret", child, "parent")
        relate("marthe-rougon", child, "parent")
        relate(child, "francois-mouret", "child")
        relate(child, "marthe-rougon", "child")

    # ── Gervaise's children ──────────────────────────────────────────────────
    for child in ["etienne-lantier", "claude-lantier", "jacques-lantier"]:
        relate("gervaise-macquart", child, "parent")
        relate("lantier", child, "parent")
        relate(child, "gervaise-macquart", "child")
        relate(child, "lantier", "child")
    relate("gervaise-macquart", "nana", "parent")
    relate("coupeau", "nana", "parent")
    relate("nana", "gervaise-macquart", "child")
    relate("nana", "coupeau", "child")

    # ── Aristide Saccard's children ──────────────────────────────────────────
    relate("aristide-saccard", "maxime-saccard", "parent")
    relate("maxime-saccard", "aristide-saccard", "child")
    relate("aristide-saccard", "victor-saccard", "parent",
           "Illegitimate son, acknowledged late in L'Argent.")
    relate("victor-saccard", "aristide-saccard", "child")

    # ── Lisa's children ──────────────────────────────────────────────────────
    relate("lisa-quenu", "pauline-quenu", "parent")
    relate("quenu", "pauline-quenu", "parent")
    relate("pauline-quenu", "lisa-quenu", "child")
    relate("pauline-quenu", "quenu", "child")

    # ── Hélène's children ────────────────────────────────────────────────────
    relate("helene-grandjean", "jeanne-grandjean", "parent")
    relate("jeanne-grandjean", "helene-grandjean", "child")

    # ── Siblings ─────────────────────────────────────────────────────────────
    sibling_pairs = [
        ("pierre-rougon", "antoine-macquart"),
        ("pierre-rougon", "ursule-macquart"),
        ("antoine-macquart", "ursule-macquart"),
        ("eugene-rougon", "aristide-saccard"),
        ("eugene-rougon", "pascal-rougon"),
        ("eugene-rougon", "sidonie-rougon"),
        ("eugene-rougon", "marthe-rougon"),
        ("aristide-saccard", "pascal-rougon"),
        ("aristide-saccard", "sidonie-rougon"),
        ("aristide-saccard", "marthe-rougon"),
        ("pascal-rougon", "sidonie-rougon"),
        ("pascal-rougon", "marthe-rougon"),
        ("sidonie-rougon", "marthe-rougon"),
        ("lisa-quenu", "gervaise-macquart"),
        ("lisa-quenu", "jean-macquart"),
        ("gervaise-macquart", "jean-macquart"),
        ("etienne-lantier", "claude-lantier"),
        ("etienne-lantier", "jacques-lantier"),
        ("etienne-lantier", "nana"),
        ("claude-lantier", "jacques-lantier"),
        ("claude-lantier", "nana"),
        ("jacques-lantier", "nana"),
        ("octave-mouret", "serge-mouret"),
        ("octave-mouret", "desiree-mouret"),
        ("serge-mouret", "desiree-mouret"),
        ("francois-mouret", "helene-grandjean"),
        ("francois-mouret", "silvere-mouret"),
        ("helene-grandjean", "silvere-mouret"),
    ]
    for a, b in sibling_pairs:
        relate(a, b, "sibling")
        relate(b, a, "sibling")

    # ── Marriages & unions ───────────────────────────────────────────────────
    for a, b in [
        ("pierre-rougon", "felicite-rougon"),
        ("felicite-rougon", "pierre-rougon"),
        ("antoine-macquart", "josephine-macquart"),
        ("josephine-macquart", "antoine-macquart"),
        ("francois-mouret", "marthe-rougon"),
        ("marthe-rougon", "francois-mouret"),
        ("lisa-quenu", "quenu"),
        ("quenu", "lisa-quenu"),
        ("roubaud", "severine-roubaud"),
        ("severine-roubaud", "roubaud"),
    ]:
        relate(a, b, "spouse")

    relate("aristide-saccard", "renee-saccard", "spouse",
           "Second marriage — scandalous and unhappy.")
    relate("renee-saccard", "aristide-saccard", "spouse")
    relate("gervaise-macquart", "coupeau", "union",
           "Married; his alcoholism destroys them both.")
    relate("coupeau", "gervaise-macquart", "union")

    # ── Other significant relationships ──────────────────────────────────────
    relate("maxime-saccard", "renee-saccard", "lover",
           "Stepson and stepmother — the scandalous affair at the heart of La Curée.")
    relate("renee-saccard", "maxime-saccard", "lover")
    relate("octave-mouret", "denise-baudu", "lover",
           "He pursues her relentlessly; she refuses until he truly loves her; they marry.")
    relate("denise-baudu", "octave-mouret", "lover")
    relate("pascal-rougon", "clotilde-rougon", "lover",
           "Uncle and niece — a controversial late-life love, framed as life-affirming in the final novel.")
    relate("clotilde-rougon", "pascal-rougon", "lover")
    relate("etienne-lantier", "catherine-maheu", "lover",
           "He loves her throughout Germinal; they are united only in the flooded mine, where they die.")
    relate("catherine-maheu", "etienne-lantier", "lover")
    relate("catherine-maheu", "chaval", "union",
           "An unwilling relationship — Chaval took her at fifteen and dominates her through fear.")
    relate("serge-mouret", "albine", "lover",
           "His love for Albine in Le Paradou — passionate, Edenic, and ultimately impossible.")
    relate("albine", "serge-mouret", "lover")
    relate("helene-grandjean", "dr-deberle", "lover",
           "A brief but catastrophic affair that costs Hélène her daughter.")
    relate("dr-deberle", "helene-grandjean", "lover")
    relate("jacques-lantier", "severine-roubaud", "lover",
           "Their doomed love affair in La Bête humaine.")
    relate("severine-roubaud", "jacques-lantier", "lover")
    relate("silvere-mouret", "miette", "lover",
           "Young Republican lovers who die together during the 1851 coup.")
    relate("miette", "silvere-mouret", "lover")
    relate("florent-quenu", "lisa-quenu", "sibling-in-law",
           "Lisa's brother-in-law — the idealist in the world of the comfortable charcuterie.")
    relate("gervaise-macquart", "lantier", "union",
           "Her first partner, who abandoned her and later returned to live off her.")

    db.commit()

    # ── CHARACTER ↔ NOVEL APPEARANCES ────────────────────────────────────────
    appearances = [
        # La Fortune des Rougons
        ("adelaide-fouque",     "la-fortune-des-rougon",        "major"),
        ("pierre-rougon",       "la-fortune-des-rougon",        "major"),
        ("felicite-rougon",     "la-fortune-des-rougon",        "major"),
        ("antoine-macquart",    "la-fortune-des-rougon",        "major"),
        ("josephine-macquart",  "la-fortune-des-rougon",        "minor"),
        ("silvere-mouret",      "la-fortune-des-rougon",        "major"),
        ("miette",              "la-fortune-des-rougon",        "major"),
        ("eugene-rougon",       "la-fortune-des-rougon",        "minor"),
        ("aristide-saccard",    "la-fortune-des-rougon",        "minor"),
        ("pascal-rougon",       "la-fortune-des-rougon",        "minor"),

        # La Curée
        ("aristide-saccard",    "la-curee",                     "major"),
        ("renee-saccard",       "la-curee",                     "major"),
        ("maxime-saccard",      "la-curee",                     "major"),
        ("sidonie-rougon",      "la-curee",                     "minor"),

        # Le Ventre de Paris
        ("lisa-quenu",          "le-ventre-de-paris",           "major"),
        ("florent-quenu",       "le-ventre-de-paris",           "major"),
        ("quenu",               "le-ventre-de-paris",           "major"),
        ("la-normande",         "le-ventre-de-paris",           "major"),
        ("claude-lantier",      "le-ventre-de-paris",           "minor"),

        # La Conquête de Plassans
        ("marthe-rougon",       "la-conquete-de-plassans",      "major"),
        ("francois-mouret",     "la-conquete-de-plassans",      "major"),
        ("abbe-faujas",         "la-conquete-de-plassans",      "major"),
        ("serge-mouret",        "la-conquete-de-plassans",      "minor"),

        # La Faute de l'Abbé Mouret
        ("serge-mouret",        "la-faute-de-labbe-mouret",     "major"),
        ("albine",              "la-faute-de-labbe-mouret",     "major"),
        ("desiree-mouret",      "la-faute-de-labbe-mouret",     "major"),
        ("frere-archangias",    "la-faute-de-labbe-mouret",     "major"),
        ("pascal-rougon",       "la-faute-de-labbe-mouret",     "minor"),

        # Son Excellence Eugène Rougon
        ("eugene-rougon",       "son-excellence-eugene-rougon", "major"),
        ("clorinde-balbi",      "son-excellence-eugene-rougon", "major"),
        ("felicite-rougon",     "son-excellence-eugene-rougon", "minor"),
        ("pierre-rougon",       "son-excellence-eugene-rougon", "minor"),
        ("sidonie-rougon",      "son-excellence-eugene-rougon", "minor"),

        # L'Assommoir
        ("gervaise-macquart",   "lassommoir",                   "major"),
        ("coupeau",             "lassommoir",                   "major"),
        ("lantier",             "lassommoir",                   "major"),
        ("goujet",              "lassommoir",                   "major"),
        ("virginie-poisson",    "lassommoir",                   "major"),
        ("nana",                "lassommoir",                   "minor"),
        ("etienne-lantier",     "lassommoir",                   "minor"),
        ("claude-lantier",      "lassommoir",                   "minor"),
        ("antoine-macquart",    "lassommoir",                   "minor"),
        ("josephine-macquart",  "lassommoir",                   "minor"),

        # Une Page d'amour
        ("helene-grandjean",    "une-page-damour",              "major"),
        ("jeanne-grandjean",    "une-page-damour",              "major"),
        ("dr-deberle",          "une-page-damour",              "major"),

        # Nana
        ("nana",                "nana",                         "major"),
        ("count-muffat",        "nana",                         "major"),
        ("fontan",              "nana",                         "major"),
        ("gervaise-macquart",   "nana",                         "minor"),
        ("maxime-saccard",      "nana",                         "minor"),

        # Pot-Bouille
        ("octave-mouret",       "pot-bouille",                  "major"),
        ("denise-baudu",        "pot-bouille",                  "minor"),

        # Au Bonheur des Dames
        ("octave-mouret",       "au-bonheur-des-dames",         "major"),
        ("denise-baudu",        "au-bonheur-des-dames",         "major"),
        ("bourdoncle",          "au-bonheur-des-dames",         "major"),

        # La Joie de Vivre
        ("pauline-quenu",       "la-joie-de-vivre",             "major"),
        ("lazare-chanteau",     "la-joie-de-vivre",             "major"),

        # Germinal
        ("etienne-lantier",     "germinal",                     "major"),
        ("souvarine",           "germinal",                     "major"),
        ("toussaint-maheu",     "germinal",                     "major"),
        ("la-maheude",          "germinal",                     "major"),
        ("catherine-maheu",     "germinal",                     "major"),
        ("bonnemort",           "germinal",                     "major"),
        ("jeanlin-maheu",       "germinal",                     "major"),
        ("chaval",              "germinal",                     "major"),
        ("rasseneur",           "germinal",                     "major"),
        ("hennebeau",           "germinal",                     "major"),
        ("deneulin",            "germinal",                     "major"),
        ("jacques-lantier",     "germinal",                     "minor"),

        # L'Œuvre
        ("claude-lantier",      "loeuvre",                      "major"),
        ("christine-halleguen", "loeuvre",                      "major"),
        ("sandoz",              "loeuvre",                      "major"),

        # La Terre
        ("jean-macquart",       "la-terre",                     "major"),
        ("antoine-macquart",    "la-terre",                     "minor"),

        # Le Rêve
        ("angelique-rougon",        "le-reve",                      "major"),
        ("felicien-de-hautecoeur",  "le-reve",                      "major"),

        # La Bête humaine
        ("jacques-lantier",     "la-bete-humaine",              "major"),
        ("severine-roubaud",    "la-bete-humaine",              "major"),
        ("roubaud",             "la-bete-humaine",              "major"),
        ("flore",               "la-bete-humaine",              "major"),
        ("etienne-lantier",     "la-bete-humaine",              "minor"),

        # L'Argent
        ("aristide-saccard",    "largent",                      "major"),
        ("caroline-hamelin",    "largent",                      "major"),
        ("hamelin",             "largent",                      "major"),
        ("maxime-saccard",      "largent",                      "minor"),
        ("victor-saccard",      "largent",                      "minor"),

        # La Débâcle
        ("jean-macquart",       "la-debacle",                   "major"),
        ("maurice-levasseur",   "la-debacle",                   "major"),

        # Le Docteur Pascal
        ("pascal-rougon",       "le-docteur-pascal",            "major"),
        ("clotilde-rougon",     "le-docteur-pascal",            "major"),
        ("felicite-rougon",     "le-docteur-pascal",            "major"),
        ("adelaide-fouque",     "le-docteur-pascal",            "major"),
        ("eugene-rougon",       "le-docteur-pascal",            "minor"),
        ("aristide-saccard",    "le-docteur-pascal",            "minor"),
        ("maxime-saccard",      "le-docteur-pascal",            "minor"),
    ]

    for char_slug, novel_slug, role in appearances:
        if char_slug in chars and novel_slug in novels:
            db.add(CharacterAppearance(
                character_id=chars[char_slug].id,
                novel_id=novels[novel_slug].id,
                role=role
            ))

    # ── LOCATIONS ────────────────────────────────────────────────────────────
    locations_data = [
        ("paris", "Paris", "city",
         "The heart of the Second Empire and the dominant setting of the cycle. Zola's Paris is a city in violent transformation — Haussmann's great boulevards cutting through the old warrens, fortunes made and lost on the scaffolding of demolition, the working classes driven to the periphery. It appears in at least a dozen of the twenty novels.",
         "Le cœur du Second Empire et le décor dominant du cycle. Paris est une ville en transformation violente sous Haussmann.",
         True, 48.8566, 2.3522),
        ("plassans", "Plassans", "city",
         "A fictional provincial town in the south of France, modelled closely on Aix-en-Provence (where Zola grew up). The ancestral home of the Rougon family and the setting of three novels — La Fortune des Rougon, La Conquête de Plassans, and Le Docteur Pascal. Zola describes it as a sleepy, sun-baked town divided into three quartiers — the aristocratic Saint-Marc, the bourgeois new town, and the working-class old quarter. Its gossip, its small ambitions, and its yellow-walled calm make the Rougons' scheming all the more vivid: here a man can seize power with forty-one armed neighbours and a lucky night. The aire Saint-Mittre — a disused cemetery on the edge of town — is where Silvère and Miette meet in secret, and where Silvère is ultimately executed beside the tombstone of Marie. The asylum at Les Tulettes is a few miles outside Plassans; Adélaïde Fouque will spend her last decades there.",
         "Ville provinciale fictive inspirée d'Aix-en-Provence. Berceau des Rougon et décor de trois romans. L'aire Saint-Mittre, ancien cimetière en lisière de la ville, est le lieu de rencontre secret de Silvère et Miette, et le lieu de l'exécution de Silvère.",
         True, 43.5297, 5.4474),
        ("montsou", "Montsou", "mining town",
         "A fictional coal-mining town in northern France, based on Anzin and the Valenciennes coalfield. The setting of Germinal — flat, black, dominated by the pit-heads, slag heaps, and the devouring mouth of the Voreux mine. Zola researched it exhaustively, living among miners to capture the conditions accurately.",
         "Ville minière fictive du Nord de la France. Décor de Germinal, avec le puits Voreux, les terrils et les corons.",
         True, 50.3587, 3.5161),
        ("les-halles", "Les Halles", "market district",
         "The great central market of Paris — Baltard's magnificent iron-and-glass pavilions, completed in the 1850s and 1860s. The setting of Le Ventre de Paris, representing the overwhelming, indifferent abundance of the city's belly. Demolished in 1971, it now exists only in Zola's novel.",
         "Le grand marché central de Paris, avec ses magnifiques pavillons Baltard. Décor du Ventre de Paris.",
         True, 48.8612, 2.3470),
        ("la-goutte-dor", "La Goutte d'Or", "working-class district",
         "A working-class district of northern Paris, the setting of L'Assommoir. Zola researched it meticulously, walking its streets and visiting its laundries and zinc-topped bars. Named for its golden wine, it was in Zola's time a world of overcrowded tenements, seasonal workers, and grinding poverty.",
         "Quartier ouvrier du nord de Paris, décor de L'Assommoir. Zola l'a minutieusement documenté.",
         True, 48.8843, 2.3580),
        ("le-paradou", "Le Paradou", "garden / estate",
         "The vast, wild, overgrown garden at the heart of La Faute de l'Abbé Mouret — a reimagining of Eden, where Serge and Albine live outside of time and civilisation. Based loosely on gardens near Aix-en-Provence, it is one of Zola's greatest imaginative creations.",
         "L'immense jardin sauvage au cœur de La Faute de l'Abbé Mouret — une réinvention de l'Eden.",
         True, 43.65, 5.55),
        ("voreux-mine", "The Voreux", "mine",
         "The fictional coalmine at the centre of Germinal — dark, devouring, almost alive. Its name (from Latin vorare, to devour) signals its role as the maw that swallows men whole. The flooding and collapse of the Voreux in the novel's climax is one of the great catastrophic set pieces of nineteenth-century fiction.",
         "La mine fictive au cœur de Germinal. Son nom vient du latin vorare (dévorer). Son inondation finale est une des grandes catastrophes de la fiction du XIXe siècle.",
         True, 50.36, 3.52),
        ("au-bonheur-des-dames-store", "Au Bonheur des Dames", "department store",
         "The vast, ever-expanding department store that Octave Mouret builds in central Paris — one of the first of its kind, inspired by Le Bon Marché and the Grands Magasins du Louvre. A machine for selling, for dazzling women, for crushing the small trader. The building grows with each chapter, consuming buildings and lives.",
         "Le grand magasin qu'Octave Mouret bâtit au centre de Paris, inspiré du Bon Marché. Machine à vendre qui écrase les petits commerçants.",
         False, 48.855, 2.335),
        ("la-bete-humaine-railway", "Paris–Le Havre Railway", "railway",
         "The iron road of La Bête humaine — the Paris-Saint-Lazare to Le Havre line, its tunnels, level crossings, and snowbound tracks. The railway in this novel is both a character and a metaphor: modernity as unstoppable force, beautiful and murderous.",
         "La ligne ferroviaire Paris-Le Havre, décor de La Bête humaine. Le train y est à la fois personnage et métaphore de la modernité meurtrière.",
         False, 49.44, 1.10),
        ("beauce", "La Beauce", "region",
         "The vast wheat plain south of Paris, the setting of La Terre. Flat, fertile, and elemental — Zola's Beauce is the land itself as a force, indifferent to the human passions it witnesses. The peasantry's attachment to this soil, violent and almost geological, is the novel's subject.",
         "La grande plaine céréalière au sud de Paris, décor de La Terre. La Beauce est une force élémentaire, indifférente aux passions humaines.",
         False, 48.15, 1.75),
    ]

    for row in locations_data:
        db.add(Location(
            slug=row[0], name=row[1], location_type=row[2],
            description_en=row[3], description_fr=row[4],
            featured=row[5], latitude=row[6], longitude=row[7]
        ))

    # ── EVENTS ───────────────────────────────────────────────────────────────
    # Tuples: (title_en, title_fr, year, date_approx, event_type,
    #          novel_slug_or_None, description_en, description_fr, [char_slugs])
    events_data = [
        (
            "Coup d'état of 2 December 1851",
            "Coup d'État du 2 décembre 1851",
            1851, "2 December 1851", "historical",
            "la-fortune-des-rougon",
            "Napoleon III's coup overthrows the Second Republic. In Plassans, Pierre and Félicité Rougon use the chaos to seize local power, founding the family's fortune on the corpses of the Republican resistance.",
            "Le coup d'État de Napoléon III renverse la Seconde République. À Plassans, les Rougon s'emparent du pouvoir local.",
            ["pierre-rougon", "felicite-rougon"],
        ),
        (
            "Death of Silvère and Miette",
            "Mort de Silvère et de Miette",
            1851, "December 1851", "personal",
            "la-fortune-des-rougon",
            "Miette Chantegreil, thirteen years old, is shot and killed while carrying the red Republican flag near Orchères. Silvère Mouret is subsequently arrested and executed by the gendarme Rengade — shot in the head beside the tombstone at the aire Saint-Mittre, the very place where he and Miette had secretly met. Dr Pascal, who will become the cycle's scientific conscience, pronounces Miette dead. The deaths of the two lovers are the cycle's founding tragedy: the Republic, embodied in a child who thought she was carrying the Virgin's banner, is killed; the opportunists inherit.",
            "Miette Chantegreil, treize ans, est abattue en portant le drapeau républicain près d'Orchères. Silvère est ensuite fusillé par le gendarme Rengade à l'aire Saint-Mittre. Leurs morts sont la tragédie inaugurale du cycle.",
            ["silvere-mouret", "miette"],
        ),
        (
            "Adélaïde Fouque confined to Les Tulettes",
            "Internement d'Adélaïde Fouque aux Tulettes",
            1851, "December 1851", "personal",
            "la-fortune-des-rougon",
            "After witnessing her grandson Silvère's execution at the aire Saint-Mittre, Adélaïde Fouque — the matriarch of the entire dynasty — loses the last of her sanity. Raving about 'le prix du sang' (the price of blood), she is committed to the lunatic asylum at Les Tulettes near Plassans. She will remain there for more than twenty years, visited occasionally by other characters across the cycle, an ancient hollow-eyed witness to the dynasty she created. She is still alive in Le Docteur Pascal (1873), aged over a hundred.",
            "Après avoir assisté à l'exécution de son petit-fils Silvère, Adélaïde Fouque sombre définitivement dans la folie. Internée aux Tulettes, elle y vivra plus de vingt ans, témoin silencieux et oublié de la saga qu'elle a fondée.",
            ["adelaide-fouque"],
        ),
        (
            "Napoleon III proclaims the Second Empire",
            "Proclamation du Second Empire",
            1852, "2 December 1852", "historical",
            None,
            "Exactly one year after his coup, Louis-Napoléon Bonaparte declares himself Emperor Napoleon III. The twenty-year span of the Second Empire — the great backdrop of the Rougon-Macquart cycle — begins.",
            "Louis-Napoléon Bonaparte se proclame Napoléon III. Commence le Second Empire, toile de fond des vingt romans.",
            [],
        ),
        (
            "Haussmann's renovation of Paris begins",
            "Début des travaux haussmanniens",
            1853, "1853–1870", "historical",
            "la-curee",
            "Baron Haussmann begins the radical transformation of Paris — slashing boulevards through the old city, displacing the poor, and creating fortunes for speculators. The violent disruption of old Paris is the engine of Saccard's wealth in La Curée.",
            "Le baron Haussmann commence la transformation radicale de Paris. Les grands travaux créent des fortunes pour les spéculateurs comme Saccard.",
            ["aristide-saccard"],
        ),
        (
            "Aristide Saccard makes his first fortune",
            "Première fortune d'Aristide Saccard",
            1860, "c. 1857–1862", "personal",
            "la-curee",
            "Aristide Saccard — born Aristide Rougon, now reinvented as a Parisian speculator — makes his first great fortune buying properties in the path of Haussmann's demolitions. He bribes officials and cultivates informants to learn which streets will be expropriated before the announcements are made, then buys low and sells to the city at enormous profit. Within a few years he has built a lavish hôtel particulier, filled it with an extraordinary hothouse and a wife whose social credentials paper over his origins. The fortune is real; the foundations are rotten.",
            "Aristide Saccard fait sa première grande fortune en achetant des terrains voués à la démolition haussmannienne avant les annonces officielles. Il se construit un hôtel particulier luxueux et épouse Renée Béraud du Châtel. La fortune est réelle, les fondations sont pourries.",
            ["aristide-saccard"],
        ),
        (
            "Eugène Rougon falls and returns to power",
            "Chute et retour au pouvoir d'Eugène Rougon",
            1861, "c. 1856–1869", "political",
            "son-excellence-eugene-rougon",
            "Eugène Rougon's political career under Napoleon III follows a cycle of rise, forced resignation, and triumphant return that the novel traces in full. His 'bande' of followers — clients who have attached themselves to him in hopes of preferment — turn against him when he refuses to use his position for their private ends, engineering his resignation from the Council of State. When the Emperor has need of a strongman again, Rougon is recalled to office more powerful than before. The cycle repeats. Zola uses it to anatomise the machinery of imperial politics: how men rise and fall not on merit or principle, but on the shifting calculations of those who need them.",
            "La carrière d'Eugène Rougon sous Napoléon III suit un cycle de montée, démission forcée et retour triomphal. Sa bande de fidèles le fait tomber quand il refuse de leur accorder des faveurs ; l'Empereur le rappelle plus puissant qu'avant. Zola dissèque ainsi la mécanique du pouvoir impérial.",
            ["eugene-rougon"],
        ),
        (
            "Gervaise establishes her laundry",
            "Gervaise ouvre sa blanchisserie",
            1852, "c. 1852", "personal",
            "lassommoir",
            "Gervaise Macquart realises her modest dream: she opens her own laundry in the Rue Neuve de la Goutte d'Or. For a brief time, the shop succeeds — the high-water mark of her life, the one period when she seems to have won.",
            "Gervaise Macquart réalise son modeste rêve: elle ouvre sa propre blanchisserie. Une brève période de réussite avant la chute.",
            ["gervaise-macquart"],
        ),
        (
            "The great birthday feast at Gervaise's laundry",
            "La grande fête chez Gervaise",
            1854, "c. 1854", "personal",
            "lassommoir",
            "Gervaise's famous birthday feast — a magnificent roast goose shared with friends and neighbours in the laundry. One of the great set-pieces of French naturalism: abundance, warmth, community — and the first shadow of disaster already falling.",
            "Le fameux repas d'anniversaire de Gervaise — une oie rôtie partagée avec ses voisins. Un des grands tableaux du naturalisme, à la fois abondance et premier signe du désastre.",
            ["gervaise-macquart"],
        ),
        (
            "Serge Mouret recovers in the Paradou",
            "Convalescence de Serge Mouret au Paradou",
            1858, "c. 1858", "personal",
            "la-faute-de-labbe-mouret",
            "After a mystical breakdown, the young priest Serge Mouret convalesces in the vast, wild garden called Le Paradou — a reimagined Eden where he meets the irresistible Albine. A lyrical idyll that cannot last: the Church will reclaim him.",
            "Après un effondrement mystique, Serge Mouret se rétablit dans l'immense jardin sauvage du Paradou, où il rencontre l'irrésistible Albine.",
            ["serge-mouret", "albine"],
        ),
        (
            "Étienne Lantier arrives at the Voreux",
            "Étienne Lantier arrive au Voreux",
            1865, "c. 1865", "personal",
            "germinal",
            "A young mechanic arrives on foot in the darkness of a bitter winter night, looking for work at the mine. He finds the Voreux — its furnaces glowing like a maw in the dark — and, with it, his destiny as the leader of the miners' revolt.",
            "Un jeune mécanicien arrive à pied dans la nuit glaciale. Il découvre le Voreux — ses feux luisant comme une gueule dans l'obscurité — et sa destinée comme meneur.",
            ["etienne-lantier"],
        ),
        (
            "The great miners' strike at Montsou",
            "La grande grève de Montsou",
            1866, "c. 1866", "personal",
            "germinal",
            "The miners of Montsou, led by Étienne Lantier, go on strike against the Company's new pay conditions. After weeks of cold and hunger the strike collapses, the army fires on the crowd, and Étienne flees. But the seed is sown.",
            "Les mineurs de Montsou, menés par Étienne, se mettent en grève. Après des semaines de faim, la grève échoue — mais la graine est semée.",
            ["etienne-lantier", "toussaint-maheu", "la-maheude"],
        ),
        (
            "Flooding and collapse of the Voreux",
            "Inondation et effondrement du Voreux",
            1866, "c. 1866", "personal",
            "germinal",
            "The nihilist Souvarine sabotages the Voreux mine's pit-shaft timbers. Water rushes in, the earth shudders, and the pit collapses — swallowing miners alive. The great catastrophe that ends Germinal: destructive, terrifying, and obscurely hopeful.",
            "Souvarine sabote les boisages du puits du Voreux. L'eau s'engouffre, la terre tremble, le puits s'effondre, engloutissant des mineurs vivants.",
            ["etienne-lantier", "souvarine", "catherine-maheu"],
        ),
        (
            "Nana's debut at the Variétés theatre",
            "Débuts de Nana aux Variétés",
            1867, "c. 1867", "personal",
            "nana",
            "Anna Coupeau — Nana — appears on stage in the role of the Golden Venus. Her voice is thin, her acting negligible — but her body electrifies the audience. The career of the Second Empire's most destructive courtesan begins.",
            "Anna Coupeau apparaît sur scène dans le rôle de la Vénus blonde. Sa voix est mince, mais son corps électrise le public. La grande courtisane naît.",
            ["nana"],
        ),
        (
            "Universal Exposition of Paris",
            "Exposition universelle de Paris",
            1867, "1 April – 3 November 1867", "historical",
            "son-excellence-eugene-rougon",
            "The Second Empire at its zenith — Paris dazzles the world with its Universal Exposition, drawing eleven million visitors. The Emperor presides over a triumph of French industry, art, and imperial confidence. Behind the glittering spectacle, Eugène Rougon is navigating the latest phase of his political cycle, and Aristide Saccard's speculation is at its most feverish. The Exposition is the moment before the fall: within three years Napoleon III will be at war with Prussia, and the world it celebrates will be gone.",
            "Le Second Empire à son apogée. Paris éblouit le monde avec son Exposition universelle. Derrière la fête, Rougon manœuvre et Saccard spécule — le moment le plus brillant avant l'effondrement.",
            ["eugene-rougon"],
        ),
        (
            "Saccard's Universal Bank crashes on the Bourse",
            "Effondrement de la Banque Universelle de Saccard",
            1867, "c. 1867", "personal",
            "largent",
            "Aristide Saccard's Universal Bank — built on Georges Hamelin's genuine engineering projects but inflated far beyond their value through manipulation and planted rumour — crashes spectacularly on the Bourse, ruining thousands of small investors: widows, working women, retired tradespeople who had trusted Saccard's promises. Saccard is arrested; he escapes serious consequences, as he always does. His engineer Hamelin returns from the Orient to find his real work buried under rubble. Caroline Hamelin survives with her dignity intact. The crash is one of Zola's most detailed analyses of financial capitalism's capacity for destruction.",
            "La Banque Universelle de Saccard s'effondre en ruinant des milliers de petits épargnants. Saccard est arrêté puis s'en tire. Hamelin revient d'Orient trouver son travail honnête enseveli sous la fraude. Caroline survit dignement.",
            ["aristide-saccard", "caroline-hamelin", "hamelin"],
        ),
        (
            "François Mouret burns the house — the end of La Conquête de Plassans",
            "François Mouret incendie la maison — fin de La Conquête de Plassans",
            1864, "c. 1864", "personal",
            "la-conquete-de-plassans",
            "Having been committed to the lunatic asylum at Les Tulettes — the same institution where his grandmother Adélaïde Fouque lives out her decline — François Mouret escapes and returns at night to the house that Abbé Faujas has entirely taken over. He sets it on fire. Faujas, his sister Olympe, and her husband die in the blaze; François dies with them. Zola renders it as a simultaneously terrible and darkly satisfying conclusion: the good man who has been systematically destroyed takes the only action left to him. Félicité Rougon, hearing the news from Plassans, reflects that the political situation has resolved itself satisfactorily.",
            "Interné aux Tulettes, François Mouret s'échappe et met le feu à la maison occupée par Faujas. L'abbé, sa sœur et son mari meurent dans l'incendie. François aussi. Félicité Rougon juge la situation politique résolue de façon satisfaisante.",
            ["francois-mouret", "abbe-faujas"],
        ),
        (
            "Angélique dies on the cathedral steps",
            "Mort d'Angélique sur les marches de la cathédrale",
            1869, "c. 1869", "personal",
            "le-reve",
            "Having recovered from her near-fatal illness after Monseigneur de Hautecœur's blessing, Angélique marries Félicien in the cathedral — a ceremony that seems to fulfil the medieval legend she has been living inside. She dies on the church steps immediately after the ceremony, in her wedding dress, as if the dream, having been fully realised in the material world, has exhausted its substance. It is the cycle's only death that feels like completion rather than tragedy.",
            "Après sa guérison miraculeuse, Angélique épouse Félicien dans la cathédrale. Elle meurt sur les marches de l'église, en robe de mariée, comme si le rêve, une fois réalisé, n'avait plus de substance. La seule mort du cycle qui ressemble à un accomplissement.",
            ["angelique-rougon", "felicien-de-hautecoeur"],
        ),
        (
            "Octave Mouret arrives in Paris",
            "Octave Mouret arrive à Paris",
            1864, "c. 1864", "personal",
            "pot-bouille",
            "Octave Mouret — son of François and Marthe Mouret, from Plassans — arrives in Paris and takes a room in a bourgeois apartment building on the Rue de Choiseul, finding work in the drapery trade below. The years he spends in the building give him his education in Parisian bourgeois society: its hypocrisies, its hidden adulteries, its mechanisms of social pretension. He participates and observes in equal measure. He will leave it as the proprietor-in-waiting of the shop across the street that he will transform into Au Bonheur des Dames — the great department store of the cycle.",
            "Octave Mouret, fils de François et Marthe, arrive à Paris de Plassans et s'installe rue de Choiseul. Ses années dans l'immeuble bourgeois lui donnent son éducation parisienne. Il en sort prêt à bâtir Au Bonheur des Dames.",
            ["octave-mouret"],
        ),
        (
            "Coupeau falls from the rooftop",
            "Chute de Coupeau du toit",
            1852, "c. 1852", "personal",
            "lassommoir",
            "Coupeau, the zinc roofer, falls from a rooftop he is working on and survives — but the long convalescence changes everything. He never fully returns to serious work; the insurance payment is small and slow; and during the months of recovery, during which Gervaise works double to support them, he learns to drink to manage the boredom and the pain. It is not a dramatic moral collapse: it is a slow physical one, which is worse. Zola renders the fall and its aftermath as one of the novel's defining pivots — the precise moment when the trajectory that ends in the asylum at Sainte-Anne begins.",
            "Chute du zingueur Coupeau d'un toit de chantier. Il survit, mais la longue convalescence — pendant laquelle Gervaise travaille double — est le pivot du roman. Il apprend à boire pour gérer l'ennui et la douleur, ne retrouve jamais vraiment le travail régulier. La trajectoire vers Sainte-Anne commence ici.",
            ["coupeau", "gervaise-macquart"],
        ),
        (
            "Death of Gervaise Macquart",
            "Mort de Gervaise Macquart",
            1869, "c. 1869", "personal",
            "lassommoir",
            "Gervaise Macquart dies of starvation and exhaustion in the passage under the staircase of the building in the Rue de la Goutte d'Or where she once had a laundry shop. She is found by the concierge in the morning. She is not quite fifty. The building has witnessed her entire adult life: the early years of the laundry below, the years of decline as the shop failed, the years of misery as Coupeau's alcoholism consumed them both, and now this — the space under the stairs as the final address of a woman who once presided over a prosperous household. Coupeau has already died of delirium tremens at the Sainte-Anne asylum. Nana, their daughter, is somewhere in the world of the theatre and the demi-monde, on her own trajectory.",
            "Gervaise Macquart meurt de faim et d'épuisement sous l'escalier de l'immeuble rue de la Goutte d'Or où elle avait eu sa blanchisserie. Trouvée par le concierge au matin. Pas encore cinquante ans. Coupeau est déjà mort à Sainte-Anne. Nana est quelque part dans le monde du théâtre.",
            ["gervaise-macquart"],
        ),
        (
            "Nana dies of smallpox in Paris",
            "Mort de Nana, emportée par la variole",
            1870, "July 1870", "personal",
            "nana",
            "Nana returns to Paris from abroad, having heard that her son Louiset is dying. She arrives too late; the child is already dead; and she contracts smallpox from him. She is locked in a hotel room as the disease takes hold. In the final pages of the novel, her former admirers gather in the corridor outside — some still in love, some merely curious — and one of them comes out to report on her condition: the face, he says, is unrecognisable. The magnificent body that has dazzled Paris for eight years is being consumed from within. Outside in the street, the crowd is chanting 'À Berlin! À Berlin!' — the declaration of war with Prussia, the opening of the catastrophe that will destroy the Second Empire. The connection is Zola's most explicit political statement: Nana is what the Empire grew, and they die together.",
            "Nana rentre à Paris pour son fils Louiset mourant — trop tard. Elle contracte la variole de lui, est enfermée dans une chambre d'hôtel. Ses anciens admirateurs s'attroupent dans le couloir. Le visage, rapporte l'un d'eux, est méconnaissable. Dans la rue, la foule crie 'À Berlin !' — la guerre commence. Nana et le Second Empire s'effondrent ensemble.",
            ["nana"],
        ),
        (
            "Claude Lantier hangs himself before his canvas",
            "Claude Lantier se pend devant sa toile",
            1870, "c. 1870", "personal",
            "loeuvre",
            "After years of obsessive, failed revision, Claude Lantier — having lost his marriage, his son, and his sanity to the impossible canvas — is found dead in his studio by Christine, hanging before the unfinished painting. The painting is still there: a vast, overwrought, brilliant, destroyed thing that can be seen simultaneously as a masterpiece and a catastrophe. Sandoz and the surviving friends come; they stand before the canvas and say almost nothing. Claude's death is the novel's final statement about the price that a certain kind of absolute artistic ambition exacts — not from the bourgeoisie, not from society, but from the artist himself and from the woman who loved him.",
            "Claude Lantier est trouvé mort par Christine dans son atelier, pendu devant la toile inachevée. Les amis — Sandoz en tête — viennent et regardent la toile sans presque parler. Sa mort dit le prix que l'ambition artistique absolue exige : non de la bourgeoisie ou de la société, mais de l'artiste lui-même et de la femme qui l'aimait.",
            ["claude-lantier", "christine-halleguen"],
        ),
        (
            "Albine dies in the Paradou",
            "Mort d'Albine au Paradou",
            1858, "c. 1858", "personal",
            "la-faute-de-labbe-mouret",
            "After Serge Mouret is retrieved from the Paradou by Frère Archangias and restored to his priestly vows, Albine — the wild young woman who nursed him back to health and loved him during his months of amnesia — comes to the rectory to reclaim him. He turns her away. She returns to Le Paradou, gathers the flowers she has always lived among, fills a sealed room with them, and suffocates herself in their scent — willing her own death with the same elemental directness with which she has lived her entire life. It is one of Zola's most mythologically charged endings: Albine is Eve after the expulsion, returning to the garden not as a place of paradise but as a grave, the flowers that were once their Eden becoming the instrument of her death. The Church, in the form of Frère Archangias, stands unmoved.",
            "Après le retour de Serge à ses vœux, Albine vient le réclamer à son presbytère — il la renvoie. Elle retourne au Paradou, remplit une pièce close de fleurs coupées et s'y asphyxie volontairement. L'une des fins les plus mythologiquement chargées du cycle : Eve après l'expulsion, les fleurs du paradis transformées en sépulcre.",
            ["albine", "serge-mouret"],
        ),
        (
            "Florent Quenu denounced and re-arrested",
            "Florent Quenu dénoncé et de nouveau arrêté",
            1858, "c. 1858", "personal",
            "le-ventre-de-paris",
            "After months as a fish inspector at Les Halles, living in the cramped apartment above his brother's charcuterie, Florent Quenu's feeble Republican conspiracy is betrayed to the authorities — by his sister-in-law Lisa Quenu, who frames her denunciation as a civic duty. Florent is re-arrested and transported again, as quietly and efficiently as if he had never returned. The market continues without him; the fat people continue to eat. Lisa Quenu, behind her marble counter, returns to her work. Zola makes the denunciation more devastating by refusing to dramatise it: it is simply a woman who has calculated what she stands to lose and acted accordingly.",
            "Après des mois d'inspecteur des poissons aux Halles, Florent est dénoncé par sa belle-sœur Lisa Quenu, qui présente cela comme un devoir civique. Il est de nouveau arrêté et transporté. Le marché continue. Zola refuse de dramatiser la trahison : c'est simplement une femme qui a calculé ses intérêts et agi en conséquence.",
            ["florent-quenu", "lisa-quenu"],
        ),
        (
            "Jeanne Grandjean dies in Passy",
            "Mort de Jeanne Grandjean à Passy",
            1867, "c. 1867", "personal",
            "une-page-damour",
            "Hélène Grandjean's daughter Jeanne dies of the illness she contracts during the one night her mother leaves her bedside to be with Dr Deberle. Jeanne is a child of unusual emotional intensity — she has loved her mother with a jealous ferocity that Zola renders without sentimentality, and she has intuited, in the way of such children, what her mother's absence means. Her death is the price Une Page d'amour exacts for its single night of passion. Hélène understands completely what she has done; she does not evade the knowledge. She leaves Paris, remarries, and her inner life ends at the moment her daughter's does.",
            "Jeanne Grandjean meurt de la maladie contractée la nuit où Hélène abandonne son chevet pour le docteur Deberle. Enfant d'une intensité émotionnelle inhabituelle, elle a compris ce que l'absence de sa mère signifiait. Sa mort est le prix que le roman exige pour une seule nuit de passion. Hélène comprend sans équivoque ce qu'elle a fait.",
            ["jeanne-grandjean", "helene-grandjean"],
        ),
        (
            "Au Bonheur des Dames opens its final wing",
            "Inauguration du dernier agrandissement d'Au Bonheur des Dames",
            1869, "c. 1869", "personal",
            "au-bonheur-des-dames",
            "The great department store built by Octave Mouret reaches its full expansion, having consumed the surrounding streets one building at a time — including the old drapery shop of Denise Baudu's uncle Baudu, which finally closes. The novel's closing movement is the store at its maximum triumph, a machine for consuming desire and producing profit, with Denise Baudu installed as its humane conscience and about to become Mouret's wife. Zola renders the expansion without triumphalism: the old traders who are destroyed are not admirable, but the world that replaces them is not simply better.",
            "Le grand magasin d'Octave Mouret atteint son expansion maximale, ayant absorbé les rues environnantes — y compris la vieille boutique de l'oncle Baudu. Le roman se clôt sur le triomphe du magasin, avec Denise Baudu installée comme sa conscience humaine et future épouse de Mouret. Zola refuse le triomphalisme : les vieux commerçants détruits n'étaient pas admirables, le monde qui les remplace n'est pas simplement meilleur.",
            ["octave-mouret", "denise-baudu"],
        ),
        (
            "Declaration of war on Prussia",
            "Déclaration de guerre à la Prusse",
            1870, "19 July 1870", "historical",
            "la-debacle",
            "Napoleon III, manoeuvred by Bismarck, declares war on Prussia. The disastrously unprepared French army sets off for what will become the catastrophe of Sedan — the war that destroys the Second Empire and drives the Rougon-Macquart cycle to its conclusion.",
            "Manœuvré par Bismarck, Napoléon III déclare la guerre à la Prusse. L'armée française, impréparée, marche vers Sedan.",
            ["jean-macquart"],
        ),
        (
            "Death of Nana",
            "Mort de Nana",
            1870, "July 1870", "personal",
            "nana",
            "Nana dies of smallpox in a room at the Grand Hôtel, her face consumed by the disease. Outside, the crowd shouts 'À Berlin! À Berlin!' The Second Empire's most brilliant daughter dies as the Empire itself begins its collapse.",
            "Nana meurt de la variole au Grand Hôtel, son visage dévoré par la maladie. Dehors, la foule crie 'À Berlin!' — la courtisane et l'Empire meurent ensemble.",
            ["nana"],
        ),
        (
            "Battle of Sedan — capitulation of Napoleon III",
            "Défaite de Sedan — capitulation de Napoléon III",
            1870, "1–2 September 1870", "historical",
            "la-debacle",
            "The catastrophic French defeat at Sedan. Napoleon III surrenders with 100,000 men. The Second Empire collapses. Jean Macquart witnesses the destruction of everything the Rougons had built their ambitions upon.",
            "La catastrophique défaite française à Sedan. Napoléon III capitule avec 100 000 hommes. Le Second Empire s'effondre.",
            ["jean-macquart"],
        ),
        (
            "Siege of Paris",
            "Siège de Paris",
            1870, "September 1870 – January 1871", "historical",
            "la-debacle",
            "Prussian forces surround Paris for four months. The city endures cold, hunger, and bombardment. The government flees to Versailles. The experience radicalises the Parisian working class and plants the seeds of the Commune.",
            "Les forces prussiennes encerclent Paris pendant quatre mois. La ville endure le froid, la faim et le bombardement.",
            [],
        ),
        (
            "Paris Commune",
            "La Commune de Paris",
            1871, "18 March – 28 May 1871", "political",
            "la-debacle",
            "The revolutionary working-class government of Paris, born from the humiliation of war. Its brutal suppression — the 'Bloody Week' — leaves tens of thousands dead. The cycle ends in its shadow: the old world burned away, the new one not yet built.",
            "Le gouvernement révolutionnaire ouvrier de Paris. Sa suppression brutale — la Semaine sanglante — laisse des dizaines de milliers de morts.",
            ["jean-macquart"],
        ),
        (
            "Zola completes the Rougon-Macquart cycle",
            "Zola achève le cycle des Rougon-Macquart",
            1893, "1893", "historical",
            "le-docteur-pascal",
            "Zola publishes Le Docteur Pascal — a summation, a farewell, and a declaration of faith in life and science. Dr Pascal Rougon, cataloguing the family's hereditary history, stands as Zola's own surrogate looking back over twenty novels.",
            "Zola publie Le Docteur Pascal, bilan et adieu à vingt ans d'œuvre. Le docteur Pascal, cataloguant l'hérédité familiale, est le porte-parole de Zola.",
            ["pascal-rougon"],
        ),
    ]

    events = []
    for row in events_data:
        (title_en, title_fr, year, date_approx, event_type,
         novel_slug, description_en, description_fr, char_slugs) = row
        ev = Event(
            title_en=title_en, title_fr=title_fr,
            year=year, date_approx=date_approx,
            event_type=event_type,
            novel_id=novels[novel_slug].id if novel_slug and novel_slug in novels else None,
            description_en=description_en, description_fr=description_fr,
        )
        db.add(ev)
        db.flush()
        for cs in char_slugs:
            if cs in chars:
                db.add(EventCharacter(event_id=ev.id, character_id=chars[cs].id))
        events.append(ev)

    # ── QUOTES ───────────────────────────────────────────────────────────────
    # Tuples: (char_slug_or_None, novel_slug, text_fr, text_en, context)
    quotes_data = [
        (
            "eugene-rougon",
            "son-excellence-eugene-rougon",
            "Il aimait le pouvoir pour le pouvoir, avec la brutalité d'un appétit d'homme fort.",
            "He loved power for power's sake, with the brutality of a strong man's appetite.",
            "The narrator's essential verdict on Eugène Rougon — a man with no ideology, no programme, and no use for power except the experience of possessing it",
        ),
        (
            None,
            "la-curee",
            "Paris était à eux. Ils l'avaient pris d'assaut, comme une ville ennemie qu'on pille.",
            "Paris was theirs. They had taken it by storm, like an enemy city being looted.",
            "The narrator on the Saccard generation of speculators — men who treated Haussmann's Paris as conquered territory to be stripped",
        ),
        (
            None,
            "la-fortune-des-rougon",
            "Je veux expliquer comment une famille, un petit groupe d'êtres, se comporte dans une société, en s'épanouissant pour donner naissance à dix, à vingt individus qui paraissent, au premier coup d'œil, profondément dissemblables, mais que l'analyse montre intimement liés les uns aux autres. L'hérédité a ses lois, comme la pesanteur.",
            "I want to show how a family, a small group of beings, behaves within society as it blossoms and gives birth to ten, to twenty individuals who appear, at first glance, profoundly unlike one another, but whom analysis shows to be intimately linked. Heredity has its laws, just as gravity does.",
            "Preface (1871) — Zola's programmatic statement for the entire twenty-novel cycle, explaining what the Rougon-Macquart series sets out to prove",
        ),
        (
            "miette",
            "la-fortune-des-rougon",
            "Il lui semblait qu'elle était à la procession de la Fête-Dieu, et qu'elle portait la bannière de la Vierge.",
            "It seemed to her that she was in the Corpus Christi procession, and that she was carrying the banner of the Virgin.",
            "Miette, carrying the red Republican flag at the head of the insurgent column — her innocence making the tragedy to come all the more bitter",
        ),
        (
            None,
            "la-fortune-des-rougon",
            "Comme il avait relevé la fortune des Bonaparte, le coup d'État fondait la fortune des Rougon.",
            "Just as it had restored the fortunes of the Bonapartes, the coup d'état was founding the fortune of the Rougons.",
            "The narrator's ironic verdict as Pierre Rougon's triumph is complete — the cycle's founding political equation",
        ),
        (
            None,
            "germinal",
            "Des hommes poussaient, une armée noire, vengeresse, qui germait lentement dans les sillons, grandissant pour les récoltes du siècle futur, et leur germination allait faire bientôt éclater la terre.",
            "Men were pushing up, a black avenging army, germinating slowly in the furrows, growing towards the harvests of the next century, and their germination would crack the earth asunder.",
            "Final lines of Germinal — the narrator's voice, as Étienne walks away from the ruined Voreux",
        ),
        (
            "gervaise-macquart",
            "lassommoir",
            "Moi, ce que je voulais, c'était travailler tranquille, avoir du pain toujours, un coin propre pour dormir... et mourir dans mon lit.",
            "What I wanted was to work in peace, always have bread, a clean corner to sleep in... and to die in my own bed.",
            "Gervaise states her modest ambitions early in the novel — a passage that haunts the reader as every element of it is later denied",
        ),
        (
            "etienne-lantier",
            "germinal",
            "Nous sommes trop misérables, il faut que ça finisse.",
            "We are too wretched — it has to end.",
            "Étienne Lantier to the miners, before the strike vote",
        ),
        (
            None,
            "nana",
            "Elle était comme un soleil couchant qui embrase tout à l'horizon. Les hommes tombaient devant elle comme des épis.",
            "She was like a setting sun setting the whole horizon ablaze. Men fell before her like corn before the scythe.",
            "Narrator, on Nana at the height of her power",
        ),
        (
            "jacques-lantier",
            "la-bete-humaine",
            "Il avait beau ne pas vouloir, quelque chose en lui ne voulait pas non plus, quelque chose d'ancestral et de bestial qui le secouait.",
            "He could not help himself, and something in him could not help itself either — something ancestral and bestial that shook him to his foundations.",
            "Jacques Lantier struggling against his murderous impulse",
        ),
        (
            "aristide-saccard",
            "la-curee",
            "Paris m'appartient. Je n'ai qu'à me baisser pour en ramasser l'or.",
            "Paris belongs to me. All I need to do is bend down and scoop up the gold.",
            "Aristide Saccard, contemplating the fortunes to be made from Haussmann's demolitions",
        ),
        (
            None,
            "la-terre",
            "La terre, elle, ne mourait pas. Elle restait là, muette, dans son éternité.",
            "The land did not die. It remained there, silent, in its eternity.",
            "Narrator's voice, on the indifference of the earth to human suffering",
        ),
        (
            "pascal-rougon",
            "le-docteur-pascal",
            "L'hérédité n'est pas une fatalité. La volonté peut tout.",
            "Heredity is not fatality. The will can do everything.",
            "Dr Pascal Rougon, defending his belief in the possibility of human progress",
        ),
        (
            "octave-mouret",
            "au-bonheur-des-dames",
            "La femme, c'est le grand ressort de la machine. Il faut la flatter, l'affoler, puis on a tout.",
            "Woman is the great mainspring of the machine. Flatter her, drive her to distraction — and you have everything.",
            "Octave Mouret explaining his commercial philosophy",
        ),
        (
            None,
            "lassommoir",
            "L'Assommoir de la rue de la Goutte-d'Or était un grand diable de machine à soûler le peuple.",
            "The dram-shop in the Rue de la Goutte-d'Or was a great devil of a machine for making the people drunk.",
            "Narrator's description of the distillery, seen by Gervaise on first arrival in the neighbourhood",
        ),
        (
            None,
            "la-faute-de-labbe-mouret",
            "Le Paradou était une mer de verdure, si vaste, si profonde, qu'on aurait dit que le monde s'arrêtait là.",
            "Le Paradou was a sea of greenery, so vast and deep that one might have said the world ended there.",
            "Narrator's first description of the Paradou garden",
        ),
        (
            "etienne-lantier",
            "germinal",
            "C'est nous qui avons fait la richesse du monde, et c'est nous qui en crevons de faim.",
            "We are the ones who made the wealth of the world, and we are the ones who starve for it.",
            "Étienne Lantier, addressing the miners during the strike",
        ),
        (
            None,
            "au-bonheur-des-dames",
            "Au Bonheur des Dames flambait comme un palais du rêve, débordant de toutes les séductions.",
            "Au Bonheur des Dames blazed like a palace of dreams, overflowing with every seduction.",
            "Narrator's description of the department store illuminated at night",
        ),
        (
            "gervaise-macquart",
            "lassommoir",
            "Je ne demande pas à être heureuse, mon Dieu. Je demande juste à ne pas souffrir.",
            "I do not ask to be happy, dear God. I only ask not to suffer.",
            "Gervaise, in the later stages of her decline",
        ),
        (
            None,
            "germinal",
            "La mine dévorait tout, les hommes, les familles, les espoirs.",
            "The mine devoured everything — men, families, hope.",
            "Narrator's voice, on the Voreux and what it takes from those who serve it",
        ),
    ]

    for char_slug, novel_slug, text_fr, text_en, context in quotes_data:
        db.add(Quote(
            character_id=chars[char_slug].id if char_slug and char_slug in chars else None,
            novel_id=novels[novel_slug].id if novel_slug and novel_slug in novels else None,
            text_fr=text_fr,
            text_en=text_en,
            context=context,
        ))

    db.commit()
    db.close()
    print("OK Database seeded successfully.")
    print(f"  Novels:      {len(novels_data)}")
    print(f"  Characters:  {len(chars_data)}")
    print(f"  Locations:   {len(locations_data)}")
    print(f"  Events:      {len(events_data)}")
    print(f"  Quotes:      {len(quotes_data)}")
    print(f"  Appearances: {len(appearances)}")


if __name__ == "__main__":
    run()
