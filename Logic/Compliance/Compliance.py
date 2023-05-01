from typing import List

from Logic.Structure.Session import Session

class Compliance:
    def __init__(self) -> None:
      

        self.sessions_holder: List[Session] = []
    
    def AddSession(self, session: Session):
        self.sessions_holder.append(session)