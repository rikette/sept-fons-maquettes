# -*- coding: utf-8 -*-
"""Source unique du texte des trois versions.

Le texte est recopié mot pour mot :
- page d'accueil : maquette éditoriale des frères (sans les indications entre crochets) ;
- Chercher Dieu / Avec des frères / Une vocation ? : PDF « Vie_monastique_version_revisee » ;
- autres pages : site actuel abbayedeseptfons.com.

Syntaxe inline : [libellé](url) pour un lien, *texte* pour l'italique.
"""

SITE = "Abbaye de Sept-Fons"
MAIL = "mailto:abbaye@septfons.com"
OLD = "https://www.abbayedeseptfons.com"

# Navigation principale (maquette des frères)
NAV = [
    ("Chercher Dieu", "vie-monastique.html", []),
    ("Prier et vivre chaque jour", "priere.html", [
        ("Prier toujours", "priere.html"),
        ("Travail monastique", "travail.html"),
        ("Horaires des offices religieux", "horaires.html"),
    ]),
    ("Avec des frères", "vie-fraternelle.html", []),
    ("Une vocation ?", "vocation.html", []),
]
CTA = ("Nous écrire", "ecrire.html")
FORM = "ecrire.html"

FOOTER_TEXT = ("L’Abbaye de Sept-Fons se trouve aux confluents de la Loire et de la Besbre (Allier). "
               "La vie monastique cistercienne trappiste y est menée quasi sans interruption depuis 1132. "
               "Vie de prière, de travail, de lecture, de fraternité, dans le respect du silence. "
               "Une prière pour tous les hommes nos frères. Découvrez notre actualité et celle de nos maisons-filles.")
FOOTER_QUOTE = ("« Ne rien avoir de plus cher que le Christ. »", "Règle de S. Benoît")
FOOTER_ADDRESS = ["Abbaye de Sept-Fons", "03290 Dompierre-sur-Besbre", "Téléphone standard : 04 70 48 14 90"]
FOOTER_LINKS = [
    ("L’abbaye", [
        ("Histoire de l’Abbaye", "histoire.html"),
        ("La croix de nos martyrs", "martyrs.html"),
        ("Filiation", "filiation.html"),
        ("Ordre Cistercien de la Stricte Observance", "ocso.html"),
    ]),
    ("Venir à Sept-Fons", [
        ("Hôtellerie", "hotellerie.html"),
        ("Horaires des offices religieux", "horaires.html"),
        ("Visitez notre magasin", "horaires.html#magasin"),
        ("Contacts", "contact.html"),
    ]),
    ("Ressources", [
        ("Homélies", OLD + "/homelies/"),
        ("Actualités", OLD + "/category/actualite-abbaye-sept-fons/"),
        ("Boutique en ligne", "https://www.boutique-abbayedeseptfons.com/"),
        ("Faire un don", "don.html"),
    ]),
]

# ---------------------------------------------------------------------------
# PAGE D'ACCUEIL — maquette éditoriale des frères
# ---------------------------------------------------------------------------
HOME = {
    "hero_title": ["Quel est l’homme", "qui veut la vie ?"],
    "hero_img": ("office-nuit", "La communauté à l’office, dans l’église"),
    "intro": [
        "Nous désirons tous le bonheur : une vie pleine, une vie vécue à fond, une vie où aimer et être aimé.",
        "Pourtant, ni le succès, ni l’argent, ni le plaisir ne suffisent à remplir notre cœur. Nous avons soif d’une vie plus profonde, d’un amour qui demeure.",
        "Cette vie, Dieu nous l’offre. Elle a un visage : Jésus-Christ.",
    ],
    "intro_faq": [
        ("Pourquoi des hommes deviennent-ils moines aujourd’hui ?", [
            "Parce que certains hommes découvrent que Jésus les appelle à lui consacrer leur vie.",
            "Le moine ne cherche pas seulement le silence ou une existence plus paisible. Il désire devenir ami de Dieu et répondre à son amour par le don de lui-même.",
            "La vie monastique est organisée autour de cette recherche : la prière, la lecture, le travail et la vie fraternelle sont au service d’une même amitié.",
        ]),
    ],
    "ami": {
        "title": "Devenir ami de Dieu",
        "img": ("frere-livre", "Un frère seul avec son livre, dans la lumière"),
        "paras": [
            "C’est fou, mais c’est la réalité : l’homme peut devenir ami de Dieu ! Ce n’est pas une pieuse formule.",
            "Dieu nous appelle à le connaître, à l’aimer, à vivre avec lui. Non pas seulement pendant quelques moments de prière, mais dans toute notre existence.",
            "Ce bonheur est offert à tous. La vie monastique donne à ceux qui y sont appelés des moyens particulièrement adaptés pour le chercher.",
        ],
        "faq": [
            ("Peut-on chercher cette amitié au milieu du monde ?", [
                "Oui. L’amitié avec Dieu est offerte à tous, dans des situations et des vocations différentes.",
                "Mais celui qui désire donner à Dieu une place toujours plus grande dans sa vie rencontre aussi une difficulté concrète : comment garder du temps pour lui au milieu des occupations et des sollicitations ?",
                "Le monastère offre un cadre où le silence, la prière, le travail et le soutien des frères aident à orienter toute la vie vers Dieu. Celui qui porte ce désir peut alors se demander si Notre Seigneur l’appelle à le chercher de cette manière.",
            ]),
            ("Qu’est-ce que prier ?", [
                "Prier, c’est vivre cette relation d’amitié avec Dieu.",
                "Cette prière prend différentes formes : la louange commune de l’Office divin, l’entretien silencieux de l’oraison, les courts appels adressés à Jésus au fil des heures.",
                "Mais c’est toujours la même amitié qui cherche à s’exprimer et à grandir.",
            ]),
            ("Tout quitter, est-ce abandonner les autres ?", [
                "Le moine ne cherche pas auprès de Dieu un bonheur qu’il garderait pour lui. Sa vie est donnée pour louer Dieu et prier pour le salut des hommes.",
                "Il porte dans sa prière ceux qu’il connaît et ceux qu’il ne connaîtra jamais, ceux qui cherchent Dieu et ceux qui ne s’intéressent pas à lui.",
                "Comme le rameau reçoit la sève du tronc, il reçoit de Jésus la vie qu’il est appelé à partager. C’est de son union à Dieu que peut naître la fécondité de son existence.",
            ]),
        ],
    },
    "quote": ["Dieu commence par se mettre à notre pas.",
              "Puis, l’heure vient pour le moine de se mettre au pas de Dieu."],
    "freres": {
        "title": "Chercher Dieu avec des frères",
        "img": ("vaisselle", "Les frères à la vaisselle partagée"),
        "paras": [
            "Le moine ne cherche pas Dieu seul. Il entre dans une communauté où il reçoit une vie, se laisse guider et apprend à aimer.",
            "Les frères le soutiennent. Ils sont aussi ceux à travers lesquels Dieu lui apprend à sortir de lui-même et à s’ouvrir aux autres.",
        ],
        "faq": [
            ("Pourquoi a-t-on besoin d’être guidé ?", [
                "Notre désir de chercher Dieu est indispensable, mais il ne suffit pas à nous montrer le chemin. Nous avons besoin de recevoir un art de vivre avec lui.",
                "Comme celui qui apprend un instrument se met à l’école d’un maître, le moine accepte de se laisser former par ceux qui ont l’expérience de cette vie et la charge de le guider.",
                "Il ne renonce pas à son intelligence ou à sa liberté : il les engage dans cet apprentissage.",
            ]),
            ("Comment la vie commune nous rapproche-t-elle de Dieu ?", [
                "Nous n’avons pas choisi chacun de nos frères. Leurs habitudes, leurs caractères et leurs façons de faire nous font parfois découvrir nos propres limites.",
                "C’est là que la vie commune devient une école de charité. Les petits renoncements quotidiens peuvent devenir un puissant moyen d’union à Dieu lorsque nous les vivons en nous tournant vers lui, en reconnaissant notre impuissance et notre besoin de sa grâce.",
                "Avec nos frères, nous apprenons à recevoir l’amour de Dieu et à y répondre par le don de nous-mêmes.",
            ]),
        ],
        "link": ("Découvrir la vie fraternelle →", "vie-fraternelle.html"),
    },
    "journee": {
        "title": "Une journée pour chercher Dieu",
        "imgs": [("pupitres", "La lecture aux pupitres éclairés"),
                 ("fourche", "Les frères au travail à la fourche")],
        "paras": [
            "Prier, lire, travailler, vivre avec ses frères : les activités changent, mais une même recherche traverse la journée.",
            "Toute la vie monastique est organisée pour aider le moine à demeurer auprès de Jésus et à lui donner sa vie.",
        ],
        # Lien à activer lorsque la page sera rédigée (None = inactif)
        "link": ("Découvrir une journée au monastère →", None),
    },
    "vocation": {
        "title": "Et si Dieu m’appelait ?",
        "paras": [
            "La vocation monastique n’est pas d’abord un projet que l’on invente. C’est une invitation de Dieu que l’on apprend à reconnaître et à laquelle on désire répondre librement.",
            "Il n’est pas nécessaire d’avoir tout éclairci pour commencer à en parler.",
        ],
        "faq": [
            ("Quels signes peuvent m’aider à discerner ?", [
                "Nous regardons trois signes : un désir profond, les événements et les rencontres qui nous conduisent vers une communauté, puis la croissance qui se vérifie lorsque nous commençons réellement à vivre cette vie.",
                "Les deux premiers signes ouvrent un chemin vers le monastère. Le troisième demande l’expérience de la vie commune et le regard de ceux qui nous accompagnent.",
            ]),
            ("Puis-je avoir une vocation si je désire aussi me marier ?", [
                "Notre cœur est habité par de nombreux désirs, parfois contradictoires. L’appel de Dieu ne fait pas disparaître d’un coup le désir d’une relation amoureuse, d’une famille ou d’une carrière.",
                "Ces aspirations ne suffisent donc pas, à elles seules, à écarter une vocation monastique. Le désir profond a besoin d’être peu à peu reconnu, éclairé et purifié. Ce travail peut prendre du temps, parfois des années.",
            ]),
            ("Faut-il être certain avant de faire un premier pas ?", [
                "On ne possède pas à l’avance une certitude qui dispenserait de faire le chemin. Mais on peut reconnaître des signes suffisamment sérieux pour commencer.",
                "Le discernement se poursuit dans la rencontre avec la communauté, puis dans l’expérience de cette vie. Il ne s’agit ni de s’engager aveuglément, ni d’attendre d’avoir tout compris avant d’avancer.",
            ]),
        ],
        "link": ("Approfondir la question de la vocation →", "vocation.html"),
    },
    "contact": {
        "title": "Une question ? Vous pouvez nous écrire.",
        "paras": [
            "Vous vous interrogez sur la vie monastique ou sur un possible appel de Dieu ? Vous pouvez nous dire simplement où vous en êtes et nous poser vos questions.",
            "Il ne s’agit pas de vous décider avant de nous rencontrer, mais de commencer un échange.",
        ],
        "button": ("Nous écrire", "ecrire.html?objet=question"),
    },
}

# ---------------------------------------------------------------------------
# PAGES INTÉRIEURES
# Blocs : ("h2", t) ("h3", t) ("p", t) ("lead", t) ("quote", t, cite)
#         ("box", titre, [lignes]) ("img", clé, alt, légende) ("imgs", [(clé, alt)])
#         ("btn", libellé, url) ("lines", [lignes]) ("table", entêtes, lignes, légende)
#         ("cta",) = encadré « Nous écrire »
# ---------------------------------------------------------------------------
PAGES = {}

# ----- PDF : Vie monastique (1) -----
PAGES["vie-monastique"] = {
    "nav": "Chercher Dieu",
    "kicker": "Chercher Dieu",
    "title": "Quel est l’homme qui veut la vie ?",
    "hero": ("wa-eglise", "La communauté dans l’église abbatiale"),
    "blocks": [
        ("lead", "Nous désirons tous le bonheur : une vie pleine, une vie vécue à fond, une vie où aimer et être aimé."),
        ("p", "Pourtant, ce désir profond se heurte à des obstacles et à des déceptions. On peut monter une super boîte, devenir champion du monde de football, star de pop ou milliardaire : cela ne suffit pas à remplir le cœur de l’homme. À certains moments, nous pressentons que la vie est plus que l’argent, le succès ou le plaisir."),
        ("p", "Nous avons soif d’une joie qui ne se dissipe pas comme la rosée du matin, d’une paix plus profonde que nos inquiétudes, d’une vie que la mort ne puisse nous enlever."),
        ("p", "Cette vie, Dieu nous l’offre. Elle a un visage : Jésus-Christ."),
        ("h2", "Devenir ami de Dieu"),
        ("p", "Dieu ne nous propose pas seulement des idées auxquelles croire ou des règles à suivre. Il nous offre son amitié. Il nous appelle à le connaître, à l’aimer, à vivre avec lui."),
        ("p", "C’est fou, mais c’est la réalité : l’homme peut devenir ami de Dieu ! Ce n’est pas une pieuse formule."),
        ("p", "Pensez à ce qu’une amitié profonde peut apporter à une existence : la joie de se connaître, de partager, de pouvoir compter l’un sur l’autre. Dieu nous propose une amitié qui dépasse tout ce que nous pouvons imaginer. Non pas une relation lointaine, réservée à quelques moments de prière, mais une présence appelée à transformer toute notre vie."),
        ("img", "frere-livre", "Un frère en prière dans l’église", None),
        ("p", "Ce bonheur en Dieu est offert à tous. On peut chercher son amitié au milieu du monde, dans des situations et des vocations différentes."),
        ("p", "Mais celui qui désire donner à Dieu une place toujours plus grande dans sa vie rencontre aussi des difficultés très concrètes : comment dégager du temps pour lui au milieu des multiples occupations et sollicitations ? Comment garder son cœur tourné vers lui dans une vie si souvent dispersée ?"),
        ("p", "La vie monastique offre des moyens particulièrement adaptés à cette recherche. Le silence, le temps consacré à la prière, la lecture, le travail et le soutien des frères sont ordonnés à une même fin : permettre à l’amitié avec Jésus de grandir et de pénétrer toute l’existence."),
        ("p", "Celui qui porte ce désir peut alors se demander : Dieu m’appelle-t-il à le chercher dans la vie monastique ?"),
        ("h2", "Pourquoi devenir moine ?"),
        ("p", "On ne devient pas moine simplement parce qu’on aime le silence, les belles liturgies ou la vie à la campagne. On ne le devient pas non plus pour se construire une existence à l’abri des difficultés du monde."),
        ("p", "Le moine est un homme qui se laisse saisir par Jésus. Il découvre, parfois peu à peu, que Dieu l’appelle à tout quitter pour lui consacrer sa vie."),
        ("p", "Ce n’est donc pas d’abord un projet qu’il invente. C’est une invitation qu’il apprend à reconnaître et à laquelle il désire répondre librement."),
        ("p", "Pourquoi tout quitter ? Pour vivre de cette amitié. Pour chercher Dieu, apprendre à l’aimer et ne rien lui préférer. Le silence, la prière, le travail et la vie commune prennent leur sens à partir de là : ils sont au service de cette relation avec Notre Seigneur."),
        ("img", "wa-cloitre", "Les frères dans le cloître", None),
        ("h2", "Tout quitter, sans abandonner les hommes"),
        ("p", "Mais cette amitié serait-elle un bonheur que le moine garderait pour lui ?"),
        ("p", "Au contraire. Le moine ne quitte pas tout pour devenir indifférent aux autres. Il ne cherche pas auprès de Dieu un refuge qui le dispenserait d’aimer."),
        ("p", "Sa vie est donnée pour louer Dieu et prier pour le salut des hommes. Dans sa prière, il porte ceux qu’il connaît et ceux qu’il ne connaîtra jamais, ceux qui cherchent Dieu et ceux qui ne s’intéressent pas à lui."),
        ("p", "Cette prière ne tient pas sa force des seules qualités du moine. Il ne peut rien par lui-même. Comme le rameau reçoit la sève du tronc, il reçoit de Jésus la vie qu’il est appelé à partager. C’est de son union à Dieu que peut naître la fécondité de son existence."),
        ("h2", "Une vie entière pour apprendre à aimer"),
        ("p", "La prière tient une place centrale dans la journée monastique. Elle prend plusieurs formes : la louange de l’Office divin, l’entretien silencieux de l’oraison, les courts appels adressés à Dieu au fil des heures."),
        ("p", "Mais c’est toujours la même amitié qui cherche à s’exprimer et à grandir."),
        ("p", "Cette relation ne s’arrête pas à la porte de l’église. Le travail, la lecture et la vie avec les frères font partie de la même recherche. Toute la journée est organisée pour aider le moine à se tourner vers Jésus et à lui donner sa vie."),
        ("p", "Cela ne veut pas dire que tout devient facile. L’amitié avec Dieu ne supprime pas le combat, la fatigue ou les difficultés. Le moine apprend, jour après jour, à chercher auprès de Jésus sa paix et sa joie, et à lui rester fidèle."),
        ("box", "Se mettre au pas de Dieu", [
            "« Dieu commence par se mettre à notre pas. Il enfonce nos barrières, nous attire d’une manière puissante, se manifeste pour retenir notre attention. Puis, l’heure vient pour le moine de se mettre au pas de Dieu. Sans insister, Dieu sollicite, donne de légères indications. Il faut exercer son regard pour voir, penser, juger et réagir à ses sollicitations. »"]),
        ("h2", "Et si Dieu m’appelait ?"),
        ("p", "Une question peut alors se faire jour : cette vie est-elle aussi celle à laquelle Dieu m’appelle ?"),
        ("p", "Il n’est pas nécessaire de posséder déjà une réponse pour commencer à en parler. Une interrogation, un attrait, un désir de chercher Dieu peuvent être le point de départ d’une rencontre."),
        ("p", "Il ne s’agit pas de décider seul, ni de s’engager précipitamment, mais de prendre le temps de discerner."),
        ("p", "Vous pouvez nous écrire simplement pour nous dire où vous en êtes et nous poser vos questions."),
        ("cta",),
    ],
    "next": [("Avec des frères", "vie-fraternelle.html"), ("Une vocation ?", "vocation.html")],
}

# ----- PDF : Chercher Dieu avec des frères -----
PAGES["vie-fraternelle"] = {
    "nav": "Avec des frères",
    "kicker": "Avec des frères",
    "title": "Chercher Dieu avec des frères",
    "hero": ("wa-freres", "Des frères en conversation"),
    "blocks": [
        ("lead", "Le moine ne cherche pas Dieu seul. Il vient le chercher dans une communauté de frères. Il y trouve un soutien, mais aussi une vie à recevoir et un amour à apprendre."),
        ("h2", "Une vie que l’on reçoit"),
        ("p", "On ne se donne pas à soi-même la vie : on la reçoit. Dans une famille, l’enfant reçoit bien plus que la naissance. Il apprend à parler, à marcher, à entrer en relation avec les autres. Il grandit grâce à ceux qui l’ont précédé."),
        ("p", "Il en va de même au monastère. Celui qui arrive entre dans une vie qui le précède. Il reçoit une manière de chercher Dieu, une sagesse et des moyens éprouvés, transmis de génération en génération par des hommes qui se sont eux-mêmes laissé façonner par cette vie."),
        ("p", "C’est cela, une tradition vivante : non pas seulement des usages anciens que l’on conserve, mais un art de vivre avec Dieu que l’on reçoit pour en vivre à son tour."),
        ("p", "Notre désir de chercher Dieu est indispensable, mais il ne suffit pas à nous montrer le chemin. Nous avons besoin du soutien des frères et de l’expérience de ceux qui nous précèdent. Nous n’avons pas à tout inventer seuls."),
        ("img", "wa-chapitre", "La communauté réunie", None),
        ("h2", "Apprendre à se laisser guider"),
        ("p", "Celui qui veut apprendre un instrument cherche un maître capable de lui transmettre son art. Il sait qu’il ne lui suffira pas d’aimer la musique pour devenir musicien. Il lui faudra écouter, s’exercer, accepter d’être corrigé et reprendre patiemment ce qu’il ne maîtrise pas encore."),
        ("p", "Il ne renonce pas pour autant à son intelligence ou à sa liberté. Au contraire, il les engage dans un apprentissage qui lui permettra de progresser."),
        ("p", "Au monastère aussi, il y a un art à apprendre : l’art de la vie avec Dieu. On le reçoit auprès d’hommes qui ont vécu la prière, traversé des épreuves et des combats, et qui ont la charge de nous former et de nous guider."),
        ("p", "C’est dans cette perspective que l’on peut comprendre l’obéissance monastique. Le moine n’accepte pas d’obéir parce qu’il serait incapable de réfléchir ou de prendre ses responsabilités. Il choisit librement de se laisser conduire parce qu’il reconnaît qu’il a besoin de recevoir et d’apprendre."),
        ("p", "Comme dans une cordée, celui qui connaît mieux le chemin aide les autres à avancer et à éviter les passages dangereux. Accepter de le suivre ne dispense pas de marcher : personne ne peut faire le chemin à notre place. Mais nous ne sommes pas seuls pour le découvrir."),
        ("p", "Cette confiance n’abolit ni les questions ni le dialogue. Elle demande d’engager son intelligence, d’exprimer simplement ses difficultés et d’accepter aussi que l’on nous invite à aller au-delà de nos premières réactions. Peu à peu, nous apprenons à ne plus faire de nos préférences la seule mesure de ce qui est bon pour nous."),
        ("img", "wa-entretien", "Un frère reçu par un ancien", None),
        ("p", "Dans la vie de prière, nous pouvons être tentés de mesurer notre relation à Dieu à ce que nous éprouvons. Un jour, la prière nous paraît facile et nous nous croyons proches de lui. Un autre jour, nous ne ressentons rien et nous pensons avoir tout perdu."),
        ("p", "C’est aussi pour cela que nous avons besoin d’être guidés. L’expérience d’un ancien nous aide à prendre du recul, à comprendre ce que nous traversons et à porter un jugement plus sûr sur notre vie. Il ne s’agit pas d’ignorer nos sentiments, mais de ne pas leur laisser seuls le dernier mot."),
        ("box", "Sentiments et discernement", [
            "« Il ne s’agit pas d’un sentiment préféré à un autre sentiment, mais d’un jugement préféré à un sentiment. »"]),
        ("h2", "Une école de charité"),
        ("p", "La communauté n’est pas seulement le lieu où l’on reçoit un enseignement. Elle est aussi celui où l’on apprend à aimer."),
        ("p", "Nous venons au monastère pour chercher Dieu, mais nous ne pouvons pas séparer cette recherche de notre manière de vivre avec nos frères. L’amitié avec Jésus doit prendre corps dans les relations les plus ordinaires : rendre un service, écouter, partager un travail, accueillir une remarque, demander pardon."),
        ("p", "Il ne s’agit pas simplement d’être gentils les uns avec les autres. Il s’agit d’apprendre un amour qui ne dépend pas seulement de la sympathie, de l’humeur ou de ce que l’autre nous apporte."),
        ("img", "vaisselle", "La vaisselle partagée", None),
        ("p", "Les frères sont un soutien précieux. Leur fidélité nous encourage lorsque notre propre élan faiblit. Nous recevons leur aide, leur expérience, parfois une parole très simple qui nous permet de reprendre courage. Et, à notre tour, nous apprenons à les soutenir."),
        ("p", "Mais les frères ne sont pas seulement ceux qui nous soutiennent. Ils sont aussi ceux qui nous dérangent et nous font découvrir nos limites. Nous ne les avons pas choisis : leurs caractères, leurs habitudes et leurs façons de faire ne correspondent pas toujours aux nôtres. Et voilà que notre désir d’aimer rencontre une difficulté très concrète : aimer ce frère-ci, tel qu’il est."),
        ("p", "C’est là que la vie commune devient une école de charité. À travers nos frères, Dieu nous apprend à sortir de nous-mêmes et à nous ouvrir aux autres. Les contrariétés quotidiennes peuvent devenir autant d’occasions de lui laisser transformer notre cœur et de nous unir à lui. Ces petits renoncements sont un puissant moyen d’union à Dieu lorsque nous les vivons en nous tournant vers lui, en reconnaissant notre impuissance et notre besoin de sa grâce."),
        ("p", "La vie commune n’est donc pas un simple cadre autour de la prière. Elle est l’un des lieux où notre prière devient une vie. Avec nos frères, nous apprenons à recevoir l’amour de Dieu et à y répondre par le don de nous-mêmes."),
    ],
    "next": [("Une vocation ?", "vocation.html"), ("Chercher Dieu", "vie-monastique.html")],
}

# ----- PDF : Comment savoir si Dieu m'appelle ? -----
PAGES["vocation"] = {
    "nav": "Une vocation ?",
    "kicker": "Une vocation ?",
    "title": "Comment savoir si Dieu m’appelle ?",
    "hero": ("wa-couchant", "Un chemin dans la lumière du soir"),
    "blocks": [
        ("lead", "Il n’est pas nécessaire d’avoir tout éclairci avant de commencer à chercher. Mais on ne s’engage pas non plus sans raisons. Pour reconnaître un éventuel appel de Dieu, nous regardons trois signes : un désir profond, les événements qui nous conduisent vers une communauté et, enfin, ce que cette vie fait grandir en nous lorsque nous commençons réellement à la vivre."),
        ("h2", "Un désir profond, à reconnaître parmi d’autres"),
        ("p", "Le premier signe est un désir que Dieu met dans notre cœur : chercher son amitié, lui consacrer notre vie, nous donner à lui dans la vie monastique."),
        ("p", "Mais notre cœur est habité par de nombreux désirs, parfois contradictoires. Nous pouvons désirer nous donner à Dieu et, en même temps, éprouver le désir d’une relation amoureuse, de fonder une famille, de réussir une carrière ou de construire une maison. L’appel de Dieu ne fait pas disparaître d’un coup toutes les autres aspirations de notre humanité."),
        ("p", "Continuer à désirer le mariage ou la vie de famille ne signifie donc pas, à lui seul, que l’on n’a pas de vocation monastique. Il ne faut pas attendre de ne plus rien désirer d’autre pour commencer à prendre au sérieux un possible appel."),
        ("p", "Il s’agit plutôt d’apprendre à reconnaître, parmi ces aspirations, le désir profond que Dieu fait grandir en nous. Quelle place prend-il dans notre vie ? Est-il seulement un enthousiasme passager ou une question qui demeure et revient, même lorsque d’autres projets nous attirent ? Sommes-nous prêts à lui donner une réponse concrète ?"),
        ("p", "Ce désir a besoin d’être peu à peu dégagé, éclairé et purifié. Cela ne signifie pas que les autres désirs seraient nécessairement mauvais, mais qu’ils ne peuvent pas tous orienter notre vie de la même manière. Répondre à un appel demande de choisir et, par conséquent, de renoncer à d’autres possibilités, qui peuvent être bonnes et rester attirantes."),
        ("p", "Ce travail ne se fait pas en un jour. Il peut prendre des années. La prière, les rencontres avec la communauté et l’aide de ceux qui nous accompagnent permettent d’y voir progressivement plus clair."),
        ("p", "Nous ne cherchons donc pas un cœur sans hésitation ni partage, mais à reconnaître un appel auquel nous pourrons répondre librement, avec toute notre humanité."),
        ("img", "wa-allee", "Des frères sur une allée du domaine", None),
        ("h2", "Des rencontres qui ouvrent un chemin"),
        ("p", "Ce désir ne se développe pas à l’écart de notre histoire. Une rencontre, un livre, la découverte d’un monastère ou une conversation peuvent lui donner une direction concrète."),
        ("p", "Ce sont parfois des événements très simples. Ils nous font découvrir une vie que nous connaissions peu, nous conduisent vers une communauté et nous invitent à faire un premier pas."),
        ("p", "Le désir intérieur et ces événements se répondent. Nous n’y cherchons pas des messages à déchiffrer à tout prix, mais nous apprenons à reconnaître comment Dieu peut nous conduire à travers ce que nous vivons."),
        ("p", "Ces deux premiers signes permettent d’envisager une entrée au monastère. Mais ils ne suffisent pas encore à confirmer que nous pourrons y prendre racine."),
        ("h2", "Une vie dans laquelle on peut grandir"),
        ("p", "Le troisième signe ne se vérifie qu’en commençant réellement à vivre dans la communauté."),
        ("p", "Comme une plante a besoin d’un terrain propice pour prendre racine et se développer, celui qui entre au monastère doit pouvoir y trouver un cadre favorable à sa croissance. Peut-il entrer dans cette vie ? Apprend-il à prier, à vivre avec ses frères, à travailler, à recevoir une formation et à se laisser guider ? Cette vie l’aide-t-elle à grandir dans le don de lui-même et dans l’amour de Dieu ?"),
        ("p", "Cela ne signifie pas que tout lui sera facile ou agréable. Les difficultés ne suffisent pas à dire qu’il n’est pas à sa place. Mais, à travers les efforts et les épreuves, il faut pouvoir constater qu’il progresse et que cette vie porte du fruit en lui."),
        ("p", "Ce regard ne peut pas être seulement le sien. Il a besoin de l’aide de ceux qui l’accompagnent, notamment du père maître et des anciens chargés de sa formation. Leur expérience les aide à discerner avec lui ce qu’il vit, ses capacités et son évolution."),
        ("signs", "Trois signes qui se répondent", [
            "Un désir profond que l’on apprend à reconnaître.",
            "Des événements et des rencontres qui ouvrent un chemin concret.",
            "Une croissance qui se vérifie dans la vie de communauté, avec l’aide de ceux qui nous accompagnent.",
        ]),
        ("h2", "Faut-il donc être certain avant d’entrer ?"),
        ("p", "On ne possède pas à l’avance une certitude qui dispenserait de faire le chemin. On peut reconnaître des signes assez sérieux pour commencer, sans savoir encore tout ce que la vie monastique nous fera découvrir."),
        ("p", "C’est pourquoi le discernement ne s’arrête pas à la porte du monastère. Il se poursuit dans l’expérience de la vie commune. Le désir qui nous a conduits jusqu’ici doit peu à peu recevoir une confirmation dans la réalité vécue, avec l’aide de ceux qui nous accompagnent."),
        ("p", "Il ne s’agit ni d’attendre une preuve impossible avant de faire un pas, ni de s’engager aveuglément. Il s’agit d’avancer avec confiance et vérité, en acceptant que l’appel se précise et se confirme au cours du chemin."),
        ("h2", "Répondre à une invitation"),
        ("quote", "« Le seul fondement solide d’une vocation religieuse est celui-ci : Dieu m’a invité à une vie orientée vers lui seul et j’ai obéi. »", None),
        ("cta",),
    ],
    "next": [("Chercher Dieu", "vie-monastique.html"), ("Avec des frères", "vie-fraternelle.html")],
}

# ----- Site actuel : Prier toujours -----
PAGES["priere"] = {
    "nav": "Prier et vivre chaque jour",
    "kicker": "Prier et vivre chaque jour",
    "title": "Prier toujours",
    "hero": ("eglise-choeur", "Le chœur des moines"),
    "blocks": [
        ("lead", "Entre les offices, le moine doit veiller à « la garde du cœur ». Cela signifie maintenir un lien constant et délicat avec Dieu, Notre Seigneur et la Vierge Marie. Ce lien n’est pas une tension forcée ou une concentration nerveuse. Il s’agit plutôt d’une présence calme et intérieure, semblable à l’amour paisible d’un enfant pour sa mère ou d’un ami pour un autre. En effet, il s’agit d’un lien d’amitié spirituelle qui demande une vigilance aimante."),
        ("h2", "L’invocation : l’axe intime de la vocation"),
        ("p", "L’oraison jaculatoire, ou invocation, est une courte prière personnelle. Elle est précise et théologiquement juste. Elle exprime l’orientation du cœur et incarne l’axe de la vocation du moine. Dans le flot des pensées quotidiennes, ces invocations doivent être régulièrement glissées pour purifier et recentrer l’âme. C’est comparable au bâton de Moïse purifiant les eaux amères. Dès le début de la vie monastique, chaque moine, avec l’aide d’un Ancien, doit créer et s’approprier une invocation. Celle-ci l’accompagnera toute sa vie."),
        ("img", "autel", "Un moine en prière près de l’autel", None),
        ("h2", "Forger une invocation : du sur mesure"),
        ("p", "Forger une invocation avec un jeune frère dès le postulat est un travail délicat. Le Père Maître ne doit pas imposer la sienne. Cela reste vrai même si cela semble plus simple. L’invocation ne peut pas seulement être une réponse émotionnelle. En réalité, elle doit toucher l’identité profonde du futur moine et correspondre à l’appel spécifique de sa vocation. Elle est donc personnelle, façonnée dans le dialogue spirituel et le discernement."),
        ("img", "office-nuit", "L’église à l’office de nuit", None),
        ("h2", "Un art ancien, toujours vivant"),
        ("p", "Bien que la pratique des invocations puisse paraître démodée ou mécanique, elle joue un rôle essentiel pour maintenir la communion avec Dieu après l’office ou l’oraison. C’est comme garder le lien avec un être aimé à distance. Une photo, un message, un appel permettent de conserver ce lien. L’invocation s’apparente à ces anciens appels brefs. Il s’agit de deux ou trois sonneries qui servaient à dire « je pense à toi » sans mots. C’est cette image qui guide l’enseignement de l’art des invocations."),
        ("img", "frere-livre", "Un frère dans les stalles", None),
        ("h2", "La simplicité d’un geste, la persévérance d’une vie"),
        ("p", "En apparence simple, l’invocation s’enseigne en peu de temps. Mais pour l’incarner vraiment, il faut une vie. Elle demande fidélité, effort, ténacité. Elle devient alors ce fil discret mais solide qui relie l’âme de l’homme à Dieu, dans les silences du quotidien."),
        ("btn", "Horaires des offices religieux", "horaires.html"),
    ],
    "next": [("Travail monastique", "travail.html"), ("Horaires des offices religieux", "horaires.html")],
}

# ----- Site actuel : Travail monastique -----
PAGES["travail"] = {
    "nav": "Prier et vivre chaque jour",
    "kicker": "Prier et vivre chaque jour",
    "title": "Travail monastique",
    "hero": ("fourche", "Les frères au travail à la fourche"),
    "blocks": [
        ("lead", "Saint Benoît est réaliste. Appelé à une aventure extraordinaire – vivre proche de Dieu et collaborer à l’œuvre du salut –, le moine reste un homme ordinaire. L’idéal de sa vocation, il le réalise au milieu des exigences communes à toute vie humaine. Ainsi, pour vivre, doit-il travailler."),
        ("img", "travail-1", "Travail monastique", None),
        ("p", "Plus profondément, il s’agit d’acquérir un certain nombre de qualités indispensables à la vie d’union à Dieu. Le travail est l’occasion de développer les vertus du désert. Celles dont le moine a le plus besoin pour soutenir le combat spirituel : détermination, régularité, persévérance…"),
        ("quote", "« Qu’il est nécessaire aux moines de travailler dans les champs, sous la pluie, le soleil, dans la boue, la glaise et le vent ! Ils nous inspirent la vertu, nous rendent stables comme la terre où nous vivons. »", "Thomas Merton"),
        ("imgs", [("travail-3", "Travail à l’atelier"), ("wa-champ", "Frères au travail dans les champs")]),
        ("p", "Le travail manuel en équipe procure le sens du sacrifice. Savoir payer de sa personne, s’oublier, donner son temps et sa fatigue, sans espérer de louange. Ce dévouement que donne la vie concrète, les livres peuvent le faire oublier. C’est pourtant là une attitude essentielle. En même temps, le travail est apprentissage de la vie commune. C’est le lieu par excellence où cristallisent les relations fraternelles. Ainsi, en plus du courage et de la ténacité, du sens du réel et de la responsabilité, le travail inculque au moine l’attention aux autres, la délicatesse, la générosité, la patience. Toutes qualités dont l’absence pourrait compromettre sa vie de prière. Mais il n’acquiert pas forcément ces qualités, ni même d’abord, sur ce terrain-là."),
        ("quote", "La grandeur d’un métier est peut-être, avant tout, d’unir des hommes.", "Antoine de Saint-Exupéry"),
        ("img", "travail-4", "Travail des frères", None),
        ("h2", "Concrètement, le travail à Sept-Fons"),
        ("p", "La part lucrative du travail, celle qui garantit à la communauté sa subsistance matérielle, repose pour l’essentiel sur l’activité de notre atelier de confitures et celle du Moulin de La Trappe. Cette petite PME fabrique, conditionne et expédie toute la gamme de nos compléments alimentaires. Ce sont des dérivés de la fameuse Germalyne, notre produit phare à base de germe de blé, mis au point dans les années 1930. Ces deux emplois occupent à eux seuls une bonne douzaine de frères. Quelques six ouvriers y travaillent matin et soir."),
        ("img", "travail-5", "L’atelier de confitures", None),
        ("btn", "Visitez notre boutique en ligne", "https://www.boutique-abbayedeseptfons.com"),
        ("p", "L’autre part du travail est plus « gratuite ». Si l’on excepte les tâches domestiques (cuisine, buanderie, vestiaire, divers entretiens et nettoyages), c’est principalement le travail de la terre – dans la grande tradition trappiste – qui assure cette fonction."),
        ("imgs", [("wa-maraichage", "Les frères au maraîchage"), ("wa-recolte", "Un frère à la récolte")]),
        ("p", "Avec quelques 100 hectares de surfaces agricoles, ce n’est pas la besogne qui manque ! Celle-ci comprend l’élevage et la traite d’un troupeau de vaches normandes (80 têtes de bétail environ), dont le lait est destiné à la transformation fromagère. Elle comprend aussi les cultures nécessaires à l’affourragement du bétail (maïs, céréales, légumineuses, foin) et au paillage des litières."),
        ("img", "travail-7", "Le troupeau", None),
        ("p", "L’excédent de production est vendu à l’extérieur. Les productions maraîchères et fruitières du potager et du verger viennent agrémenter de produits frais de saison la table des moines et celle des hôtes. Enfin, elle inclut l’entretien des bosquets, des chemins, des haies et des espaces verts… Dans une communauté nombreuse, constituée majoritairement d’hommes jeunes, dans la force de l’âge, cette forme de travail revêt une importance particulière."),
        ("img", "travail-8", "Les champs de l’abbaye", None),
    ],
    "next": [("Prier toujours", "priere.html"), ("Avec des frères", "vie-fraternelle.html")],
}

# ----- Site actuel : Horaires des offices + magasin -----
PAGES["horaires"] = {
    "nav": "Prier et vivre chaque jour",
    "kicker": "Venir à Sept-Fons",
    "title": "Horaires des offices religieux",
    "hero": ("horaires-cloches", "Les cloches de l’abbaye"),
    "blocks": [
        ("lead", "Les offices religieux, dont la messe, sont accessibles au public excepté les matines qui ne sont accessibles qu’aux retraitants. En dehors des heures d’ouverture de la boutique et donc de la présence du frère portier, le monastère est fermé au public. Autrement dit, si vous voulez assister à un office, veuillez consulter les horaires d’ouverture de la porterie."),
        ("tables", [
            ("Horaire d’été", "de mai à octobre", ["", "Dimanches", "En semaine"], [
                ["Matines", "3h45", "3h45"],
                ["Messe", "10h20\nprécédée de Tierce", "6h45\navec Laudes"],
                ["Tierce", "", "9h15"],
                ["Sexte", "12h15", "12h15"],
                ["None", "14h30", "14h30"],
                ["Vêpres", "16h30", "18h00"],
                ["Salut du Saint-Sacrement", "18h20", ""],
                ["Complies", "20h00", "20h00"],
            ]),
            ("Horaire d’hiver", "de novembre à avril", ["", "Dimanches", "En semaine"], [
                ["Matines", "3h30", "3h30"],
                ["Messe", "10h20\nprécédée de Tierce", "6h45\navec Laudes"],
                ["Tierce", "", "9h15"],
                ["Sexte", "12h15", "12h15"],
                ["None", "14h15", "14h15"],
                ["Vêpres", "16h00", "17h30"],
                ["Salut du Saint-Sacrement", "17h50", ""],
                ["Complies", "19h30", "19h30"],
            ]),
        ]),
        ("h2", "Horaires de la solennité de Noël"),
        ("p", "(25 décembre)"),
        ("lines", ["Minuit — Messe solennelle", "7h30 — Laudes", "10h20 — Messe du jour de Noël"]),
        ("p", "Autres offices du jour de Noël :\nHoraires du dimanche"),
        ("h2", "Horaires des offices pendant la Semaine Sainte"),
        ("h3", "DIMANCHE DES RAMEAUX"),
        ("p", "10h : Messe commémorant l’entrée du Seigneur à Jérusalem"),
        ("h3", "JEUDI SAINT"),
        ("p", "16h30 : Messe du soir en mémoire de la Cène du Seigneur"),
        ("h3", "VENDREDI SAINT"),
        ("p", "15 h 00 : Célébration de la Passion du Seigneur"),
        ("h3", "DIMANCHE DE PÂQUES"),
        ("p", "SAMEDI : 23 h 00 : Vigile pascale dans la Nuit Sainte"),
        ("p", "DIMANCHE : 10 h 20 : Tierce suivie de la messe du Jour de Pâques"),
        ("h3", "LUNDI DE PÂQUES"),
        ("p", "Horaire du dimanche, le matin:\nLa messe à 10h20"),
        ("img", "horaires-hotes", "Des hôtes dans l’église", None),
        ("anchor", "magasin"),
        ("h2", "Visitez notre magasin"),
        ("p", "À l’entrée du monastère se trouvent la porterie et un magasin qui vend nos produits et ceux d’autres monastères. Vous y trouverez aussi un grand choix d’articles religieux (chapelets, statues, croix, icônes, médailles…) et une librairie religieuse. La porterie est fermée pendant les offices."),
        ("tables", [
            ("Les heures d’ouvertures", "", ["", "En semaine", "Dimanches et Solennités"], [
                ["De mai\nà octobre", "8h30 – 9h\n9h45 – 12h\n14h50 – 17h30", "8h30 – 10h\n11h50-12h10\n14h50 – 16h15\n17h10 – 18h"],
                ["De novembre\nà avril", "8h30 – 9h\n9h45 – 12h\n14h35 – 17h", "8h30 – 10h\n11h50 – 12h10\n14h35 – 15h45\n16h40 – 17h30"],
            ]),
        ]),
        ("imgs", [("mag-1", "Le magasin de l’abbaye"), ("mag-2", "La librairie"), ("mag-3", "Le magasin")]),
    ],
    "next": [("Hôtellerie", "hotellerie.html"), ("Contacts", "contact.html")],
}

# ----- Site actuel : Hôtellerie -----
PAGES["hotellerie"] = {
    "nav": None,
    "kicker": "Venir à Sept-Fons",
    "title": "Hôtellerie",
    "hero": ("hot-eglise", "L’église abbatiale"),
    "blocks": [
        ("lead", "Fidèles à la tradition bénédictine, les moines accordent une grande importance à l’accueil et à l’hospitalité de quiconque souhaite partager pendant quelques jours leur vie de prière et de silence."),
        ("btn", "Contacter le Père Hôtelier", "ecrire.html?objet=sejour"),
        ("p", "L’église abbatiale est accessible aux heures des offices pour qui veut se joindre au chœur des moines. Ces derniers se rassemble dans l’église tout au long du jour pour y chanter les offices liturgiques."),
        ("btn", "Horaires des offices religieux", "horaires.html"),
        ("p", "La célébration de l’Eucharistie est le cœur de la journée monastique."),
        ("imgs", [("hot-visiteurs", "Des hôtes à l’office"), ("hot-arcades", "Arcades de l’abbaye")]),
        ("p", "À l’entrée du monastère se trouve la porterie, qui comprend l’accueil et le magasin. Vous y découvrirez une large gamme de produits monastiques – dont les nôtres – ainsi que des objets et des livres religieux."),
        ("btn", "Horaires d’ouverture du magasin", "horaires.html#magasin"),
        ("p", "Tout au long de la journée, vous pouvez également visiter notre salle d’exposition, dont l’entrée se situe dans la cour, devant la porterie.\nEntre autres, vous aurez la possibilité de visionner un documentaire présentant notre vie monastique : Présence à Dieu."),
        ("img", "hot-porte", "Une porte ouverte sur le jardin", None),
        ("p", "Si vous souhaitez faire un séjour dans notre hôtellerie, nous recommandons, pour une première visite dans ce lieu de silence, une durée de trois ou quatre jours."),
        ("btn", "Contacter le Père Hôtelier", "ecrire.html?objet=sejour"),
        ("p", "Pour les retraitants, l’église est accessible toute la journée.\nLes repas sont pris en silence dans l’une des salles à manger de l’hôtellerie. Un oratoire, une bibliothèque, quelques salles de réunion et des parloirs sont également à leur disposition.\nNous accueillons aussi des groupes de jeunes."),
        ("p", "Pour toute demande d’information, n’hésitez pas à nous contacter :"),
        ("btn", "Contacter le Père Hôtelier", "ecrire.html?objet=sejour"),
    ],
    "next": [("Horaires des offices religieux", "horaires.html"), ("Contacts", "contact.html")],
}

# ----- Site actuel : Histoire -----
PAGES["histoire"] = {
    "nav": None,
    "kicker": "L’abbaye",
    "title": "Histoire de l’Abbaye",
    "hero": ("hist-gravure", "Gravure ancienne de l’abbaye de Sept-Fons"),
    "blocks": [
        ("lead", "Son nom historique est « Abbaye Notre Dame de Saint-Lieu »."),
        ("p", "L’abbaye de Sept-Fons a vécu, depuis le XIIème siècle, maintes péripéties qui l’ont amenée à ce qu’elle est aujourd’hui."),
        ("h2", "L’Abbaye d’avant la Révolution"),
        ("p", "En 1098, des moines venus de l’[Abbaye de Molesme](http://fr.wikipedia.org/wiki/Abbaye_Notre-Dame_de_Molesme) en Champagne, fondèrent le [monastère de Cîteaux](http://fr.wikipedia.org/wiki/Abbaye_de_C%C3%AEteaux) au sud de Dijon. Ils souhaitaient y vivre sans compromis, en la prenant non pas à la lettre, mais au sérieux, la Règle qu’ils avaient fait profession d’observer. Celle-ci avait été écrite au VIe siècle par celui qu’on appellera le Père des moines d’Occident : [saint Benoît](http://fr.wikipedia.org/wiki/Beno%C3%AEt_de_Nursie)."),
        ("figure", "hist-benoit", "Portrait ancien d’un abbé cistercien", None),
        ("h3", "St Bernard"),
        ("p", "En 1112, une troupe de trente jeunes seigneurs ayant à leur tête [Bernard de Fontaine](http://fr.wikipedia.org/wiki/Bernard_de_Clairvaux), le futur Abbé de Clairvaux, se présente au nouveau monastère. Bernard deviendra l’un des saints les plus marquants de l’Europe médiévale. Cette arrivée massive est le début de l’essor de l’Ordre de Cîteaux dans l’Europe entière."),
        ("h3", "St Étienne Harding"),
        ("figure", "hist-bernard", "Portrait ancien d’un moine", None),
        ("p", "En 1115, [saint Étienne Harding](http://fr.wikipedia.org/wiki/%C3%89tienne_Harding), auteur de la [charte de charité,](http://fr.wikipedia.org/wiki/Carta_Caritatis) troisième Abbé de Cîteaux, envoyait saint Bernard fonder Clairvaux. Trois ans plus tard, Bernard fondait en 1118 l’[Abbaye de Fontenay](http://www.abbayedefontenay.com/). Celle-ci, à son tour, fondait l’Abbaye de Saint-Lieu à Sept-Fons en 1132. Le petit groupe des fondateurs avait à sa tête Richard de Montbard, accompagné de son frère Guillaume, proches parents de Bernard de Fontaine."),
        ("figure", "hist-etienne", "Portrait ancien", None),
        ("h3", "Dom Eustache de Beaufort"),
        ("p", "Pendant des siècles à Sept-Fons, la vie des moines fut régulière et rayonnante. Puis lentement, la ferveur diminua. L’Abbaye tombait en ruines et se dépeuplait lorsqu’en 1656 fut nommé comme Abbé de Sept-Fons Dom Eustache de Beaufort, qui prit possession de son monastère en 1661. Moins de deux ans plus tard, converti à la vie régulière, il commençait une réforme complète de la vie monastique. Sous sa main ferme, Sept-Fons vit de nouveau les vocations affluer. La ferveur renaissait. Pendant tout le XVIIIe siècle, jusqu’à la Révolution, l’Abbaye connut une de ses plus belles périodes."),
        ("figure", "hist-eustache", "Carte postale ancienne", None),
        ("p", "Un successeur de Dom Eustache, Dom Dorothée Jalloutz, reconstruisit le monastère dans le style de l’époque. Achevée en 1789, l’Abbaye fraîchement rénovée subit les conséquences de la Révolution Française. En 1791, les moines sont expulsés. L’Abbaye est vendue comme « bien national ». Pendant la Terreur, plusieurs moines de Sept-Fons confessent leur foi sur les tristement fameux [pontons de Rochefort](http://fr.wikipedia.org/wiki/Pontons_de_Rochefort). Il faudra attendre 1845 pour que les moines reviennent habiter Sept-Fons. Après son rachat par l’Abbé du Gard Dom Stanislas Lapierre, la vie monastique a pu reprendre dans le Bourbonnais, et depuis lors elle n’a plus jamais cessé."),
        ("h3", "Dom Jean-Baptiste Chautard"),
        ("figure", "hist-chautard", "Dom Jean-Baptiste Chautard", None),
        ("p", "Le successeur de Dom Wyart, [Dom Jean-Baptiste Chautard](http://fr.wikipedia.org/wiki/Jean-Baptiste_Chautard) (1899-1935) marqua de sa forte personnalité religieuse l’Église de France au début du XXème siècle. Il joua un rôle important et efficace, obtenant de Clemenceau que soient épargnées à la plupart des monastères de l’Ordre les conséquences des lois laïques. Celles-ci prévoyaient l’expulsion des religieux et la confiscation de leurs biens. Par son livre « L’Âme de tout Apostolat », il exerça une influence durable sur des générations de prêtres et de laïcs."),
        ("h3", "Père Jérôme KIEFER"),
        ("p", "La communauté a connu un bon nombre de moines d’envergure, notamment le [Père Jérôme KIEFER](http://fr.wikipedia.org/wiki/P%C3%A8re_J%C3%A9r%C3%B4me) (1907-1985)."),
        ("figure", "hist-jerome", "Père Jérôme Kiefer", None),
        ("btn", "La croix de nos martyrs", "martyrs.html"),
    ],
    "next": [("La croix de nos martyrs", "martyrs.html"), ("Filiation", "filiation.html")],
}

# ----- Site actuel : La croix de nos martyrs -----
PAGES["martyrs"] = {
    "nav": None,
    "kicker": "L’abbaye",
    "title": "La croix de nos martyrs",
    "hero": ("martyrs-pano", "Fresque du martyre du bienheureux Modeste"),
    "blocks": [
        ("img", "martyrs-archive", "Archive de Casamari", "Dans le couloir du noviciat, le Frère Modeste, de Bourgogne, convers profès, ancien religieux de Sept-Fons, exemplaire en tous points, est massacré à l’arquebuse et au sabre.\nArchive de Casamari"),
        ("h2", "Fidèles jusqu’au bout"),
        ("p", "Les bienheureux Paul, Élie et Modeste, moines trappistes, ont suivi le même chemin de fidélité héroïque. Ils viennent de l’abbaye de Sept-Fons et témoignent d’une foi inébranlable face à la tourmente révolutionnaire. Tous trois ont offert leur vie au Christ, à des moments et en des lieux différents, mais avec le même esprit de don total."),
        ("h2", "Une abbaye florissante avant la tempête"),
        ("p", "À Sept-Fons, une communauté fervente, dirigée par des abbés exemplaires comme Dom Eustache et Dom Dorothée, forme les trois futurs martyrs à la vie monastique. En 1789, la Révolution vient briser cet équilibre ancestral. La confiscation des biens, la suppression des vœux religieux et la dispersion des frères annoncent la fin d’une époque."),
        ("img", "martyrs-dessin", "Dessin des martyrs", None),
        ("h2", "Une résistance silencieuse"),
        ("p", "Malgré une pression toujours plus forte, la majorité des moines choisit de rester à l’abbaye. Le prieur Paul Charles (le futur bienheureux Paul) guide la communauté et tente de préserver la vie monastique, d’abord à Montluçon, puis en exil. Leur refus de prêter le serment révolutionnaire entraîne leur expulsion et leur dispersion à travers l’Europe."),
        ("figure", "martyrs-croix", "La croix des martyrs", "La croix des martyrs avec les\nsignatures des moines de Sept-Fons"),
        ("h2", "Sur les pontons de Rochefort"),
        ("p", "Les autorités arrêtent plusieurs moines, dont Paul et Élie, et les emprisonnent sur les pontons de Rochefort. Là, dans des conditions inhumaines, ils persévèrent dans la prière et le silence. Leur martyre en 1794 exprime une foi vécue jusqu’au bout, dans une fidélité totale. La croix ci-contre, accompagnée des signatures de nos frères de Sept-Fons, a été vénérée durant leur captivité."),
        ("figure", "martyrs-reliquaire", "Reliquaire du Bx Modeste", "Reliquaire du Bx Modeste"),
        ("h2", "Le sacrifice de Modeste à Casamari"),
        ("p", "Frère Modeste trouve refuge en Italie, à l’abbaye trappiste de Casamari. Après quelques années de paix, des soldats révolutionnaires envahissent le monastère en 1799. Pour avoir défendu le sanctuaire, Modeste subit le martyre. Comme ses frères de Sept-Fons, il incarne une fidélité sans compromis jusqu’à la mort."),
        ("h2", "Une enquête toujours en cours"),
        ("p", "Des frères de notre communauté, en collaboration avec d’éminents chercheurs et historiens, poursuivent leurs travaux pour mieux éclairer la vie et le martyre du bienheureux Modeste. De nouveaux éléments pourraient bientôt enrichir notre connaissance de ce témoin de la foi. En attendant, nous vous invitons à suivre nos actualités pour en savoir plus."),
        ("btn", "Découvrez nos actualités", OLD + "/category/actualite-abbaye-sept-fons/"),
    ],
    "next": [("Histoire de l’Abbaye", "histoire.html"), ("Filiation", "filiation.html")],
}

# ----- Site actuel : Filiation -----
PAGES["filiation"] = {
    "nav": None,
    "kicker": "L’abbaye",
    "title": "Filiation",
    "hero": ("aerienne", "Vue aérienne de l’abbaye de Sept-Fons"),
    "blocks": [
        ("lead", "Découvrez les maisons filles de l’Abbaye Notre-Dame de Sept-Fons."),
        ("house", "Bàdi", "fil-badi", "Fondation de l’abbaye de Sept-Fons, le monastère Notre-Dame de Bàdi a été implanté en 2017 dans la région de Tambacounda, à l’est du Sénégal. Il est né d’un lien ancien entre le monastère et le pays : les frères sénégalais formés à Sept-Fons font aujourd’hui partie de la communauté de Bàdi. La vie monastique cistercienne y est vécue dans le silence, la prière et le travail, au cœur des réalités locales.", ("Visitez le site de Bàdi", "https://www.notredamedebadi.sn/")),
        ("house", "Nový Dvůr", "fil-novydvur", "En 1991, avec la chute du communisme dans les pays de l’Europe de l’Est, de jeunes candidats tchèques aspirant à la vie monastique, se sont présentés à l’abbaye de Sept-Fons. Onze plus tard, un monastère près de Plzen, dans la région montagneuse des Sudètes, a été construit dans un style moderne mais fidèle aux intuitions cisterciennes", ("Consultez le site de Nový Dvůr", "http://www.novydvur.cz/fr/day.html")),
        ("house", "Latroun", "fil-latroun", "Fondée en 1890 par des moines cisterciens-trappistes venus de Sept-Fons, l’abbaye de Latroun est située en Terre Sainte, à proximité de Jérusalem. Au fil des décennies, la communauté a aménagé le domaine, construit le monastère et développé notamment la culture de la vigne et de l’olivier. Malgré les conflits qui ont marqué la région, les moines y poursuivent leur vocation de prière et de travail.", ("En savoir plus sur Latroun", "http://www.abbayelatroun.com")),
        ("house", "Tamié", "fil-tamie", "Fondée à partir de 1133 à proximité d’un col de la Tarentaise, l’Abbaye de Tamié porte avec elle un bel héritage : plus de huit cent cinquante ans d’histoire d’une abbaye « à l’écart sur la montagne »", ("Accédez au site de Tamié", "https://www.abbaye-tamie.com/")),
        ("house", "Chambarand", "fil-chambarand", "Fondée en 1868 par des moines cisterciens-trappistes venus de Sept-Fons et de Mérignat, l’abbaye de Chambarand a accueilli successivement des communautés de moines et de moniales. En 2020, la Fraternité bernardine a repris le monastère et y poursuit aujourd’hui la tradition de prière et de vie contemplative.", ("Plus d’infos sur Chambarand", "https://www.chambarand.fr")),
    ],
    "next": [("Ordre Cistercien de la Stricte Observance", "ocso.html"), ("Histoire de l’Abbaye", "histoire.html")],
}

# ----- Site actuel : OCSO -----
PAGES["ocso"] = {
    "nav": None,
    "kicker": "L’abbaye",
    "title": "Ordre Cistercien de la Stricte Observance (OCSO)",
    "hero": ("silhouettes", "Deux moines dans la lumière"),
    "blocks": [
        ("lead", "L’Abbaye de Sept-Fons fait partie de Ordre Cistercien de la Stricte Observance (OCSO) sur le site duquel vous découvrirez histoire de l’ordre, ses textes fondateurs (Charte de Charité, Constitutions, etc.), sa structure, et des photos de tous nos monastères à travers le monde."),
        ("btn", "Le site web de l’OCSO", "https://www.ocso.org/"),
    ],
    "next": [("Filiation", "filiation.html"), ("Histoire de l’Abbaye", "histoire.html")],
}

# ----- Site actuel : Contacts -----
PAGES["contact"] = {
    "nav": None,
    "kicker": "Venir à Sept-Fons",
    "title": "Contacts",
    "hero": ("contact-ble", "Les champs de blé de l’abbaye"),
    "blocks": [
        ("contacts", [
            ("Adresse postale de la communauté",
             ["Abbaye de Sept-Fons", "03290 Dompierre-sur-Besbre", "Téléphone standard : 04 70 48 14 90",
              "(composez le 04 70 48 14 70 pour toute demande concernant nos produits)"],
             [("Écrivez-nous", "ecrire.html?objet=question")]),
            ("Pour un séjour à l’hôtellerie ou pour une retraite",
             ["ou téléphonez : 04 70 48 14 90"],
             [("Écrivez au Père Hôtelier", "ecrire.html?objet=sejour")]),
            ("Pour les commandes par courrier",
             ["Moulin de la Trappe", "BP 13", "Abbaye de Sept-Fons", "03290 Dompierre-sur-Besbre", "Téléphone : 04 70 48 14 70"],
             [("Visitez notre boutique officielle", "http://www.boutique-abbayedeseptfons.com"),
              ("Écrivez-nous pour une commande", "ecrire.html?objet=commande")]),
        ]),
        ("img", "contact-cave", "Un frère sous les voûtes", None),
    ],
    "next": [("Hôtellerie", "hotellerie.html"), ("Faire un don", "don.html")],
}

# ----- Site actuel : Faire un don -----
PAGES["don"] = {
    "nav": None,
    "kicker": "Soutenir",
    "title": "Faire un don",
    "hero": ("don-bandeau", "Les terres de l’abbaye"),
    "blocks": [
        ("h2", "Nous avons besoin de vous pour nous soutenir!"),
        ("p", "Si notre travail nous permet de répondre aux besoins courants de la vie de la communauté, nous avons besoin de donateurs pour nous soutenir dans nos projets de vie monastique. Ces projets s’étendent à travers le monde et dans nos travaux de rénovation."),
        ("h3", "POUR NOUS SOUTENIR\nPASSEZ PAR LA FONDATION DES MONASTÈRES"),
        ("p", "La Fondation des Monastères délivre systématiquement un reçu fiscal"),
        ("btn", "Faire un don en ligne par la Fondation", "https://don.fondationdesmonasteres.org/septfons"),
        ("h3", "OU PAR COURRIER"),
        ("p", "Libellez votre chèque à l’ordre de la Fondation des Monastères,\nen précisant au dos « Abbaye de Sept Fons »,\net envoyez votre courrier à l’adresse suivante :"),
        ("lines", ["FRÈRE GODEFROID", "ABBAYE DE SEPT FONS", "03290 DOMPIERRE SUR BESBRE"]),
        ("p", "La Fondation des Monastères, reconnue d’utilité publique depuis 1974, a pour but d’apporter son concours charitable aux membres des collectivités religieuses de toutes confessions chrétiennes."),
        ("p", "Vous bénéficiez d’un cadre fiscal avantageux : une réduction d’impôts de 66 % dans la limite de 20 % de votre revenu net imposable. Un reçu fiscal vous sera systématiquement envoyé. 5% de la somme seront réservés à la Fondation. Le restant sera reversé à notre abbaye."),
        ("p", "Pour tout renseignement concernant les dons, veuillez nous contacter à [secretariat@septfons.com](mailto:secretariat@septfons.com) ou au 04 70 48 14 84."),
    ],
    "next": [("Contacts", "contact.html"), ("Travail monastique", "travail.html")],
}

PAGE_ORDER = ["vie-monastique", "vie-fraternelle", "vocation", "priere", "travail", "horaires",
              "hotellerie", "histoire", "martyrs", "filiation", "ocso", "contact", "don"]

# ----- Site actuel : Album « Possibilités et mélodies » -----
PAGES["cd"] = {
    "nav": None,
    "kicker": "Album",
    "title": "Possibilités et mélodies",
    "hero": ("cd-2", "Vitrail de la Vierge à l’Enfant"),
    "blocks": [
        ("linkrow", [("Téléchargement", OLD + "/cd/telechargement/"), ("Livret", OLD + "/cd/livret/"),
                     ("Témoignage", OLD + "/cd/temoignage/"), ("Historique", OLD + "/cd/historique/"), ("CZ", OLD + "/cd/cz/")]),
        ("figure", "cd-couverture", "Pochette de l’album « Possibilités et mélodies »", None),
        ("p", "Notre album est disponible au [magasin de l’abbaye](horaires.html#magasin) ou"),
        ("btn", "sur notre boutique en ligne", "https://www.boutique-abbayedeseptfons.com/fr/home/488-album-possibilites-melodies-3264950900149.html"),
        ("lead", "Ce disque offre un aperçu d’une journée monastique solennelle vécue à l’abbaye de Sept-Fons. Du premier appel des Matines jusqu’au Salve Regina, au seuil de la nuit, le chant grégorien et la musique instrumentale s’unissent pour célébrer Celui qui est au cœur de notre vie, source de toutes possibilités et de toutes mélodies."),
        ("btn", "Découvrir le contenu du disque", OLD + "/cd/livret/#h-contenu-du-cd"),
        ("lines", ["Matines et Laudes – La Messe – Intermezzo –", "Vêpres et Complies – Postlude"]),
        ("p", "Durée totale : 79 min 56 s"),
        ("img", "cd-3", "Les frères dans le cloître", None),
        ("p", "La couverture du CD met en avant un motif graphique inspiré d’une ancienne forme de la ligature latine « et » (le signe « & »). Utilisé depuis l’Antiquité, ce symbole relie non seulement les deux mots du titre, mais évoque aussi le lien entre passé et présent que porte cet enregistrement. En arrière-plan, une photographie d’un mur  de l’abbaye rappelle le lieu et renforce l’idée d’une continuité à travers les âges."),
    ],
    "next": [("Horaires des offices religieux", "horaires.html"), ("Histoire de l’Abbaye", "histoire.html")],
}
PAGE_ORDER.append("cd")

SOURCE_URL = OLD + "/source-magazine/"
SHOP_URL = "https://www.boutique-abbayedeseptfons.com/"

# Menu « L'abbaye » : tout le reste du site, rangé en trois colonnes courtes
MORE_LABEL = "L’abbaye"
MORE = [
    ("Venir à Sept-Fons", [
        ("Hôtellerie", "hotellerie.html"),
        ("Horaires des offices religieux", "horaires.html"),
        ("Visitez notre magasin", "horaires.html#magasin"),
        ("Contacts", "contact.html"),
    ]),
    ("Découvrir", [
        ("Histoire de l’Abbaye", "histoire.html"),
        ("La croix de nos martyrs", "martyrs.html"),
        ("Filiation", "filiation.html"),
        ("Album « Possibilités et mélodies »", "cd.html"),
        ("SOURCE – Le Magazine", SOURCE_URL),
        ("Homélies", OLD + "/homelies/"),
    ]),
    ("Soutenir", [
        ("Boutique en ligne", SHOP_URL),
        ("Faire un don", "don.html"),
    ]),
]
# Barre discrète (versions « utilitaires ») : cinq accès directs
UTILITY = [("Hôtellerie", "hotellerie.html"), ("Boutique", SHOP_URL), ("Album", "cd.html"),
           ("SOURCE – Le Magazine", SOURCE_URL), ("Faire un don", "don.html")]

FOOTER_LINKS = [
    ("L’abbaye", [
        ("Histoire de l’Abbaye", "histoire.html"),
        ("La croix de nos martyrs", "martyrs.html"),
        ("Filiation", "filiation.html"),
        ("Ordre Cistercien de la Stricte Observance", "ocso.html"),
        ("Album « Possibilités et mélodies »", "cd.html"),
        ("SOURCE – Le Magazine", SOURCE_URL),
    ]),
    ("Venir à Sept-Fons", [
        ("Hôtellerie", "hotellerie.html"),
        ("Horaires des offices religieux", "horaires.html"),
        ("Visitez notre magasin", "horaires.html#magasin"),
        ("Contacts", "contact.html"),
        ("Nous écrire", "ecrire.html"),
    ]),
    ("Ressources", [
        ("Homélies", OLD + "/homelies/"),
        ("Actualités", OLD + "/category/actualite-abbaye-sept-fons/"),
        ("Boutique en ligne", SHOP_URL),
        ("Faire un don", "don.html"),
    ]),
]

LANGS = [("fr", "Français"), ("en", "English"), ("de", "Deutsch"), ("es", "Español"),
         ("it", "Italiano"), ("cs", "Čeština"), ("pl", "Polski")]
