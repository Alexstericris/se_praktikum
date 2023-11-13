import TreeView from "@mui/lab/TreeView";
import TreeItem from "@mui/lab/TreeItem";
import React, {useState} from "react";
import {
    columnInfo,
    FileMetadata,
    getAllFilenamesResponse,
    UserFiles
} from "../../RequestTypes";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";



export default function ColumnDataTree(props: {treeData:getAllFilenamesResponse|null, showColumns: boolean, onSelect: (newVal: string) => void}) {
    const initTree: getAllFilenamesResponse = {
        userdata: []
    }

    let [metadataColumns,setMetadataColumns] = useState(initTree)

    const userfilesToJsx = (val: UserFiles) =>
        <TreeItem nodeId={val.username} onClick={(e)=> e.stopPropagation()} label={<span style={{color: 'white'}}>{val.username}</span>}>
            {val.filenames.map(fileMetadataToJsx)}</TreeItem>

    const fileMetadataToJsx = (val: FileMetadata) =>
        <TreeItem nodeId={val.id.toString()} label={<span style={{color: 'white'}}>{val.name}</span>}>
            {props.showColumns?val.columns.map(filecolToJsx):null}</TreeItem>

    const filecolToJsx = (val: columnInfo) =>
        <TreeItem nodeId={"[" + val.id.toString() + "] " + val.name} label={<span style={{color: 'white'}}>{val.name}</span>}></TreeItem>


    if(props.treeData == null){ //treedata null
        return(
            <div>
                //TODO Spinner
                loading
            </div>
        )
    }else{
        console.log(props.treeData)
        const tree = props.treeData.userdata.map(userfilesToJsx);

        return (
            <TreeView
                color={"#ffffff"}
                defaultCollapseIcon={<ExpandMoreIcon style={{ color: "white" }} />}
                defaultExpandIcon={<ChevronRightIcon style={{ color: "white" }} />}
                onNodeSelect={(event: any, nodeIds: string) => props.onSelect(nodeIds)}
                >
                {tree}
            </TreeView>
        );
    }
}