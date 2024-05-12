import {useState} from "react";
import {useNavigate} from "react-router-dom";


const SignUp = () => {

    const [formData, setFormData] = useState(
        { "email": '', "password": '', "password_repeat": ''}
    );

    const navigate = useNavigate();

    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();
        if (formData.password != formData.password_repeat) {
            return false;
        }

        const {password_repeat, ...newFormData} = formData;

        try {

            const response = await fetch(`${import.meta.env.VITE_BACKEND_API_URL}/api/users/create_user/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(newFormData)
            });

            if (response.ok) {
                const responseData = await response.json();
                localStorage.setItem('access_token', responseData.access_token);
                localStorage.setItem('refresh_token', responseData.refresh_token);
                navigate("/");
            } else {
                console.error('Ошибка при отправке данных');
            }
        } catch (error) {
            console.error('Произошла ошибка:', error);
        }
    };

    const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({
            ...formData,
            [event.target.name]: event.target.value
        });
    };


    return (
        <div className="h-screen flex items-center">
            <form className="max-w-sm mx-auto w-1/3" onSubmit={handleSubmit}>
                <div className="mb-5">
                    <label htmlFor="email" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Your
                        email</label>
                    <input type="email" id="email"
                           className="shadow-sm bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light"
                           placeholder="name@gmail.com"
                           name="email"
                           value={formData.email}
                           onChange={handleChange}
                           required/>
                </div>
                <div className="mb-5">
                    <label htmlFor="password" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Your
                        password</label>
                    <input type="password" id="password"
                           className="shadow-sm bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light"
                           name="password"
                           value={formData.password}
                           onChange={handleChange}
                           required/>
                </div>
                <div className="mb-5">
                    <label htmlFor="repeat-password"
                           className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Repeat
                        password</label>
                    <input type="password" id="repeat-password"
                           name="password_repeat"
                           className="shadow-sm bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light"
                           value={formData.password_repeat}
                           onChange={handleChange}
                           required/>
                </div>
                <div className="flex items-start mb-5">
                    <div className="flex items-center h-5">
                        <input id="terms" type="checkbox" value=""
                               className="w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-blue-300 dark:bg-gray-700 dark:border-gray-600 dark:focus:ring-blue-600 dark:ring-offset-gray-800 dark:focus:ring-offset-gray-800"
                               required/>
                    </div>
                    <label htmlFor="terms" className="ms-2 text-sm font-medium text-gray-900 dark:text-gray-300">I agree
                        with the <a href="#" className="text-blue-600 hover:underline dark:text-blue-500">terms and
                            conditions</a></label>
                </div>
                <button type="submit"
                        className="w-full text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Register
                    new account
                </button>
            </form>
        </div>
    );
};

export default SignUp;