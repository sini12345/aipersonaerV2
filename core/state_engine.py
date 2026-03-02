from dataclasses import dataclass


@dataclass
class PersonaState:
    trust: int = 35
    stress: int = 60
    shame: int = 50
    hope: int = 40
    control_loss: int = 60
    difficulty: int = 2

    def clamp(self):
        for attr in ["trust", "stress", "shame", "hope", "control_loss"]:
            value = getattr(self, attr)
            setattr(self, attr, max(0, min(100, value)))

    def to_dict(self) -> dict:
        return {
            "trust": self.trust,
            "stress": self.stress,
            "shame": self.shame,
            "hope": self.hope,
            "control_loss": self.control_loss,
            "difficulty": self.difficulty,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    def to_panel_text(self) -> str:
        return (
            f"Trust: {self.trust}\n"
            f"Stress: {self.stress}\n"
            f"Skam: {self.shame}\n"
            f"Håb: {self.hope}\n"
            f"Kontroltab: {self.control_loss}"
        )


def update_state_from_turn(state: PersonaState, user_text: str, ai_text: str, learning_goal: str) -> PersonaState:
    s = PersonaState.from_dict(state.to_dict())
    text = user_text.lower()

    validating_words = ["forstår", "giver mening", "hører", "tak", "valgmulighed", "hvad tænker du"]
    pressure_words = ["skal", "burde", "konsekvens", "sanktion", "nu gør du"]

    # Compute deltas first, then cap per turn so state doesn't swing too wildly.
    d_trust = 0
    d_stress = 0
    d_shame = 0
    d_hope = 0
    d_control = 0

    if any(w in text for w in validating_words):
        d_trust += 4
        d_hope += 3
        d_stress -= 3
        d_control -= 3

    if any(w in text for w in pressure_words):
        d_trust -= 5
        d_stress += 5
        d_shame += 3
        d_control += 4

    if learning_goal == "Deeskalering" and "rolig" in text:
        d_stress -= 2
        d_trust += 2

    if learning_goal == "Grænsesætning" and "ramme" in text:
        d_control -= 2

    # Difficulty shifts baseline resistance.
    baseline = max(0, s.difficulty - 2)
    d_stress += baseline
    d_control += baseline

    # Per-turn stability caps (training-friendly, not deterministic evaluation).
    d_trust = max(-6, min(6, d_trust))
    d_stress = max(-8, min(8, d_stress))
    d_shame = max(-6, min(6, d_shame))
    d_hope = max(-6, min(6, d_hope))
    d_control = max(-8, min(8, d_control))

    s.trust += d_trust
    s.stress += d_stress
    s.shame += d_shame
    s.hope += d_hope
    s.control_loss += d_control

    s.clamp()
    return s
