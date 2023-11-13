import axios from "../../axios";
import React, {useEffect, useState} from "react";
import CategoryBarChart from "./CategoryBarChart";
import MultipleLineChart from "./MultipleLineChart";
import HorizontalBarChart from "./HorizontalBarChart";
import PieChart from "./PieChart";
import Card from "@mui/material/Card";
import {Button, CardActionArea, CardActions, Grid, ListItemIcon} from "@mui/material";
import CardContent from "@mui/material/CardContent";
import {BackendApi} from "../../backendApi";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import {Settings} from "@mui/icons-material";
import IconButton from "@mui/material/IconButton";
import DeleteIcon from "@mui/icons-material/Delete";

export default function Chart(props: any) {
    let [chartData, setChartData] = useState([]);
    const [gridSize, setGridSize] = useState(6);
    const [zoom, isZoomed] = useState(false)
    let [chartClass, setChartClass] = useState("chart")
    const enlarge = () => {
        if (zoom) {
            setGridSize(6)
            setChartClass("chart")
            isZoomed(false)
        }

        else {
            setGridSize(12)
            setChartClass("max")
            isZoomed(true)

        }
    }

    useEffect(()=>{
        BackendApi.filterApply(props.columnId).then(response=>{
            setChartData(response.data.data.data);
        })
    }, [])
    return (<Grid item xs={gridSize}>
        <Card style={{backgroundColor: "#3B3B3B"}}>
            <CardActionArea>
                <CardContent>
                    {props.chartType === 'CategoryBarChart' ?
                        (<CategoryBarChart chartID={props.chartID}
                                           chartData={chartData}
                                           class={chartClass}></CategoryBarChart>) : null}
                    {props.chartType === 'MultipleLineChart' ?
                        (<MultipleLineChart chartID={props.chartID}
                                            chartData={chartData}
                                            class={chartClass}></MultipleLineChart>) : null}
                    {props.chartType === 'HorizontalBarChart' ?
                        (<HorizontalBarChart chartID={props.chartID}
                                             chartData={chartData}
                                             class={chartClass}>

                        </HorizontalBarChart>) : null}
                    {props.chartType === 'PieChart' ?
                        (<PieChart chartID={props.chartID}
                                   chartData={chartData}></PieChart>) : null}
                </CardContent>
            </CardActionArea>
            <CardActions>
                <React.Fragment>
                    <Button size="small" color="primary" onClick={enlarge}>
                        Zoom
                    </Button>
                    <IconButton>
                        <DeleteIcon style={{color: "white"}}></DeleteIcon>
                    </IconButton>
                    {/*<Menu anchorEl={anchorEl}*/}
                    {/*    id="account-menu"*/}
                    {/*    open={open}*/}
                    {/*    onClose={handleClose}*/}
                    {/*    onClick={handleClose}*/}
                    {/*    PaperProps={{*/}
                    {/*        elevation: 0,*/}
                    {/*        sx: {*/}
                    {/*            overflow: 'visible',*/}
                    {/*            filter: 'drop-shadow(0px 2px 8px rgba(0,0,0,0.32))',*/}
                    {/*            mt: 1.5,*/}
                    {/*            backgroundColor: '#3B3B3B',*/}
                    {/*            '& .MuiAvatar-root': {*/}
                    {/*                width: 32,*/}
                    {/*                height: 32,*/}
                    {/*                ml: -0.5,*/}
                    {/*                mr: 1,*/}
                    {/*                backgroundColor: '#3B3B3B'*/}
                    {/*            },*/}
                    {/*            '&:before': {*/}
                    {/*                content: '""',*/}
                    {/*                display: 'block',*/}
                    {/*                position: 'absolute',*/}
                    {/*                top: 0,*/}
                    {/*                right: 14,*/}
                    {/*                width: 10,*/}
                    {/*                height: 10,*/}
                    {/*                backgroundColor: '#3B3B3B',*/}
                    {/*                transform: 'translateY(-50%) rotate(45deg)',*/}
                    {/*                zIndex: 0,*/}
                    {/*            },*/}
                    {/*        },*/}
                    {/*    }}*/}
                    {/*    transformOrigin={{ horizontal: 'right', vertical: 'top' }}*/}
                    {/*    anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}*/}
                    {/*>*/}
                    {/*    <MenuItem onClick={handleClose} id={config.chartType}>*/}
                    {/*        <ListItemIcon>*/}
                    {/*            <Settings fontSize="small"/>*/}
                    {/*        </ListItemIcon>*/}
                    {/*        <p style={{color: "#FFFFFF"}}>Change to Category Bar chart </p>*/}
                    {/*    </MenuItem>*/}
                    {/*    <MenuItem onClick={handleClose}>*/}
                    {/*        <ListItemIcon>*/}
                    {/*            <Settings fontSize="small" />*/}
                    {/*        </ListItemIcon>*/}
                    {/*        Change to Horizontal Bar chart*/}
                    {/*    </MenuItem>*/}
                    {/*    <MenuItem onClick={handleClose}>*/}
                    {/*        <ListItemIcon>*/}
                    {/*            <Settings fontSize="small" />*/}
                    {/*        </ListItemIcon>*/}
                    {/*        Change to Multiple Line chart*/}
                    {/*    </MenuItem>*/}
                    {/*    <MenuItem onClick={handleClose}>*/}
                    {/*        <ListItemIcon>*/}
                    {/*            <Settings fontSize="small" />*/}
                    {/*        </ListItemIcon>*/}
                    {/*        Change to Pie chart*/}
                    {/*    </MenuItem>*/}
                    {/*</Menu>*/}
                </React.Fragment>
            </CardActions>
        </Card>
    </Grid>)
}