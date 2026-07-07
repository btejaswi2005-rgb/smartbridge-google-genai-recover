const STAGES = ["Severe", "High", "Moderate", "Low"];

// "Severe" stress = early in the recovery journey (0 filled steps),
// "Low" stress = furthest along the path (fully filled).
export default function RecoveryPath({ stressLevel }) {
  const currentIndex = STAGES.indexOf(stressLevel);
  const filledCount = currentIndex >= 0 ? currentIndex + 1 : 0;

  return (
    <div>
      <div className="recovery-labels">
        <span>Distressed</span>
        <span>Recovering</span>
        <span>Stable</span>
      </div>
      <div className="recovery-path">
        {STAGES.map((stage, i) => (
          <div
            key={stage}
            className={`recovery-step ${i < filledCount ? "filled" : ""}`}
            title={stage}
          />
        ))}
      </div>
    </div>
  );
}
