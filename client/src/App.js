import React from 'react'
import { BrowserRouter, Route, Routes} from 'react-router-dom';

import Test from "./Test.js"
import Landing from "./pages/Landing.tsx"

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path = "/" element = {<Landing />}/>
      </Routes>
    </BrowserRouter>
  )
}

export default App