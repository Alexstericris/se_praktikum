import React, {useEffect, useState} from 'react';
import './DataManager.css';
import Upload from './Upload';
import DataTree from "../DataTree";
import {column, getAllFilenamesResponse} from "../../RequestTypes";
import {getAllFilenames} from "../../Services/TreeDataService";
import UploadFileSharpIcon from '@mui/icons-material/UploadFileSharp';
import IconButton from "@mui/material/IconButton";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import {ThemeProvider} from "@mui/material/styles";
import {tabTheme} from "../../globalStyle";
import {Button, Tooltip} from "@mui/material";
import Dialog from "@mui/material/Dialog";
import Paper from '@mui/material/Paper';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import {BackendApi} from "../../backendApi";
import axios from "../../axios";



interface Column {
    id: 'name' | 'code' | 'population' | 'size' | 'density';
    label: string;
    minWidth?: number;
    align?: 'right';
    format?: (value: number) => string;
}


//TODO remove mock-table

interface Column {
    id: 'name' | 'code' | 'population' | 'size' | 'density';
    label: string;
    minWidth?: number;
    align?: 'right';
    format?: (value: number) => string;
}

const columns: Column[] = [
    { id: 'name', label: 'Name', minWidth: 170 },
    { id: 'code', label: 'ISO\u00a0Code', minWidth: 100 },
    {
        id: 'population',
        label: 'Population',
        minWidth: 170,
        align: 'right',
        format: (value: number) => value.toLocaleString('en-US'),
    },
    {
        id: 'size',
        label: 'Size\u00a0(km\u00b2)',
        minWidth: 170,
        align: 'right',
        format: (value: number) => value.toLocaleString('en-US'),
    },
    {
        id: 'density',
        label: 'Density',
        minWidth: 170,
        align: 'right',
        format: (value: number) => value.toFixed(2),
    },
];

interface Data {
    name: string;
    code: string;
    population: number;
    size: number;
    density: number;
}

function createData(
    name: string,
    calories: number,
    fat: number,
    carbs: number,
    protein: number,
) {
    return { name, calories, fat, carbs, protein };
}

const rows = [
    createData("100", 159, 6.0, 24, 4.0),
    createData("200", 237, 9.0, 37, 4.3),
    createData("300", 262, 16.0, 24, 6.0),
    createData("400", 305, 3.7, 67, 4.3),
    createData("500", 356, 16.0, 49, 3.9),
];




export default function DataManager(props: { setLoading: (loading: boolean) => void }){
    const [openPop, setOpen] = React.useState(false);
    const [page, setPage] = React.useState(0);
    const [rowsPerPage, setRowsPerPage] = React.useState(10);
    const [refreshState, updateState] = React.useState<number>(0);
    const [usersFileData, setUsersFileData] = useState({userdata: []})
    const [selectedFileColumns, setSelectedFileColumns] = useState([])
    const [columnsHeader, setColumnsHeader] = useState(<div></div>)
    const [columnsData, setColumnsData] = useState(<TableRow></TableRow>)

    const handleChangePage = (event: unknown, newPage: number) => {
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
        setRowsPerPage(+event.target.value);
        setPage(0);
    };

    const handleClickOpenPop = () => {
        setOpen(true);
    };

    const handleClosePop = () => {
        setOpen(false);
    };

    const initTree: getAllFilenamesResponse = {
        userdata: []
    }
    let [treeData, setTreeData] = useState(initTree)
    useEffect(() => {
        BackendApi.getAllUserFilenames().then(response => {
            setUsersFileData(response.data)
        })
        getAllFilenames(setTreeData)
    }, [refreshState])

    const tableDataInit: column[] = []

    let[tableData, setTableData] = useState(tableDataInit)

    const getColsFromFileID = (fileID: string) => {
        const runAsync=async ()=>{
            let selected:any[] = [];
            let filtered=usersFileData.userdata.filter(row=>{
                // @ts-ignore
                return row.filenames.filter(innerRow=>innerRow.id==fileID).length
            });
            // @ts-ignore
            if (filtered[0]&&filtered[0].filenames[0]) {
                // @ts-ignore
                selected=filtered[0].filenames[0].columns
                // @ts-ignore
                setSelectedFileColumns(filtered[0].filenames[0].columns);
                // @ts-ignore
                setColumnsHeader(selected.map((row: any) => <TableCell style={{color: "white"}}>{row.name}</TableCell>))
                let serverColumnsData: any[] = [];
                await Promise.all(selected.map((col:any)=>{
                    return BackendApi.filterApply(col.id).then(response => {
                        serverColumnsData.push(response.data.data.data);
                    })
                }))
                // @ts-ignore
                setColumnsData(
                    // @ts-ignore
                    serverColumnsData[0].map((cell: any,index) => {
                        return (
                            <TableRow key={'row'+index}
                                      sx={{'&:last-child td, &:last-child th': {border: 0}}}>
                                {
                                    // @ts-ignore
                                    selected.map((col,index)=>{
                                        return (
                                            <TableCell key={col.name + cell.value}
                                                       style={{color: "white"}}
                                                       component="th"
                                                   scope="row">
                                            {cell.value}
                                        </TableCell>)
                                })
                            }
                        </TableRow>)

                }))
            }
        }
        runAsync();
    }

    return (
        <div className={"dataManagerFlex"}>
            <div className={"sidebar"}>
                <div className={"dataTree"}>
                    <DataTree treeData={treeData} showColumns={false} isDataManager={true} admin={true} forceRefresh={updateState} onSelect={getColsFromFileID }></DataTree>
                </div>
                <div className={"uploadIcon"}>
                    <IconButton onClick={handleClickOpenPop}>
                        <Tooltip title={"Upload Data"}><UploadFileSharpIcon  fontSize={"large"} style={{color:"white"}}></UploadFileSharpIcon></Tooltip>
                    </IconButton>
                    <Dialog open={openPop}
                            onClose={handleClosePop}
                            >
                        <DialogTitle style={{backgroundColor: "#3B3B3B"}} color={"#ffffff"} id="UploadPopup">
                            {"Select File to upload/ download."}
                        </DialogTitle>
                        <DialogContent style={{backgroundColor: "#3B3B3B"}} className={"uploadPopup"}>
                            <div>
                                <Upload setLoading = {props.setLoading}></Upload>
                            </div>
                        </DialogContent>
                        <DialogActions style={{backgroundColor: "#3B3B3B"}}>
                            <ThemeProvider theme={tabTheme}>
                                <Button onClick={handleClosePop}>Close</Button>
                            </ThemeProvider>
                        </DialogActions>
                    </Dialog>
                </div>
            </div>
            <div className={"table"}>
                <TableContainer component={Paper} style={{height: "82vh", backgroundColor: "#636363"}}>
                    <Table sx={{ width: "80vw" }} aria-label="simple table">
                        <TableHead style={{backgroundColor: "#3B3B3B"}}>
                            <TableRow>
                                {columnsHeader}
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {columnsData}
                        </TableBody>
                    </Table>
                </TableContainer>
            </div>
        </div>
    );
}