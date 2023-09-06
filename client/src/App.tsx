import { Routes, Route } from 'react-router-dom';

import { GameProvider } from './utils/GameContext';
import Landing from './components/Landing';
import Game from './components/Game';

function App() {
  return (
    <GameProvider>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/game" element={<Game />} />
      </Routes>
    </GameProvider>
  );
}

export default App;
