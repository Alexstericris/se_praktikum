import {createBrowserRouter} from "react-router-dom";
import MultipleLineChart from "./Components/Charts/MultipleLineChart";
import CategoryBarChart from "./Components/Charts/CategoryBarChart";

const router = createBrowserRouter([
    {
        path: '/',
        element:<CategoryBarChart></CategoryBarChart>
    },
    {
        path: 'tab2',
        element:<MultipleLineChart></MultipleLineChart>
    }
])
export default router;