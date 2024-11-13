import { useNavigate } from "react-router-dom";

export const Error = () => {
  // console.log('render error');
  
  const navigate = useNavigate();
  return (
    <div className="error">
      <h1 className="text-6xl font-bold text-gray-800 dark:text-white-chocolate">404</h1>
      <p className="text-2xl text-gray-600 dark:text-white">Oops! Page not found.</p>
      {/* <Link to="/" className="button button-green">
            Go Home
          </Link> */}
      <button onClick={() => { navigate(-1) }} className="button button-green">
        Go Back
      </button>
    </div>
  );
}