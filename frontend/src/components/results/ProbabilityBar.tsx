interface ProbabilityBarProps {
  homeTeam: string;
  awayTeam: string;
  pHome: number;
  pDraw: number;
  pAway: number;
}

export function ProbabilityBar({ homeTeam, awayTeam, pHome, pDraw, pAway }: ProbabilityBarProps) {
  return (
    <div
      className="mt-6 flex h-14 gap-0.5 overflow-hidden rounded-xl"
      role="img"
      aria-label={`Probabilités : ${homeTeam} ${pHome}%, Nul ${pDraw}%, ${awayTeam} ${pAway}%`}
    >
      <div
        className="flex flex-col items-center justify-center gap-0.5 overflow-hidden rounded-l-lg bg-[var(--color-blue)] px-1 font-mono text-white"
        style={{ flex: pHome || 0.001 }}
      >
        <span className="text-base font-bold">{pHome}%</span>
        <small className="max-w-[90%] overflow-hidden font-sans text-[0.65rem] font-medium text-ellipsis whitespace-nowrap opacity-90">
          {homeTeam}
        </small>
      </div>
      <div
        className="flex flex-col items-center justify-center gap-0.5 overflow-hidden bg-[var(--color-gold)] px-1 font-mono text-[#1e293b]"
        style={{ flex: pDraw || 0.001 }}
      >
        <span className="text-base font-bold">{pDraw}%</span>
        <small className="max-w-[90%] overflow-hidden font-sans text-[0.65rem] font-medium text-ellipsis whitespace-nowrap opacity-90">
          Nul
        </small>
      </div>
      <div
        className="flex flex-col items-center justify-center gap-0.5 overflow-hidden rounded-r-lg bg-[var(--color-green)] px-1 font-mono text-white"
        style={{ flex: pAway || 0.001 }}
      >
        <span className="text-base font-bold">{pAway}%</span>
        <small className="max-w-[90%] overflow-hidden font-sans text-[0.65rem] font-medium text-ellipsis whitespace-nowrap opacity-90">
          {awayTeam}
        </small>
      </div>
    </div>
  );
}
