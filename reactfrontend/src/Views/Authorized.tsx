import React, {CSSProperties, useContext, useEffect, useState} from "react";
import {BackendApi} from "../backendApi";
import axios from "../axios";
import {Navigate, Outlet, OutletProps, Route, Routes, useNavigate} from "react-router-dom";
import TopBar from "../Components/TopBar";
import {UserContext, UserDispatchContext} from "../UserContext";
import ClipLoader from "react-spinners/ClipLoader";
import {User} from "../types";

const tabs=[
    {title: "Filter Editor", active: true, path: '/filter', isDisabled: false},
    {title: "Graphs", active: false, path: '/diagram', isDisabled: false},
    {title: "Logs", active: false, path: '/log', isDisabled: false},
    {title: "Data Manager", active: false, path: '/upload', isDisabled: false},
];

const spinnerOverride: CSSProperties = {
    height: "100px",
    width: "100px",
    borderColor: "#87CEFA",
};

export default function Authorized(props:any){
    const user=useContext(UserContext)
    const updateUser=useContext(UserDispatchContext)
    const navigate = useNavigate();
    const [loading, setLoading] = React.useState(false);
    const [topBarTabs, setTopBarTabs] = React.useState(tabs);

    useEffect(() => {
        let localUser:User|null= null;
        const localAsync=async ()=>{
            await BackendApi.refresh().then(response => {
                localStorage.setItem('access', response.data.access)
            }).catch((e:any) => {
                localStorage.clear();
            })
            await BackendApi.getUser().then(response=>{
                localUser = response.data;
            }).catch(e=>{
                localStorage.clear();
            })

            let filteredTabs=tabs.filter(tab=>{
                if (tab.title === "Data Manager"&&localUser!==null) {
                    return localUser['isDataOwner'] || localUser['isAdmin'] || localUser['isDataAnalyst']
                }
                if (tab.title === "Graphs"&&localUser!==null) {
                    return localUser['isDataOwner']||localUser['isSimulationEngineer'] || localUser['isDataAnalyst']
                }
                if (tab.title === "Logs"&&localUser!==null) {
                    return localUser['isAdmin']
                }
                if (tab.title === "Filter Editor"&&localUser!==null) {
                    return localUser['isSimulationEngineer']
                }
                return false;
            })
            setTopBarTabs(filteredTabs)
            setLoading(false);
            updateUser(localUser);
            if (localUser) {
                navigate(filteredTabs[0].path);
            }else{
                navigate('/login')
            }
        }
        setLoading(true);
        localAsync();
        // User Tabs setzen, sobald sich user roles ändern
        // if Abfrage nötig, da useEffect sonst sofort ausgeführt wird
    },[])
    if (loading) {
        return(<div className="spinnerDiv">
            <ClipLoader className="spinner"
                        loading={loading}
                        cssOverride={spinnerOverride}
                        size={150}
                        aria-label="Loading Spinner"
                        data-testid="loader"
            />
        </div>)
    }else {
        return <div>
            {/*@ts-ignore*/}
            <TopBar username={user?user.username:''} tabs={topBarTabs}></TopBar>
            <Outlet/>
        </div>;
    }

}