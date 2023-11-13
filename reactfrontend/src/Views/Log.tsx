import React, {useEffect, useState} from "react";
import '../Log.css';
import {ThemeProvider, useTheme} from '@mui/material/styles';
import Box from '@mui/material/Box';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableFooter from '@mui/material/TableFooter';
import TablePagination from '@mui/material/TablePagination';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import IconButton from '@mui/material/IconButton';
import FirstPageIcon from '@mui/icons-material/FirstPage';
import KeyboardArrowLeft from '@mui/icons-material/KeyboardArrowLeft';
import KeyboardArrowRight from '@mui/icons-material/KeyboardArrowRight';
import LastPageIcon from '@mui/icons-material/LastPage';
import { DemoContainer } from '@mui/x-date-pickers/internals/demo';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import {FormControl, InputLabel, Input, InputAdornment} from "@mui/material";
import {AccountCircle} from "@mui/icons-material";
import {datePickerTheme} from "../globalStyle";
import TableSortLabel from "@mui/material/TableSortLabel";
import {getLogRequest} from "../RequestTypes";
import {formatDate, LogMockdata, LogMockdata2} from "../Services/LogService";
import axios from "../axios";


interface TablePaginationActionsProps {
    count: number;
    page: number;
    rowsPerPage: number;
    onPageChange: (
        event: React.MouseEvent<HTMLButtonElement>,
        newPage: number,
    ) => void;
}

function TablePaginationActions(props: TablePaginationActionsProps) {
    const theme = useTheme();
    const {count, page, rowsPerPage, onPageChange} = props;

    const handleFirstPageButtonClick = (
        event: React.MouseEvent<HTMLButtonElement>,
    ) => {
        onPageChange(event, 0);
    };

    const handleBackButtonClick = (event: React.MouseEvent<HTMLButtonElement>) => {
        onPageChange(event, page - 1);
    };

    const handleNextButtonClick = (event: React.MouseEvent<HTMLButtonElement>) => {
        onPageChange(event, page + 1);
    };

    const handleLastPageButtonClick = (event: React.MouseEvent<HTMLButtonElement>) => {
        onPageChange(event, Math.max(0, Math.ceil(count / rowsPerPage) - 1));
    };


    return (
        <Box sx={{flexShrink: 0, ml: 2.5}}>
            <IconButton id={"text"}
                        onClick={handleFirstPageButtonClick}
                        disabled={page === 0}
                        aria-label="first page"
            >
                {theme.direction === 'rtl' ? <LastPageIcon/> : <FirstPageIcon/>}
            </IconButton>
            <IconButton id={"text"}
                        onClick={handleBackButtonClick}
                        disabled={page === 0}
                        aria-label="previous page"
            >
                {theme.direction === 'rtl' ? <KeyboardArrowRight/> : <KeyboardArrowLeft/>}
            </IconButton>
            <IconButton id={"text"}
                        onClick={handleNextButtonClick}
                        disabled={page >= Math.ceil(count / rowsPerPage) - 1}
                        aria-label="next page"
            >
                {theme.direction === 'rtl' ? <KeyboardArrowLeft/> : <KeyboardArrowRight/>}
            </IconButton>
            <IconButton id={"text"}
                        onClick={handleLastPageButtonClick}
                        disabled={page >= Math.ceil(count / rowsPerPage) - 1}
                        aria-label="last page"
            >
                {theme.direction === 'rtl' ? <FirstPageIcon/> : <LastPageIcon/>}
            </IconButton>
        </Box>
    );
}


export default function CustomPaginationActionsTable() {
    const [page, setPage] = React.useState(0);
    const [rowsPerPage, setRowsPerPage] = React.useState(5);

    const [users, setUsers] = useState("")
    const [date1, setDate1] = useState("")
    const [date2, setDate2] = useState("")
    const [data, setData] = useState<any[]>([]);
    const [logs, setLogs] = useState(<TableRow></TableRow>)


    const [rowData, setRowData] = useState(data);
    const [orderDirection, setOrderDirection] = useState<"asc" | "desc" | undefined>('asc');

    const sortTable = (table: any[], orderBy: "asc" | "desc" | undefined) => {
        switch (orderBy) {
            case "asc":
            default:
                return table.sort((a,b) =>
                    a.timestamp > b.timestamp ? 1 : b.timestamp > a.timestamp ? -1 : 0
                );
            case "desc":
                return table.sort((a, b) =>
                    a.timestamp < b. timestamp ? 1 : b.timestamp < a.timestamp ? -1 : 0
                );
        }
    };

    const handleSortRequest = () => {
        setRowData(sortTable(data, orderDirection));
        setOrderDirection(orderDirection === "asc" ? "desc" : "asc");
    }


    function sendFilterLog(userNames:string[], from:string, to:string){
        const postData:getLogRequest = {userNames, from, to}
        //const Mockurl = "https://9070499e-4612-41d7-ab32-a3380b12a0db.mock.pstmn.io/postFilterLog"
         const url = "/getLog/"
        axios.post(url, postData).then(response => {
            setData(response.data)
        }).catch((error) => {
            //console.log(error);
            console.log("sendError")
            //setData(LogMockdata2)
        });
    }

    const getLog = () => {
        //const Mockurl = 'https://62148659-4312-4a48-94c0-713873624562.mock.pstmn.io/getLog';
        const url = "/getLog/"
        const userNames:string[] = []
        const postData:getLogRequest = {userNames}
        axios.post(url, postData, {headers: {
            Authorization: 'Bearer '+localStorage.getItem('accessKey')
        }}).then(response=>{
            setData(response.data);
            if(response.data&&response.data.length){
                setRowData(data.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage).map((row,index)=>{
                    return (<TableRow key={'row'+index}>
                        <TableCell>
                            <p id={"row"}> {row.timestamp} </p>
                        </TableCell>
                        <TableCell style={{ width: 160 }} align={"left"}>
                            <p id={"row"}> {row.userName} </p>
                        </TableCell>
                        <TableCell style={{ width: 160 }} align={"left"}>
                            <p id={"row"}> {row.action} </p>
                        </TableCell>
                    </TableRow>)
                }))
            }
        }).catch((error) => {
            console.log("getError")
            //setData(LogMockdata)
        });
    }

    useEffect(()=>{
        getLog();
    }, []);



    const handleUserChange = (event:any) => {
        let str1 = (event.target.value).toString();
        console.log(str1.split(","));
        setUsers(str1.split(","))
        sendFilterLog(str1.split(","),date1, date2);

    }


    const handleStartDate = (event:any) => {
        console.log(formatDate(event))
        setDate1(formatDate(event))
        sendFilterLog([users], formatDate(event), date2);
    }
    const handleEndDate = (event:any) => {
        console.log(formatDate(event))
        setDate2(formatDate(event))
        sendFilterLog([users], date1, formatDate(event));
    }


    // Avoid a layout jump when reaching the last page with empty rows.
    const emptyRows =
        page > 0 ? Math.max(0, (1 + page) * rowsPerPage - data.length) : 0;

    const handleChangePage = (
        event: React.MouseEvent<HTMLButtonElement> | null,
        newPage: number,
    ) => {
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (
        event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
    ) => {
        setRowsPerPage(parseInt(event.target.value, 10));
        setPage(0);
    };


    return(
        <div>
            <div id={"filtercontainer"}>
                <div id={"filter_date"}>
                    <div id={"filter_date_start"}>
                        <LocalizationProvider dateAdapter={AdapterDayjs}>
                            <DemoContainer components={['DatePicker']}>
                                <ThemeProvider theme={datePickerTheme}>
                                    <DatePicker
                                        onChange={ (e) => handleStartDate(e)}
                                        className={"datepicker"}
                                        format={"DD/MM/YYYY"}
                                        label="filter-by-date-start"/>
                                </ThemeProvider>
                            </DemoContainer>
                        </LocalizationProvider>
                    </div>
                    <div id={"filter_date_start"}>
                        <LocalizationProvider dateAdapter={AdapterDayjs}>
                            <DemoContainer components={['DatePicker']}>
                                <ThemeProvider theme={datePickerTheme}>
                                    <DatePicker
                                        onChange={ (e) =>
                                            handleEndDate(e)}
                                        className={"datepicker"}
                                        format={"DD/MM/YYYY"}
                                        label="filer-by-date-end"/>
                                </ThemeProvider>
                            </DemoContainer>
                        </LocalizationProvider>
                    </div>
                </div>
                <div id={"filter_user"}>
                    <Box sx={{ '& > :not(style)': { m: 1 } }}>
                        <FormControl variant="standard">
                            <InputLabel id={"user_label"} htmlFor="input-with-icon-adornment">
                                filter by users, seperated by commas
                            </InputLabel>
                            <Input
                                onKeyDown={ (e) => {
                                    if (e.key === "Enter") {
                                        handleUserChange(e);
                                    }
                                }}
                                placeholder={"user1, user2, ..."}
                                id="user_placeholder"
                                startAdornment={
                                    <InputAdornment position="start">
                                        <AccountCircle />
                                    </InputAdornment>
                                }
                            />
                        </FormControl>
                    </Box>
                </div>
                <TableContainer id={"table"} component={Paper}>
                    <Table sx={{ minWidth: 500 }} aria-label="activity-log">
                        <colgroup>
                            <col width="10%" />
                            <col width="10%" />
                            <col width="60%" />
                        </colgroup>
                        <TableHead id={"head"}>
                            <TableRow>
                                <TableCell onClick={handleSortRequest}>
                                    <TableSortLabel id={"dateArrow"} active={true} direction={orderDirection}>
                                        Date
                                    </TableSortLabel>
                                </TableCell>
                                <TableCell> <p id={"headrow"}> User </p></TableCell>
                                <TableCell> <p id={"headrow_action"}> Action </p></TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {rowData}
                            {emptyRows > 0 && (
                                <TableRow style={{ height: 53 * emptyRows }}>
                                    <TableCell colSpan={6} />
                                </TableRow>
                            )}
                        </TableBody>
                        <TableFooter>
                            <TableRow>
                                <TablePagination id={"text"}
                                                 rowsPerPageOptions={[5, 10, 25, { label: 'All', value: -1 }]}
                                                 colSpan={3}
                                                 count={data.length}
                                                 rowsPerPage={rowsPerPage}
                                                 page={page}
                                                 SelectProps={{
                                                     inputProps: {
                                                         'aria-label': 'rows per page',
                                                     },
                                                     native: true,
                                                 }}
                                                 onPageChange={handleChangePage}
                                                 onRowsPerPageChange={handleChangeRowsPerPage}
                                                 ActionsComponent={TablePaginationActions}
                                />
                            </TableRow>
                        </TableFooter>
                    </Table>
                </TableContainer>
            </div>
        </div>
    );
}


