import React, {CSSProperties, useContext, useEffect, useReducer, useState} from 'react';
// import logo from './logo.svg';
import './App.css';
import './Components/NavTabs'
import LogIn from './Views/LogIn'
import Filter from './Views/FilterEditor/Filter'
import Diagram from './Views/Diagram'
import Log from "./Views/Log"
import {tabData} from "./types";
// import {AppBar} from "@mui/material";
import {Navigate, Route, Routes, useNavigate} from "react-router-dom";
import Button from '@mui/material/Button';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import axios from "./axios";
import {roles, loginUserRequest} from "./RequestTypes";
import TopBar from "./Components/TopBar";
import ClipLoader from "react-spinners/ClipLoader";
import {BackendApi} from "./backendApi";
import Authorized from "./Views/Authorized";
import {UserContext, UserContextProvider, UserDispatchContext, userReducer} from "./UserContext";
import Upload from "./Components/Upload/Upload";
import DataManager from "./Components/Upload/DataManager";

function App() {
    const user = useContext(UserContext)
    const updateUser = useContext(UserDispatchContext);
    const [FilterList, setFilterList] = React.useState("");
    const [loading, setLoading] = React.useState(false);
    const [userTabs, setUserTabs] = React.useState<tabData[]>([]);

    const navigate = useNavigate();
    useEffect(()=>{

    },[])

    const handleButton = (event: any) => {
        if (event.currentTarget.name == "clear") {
            setFilterList("")}
        else {
            setFilterList(event.currentTarget.value + " " + event.currentTarget.name)
        }
    };


    return (
        <div className="App">
            <div>
                <img className={"logoBar"} src={"/easy_analytics.png"}/>

            </div>
            <Routes>
                <Route path="/" element={<Authorized></Authorized>}>
                    <Route path="/filter" element={<Filter/>}/>
                    <Route path="/diagram" element={<Diagram/>}/>
                    <Route path="/log" element={<Log/>}/>
                    <Route path="/upload" element={<DataManager setLoading={setLoading}/>}/>
                </Route>
                <Route path="/login" element={<LogIn/>}/>
            </Routes>
        </div>
    )
}

export default App;
