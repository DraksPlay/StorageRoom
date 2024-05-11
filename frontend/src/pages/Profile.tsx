import {useContext, useEffect} from "react";
import {AuthContext} from "../context";


const Profile = () => {
    const {isAuthenticated} = useContext(AuthContext);

    useEffect(() => {console.log(isAuthenticated)})

    return (
        <div>
            Profile
        </div>
    );
};

export default Profile;