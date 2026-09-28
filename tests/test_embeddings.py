from devassistant.embeddings import embed


texts = [
    "Le Nutri-Score évalue la qualité nutritionnelle des aliments.",
    "Le produit contient beaucoup de protéines.",
    "Les pommes sont des fruits.",
]


vectors = embed(texts)


for i, vector in enumerate(vectors):
    print(f"Texte {i + 1}")
    print(f"Nombre de dimensions : {len(vector)}")
    print(f"Premières valeurs : {vector[:5]}")
    print()