"""Banque de contenus : textes, chiffres et icônes par secteur.
Tout est en français et volontairement générique pour rester réutilisable.
"""
from __future__ import annotations

SECTORS = {
    "corporate": {
        "label": "Entreprise & Stratégie",
        "kicker": "Stratégie d'entreprise",
        "title": "Feuille de route 2026",
        "subtitle": "Un cap clair, des priorités mesurables et une exécution disciplinée.",
        "icons": ["building-2", "target", "handshake", "trending-up", "users", "briefcase"],
        "kpis": [("+24 %", "Croissance du chiffre d'affaires"), ("92 %", "Satisfaction client"),
                 ("18 mois", "Retour sur investissement"), ("3,4 M€", "Économies identifiées")],
        "items": [
            ("Vision", "Devenir la référence régionale sur notre marché d'ici trois ans."),
            ("Priorités", "Concentrer 80 % des ressources sur quatre chantiers structurants."),
            ("Exécution", "Un pilotage mensuel, des indicateurs partagés et des arbitrages rapides."),
            ("Culture", "Une organisation apprenante, responsable et orientée résultats."),
        ],
        "steps": ["Diagnostic", "Cadrage", "Déploiement", "Mesure", "Industrialisation"],
    },
    "finance": {
        "label": "Finance & Investissement",
        "kicker": "Performance financière",
        "title": "Résultats consolidés 2026",
        "subtitle": "Une croissance rentable, une trésorerie solide et un endettement maîtrisé.",
        "icons": ["banknote", "chart-line", "percent", "wallet", "landmark", "receipt"],
        "kpis": [("48,2 M€", "Chiffre d'affaires"), ("+18,6 %", "Marge brute"),
                 ("12,4 %", "EBITDA"), ("2,1 M€", "Flux de trésorerie libre")],
        "items": [
            ("Revenus", "Hausse portée par les offres récurrentes et l'expansion géographique."),
            ("Marges", "Gain de 2,3 points grâce à l'optimisation des coûts variables."),
            ("Trésorerie", "Une génération de cash stable sur les quatre derniers trimestres."),
            ("Risques", "Sensibilité limitée aux taux et couverture de change en place."),
        ],
        "steps": ["Budget", "Réalisé", "Écart", "Révision", "Prévision"],
    },
    "medical": {
        "label": "Santé & Médical",
        "kicker": "Santé & innovation médicale",
        "title": "Parcours de soins 2026",
        "subtitle": "Une prise en charge plus fluide, plus humaine et mieux coordonnée.",
        "icons": ["stethoscope", "heart-pulse", "pill", "microscope", "syringe", "activity"],
        "kpis": [("98,4 %", "Patients satisfaits"), ("-32 %", "Délai de prise en charge"),
                 ("12 400", "Consultations / an"), ("4,8/5", "Note des équipes")],
        "items": [
            ("Prévention", "Dépistage précoce et suivi personnalisé des patients à risque."),
            ("Coordination", "Un dossier partagé entre médecins, infirmiers et pharmacies."),
            ("Qualité", "Protocoles validés et indicateurs cliniques suivis en continu."),
            ("Accès", "Téléconsultation et unités mobiles pour les zones isolées."),
        ],
        "steps": ["Admission", "Diagnostic", "Traitement", "Suivi", "Prévention"],
    },
    "creative": {
        "label": "Agence créative",
        "kicker": "Studio de création",
        "title": "Identité de marque",
        "subtitle": "Une direction artistique affirmée, cohérente sur tous les points de contact.",
        "icons": ["palette", "pen-tool", "sparkles", "camera", "layers", "type"],
        "kpis": [("+142 %", "Engagement social"), ("3,2 M", "Impressions organiques"),
                 ("28", "Campagnes livrées"), ("4,9/5", "Satisfaction client")],
        "items": [
            ("Positionnement", "Une promesse simple, différenciante et mémorable."),
            ("Direction artistique", "Typographie forte, couleurs assumées, composition aérée."),
            ("Ton de voix", "Direct, chaleureux, jamais institutionnel."),
            ("Déclinaisons", "Réseaux sociaux, print, packaging et motion design."),
        ],
        "steps": ["Brief", "Recherche", "Concept", "Production", "Lancement"],
    },
    "tech": {
        "label": "Technologie & Produit",
        "kicker": "Plateforme technologique",
        "title": "Architecture produit 2026",
        "subtitle": "Une plateforme modulaire, observable et prête à passer à l'échelle.",
        "icons": ["cpu", "server", "code", "database", "cloud", "shield-check"],
        "kpis": [("99,98 %", "Disponibilité"), ("68 ms", "Latence moyenne"),
                 ("1,2 M", "Utilisateurs actifs"), ("42/j", "Déploiements")],
        "items": [
            ("Modularité", "Des services découplés, versionnés et testés automatiquement."),
            ("Observabilité", "Traces, métriques et alertes corrélées en temps réel."),
            ("Sécurité", "Chiffrement de bout en bout et gestion fine des accès."),
            ("Scalabilité", "Montée en charge horizontale et coûts maîtrisés."),
        ],
        "steps": ["Discovery", "Design", "Build", "Test", "Run"],
    },
    "sport": {
        "label": "Sport & Performance",
        "kicker": "Performance sportive",
        "title": "Saison 2026",
        "subtitle": "Préparation, intensité et récupération : la performance se construit chaque jour.",
        "icons": ["trophy", "dumbbell", "timer", "activity", "target", "medal"],
        "kpis": [("+12 %", "Puissance maximale"), ("4,1 s", "Sprint 30 m"),
                 ("86 %", "Temps de possession"), ("24", "Victoires")],
        "items": [
            ("Préparation physique", "Cycles de charge et récupération individualisés."),
            ("Analyse vidéo", "Décryptage tactique après chaque rencontre."),
            ("Nutrition", "Plans personnalisés et suivi biologique mensuel."),
            ("Mental", "Routines de concentration et gestion de la pression."),
        ],
        "steps": ["Pré-saison", "Championnat", "Play-offs", "Finale", "Bilan"],
    },
    "education": {
        "label": "Éducation & Formation",
        "kicker": "Pédagogie & apprentissage",
        "title": "Programme pédagogique",
        "subtitle": "Des parcours actifs, mesurables et adaptés à chaque profil d'apprenant.",
        "icons": ["graduation-cap", "book-open", "lightbulb", "users", "award", "pencil"],
        "kpis": [("94 %", "Taux de réussite"), ("1 800", "Apprenants formés"),
                 ("+31 %", "Engagement des élèves"), ("4,7/5", "Évaluation des cours")],
        "items": [
            ("Pédagogie active", "Apprentissage par projet et mises en situation réelles."),
            ("Suivi", "Évaluations formatives et retours individualisés."),
            ("Outils", "Plateforme, ressources multimédia et classes virtuelles."),
            ("Inclusion", "Adaptations pour les profils à besoins spécifiques."),
        ],
        "steps": ["Diagnostic", "Parcours", "Pratique", "Évaluation", "Certification"],
    },
    "realestate": {
        "label": "Immobilier",
        "kicker": "Immobilier & territoires",
        "title": "Projet immobilier",
        "subtitle": "Un programme pensé pour l'usage, la durabilité et la valeur patrimoniale.",
        "icons": ["building", "house", "map-pin", "ruler", "leaf", "key"],
        "kpis": [("128", "Logements"), ("4 200 m²", "Surface habitable"),
                 ("-38 %", "Consommation d'énergie"), ("2027", "Livraison prévue")],
        "items": [
            ("Localisation", "Un emplacement connecté, desservi et attractif."),
            ("Conception", "Volumes lumineux et espaces modulables."),
            ("Durabilité", "Matériaux biosourcés et performance énergétique."),
            ("Valorisation", "Une rentabilité locative sécurisée sur le long terme."),
        ],
        "steps": ["Foncier", "Conception", "Autorisations", "Chantier", "Livraison"],
    },
    "tourism": {
        "label": "Tourisme & Hôtellerie",
        "kicker": "Expérience voyageur",
        "title": "Destination 2026",
        "subtitle": "Une expérience client fluide, sensorielle et mémorable à chaque étape.",
        "icons": ["plane", "map", "hotel", "compass", "camera", "utensils"],
        "kpis": [("+27 %", "Nuitées"), ("8,7/10", "Note voyageurs"),
                 ("72 %", "Taux d'occupation"), ("+19 %", "Panier moyen")],
        "items": [
            ("Arrivée", "Un accueil personnalisé et sans friction."),
            ("Séjour", "Des expériences locales sélectionnées avec soin."),
            ("Services", "Conciergerie, restauration et bien-être sur place."),
            ("Fidélisation", "Programme de reconnaissance et offres sur mesure."),
        ],
        "steps": ["Réservation", "Accueil", "Séjour", "Expériences", "Fidélisation"],
    },
    "retail": {
        "label": "Commerce & Retail",
        "kicker": "Commerce & distribution",
        "title": "Plan commercial",
        "subtitle": "Des points de contact cohérents et une expérience d'achat sans couture.",
        "icons": ["shopping-bag", "store", "package", "credit-card", "truck", "tag"],
        "kpis": [("+21 %", "Ventes en ligne"), ("3,8 %", "Taux de conversion"),
                 ("24 €", "Panier moyen"), ("-15 %", "Taux de retour")],
        "items": [
            ("Assortiment", "Une sélection resserrée et lisible, pilotée par la donnée."),
            ("Prix", "Une politique tarifaire claire et compétitive."),
            ("Parcours", "Retrait en magasin, livraison et retours simplifiés."),
            ("Animation", "Temps forts commerciaux et contenus engageants."),
        ],
        "steps": ["Sourcing", "Merchandising", "Campagne", "Vente", "Fidélisation"],
    },
    "energy": {
        "label": "Énergie & Environnement",
        "kicker": "Transition énergétique",
        "title": "Plan climat",
        "subtitle": "Réduire nos émissions tout en sécurisant l'approvisionnement.",
        "icons": ["leaf", "zap", "wind", "sun", "recycle", "factory"],
        "kpis": [("-42 %", "Émissions de CO₂e"), ("68 %", "Énergie renouvelable"),
                 ("1,4 GWh", "Production annuelle"), ("2,6 M€", "Économies d'énergie")],
        "items": [
            ("Sobriété", "Réduire la consommation avant de produire plus."),
            ("Décarbonation", "Électrification des usages et chaleur renouvelable."),
            ("Réseaux", "Stockage, pilotage intelligent et effacement."),
            ("Gouvernance", "Trajectoire alignée sur l'accord de Paris."),
        ],
        "steps": ["Audit", "Trajectoire", "Investissements", "Déploiement", "Reporting"],
    },
    "ngo": {
        "label": "ONG & Impact social",
        "kicker": "Impact social",
        "title": "Rapport d'impact",
        "subtitle": "Des résultats concrets, mesurés et partagés avec nos partenaires.",
        "icons": ["heart-handshake", "users", "globe", "sprout", "hand-heart", "droplets"],
        "kpis": [("48 000", "Bénéficiaires"), ("126", "Projets financés"),
                 ("18", "Pays d'intervention"), ("92 %", "Fonds affectés")],
        "items": [
            ("Éducation", "Scolarisation et alphabétisation des jeunes filles."),
            ("Santé", "Accès aux soins primaires dans les zones rurales."),
            ("Eau", "Points d'eau potable et assainissement durable."),
            ("Autonomie", "Formation professionnelle et microcrédit."),
        ],
        "steps": ["Identification", "Co-création", "Mise en œuvre", "Suivi", "Capitalisation"],
    },
    "hr": {
        "label": "Ressources humaines",
        "kicker": "Capital humain",
        "title": "Expérience collaborateur",
        "subtitle": "Attirer, développer et fidéliser les talents qui feront la différence.",
        "icons": ["users", "user-check", "graduation-cap", "heart", "briefcase", "sparkles"],
        "kpis": [("+9 pts", "Engagement"), ("14 j", "Délai de recrutement"),
                 ("87 %", "Rétention à 2 ans"), ("32 h", "Formation / an")],
        "items": [
            ("Attraction", "Marque employeur claire et parcours candidat fluide."),
            ("Intégration", "Un onboarding structuré sur 90 jours."),
            ("Développement", "Plans de formation et mobilité interne."),
            ("Qualité de vie", "Flexibilité, équilibre et prévention des risques."),
        ],
        "steps": ["Sourcing", "Entretien", "Onboarding", "Développement", "Fidélisation"],
    },
    "industry": {
        "label": "Industrie & Production",
        "kicker": "Excellence opérationnelle",
        "title": "Performance industrielle",
        "subtitle": "Fiabiliser la production, réduire les pertes et accélérer les cycles.",
        "icons": ["factory", "cog", "truck", "wrench", "gauge", "boxes"],
        "kpis": [("+16 %", "OEE"), ("-28 %", "Temps d'arrêt"), ("99,2 %", "Qualité"),
                 ("4,2 j", "Rotation des stocks")],
        "items": [
            ("Flux", "Réorganisation en îlots et réduction des en-cours."),
            ("Maintenance", "Préventif prédictif basé sur les capteurs."),
            ("Qualité", "Contrôles en ligne et analyse des causes racines."),
            ("Sécurité", "Standards, formation et culture du signalement."),
        ],
        "steps": ["Analyse", "Standardisation", "Automatisation", "Mesure", "Amélioration"],
    },
    "legal": {
        "label": "Juridique & Conformité",
        "kicker": "Conformité & gouvernance",
        "title": "Cadre de conformité",
        "subtitle": "Un dispositif de contrôle proportionné, documenté et auditable.",
        "icons": ["scale", "shield", "file-check", "lock", "gavel", "clipboard-check"],
        "kpis": [("0", "Sanction réglementaire"), ("98 %", "Actions de remédiation clôturées"),
                 ("12", "Politiques mises à jour"), ("100 %", "Collaborateurs formés")],
        "items": [
            ("Cartographie", "Identification des risques et des obligations applicables."),
            ("Politiques", "Règles internes claires et accessibles à tous."),
            ("Contrôles", "Dispositif de tests et de revues indépendantes."),
            ("Formation", "Sensibilisation continue et culture de la conformité."),
        ],
        "steps": ["Cartographie", "Politiques", "Contrôles", "Audit", "Remédiation"],
    },
    "logistics": {
        "label": "Logistique & Supply chain",
        "kicker": "Chaîne d'approvisionnement",
        "title": "Supply chain 2026",
        "subtitle": "Une chaîne plus courte, plus prévisible et plus résiliente.",
        "icons": ["truck", "package", "warehouse", "route", "ship", "boxes"],
        "kpis": [("−21 %", "Coût logistique"), ("98,6 %", "Taux de service"),
                 ("2,4 j", "Délai moyen"), ("−34 %", "Empreinte transport")],
        "items": [
            ("Prévision", "Planification collaborative avec les fournisseurs."),
            ("Stockage", "Implantations optimisées et stocks mutualisés."),
            ("Transport", "Multimodal, groupage et tournées optimisées."),
            ("Visibilité", "Suivi temps réel de bout en bout."),
        ],
        "steps": ["Prévision", "Approvisionnement", "Entreposage", "Transport", "Livraison"],
    },
    "food": {
        "label": "Restauration & Food",
        "kicker": "Art de la table",
        "title": "Nouvelle carte",
        "subtitle": "Des produits de saison, une exécution simple et une expérience généreuse.",
        "icons": ["utensils", "coffee", "chef-hat", "wine", "croissant", "leaf"],
        "kpis": [("+26 %", "Fréquentation"), ("4,6/5", "Avis clients"),
                 ("18", "Producteurs locaux"), ("-12 %", "Gaspillage")],
        "items": [
            ("Sourcing", "Circuits courts et produits de saison."),
            ("Carte", "Une offre resserrée, signature et rentable."),
            ("Service", "Un accueil chaleureux et un service rapide."),
            ("Expérience", "Ambiance, sonorisation et fidélisation."),
        ],
        "steps": ["Sélection", "Création", "Dégustation", "Lancement", "Ajustement"],
    },
    "auto": {
        "label": "Automobile & Mobilité",
        "kicker": "Mobilité de demain",
        "title": "Offre mobilité",
        "subtitle": "Électrification, services connectés et expérience client repensée.",
        "icons": ["car", "battery-charging", "map-pin", "gauge", "wrench", "route"],
        "kpis": [("+38 %", "Véhicules électriques"), ("92 %", "Satisfaction"),
                 ("14 min", "Temps de charge"), ("2,1 M", "Km parcourus")],
        "items": [
            ("Gamme", "Une offre électrifiée couvrant tous les usages."),
            ("Recharge", "Réseau dense et paiement simplifié."),
            ("Services", "Connectivité, maintenance prédictive et mobilité partagée."),
            ("Réseau", "Un parcours d'achat omnicanal et transparent."),
        ],
        "steps": ["Conception", "Homologation", "Production", "Distribution", "Service"],
    },
    "telecom": {
        "label": "Télécoms",
        "kicker": "Connectivité",
        "title": "Réseau nouvelle génération",
        "subtitle": "Plus de débit, moins de latence et une couverture élargie.",
        "icons": ["wifi", "signal", "smartphone", "radio", "satellite", "globe"],
        "kpis": [("+64 %", "Débit moyen"), ("12 ms", "Latence"), ("98,9 %", "Couverture"),
                 ("-23 %", "Consommation réseau")],
        "items": [
            ("Densification", "Nouvelles antennes et petites cellules urbaines."),
            ("Fibre", "Déploiement accéléré en zones périurbaines."),
            ("Services", "Offres convergentes fixe, mobile et cloud."),
            ("Énergie", "Sites autonomes et équipements basse consommation."),
        ],
        "steps": ["Planification", "Déploiement", "Optimisation", "Qualité", "Exploitation"],
    },
    "agri": {
        "label": "Agriculture",
        "kicker": "Agriculture durable",
        "title": "Récolte 2026",
        "subtitle": "Produire mieux avec moins d'intrants et plus de données.",
        "icons": ["sprout", "tractor", "droplets", "sun", "wheat", "leaf"],
        "kpis": [("+19 %", "Rendement"), ("-31 %", "Intrants"), ("2 400 ha", "Surface suivie"),
                 ("100 %", "Traçabilité")],
        "items": [
            ("Sols", "Couverture, rotation et matière organique."),
            ("Irrigation", "Pilotage par capteurs et goutte-à-goutte."),
            ("Données", "Cartographie parcellaire et modulation des intrants."),
            ("Filières", "Contrats pluriannuels et juste rémunération."),
        ],
        "steps": ["Semis", "Croissance", "Protection", "Récolte", "Distribution"],
    },
    "insurance": {
        "label": "Assurance",
        "kicker": "Protection & confiance",
        "title": "Parcours assuré",
        "subtitle": "Souscrire et être indemnisé simplement, en quelques minutes.",
        "icons": ["shield-check", "umbrella", "file-text", "phone", "heart-handshake", "lock"],
        "kpis": [("-45 %", "Délai d'indemnisation"), ("94 %", "Clients satisfaits"),
                 ("+17 %", "Taux de souscription"), ("3,4 M€", "Sinismes évités")],
        "items": [
            ("Souscription", "Parcours digital et tarification transparente."),
            ("Prévention", "Conseils personnalisés et détection des risques."),
            ("Sinistres", "Déclaration simplifiée et expertise rapide."),
            ("Fidélité", "Offres évolutives selon le profil."),
        ],
        "steps": ["Devis", "Souscription", "Vie du contrat", "Sinistre", "Indemnisation"],
    },
    "luxury": {
        "label": "Luxe & Art de vivre",
        "kicker": "Maison & savoir-faire",
        "title": "Collection signature",
        "subtitle": "L'excellence du geste, la rareté des matières et le temps juste.",
        "icons": ["gem", "crown", "sparkles", "watch", "scissors", "award"],
        "kpis": [("+31 %", "Croissance"), ("120", "Heures de façonnage"),
                 ("18", "Ateliers partenaires"), ("96 %", "Clients fidèles")],
        "items": [
            ("Matières", "Sélection exigeante et traçabilité complète."),
            ("Savoir-faire", "Gestes transmis et artisans d'exception."),
            ("Rareté", "Séries limitées et personnalisation."),
            ("Expérience", "Salons privés et service sur mesure."),
        ],
        "steps": ["Esquisse", "Matière", "Façonnage", "Contrôle", "Écrin"],
    },
    "startup": {
        "label": "Startup & Levée de fonds",
        "kicker": "Pitch investisseurs",
        "title": "Notre histoire",
        "subtitle": "Un problème massif, une solution simple et une traction mesurable.",
        "icons": ["rocket", "lightbulb", "trending-up", "users", "coins", "target"],
        "kpis": [("+38 %", "Croissance mensuelle"), ("1 200", "Clients actifs"),
                 ("94 %", "Rétention"), ("1,8 M€", "ARR")],
        "items": [
            ("Problème", "Un marché fragmenté et des processus chronophages."),
            ("Solution", "Une plateforme unifiée, rapide à déployer."),
            ("Traction", "Une croissance organique portée par le produit."),
            ("Marché", "Un potentiel de 4,2 milliards d'euros en Europe."),
        ],
        "steps": ["Idée", "MVP", "Traction", "Scale", "Exit"],
    },
}

SECTORS_KEYS = list(SECTORS.keys())


def sector(key):
    return SECTORS.get(key, SECTORS["corporate"])


# Contenus supplémentaires génériques
VALUES = [
    ("Excellence", "Nous visons le meilleur dans chaque détail, sans compromis."),
    ("Transparence", "Nous partageons nos résultats, nos doutes et nos décisions."),
    ("Audace", "Nous testons vite, apprenons vite et assumons nos choix."),
    ("Collectif", "Nous réussissons ensemble ou pas du tout."),
    ("Responsabilité", "Nous mesurons notre impact et en rendons compte."),
    ("Simplicité", "Nous retirons tout ce qui n'ajoute pas de valeur."),
]

PERSONAS = [
    ("Le décideur pressé", "Veut des chiffres, des faits et une conclusion en 10 secondes."),
    ("L'utilisateur quotidien", "Cherche de la fluidité, de la confiance et du temps gagné."),
    ("Le partenaire technique", "Attend de la documentation, des API et de la stabilité."),
    ("L'acheteur financier", "Compare le coût total, le risque et le retour sur investissement."),
]

RISKS = [
    ("Dépendance fournisseur", 4, 4, "Double sourcing et contrats révisables"),
    ("Cybermenace", 3, 5, "SOC, chiffrement, plan de continuité"),
    ("Tension de recrutement", 3, 3, "Marque employeur et viviers internes"),
    ("Volatilité des coûts", 4, 3, "Couvertures et clauses d'indexation"),
    ("Réglementation", 2, 4, "Veille juridique et conformité by design"),
]

MONTHS = ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin", "Juil", "Août", "Sep", "Oct", "Nov", "Déc"]
QUARTERS = ["T1", "T2", "T3", "T4"]

COUNTRY_STATS = [
    ("France", "Europe", 68, 42), ("Sénégal", "Afrique", 34, 21), ("Maroc", "Afrique", 52, 33),
    ("Canada", "Amérique", 61, 38), ("Brésil", "Amérique", 47, 30), ("Inde", "Asie", 74, 51),
    ("Japon", "Asie", 82, 58), ("Australie", "Océanie", 39, 24),
]

SECTORS_GEO = [
    ("Siège", (2.35, 48.85), "Paris"), ("Bureau", (-17.45, 14.72), "Dakar"),
    ("Bureau", (-74.0, 40.71), "New York"), ("Bureau", (55.27, 25.2), "Dubaï"),
    ("Bureau", (103.82, 1.35), "Singapour"), ("Bureau", (-46.63, -23.55), "São Paulo"),
]

TEAM = [
    ("Aminata Diallo", "Directrice générale", "users"),
    ("Lucas Moreau", "Directeur financier", "calculator"),
    ("Sofia Bennani", "Directrice marketing", "megaphone"),
    ("Kenji Tanaka", "CTO", "cpu"),
]

TESTIMONIALS = [
    ("« Le déploiement a pris trois semaines, pas trois mois. »",
     "Claire Fontaine", "Directrice des opérations, Novara"),
    ("« Enfin un outil que nos équipes utilisent vraiment au quotidien. »",
     "Ibrahim Sow", "Responsable régional, Sahel Distribution"),
    ("« Les résultats sont là, mesurables et partagés avec toute l'entreprise. »",
     "Marina Rossi", "CFO, Groupe Altura"),
]

FAQ = [
    ("Combien de temps pour démarrer ?", "Le déploiement standard prend trois semaines, accompagnement inclus."),
    ("Quelles données sont nécessaires ?", "Un extrait de votre référentiel produit et vos historiques de ventes."),
    ("Comment se passe la formation ?", "Deux ateliers en visio et une bibliothèque de tutoriels courts."),
    ("Quel est le modèle tarifaire ?", "Un abonnement mensuel par utilisateur, sans engagement de durée."),
]

ICON_SETS = {
    "Direction": ["target", "compass", "map", "flag", "milestone", "route"],
    "Finance": ["wallet", "coins", "banknote", "receipt", "calculator", "piggy-bank"],
    "Équipe": ["users", "user-check", "handshake", "message-circle", "heart", "sparkles"],
    "Technologie": ["cpu", "cloud", "database", "server", "wifi", "shield-check"],
    "Créativité": ["palette", "pen-tool", "brush", "camera", "music", "film"],
    "Santé": ["heart-pulse", "stethoscope", "pill", "activity", "microscope", "syringe"],
    "Écologie": ["leaf", "sprout", "recycle", "sun", "wind", "droplets"],
    "Croissance": ["trending-up", "chart-line", "rocket", "zap", "award", "trophy"],
}


# Dates / périodes / mesures génériques, pour varier les visuels de données
for key, sd in SECTORS.items():
    y = 2020
    sd.setdefault("years", [str(2021 + i) for i in range(6)])
    sd.setdefault("regions", ["Amérique du Nord", "Europe", "Afrique", "Asie-Pacifique",
                              "Amérique latine"])
    sd.setdefault("segments", ["Grands comptes", "ETI", "PME", "Particuliers"])
    sd.setdefault("units", ["k€", "unités", "clients", "projets"])
    sd.setdefault("months", MONTHS)
