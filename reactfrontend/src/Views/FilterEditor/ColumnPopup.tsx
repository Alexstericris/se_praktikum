import {Button} from "@mui/material";
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import {ThemeProvider} from "@mui/material/styles";
import {tabTheme} from "../../globalStyle";
import React, {useEffect, useState} from "react";
import {getAllFilenames} from "../../Services/TreeDataService";
import {getAllFilenamesResponse, UserFiles} from "../../RequestTypes";
import ColumnDataTree from "./ColumnDataTree";

export default function ColumnPopup(props: { isOpen: boolean, handleCancel: () => void, handleSubmit: (selection: string) => void}) {
    const initTree: getAllFilenamesResponse = {
        userdata: []
    }
    const initColumnInfo: string = "-1"
    let [treeData, setTreeData] = useState(initTree)
    let [select, setSelect] = useState(initColumnInfo)
    useEffect(() => {
        getAllFilenames(setTreeData)
    }, [])
    const submitWrapper = () => {
        props.handleSubmit(select)
    }

    return (
        <div>
            <Dialog open={props.isOpen}
                    onClose={props.handleCancel}
                    className={"inputDialog"}
                    PaperProps={{ sx: { width: "70%", height: "80%", borderRadius:"16px" } }}
            >
                <DialogTitle style={{backgroundColor: "#3B3B3B"}} color={"#ffffff"} id="DataTree">
                    {"Select Column to add."}
                </DialogTitle>
                <DialogContent style={{backgroundColor: "#3B3B3B"}}>
                    <ColumnDataTree treeData={treeData} showColumns={true} onSelect={(data) => setSelect(data)}></ColumnDataTree>
                </DialogContent>
                <DialogActions style={{backgroundColor: "#3B3B3B"}}>
                    <ThemeProvider theme={tabTheme}>
                        <Button onClick={props.handleCancel}>Close</Button>
                        <Button onClick={submitWrapper}>Submit</Button>
                    </ThemeProvider>
                </DialogActions>
            </Dialog>
        </div>
    );
}