import {useContext} from "react";
import {AuthContext} from "../context";
import {useNavigate} from "react-router-dom";


const Profile = () => {
    const {setIsAuthenticated} = useContext(AuthContext);

    const navigate = useNavigate();

    const handleLogOut = async () => {
        setIsAuthenticated(false);
        navigate("/auth")
        localStorage.removeItem('access_token');
        localStorage.removeItem("refresh_token");
    }

    return (
        <div>
            Profile
            <button onClick={handleLogOut} type="submit"
                    className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
                Log out
            </button>
        </div>
    );
};

export default Profile;