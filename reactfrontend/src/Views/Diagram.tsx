import React from "react";
import "../Diagram.css";
import Cockpit from "./Cockpit";
import {Route, Routes} from "react-router-dom";

export default function Diagram (){
    return(
        <div>
            <Routes>
                <Route index element={<Cockpit/>}/>
            </Routes>
        </div>
    );
}