import {BrowserRouter} from "react-router-dom";
import {useEffect, useState} from "react";
import {AuthContext} from "./context";
import AppRouter from "./pages/AppRouter.tsx";


function App() {
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    useEffect(() => {
        const checkAuthentication = async () => {
            const access_token = localStorage.getItem('access_token') || '';
            const formData = { access_token };

            try {
                const response = await fetch('http://127.0.0.1:8000/auth/check-auth/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });
                if (response.ok) {
                    console.log(response)
                    setIsAuthenticated(true);
                }
            } catch (error) {
                console.error(error);
            }
        };
        checkAuthentication();
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
