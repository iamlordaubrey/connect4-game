import { createContext } from "react";

interface PlayerContextType {
  status?: string,
  id: string,
  username: string,
  wins: number,
  losses: number,
}

const PlayerContext = createContext<PlayerContextType|null>(null);
export default PlayerContext;