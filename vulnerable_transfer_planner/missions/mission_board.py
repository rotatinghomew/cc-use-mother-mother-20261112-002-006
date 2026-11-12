from __future__ import annotations
from typing import Any
from vulnerable_transfer_planner.households.runtime import RunState, SQLiteLedger, fingerprint, number, sequence

class MissionBoard:
    artifact_key = 'mission_board'

    def execute(self, state: RunState, stages: list[Any], ledger: SQLiteLedger) -> None:
        risk_stages, assignment_stages, verification_stages = stages[:3], stages[3:5], stages[5:]
        board = {"risk": [], "assignments": [], "verification": []}
        for lane, selected in (("risk", risk_stages), ("assignments", assignment_stages), ("verification", verification_stages)):
            for stage in selected:
                stage.apply(state)
                board[lane].append({"stage": stage.name, "score": state.artifacts[stage.name]["score"]})
                ledger.save(state)
        risk = number(state.payload.get("attributes", {}).get("risk_score"))
        priority = "immediate" if risk >= 80 else "urgent" if risk >= 60 else "scheduled"
        state.artifacts[self.artifact_key] = {"lanes": board, "priority": priority, "escort_slots": max(1, int(number(state.payload.get("count"), 1) / 2)), "signature": fingerprint(board)}
        state.emit(self.artifact_key, "mission_board_completed", priority=priority)
