import {BrowserRouter} from "react-router-dom";
import {useEffect, useState} from "react";
import {AuthContext} from "./context";
import AppRouter from "./pages/AppRouter.tsx";


function App() {
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    useEffect(() => {
        const access_token = localStorage.getItem('access_token') || '';
        const formData = { access_token };
        fetch(`${import.meta.env.VITE_BACKEND_API_URL}/auth/check-auth/`, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        }).then(response => {
            if (response.ok) {
                setIsAuthenticated(true);
            }
        })

    }, []);

    return (
        <AuthContext.Provider value={{
            isAuthenticated,
            setIsAuthenticated
        }}>
            <BrowserRouter>
                <AppRouter />
            </BrowserRouter>
      </AuthContext.Provider>
    )
}

export default App
