import "./App.css"
import { createBrowserRouter, Navigate, Outlet, RouteObject, RouterProvider } from 'react-router-dom';
import { CompanyComponent } from './components/company/CompanyComponent.tsx';
import { TaskComponent } from './components/tasks/TaskComponent.tsx';
import { UserComponent } from './components/user/UserComponent.tsx';
import { Header } from './components/commons/Header.tsx';
import { Error } from './components/commons/Error.tsx';
import Footer from './components/commons/Footer.tsx';
import { LoginComponent } from "./components/auth/LoginComponent.tsx";
import { TaskDetailComponent } from "./components/tasks/TaskDetailComponent.tsx";
import CreateTaskComponent from "./components/tasks/CreateTaskComponent.tsx";

const children: RouteObject[] = [
    {
        path: "/",
        element: <Home />
    },
    {
        path: "/users",
        element: <UserComponent />,
    },
    {
        path: "/tasks",
        element: <TaskComponent />,
    },
    {
        path: "/tasks/create",
        element: <CreateTaskComponent />,
    },
    {
        path: "/tasks/:id",
        element: <TaskDetailComponent />
    },
    {
        path: "/companies",
        element: <CompanyComponent />,
    },
    {
        path: "/login",
        element: <LoginComponent />,
    },
    {
        path: "/*",
        element: <Error />
    }
]
const router = createBrowserRouter([
    {
        element: <Layout />,
        children: children
    },
]);

export default function App() {
    return <RouterProvider router={router} />;
}
function Layout() {
    return (
        <>
            <Header></Header>
            <div className="flex justify-center">
                <div className="basis-auto w-full max-w-full p-2 overflow-auto">
                    <Outlet />
                </div>
            </div>
            <Footer></Footer>
        </>
    );
}

function Home() {
    return <Navigate to={"/login"} />
}
