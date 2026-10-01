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
