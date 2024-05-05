import {BrowserRouter, Route, Routes} from "react-router-dom";
import Error404 from "./pages/Error404.tsx";
import Main from "./pages/Main.tsx";
import Auth from "./pages/Auth.tsx";
import SignUp from "./pages/SignUp.tsx";


function App() {

  return (
    <>
      <BrowserRouter>
        <Routes>
            <Route path="/" element={<Main />} />
            <Route path="/auth" element={<Auth />} />
            <Route path="/sign-up" element={<SignUp />} />
            <Route path="*" element={<Error404 />} />
        </Routes>
      </BrowserRouter>
    </>
  )
}

export default App
