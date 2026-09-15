import { lazy, Suspense, useEffect, useState } from "react";
import { Navbar } from "./components/layout/Navbar";
import { Hero } from "./components/layout/Hero";
import { Footer } from "./components/layout/Footer";
import { MatchSelector } from "./components/match/MatchSelector";
import { PredictionBox } from "./components/results/PredictionBox";
import { ProbabilityBar } from "./components/results/ProbabilityBar";
import { StatCards } from "./components/results/StatCards";
import { ComparisonTable } from "./components/results/ComparisonTable";
import { RecentForm } from "./components/results/RecentForm";
import { ResultsDetail } from "./components/results/ResultsDetail";

// Recharts is the single heaviest dependency in the bundle (~150kB gzipped)
// and is only ever needed once a prediction has actually run — split it out
// of the initial bundle instead of paying for it on first paint.
const RadarProfile = lazy(() =>
  import("./components/results/RadarProfile").then((m) => ({ default: m.RadarProfile })),
);
const GoalsEvolution = lazy(() =>
  import("./components/results/GoalsEvolution").then((m) => ({ default: m.GoalsEvolution })),
);
import { SectionTitle } from "./components/ui/SectionTitle";
import { Alert } from "./components/ui/Alert";
import { Spinner } from "./components/ui/Spinner";
import { useTeams } from "./hooks/useTeams";
import { usePrediction } from "./hooks/usePrediction";

function App() {
  const { teams, loading: teamsLoading, error: teamsError } = useTeams();
  const { status, error, result, homeStats, awayStats, predict } = usePrediction();

  const [homeTeam, setHomeTeam] = useState("");
  const [awayTeam, setAwayTeam] = useState("");
  const [neutral, setNeutral] = useState(false);

  // Seed the two selects once the team list arrives, defaulting to
  // France/Brazil when available (matches the previous app's defaults).
  useEffect(() => {
    if (teams.length === 0 || homeTeam) return;
    setHomeTeam(teams.includes("France") ? "France" : teams[0]);
    setAwayTeam(teams.includes("Brazil") ? "Brazil" : (teams[1] ?? teams[0]));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [teams]);

  const probs = result?.probabilities ?? {};

  return (
    <div className="mx-auto max-w-[960px] px-4 pb-16 sm:px-6">
      <Navbar />
      <Hero />

      {teamsLoading && (
        <Spinner label="Le serveur IA se réveille... (Cela peut prendre jusqu'à 2 minutes au premier lancement)" />
      )}
      {teamsError && <Alert variant="error">{teamsError}</Alert>}

      {!teamsLoading && !teamsError && homeTeam && awayTeam && (
        <>
          <MatchSelector
            teams={teams}
            homeTeam={homeTeam}
            awayTeam={awayTeam}
            neutral={neutral}
            loading={status === "loading"}
            onHomeChange={setHomeTeam}
            onAwayChange={setAwayTeam}
            onNeutralChange={setNeutral}
            onSubmit={() => predict(homeTeam, awayTeam, neutral)}
          />

          {status === "loading" && (
            <Spinner label="Analyse en cours... (le premier appel peut prendre jusqu'à 2 minutes)" />
          )}
          {status === "error" && error && (
            <div className="mt-6">
              <Alert variant="error">{error}</Alert>
            </div>
          )}

          {status === "success" && result && homeStats && awayStats && (
            <>
              <PredictionBox result={result} />
              <ProbabilityBar
                homeTeam={homeTeam}
                awayTeam={awayTeam}
                pHome={probs["Domicile"] ?? 0}
                pDraw={probs["Nul"] ?? 0}
                pAway={probs["Extérieur"] ?? 0}
              />
              <StatCards
                homeStats={homeStats}
                awayStats={awayStats}
                homeTeam={homeTeam}
                awayTeam={awayTeam}
              />

              <ResultsDetail>
                <div>
                  <SectionTitle>Comparaison directe</SectionTitle>
                  <ComparisonTable
                    homeStats={homeStats}
                    awayStats={awayStats}
                    homeTeam={homeTeam}
                    awayTeam={awayTeam}
                  />
                </div>
                <div>
                  <SectionTitle>Profil comparatif</SectionTitle>
                  <Suspense fallback={<Spinner label="Chargement du graphique…" />}>
                    <RadarProfile
                      homeStats={homeStats}
                      awayStats={awayStats}
                      homeTeam={homeTeam}
                      awayTeam={awayTeam}
                    />
                  </Suspense>
                </div>
                <div>
                  <SectionTitle>Forme récente (5 derniers matchs)</SectionTitle>
                  <RecentForm
                    homeTeam={homeTeam}
                    awayTeam={awayTeam}
                    homeStats={homeStats}
                    awayStats={awayStats}
                  />
                </div>
                <div>
                  <SectionTitle>Évolution des buts (10 derniers matchs)</SectionTitle>
                  <Suspense fallback={<Spinner label="Chargement du graphique…" />}>
                    <GoalsEvolution
                      homeStats={homeStats}
                      awayStats={awayStats}
                      homeTeam={homeTeam}
                      awayTeam={awayTeam}
                    />
                  </Suspense>
                </div>
              </ResultsDetail>
            </>
          )}
        </>
      )}

      <Footer />
    </div>
  );
}

export default App;
