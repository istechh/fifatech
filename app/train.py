import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, log_loss, classification_report
import pickle
import os
import warnings

warnings.filterwarnings("ignore")

DATA_DIR = os.path.join(os.path.dirname(__file__), "..")
MODEL_DIR = os.path.join(os.path.dirname(__file__), "..")

FEATURES_NUM = [
    "home_rank", "away_rank", "home_points", "away_points",
    "home_avg_scored", "home_avg_conceded", "home_avg_outcome", "home_avg_gdiff",
    "away_avg_scored", "away_avg_conceded", "away_avg_outcome", "away_avg_gdiff",
]
FEATURES_CAT = ["neutral"]


def compute_team_form(results_df: pd.DataFrame, window: int = 10) -> pd.DataFrame:
    results_df = results_df.dropna(subset=["home_score", "away_score"]).copy()
    results_df["date"] = pd.to_datetime(results_df["date"])
    results_df = results_df.sort_values("date").reset_index(drop=True)
    results_df["goal_difference"] = results_df["home_score"] - results_df["away_score"]
    results_df["match_outcome"] = results_df["goal_difference"].apply(
        lambda x: 1 if x > 0 else (-1 if x < 0 else 0)
    )

    home_side = results_df[["date", "home_team", "home_score", "away_score", "match_outcome"]].rename(
        columns={"home_team": "team", "home_score": "goals_for", "away_score": "goals_against", "match_outcome": "outcome"}
    )
    away_side = results_df[["date", "away_team", "away_score", "home_score", "match_outcome"]].rename(
        columns={"away_team": "team", "away_score": "goals_for", "home_score": "goals_against"}
    )
    away_side["outcome"] = -results_df["match_outcome"]

    all_games = pd.concat([home_side, away_side]).sort_values(["team", "date"]).reset_index(drop=True)

    all_games["avg_goals_scored"] = all_games.groupby("team")["goals_for"].transform(
        lambda x: x.shift(1).rolling(window, min_periods=1).mean()
    )
    all_games["avg_goals_conceded"] = all_games.groupby("team")["goals_against"].transform(
        lambda x: x.shift(1).rolling(window, min_periods=1).mean()
    )
    all_games["avg_outcome"] = all_games.groupby("team")["outcome"].transform(
        lambda x: x.shift(1).rolling(window, min_periods=1).mean()
    )
    all_games["avg_goal_diff"] = (
        all_games.groupby("team")
        .apply(lambda x: (x["goals_for"] - x["goals_against"]).shift(1).rolling(window, min_periods=1).mean())
        .reset_index(level=0, drop=True)
    )

    return all_games


def build_dataset(
    fifa_ranking_path: str, results_path: str
) -> tuple[pd.DataFrame, pd.DataFrame, ColumnTransformer, GradientBoostingClassifier, dict]:
    fifa_ranking_df = pd.read_csv(fifa_ranking_path)
    results_df = pd.read_csv(results_path)

    all_games = compute_team_form(results_df)

    team_stats_home = all_games[["date", "team", "avg_goals_scored", "avg_goals_conceded", "avg_outcome", "avg_goal_diff"]].rename(
        columns={
            "team": "home_team",
            "avg_goals_scored": "home_avg_scored",
            "avg_goals_conceded": "home_avg_conceded",
            "avg_outcome": "home_avg_outcome",
            "avg_goal_diff": "home_avg_gdiff",
        }
    )
    team_stats_away = all_games[["date", "team", "avg_goals_scored", "avg_goals_conceded", "avg_outcome", "avg_goal_diff"]].rename(
        columns={
            "team": "away_team",
            "avg_goals_scored": "away_avg_scored",
            "avg_goals_conceded": "away_avg_conceded",
            "avg_outcome": "away_avg_outcome",
            "avg_goal_diff": "away_avg_gdiff",
        }
    )

    results_df["date"] = pd.to_datetime(results_df["date"])
    results_df = results_df.sort_values("date").reset_index(drop=True)
    results_df["goal_difference"] = results_df["home_score"] - results_df["away_score"]
    results_df["match_outcome"] = results_df["goal_difference"].apply(
        lambda x: 1 if x > 0 else (-1 if x < 0 else 0)
    )

    results_df = pd.merge_asof(
        results_df.sort_values("date"), team_stats_home.sort_values("date"), on="date", by="home_team", direction="backward"
    )
    results_df = pd.merge_asof(
        results_df.sort_values("date"), team_stats_away.sort_values("date"), on="date", by="away_team", direction="backward"
    )

    fifa_ranking_df.dropna(subset=["rank"], inplace=True)
    fifa_ranking_df["rank_date"] = pd.to_datetime(fifa_ranking_df["rank_date"])
    fifa_ranking_df = fifa_ranking_df.sort_values("rank_date")

    fifa_home = fifa_ranking_df[["rank_date", "country_full", "rank", "total_points"]].rename(
        columns={"country_full": "home_team", "rank": "home_rank", "total_points": "home_points"}
    )
    fifa_away = fifa_ranking_df[["rank_date", "country_full", "rank", "total_points"]].rename(
        columns={"country_full": "away_team", "rank": "away_rank", "total_points": "away_points"}
    )

    merged_df = pd.merge_asof(
        results_df.sort_values("date"),
        fifa_home.sort_values("rank_date"),
        left_on="date",
        right_on="rank_date",
        by="home_team",
        direction="backward",
    ).drop(columns=["rank_date"])
    merged_df = pd.merge_asof(
        merged_df.sort_values("date"),
        fifa_away.sort_values("rank_date"),
        left_on="date",
        right_on="rank_date",
        by="away_team",
        direction="backward",
    ).drop(columns=["rank_date"])

    merged_df["match_outcome"] = merged_df["match_outcome"].replace({1: 0, 0: 1, -1: 2})
    merged_df.dropna(subset=["home_rank", "away_rank"], inplace=True)
    merged_df.fillna(0, inplace=True)

    X = merged_df[FEATURES_NUM + FEATURES_CAT]
    y = merged_df["match_outcome"].astype(int)

    cutoff = int(len(X) * 0.8)
    X_train, X_test = X.iloc[:cutoff], X.iloc[cutoff:]
    y_train, y_test = y.iloc[:cutoff], y.iloc[cutoff:]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), FEATURES_NUM),
            ("cat", OneHotEncoder(handle_unknown="ignore"), FEATURES_CAT),
        ]
    )

    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)

    gbc_model = GradientBoostingClassifier(
        n_estimators=100, learning_rate=0.05, max_depth=5, random_state=42
    )
    gbc_model.fit(X_train_processed, y_train)

    preds = gbc_model.predict(X_test_processed)
    probas = gbc_model.predict_proba(X_test_processed)

    print(f"--- RÉSULTATS ---")
    print(f"Accuracy : {accuracy_score(y_test, preds):.4f}")
    print(f"Log-loss : {log_loss(y_test, probas):.4f}\n")
    print(classification_report(y_test, preds, target_names=["Domicile", "Nul", "Extérieur"]))

    latest_rankings = (
        fifa_ranking_df.sort_values("rank_date")
        .groupby("country_full")
        .last()
        .reset_index()[["country_full", "rank", "total_points"]]
    )

    metadata = {
        "teams": sorted(all_games["team"].unique().tolist()),
        "rankings": latest_rankings.to_dict(orient="records"),
    }

    return merged_df, all_games, preprocessor, gbc_model, metadata


def train_and_save(
    fifa_ranking_path: str = None,
    results_path: str = None,
    output_dir: str = None,
):
    if fifa_ranking_path is None:
        fifa_ranking_path = os.path.join(DATA_DIR, "fifa_ranking-2024-06-20.csv")
    if results_path is None:
        results_path = os.path.join(DATA_DIR, "results.csv")
    if output_dir is None:
        output_dir = MODEL_DIR

    print("Entraînement du modèle en cours...")
    merged_df, all_games, preprocessor, model, metadata = build_dataset(fifa_ranking_path, results_path)

    os.makedirs(output_dir, exist_ok=True)

    with open(os.path.join(output_dir, "best_model.pkl"), "wb") as f:
        pickle.dump(model, f)
    with open(os.path.join(output_dir, "preprocessor.pkl"), "wb") as f:
        pickle.dump(preprocessor, f)
    with open(os.path.join(output_dir, "metadata.pkl"), "wb") as f:
        pickle.dump(metadata, f)
    with open(os.path.join(output_dir, "all_games.pkl"), "wb") as f:
        pickle.dump(all_games, f)

    print(f"Modèle sauvegardé dans {output_dir}")
    return model, preprocessor, metadata, all_games


def load_artifacts(output_dir: str = None):
    if output_dir is None:
        output_dir = MODEL_DIR
    with open(os.path.join(output_dir, "best_model.pkl"), "rb") as f:
        model = pickle.load(f)
    with open(os.path.join(output_dir, "preprocessor.pkl"), "rb") as f:
        preprocessor = pickle.load(f)
    with open(os.path.join(output_dir, "metadata.pkl"), "rb") as f:
        metadata = pickle.load(f)
    with open(os.path.join(output_dir, "all_games.pkl"), "rb") as f:
        all_games = pickle.load(f)
    return model, preprocessor, metadata, all_games


if __name__ == "__main__":
    train_and_save()
