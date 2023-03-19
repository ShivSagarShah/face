import './App.css';
import UserForm from './components/UserForm/UserForm';
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

const router = createBrowserRouter([
  {
    path: "/login",
    element: <UserForm form="Login"/>,
  },
  {
    path: "/signup",
    element: <UserForm form="Signup"/>,
  },
]);

function App() {
  return (
    <div className="App">
      <RouterProvider router={router}/>
    </div>
  );
}

export default App;
