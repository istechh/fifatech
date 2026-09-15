import { clsx } from "clsx";
import { Card } from "../ui/Card";
import type { PredictResponse } from "../../types/api";

interface PredictionBoxProps {
  result: PredictResponse;
}

function resultTone(prediction: string): string {
  if (prediction.includes("Domicile")) return "text-[var(--color-blue)]";
  if (prediction.includes("Nul")) return "text-[var(--color-gold)]";
  return "text-[var(--color-green)]";
}

export function PredictionBox({ result }: PredictionBoxProps) {
  const probs = Object.values(result.probabilities);
  const confidence = probs.length ? Math.max(...probs) : 0;

  return (
    <Card className="mt-6 rounded-3xl px-8 py-10 text-center">
      <p className="mb-3 text-xs font-semibold tracking-[0.15em] text-[var(--text-secondary)] uppercase">
        Résultat prédit
      </p>
      <p
        className={clsx(
          "font-display text-[clamp(2rem,4vw,2.5rem)] font-extrabold",
          resultTone(result.prediction),
        )}
      >
        {result.prediction}
      </p>
      <div className="mx-auto mt-6 max-w-xs">
        <div className="mb-1.5 flex justify-between text-sm text-[var(--text-secondary)]">
          <span>Confiance du modèle</span>
          <span className="font-bold text-[var(--text-primary)]">{confidence}%</span>
        </div>
        <div className="h-2 overflow-hidden rounded-full bg-[var(--bg-primary)]">
          <div
            className="h-full rounded-full bg-[var(--color-blue)]"
            style={{ width: `${confidence}%` }}
            role="progressbar"
            aria-valuenow={confidence}
            aria-valuemin={0}
            aria-valuemax={100}
            aria-label="Confiance du modèle"
          />
        </div>
      </div>
    </Card>
  );
}
