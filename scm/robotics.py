from dataclasses import dataclass,field
from enum import Enum
class RobotSafety(str,Enum): ARMED='armed'; DISARMED='disarmed'; FAULT='fault'
@dataclass(frozen=True)
class RobotCommand:
    command:str
    parameters:dict
    requires_interlock:bool=True
@dataclass
class RobotController:
    controller_id:str
    state:RobotSafety=RobotSafety.DISARMED
    queue:list[RobotCommand]=field(default_factory=list)
    def arm(self): self.state=RobotSafety.ARMED
    def disarm(self): self.state=RobotSafety.DISARMED
    def fault(self): self.state=RobotSafety.FAULT
    def submit(self,command):
        if self.state is not RobotSafety.ARMED: raise RuntimeError('robot controller is not armed')
        self.queue.append(command)


def simulate_transfers(vessels: dict, steps: list) -> dict:
    """Preview a liquid-handling plan using exact integer microliters."""
    if not isinstance(vessels, dict) or not vessels:
        raise ValueError("Provide at least one named vessel.")
    if not isinstance(steps, list) or not steps:
        raise ValueError("Provide at least one transfer.")
    capacities = {}
    volumes = {}
    for name, vessel in vessels.items():
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Vessel names must be nonempty strings.")
        if not isinstance(vessel, dict) or set(vessel) != {"capacity_ul", "volume_ul"}:
            raise ValueError(f"{name} requires capacity_ul and volume_ul.")
        capacity, volume = vessel["capacity_ul"], vessel["volume_ul"]
        if type(capacity) is not int or type(volume) is not int or not 0 <= volume <= capacity or capacity == 0:
            raise ValueError(f"{name} requires integer microliters within capacity.")
        capacities[name] = capacity
        volumes[name] = volume
    initial = volumes.copy()

    trace = []
    for index, step in enumerate(steps, start=1):
        if not isinstance(step, dict) or set(step) != {"source", "destination", "volume_ul"}:
            raise ValueError(f"Step {index} requires source, destination and volume_ul.")
        source, destination, amount = step["source"], step["destination"], step["volume_ul"]
        if not isinstance(source, str) or not isinstance(destination, str):
            raise ValueError(f"Step {index} requires vessel names.")
        if source not in volumes or destination not in volumes or source == destination:
            raise ValueError(f"Step {index} requires two distinct known vessels.")
        if type(amount) is not int or amount <= 0:
            raise ValueError(f"Step {index} requires positive integer microliters.")
        if amount > volumes[source]:
            raise ValueError(f"Step {index} exceeds source volume.")
        if amount > capacities[destination] - volumes[destination]:
            raise ValueError(f"Step {index} exceeds destination capacity.")
        volumes[source] -= amount
        volumes[destination] += amount
        trace.append({
            "step": index, **step,
            "source_remaining_ul": volumes[source],
            "destination_total_ul": volumes[destination],
        })
    return {
        "method": "liquid_transfer_volume_model",
        "status": "simulated",
        "initial_volumes_ul": initial,
        "final_volumes_ul": volumes,
        "capacity_ul": capacities,
        "transfers": trace,
    }
