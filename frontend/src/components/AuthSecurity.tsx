import { useEffect, useState } from 'react';
import { Navigate, useLocation } from 'react-router-dom';

const AuthSecurity = ({ component: Component, ...rest }: any) => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const location = useLocation();

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
                    console.log(isAuthenticated)
                }
            } catch (error) {
                console.error(error);
            }
        };

        checkAuthentication();
    }, []);
    console.log(isAuthenticated)
    if (!isAuthenticated) {
        return <Navigate to="/auth" state={{ from: location }} replace />;
    }

    return <Component {...rest} />;
};

export default AuthSecurity;