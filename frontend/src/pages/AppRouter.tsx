import {useContext} from 'react';
import {Route, Routes} from "react-router-dom";
import {AuthContext} from "../context";
import Main from "./Main.tsx";
import Auth from "./Auth.tsx";
import SignUp from "./SignUp.tsx";
import Profile from "./Profile.tsx";
import Error404 from "./Error404.tsx";


const AppRouter = () => {
    const {isAuthenticated} = useContext(AuthContext);

    return (
        <Routes>
            {isAuthenticated && (
                <Route path="/profile" element={<Profile />} />
            )}
            <Route path="/" element={<Main />} />
            <Route path="/auth" element={<Auth />} />
            <Route path="/sign-up" element={<SignUp />} />
            <Route path="*" element={<Error404 />} />
        </Routes>
    );
};

export default AppRouter;