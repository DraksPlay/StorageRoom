import {useEffect} from "react";

const Main = () => {

    useEffect(() => {
        fetch(`${import.meta.env.VITE_BACKEND_API_URL}/api/storages/read_categories/`, {
            method: 'GET'
        }).then(response => {
            if (response.ok) {
                console.log(response);
            }
        })
    }, []);

    return (
        <div>

        </div>
    );
};

export default Main;