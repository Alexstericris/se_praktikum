import {Button} from "@mui/material";
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import {ThemeProvider} from "@mui/material/styles";
import {tabTheme} from "../globalStyle";
import React, {useState} from "react";
import DataTree from "../Components/DataTree";
import {getAllFilenames} from "../Services/TreeDataService";
import {getAllFilenamesResponse} from "../RequestTypes";
import axios from "../axios";

export default function Popup(props:any){
    const [openPop, setOpen] = React.useState(false);
    const [columnId, setColumnId] = useState(null);
    const initTree: getAllFilenamesResponse = {
        userdata: []
    }
    let [treeData, setTreeData] = useState(initTree)

    const handleClickOpenPop = () => {
        setOpen(true);
        getAllFilenames(setTreeData)
    };


    const handleClosePop = () => {
        setOpen(false);
    };
    const handleSubmit = () => {
        props.handleOnSubmit(columnId)
        setOpen(false);
    };

    const getColsFromFileID=(fileID: string)=>{
        // @ts-ignore
        setColumnId(fileID)
    }
    return (
        <div>
            <div className={"inputTree"}>
                <Button variant="outlined" onClick={handleClickOpenPop}>
                    Add new chart
                </Button>
                <Dialog open={openPop}
                        onClose={handleClosePop}
                        className={"inputDialog"}>
                    <DialogTitle style={{backgroundColor: "#3B3B3B"}} color={"#ffffff"} id="DataTree">
                        {"Select Column to add."}
                    </DialogTitle>
                    <DialogContent style={{backgroundColor: "#3B3B3B"}}>
                        <DataTree treeData={treeData} showColumns={true}
                                  isDataManager={false}
                                  admin={true}
                                  onSelect={getColsFromFileID}
                                  forceRefresh={()=>{}}></DataTree>
                    </DialogContent>
                    <DialogActions style={{backgroundColor: "#3B3B3B"}}>
                        <ThemeProvider theme={tabTheme}>
                            <Button onClick={handleClosePop}>Close</Button>
                            <Button onClick={handleSubmit}>Submit</Button>
                        </ThemeProvider>
                    </DialogActions>
                </Dialog>
            </div>
        </div>
    );
}