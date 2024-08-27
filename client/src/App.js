import React from 'react'
import { BrowserRouter, Route, Routes} from 'react-router-dom';

import Test from "./Test.js"
import Landing from "./pages/Landing.tsx"
import Upload from './pages/Upload.tsx';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path = "/" element = {<Landing />}/>
        <Route path = "/upload" element = {<Upload/>}/>
      </Routes>
    </BrowserRouter>
  )
}

export default App