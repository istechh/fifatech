import os
import pickle
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.train import FEATURES_NUM, FEATURES_CAT, train_and_save, load_artifacts

app = FastAPI(title="FIFA Match Predictor API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL = None
PREPROCESSOR = None
METADATA = None
ALL_GAMES = None


class PredictRequest(BaseModel):
    home_team: str
    away_team: str
    neutral: bool = False


class PredictResponse(BaseModel):
    home_team: str
    away_team: str
    neutral: bool
    prediction: str
    probabilities: dict
    home_rank: int | None
    away_rank: int | None
    home_points: float | None
    away_points: float | None


class TeamStats(BaseModel):
    team: str
    rank: int | None
    total_points: float | None
    avg_goals_scored: float | None
    avg_goals_conceded: float | None
    avg_outcome: float | None
    avg_goal_diff: float | None
    recent_matches: list[dict]


@app.on_event("startup")
def load_model():
    global MODEL, PREPROCESSOR, METADATA, ALL_GAMES
    model_path = os.path.join(os.path.dirname(__file__), "..", "best_model.pkl")

    if not os.path.exists(model_path):
        print("Modèle introuvable, entraînement en cours...")
        MODEL, PREPROCESSOR, METADATA, ALL_GAMES = train_and_save()
    else:
        try:
            MODEL, PREPROCESSOR, METADATA, ALL_GAMES = load_artifacts()
            print("Modèle chargé avec succès !")
        except Exception:
            print("Erreur de chargement, réentraînement...")
            MODEL, PREPROCESSOR, METADATA, ALL_GAMES = train_and_save()


@app.get("/")
def root():
    return {"status": "ok", "model_loaded": MODEL is not None}


@app.get("/teams")
def get_teams():
    teams = METADATA.get("teams", [])
    return {"teams": teams, "count": len(teams)}


@app.get("/team_stats/{team}")
def get_team_stats(team: str):
    if team not in METADATA.get("teams", []):
        raise HTTPException(status_code=404, detail=f"Équipe '{team}' introuvable")

    ranking_info = None
    for r in METADATA.get("rankings", []):
        if r["country_full"] == team:
            ranking_info = r
            break

    team_games = ALL_GAMES[ALL_GAMES["team"] == team].copy()
    if team_games.empty:
        raise HTTPException(status_code=404, detail="Pas de données pour cette équipe")

    latest = team_games.sort_values("date").iloc[-1]
    recent = team_games.sort_values("date").tail(10)

    recent_matches = []
    for _, row in recent.iterrows():
        recent_matches.append({
            "date": str(row["date"].date()) if hasattr(row["date"], "date") else str(row["date"]),
            "goals_for": round(float(row["goals_for"]), 1),
            "goals_against": round(float(row["goals_against"]), 1),
            "outcome": "W" if row["outcome"] > 0 else ("D" if row["outcome"] == 0 else "L"),
        })

    return TeamStats(
        team=team,
        rank=int(ranking_info["rank"]) if ranking_info else None,
        total_points=float(ranking_info["total_points"]) if ranking_info else None,
        avg_goals_scored=round(float(latest["avg_goals_scored"]), 2),
        avg_goals_conceded=round(float(latest["avg_goals_conceded"]), 2),
        avg_outcome=round(float(latest["avg_outcome"]), 2),
        avg_goal_diff=round(float(latest["avg_goal_diff"]), 2),
        recent_matches=recent_matches,
    )


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    if req.home_team not in METADATA.get("teams", []):
        raise HTTPException(status_code=404, detail=f"Équipe domicile '{req.home_team}' introuvable")
    if req.away_team not in METADATA.get("teams", []):
        raise HTTPException(status_code=404, detail=f"Équipe extérieur '{req.away_team}' introuvable")

    home_rank = home_points = away_rank = away_points = None
    for r in METADATA.get("rankings", []):
        if r["country_full"] == req.home_team:
            home_rank = r["rank"]
            home_points = r["total_points"]
        if r["country_full"] == req.away_team:
            away_rank = r["rank"]
            away_points = r["total_points"]

    def get_latest_stat(team, col):
        team_data = ALL_GAMES[ALL_GAMES["team"] == team]
        if team_data.empty:
            return 0.0
        return float(team_data.sort_values("date").iloc[-1][col])

    input_data = pd.DataFrame(
        [
            {
                "home_rank": home_rank or 100,
                "away_rank": away_rank or 100,
                "home_points": home_points or 0,
                "away_points": away_points or 0,
                "home_avg_scored": get_latest_stat(req.home_team, "avg_goals_scored"),
                "home_avg_conceded": get_latest_stat(req.home_team, "avg_goals_conceded"),
                "home_avg_outcome": get_latest_stat(req.home_team, "avg_outcome"),
                "home_avg_gdiff": get_latest_stat(req.home_team, "avg_goal_diff"),
                "away_avg_scored": get_latest_stat(req.away_team, "avg_goals_scored"),
                "away_avg_conceded": get_latest_stat(req.away_team, "avg_goals_conceded"),
                "away_avg_outcome": get_latest_stat(req.away_team, "avg_outcome"),
                "away_avg_gdiff": get_latest_stat(req.away_team, "avg_goal_diff"),
                "neutral": req.neutral,
            }
        ]
    )

    X = input_data[FEATURES_NUM + FEATURES_CAT]
    X_processed = PREPROCESSOR.transform(X)

    prediction = int(MODEL.predict(X_processed)[0])
    probas = MODEL.predict_proba(X_processed)[0]

    outcome_map = {0: "Victoire Domicile", 1: "Nul", 2: "Victoire Extérieur"}
    labels = ["Domicile", "Nul", "Extérieur"]

    return PredictResponse(
        home_team=req.home_team,
        away_team=req.away_team,
        neutral=req.neutral,
        prediction=outcome_map[prediction],
        probabilities={labels[i]: round(float(probas[i]) * 100, 1) for i in range(3)},
        home_rank=home_rank,
        away_rank=away_rank,
        home_points=home_points,
        away_points=away_points,
    )
