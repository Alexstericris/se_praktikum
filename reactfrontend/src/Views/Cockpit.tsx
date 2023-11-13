import React, {useEffect, useState} from "react";
import MultipleLineChart from "../Components/Charts/MultipleLineChart";
import {Grid} from "@mui/material";
import '../Cockpit.css';
import Popup from "./popup";
import Chart from "../Components/Charts/Chart";

export default function Cockpit() {
    const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
    const [chartsConfig,setChartsConfig] = useState([])
    const [charts,setCharts] = useState(<div></div>)
    const open = Boolean(anchorEl);
    const handleClose = (event: React.MouseEvent<HTMLElement>) => {
        setAnchorEl(null);
        event.currentTarget.id = 'MultipleLineChart'
    };

    const [openPop, setOpen] = React.useState(false);

    const handleClickOpenPop = () => {
        setOpen(true);
    };

    const handleClosePop = () => {
        setOpen(false);
    };
    const handleOnSubmit=(columnId:any)=>{
        // @ts-ignore
        setChartsConfig([...chartsConfig, {chartType:'MultipleLineChart',columnId:columnId}])
        //@ts-ignore
        setCharts([...chartsConfig, {chartType:'MultipleLineChart',columnId:columnId}].map((config,index) => {
            //@ts-ignore
            return <Chart columnId={config.columnId} chartType={config.chartType} chartID={"chart-" + index} key={"chart-" + index}/>
        }))
        console.log(columnId);
    }
    return <Grid container spacing={5} paddingTop={5} paddingLeft={5} paddingRight={5} paddingBottom={5}>
        {charts}
        <Grid item xs={6} >
            <div style={{margin: "auto", width:"fit-content"}}>
                <Popup handleOnSubmit={handleOnSubmit}></Popup>
            </div>
        </Grid>
     </Grid>
};