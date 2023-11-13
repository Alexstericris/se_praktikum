import TreeView from "@mui/lab/TreeView";
import TreeItem from "@mui/lab/TreeItem";
import React, {EventHandler, useState} from "react";
import {
    columnInfo, deleteFileRequest,
    FileMetadata,
    getAllFilenamesResponse,
    getMyFilenamesResponse,
    UserFiles
} from "../RequestTypes";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import IconButton from "@mui/material/IconButton";
import DeleteIcon from '@mui/icons-material/Delete';
import FileUploadIcon from '@mui/icons-material/FileUpload';
import {Tooltip} from "@mui/material";
import axios from "../axios";
import {response} from "express";
import {Simulate} from "react-dom/test-utils";
import error = Simulate.error;
import UploadService from "./Upload/UploadFile";



export default function DataTree(props: {treeData:getAllFilenamesResponse|getMyFilenamesResponse|null, showColumns: boolean,
    isDataManager: boolean, admin: boolean, onSelect?: (selected: string) =>void, forceRefresh: (newState: number)=>void}) {
    const initTree: getAllFilenamesResponse = {
        userdata: []
    }
    // @ts-ignore
    const onDownload = (event: any) => {
        const formValue = event.currentTarget.value;
        UploadService.download(formValue).then(response => {// create file link in browser's memory
            const href = URL.createObjectURL(response.data);

            // create "a" HTML element with href to file & click
            const link = document.createElement('a');
            link.href = href;
            link.setAttribute('download', 'file.csv'); //or any other extension
            document.body.appendChild(link);
            link.click();

            // clean up "a" element & remove ObjectURL
            document.body.removeChild(link);
            URL.revokeObjectURL(href);})}

    let [metadataColumns,setMetadataColumns] = useState(initTree)

    function sendDelete(id: any){
        // ToDo Richtige URL einfügen
        const url = "/deleteFile/"
        const postData: deleteFileRequest = id
        axios.post(url, postData).then(response =>{
            
        }).catch((error) => {
            console.log("Momentan noch, wegen fehlendem URL" + error)
        })
    }


    const userfilesToJsx = (val: UserFiles) =>
        <TreeItem key={val.username} nodeId={val.username} onClick={(e)=> e.stopPropagation()} label={<span style={{color: 'white'}}>{val.username}</span>}>
            {val.filenames.map(fileMetadataToJsx)}</TreeItem>

    const fileMetadataToJsx = (val: FileMetadata) =>{
        return <TreeItem key={val.id.toString() + val.name + val.timeRecorded} nodeId={val.id.toString()} label={<span style={{color: "white"}}>{val.name}</span>}>
            {props.showColumns?val.columns.map(filecolToJsx):null}
            {props.isDataManager && props.admin && //beide exportieren // admin löschen
                <Tooltip title={"Delete File"}>
                    <IconButton
                        id={val.id.toString()}
                        onClick={(e) => {
                            sendDelete(val.id.toString())
                            props.forceRefresh(val.id)
                        }}>
                        <DeleteIcon style={{color: "white"}}></DeleteIcon>
                    </IconButton></Tooltip>}
            {props.isDataManager && <IconButton id={val.id.toString()} value={val.name} onClick={onDownload}>
                <Tooltip title={"Export File"}><FileUploadIcon style={{color: "white"}}></FileUploadIcon></Tooltip>
            </IconButton>}
        </TreeItem>
    }
    const filecolToJsx = (val: columnInfo) =>
        <TreeItem key={val.id.toString() + val.name} nodeId={val.id.toString()} label={<span style={{color: 'white'}}>{val.name}</span>}></TreeItem>


    if(props.treeData == null){ //treedata null
        return(
            <div>
                //TODO Spinner
                loading
            </div>
        )
    }else if('userdata' in props.treeData){//treedata getAllFilesnamesResponse

        const tree = props.treeData.userdata.map(userfilesToJsx);
        if(props.showColumns){
            return (
                <TreeView
                    color={"#ffffff"}
                    onNodeSelect={(event: any, nodeIds: string) => {
                        if (props.onSelect != undefined) {
                            props.onSelect(nodeIds)
                        }
                    }}
                    defaultCollapseIcon={<ExpandMoreIcon style={{color: "white"}}/>}
                    defaultExpandIcon={<ChevronRightIcon style={{color: "white"}}/>}>
                    {tree}
                </TreeView>
            )
        }else{
            return (
                <TreeView
                    color={"#ffffff"}
                    defaultCollapseIcon={<ExpandMoreIcon style={{ color: "white" }} />}
                    defaultExpandIcon={<ChevronRightIcon style={{ color: "white" }} />}
                    onNodeSelect={(event: any, nodeIds: string) => {if(props.onSelect != undefined){props.onSelect(nodeIds)}}}>
                    {tree}
                </TreeView>
            )
        }
    }
    else { //treedata getMyFilenamesResponse
        const tree: any = (props.treeData as getMyFilenamesResponse).filenames.map(fileMetadataToJsx);

        return (
            <TreeView
                onNodeSelect={(event: any, nodeIds: string) => {
                    if (props.onSelect != undefined) {
                        props.onSelect(nodeIds)
                    }
                }}
                color={"#ffffff"}
                defaultCollapseIcon={<ExpandMoreIcon style={{color: "white"}}/>}
                defaultExpandIcon={<ChevronRightIcon style={{color: "white"}}/>}>
                {tree}
            </TreeView>
        );
    }
}