import { Link, useNavigate } from "react-router-dom";

export const Error = () => {
  const navigate = useNavigate();

    return ( 
        <div className="flex items-center justify-center min-h-screen bg-gray-100">
        <div className="text-center">
          <h1 className="text-6xl font-bold text-gray-800">404</h1>
          <p className="text-2xl text-gray-600">Oops! Page not found.</p>
          {/* <Link to="/" className="mt-4 inline-block px-4 py-2 text-white bg-emerald-400 rounded hover:bg-emerald-600">
            Go Home
          </Link> */}
          <button onClick={()=>{navigate(-1)}} className="mt-4 inline-block px-4 py-2 text-white bg-emerald-400 rounded hover:bg-emerald-600">
            Go Back
          </button>
        </div>
      </div>
    );
}