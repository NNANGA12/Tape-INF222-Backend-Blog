from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import date
from typing import List, Optional

app = FastAPI(title="Blog API INF222")

# Modèle de données pour un article
class Article(BaseModel):
    id: Optional[int] = None
    titre: str
    contenu: str
    auteur: str
    date: str = str(date.today())
    categorie: str
    tags: List[str]

# Base de données temporaire en mémoire
db_articles = []

@app.post("/api/articles", status_code=201)
def creer_article(article: Article):
    article.id = len(db_articles) + 1
    db_articles.append(article)
    return {"message": "Article créé avec succès", "id": article.id}

@app.get("/api/articles", response_model=List[Article])
def lire_articles():
    return db_articles

@app.get("/api/articles/{id}", response_model=Article)
def lire_un_article(id: int):
    for art in db_articles:
        if art.id == id:
            return art
    raise HTTPException(status_code=404, detail="Article non trouvé")

@app.put("/api/articles/{id}")
def modifier_article(id: int, article_update: Article):
    for i, art in enumerate(db_articles):
        if art.id == id:
            article_update.id = id
            db_articles[i] = article_update
            return {"message": "Article mis à jour"}
    raise HTTPException(status_code=404, detail="Article non trouvé")

@app.delete("/api/articles/{id}")
def supprimer_article(id: int):
    for i, art in enumerate(db_articles):
        if art.id == id:
            db_articles.pop(i)
            return {"message": "Article supprimé"}
    raise HTTPException(status_code=404, detail="Article non trouvé")
