import React from "react";
import "../../Filter.css";
import {Colors, FlumeConfig, NodeEditor} from 'flume'
import {ControlRenderCallback, InputData, NodeMap, NodeTypeConfig, PortTypeConfig, ValueSetter} from "flume/dist/types";
import {filterNodes} from "./FilterTypes";
import ColumnInputPopupButton from "./FileInputRenderer";

type PortProps = { label: string, name: string, portName: string, inputLabel: string, defaultValue: any }

const fileInputRender: ControlRenderCallback = (data: any, onChange: (newData: any) => void, context: any, redraw: () => void, portProps: PortProps, inputData: InputData) => {
    return(
        <div><p>{data}</p> <ColumnInputPopupButton data={data} onChange={onChange}></ColumnInputPopupButton></div>
    )
}


const useNewDataUnchanged: ValueSetter = (a, b) => a;
const config = new FlumeConfig()

const ports: PortTypeConfig[] = [
    {
    type: "data", name: "data", label: "data", color: Colors.green,
}, {
    type: "float",
    name: "float",
    hidePort: false,
    noControls: false,
    acceptTypes: ["float"],
    label: "float",
    color: Colors.pink,
    controls: [{
        type: "number", step: 0.5, label: "float", name: "float", defaultValue: 0, setValue: useNewDataUnchanged
    }]
}, {
    type: "integer",
    name: "integer",
    hidePort: false,
    noControls: false,
    acceptTypes: ["float", "integer"],
    label: "integer",
    color: Colors.red,
    controls: [{
        type: "number", step: 1, label: "integer", name: "integer", defaultValue: 0, setValue: useNewDataUnchanged
    }]
},{
    type: "kernel",
    name: "kernel",
    hidePort: false,
    noControls: false,
    acceptTypes: ["kernel"],
    label: "kernel",
    color: Colors.grey,
    controls: [{
        type: "text", label: "kernel", name: "kernel", defaultValue: "1, 2, 1", setValue: useNewDataUnchanged
    }]
}, {
    type: "boolean",
    name: "boolean",
    hidePort: false,
    noControls: false,
    acceptTypes: ["boolean"],
    label: "boolean",
    color: Colors.purple,
    controls: [{
        type: "checkbox", label: "boolean", name: "boolean", defaultValue: false, setValue: useNewDataUnchanged
    }]
}, {
    type: "string",
    name: "string",
    hidePort: false,
    noControls: false,
    acceptTypes: ["string"],
    label: "string",
    color: Colors.cyan,
    controls: [{
        type: "text", label: "window", name: "window", defaultValue: "", setValue: useNewDataUnchanged
    }]
}, {
    type: "selectNulltype",
    name: "selectNulltype",
    hidePort: false,
    noControls: false,
    acceptTypes: ["string"],
    label: "select",
    color: Colors.red,
    controls: [{
        type: "select", label: "select", name: "select", defaultValue: "nan", setValue: useNewDataUnchanged, options: [{
            label: "NaN", value: "nan"
        }, {

            label: "null", value: "null"
        }]
    }]
}, {
    type: "fileIn",
    name: "fileIn",
    hidePort: true,
    noControls: false,
    acceptTypes: ["fileIn"],
    label: "file",
    controls: [{
        type: "custom",
        name: "fileIn",
        label: "file",
        render: fileInputRender,
        defaultValue: "",
        setValue: useNewDataUnchanged
    },
    ]
},

]
let nodes: NodeTypeConfig[] = [
    {
    type: "parameterBoolean",
    label: "Input: Boolean",
    outputs: ports => [ports["boolean"]()],
    inputs: ports => [ports["boolean"]({hidePort: true, label: "true/false"})]
}, {
    type: "parameterFloat",
    label: "Input: Float",
    outputs: ports => [ports["float"]()],
    inputs: ports => [ports["float"]({hidePort: true})]
}, {
    type: "parameterInteger",
    label: "Input: Integer",
    outputs: ports => [ports["integer"]()],
    inputs: ports => [ports["integer"]({hidePort: true})]
}, {
    type: "parameterKernel",
    label: "Input: Kernel",
    outputs: ports => [ports["kernel"]({})],
    inputs: ports => [ports["kernel"]({hidePort: true})]
}, {
    type: "data_input",
    label: "Data Input",
    description: "Loads Data from Database",
    inputs: ports => [ports["fileIn"]()],
    outputs: ports => [ports["data"]()],

}, {
    type: "data_output",
    label: "Data Output",
    description: "Writes Dataset to Database",
    inputs: ports => [ports["data"](), ports["string"]({label: "filename", name: "filename", hidePort: true})],
},]

nodes = nodes.concat(filterNodes)

ports.forEach(port => {
    config.addPortType(port)
})

nodes.forEach(node => {
    config.addNodeType(node)
})

const onNodeChange = (nodes: NodeMap) => {
    console.log(nodes)
}

export default function Filter() {
    return (<div style={{width: "100%", height: "85vh"}}>
        <NodeEditor
            portTypes={config.portTypes}
            nodeTypes={config.nodeTypes}
            onChange={onNodeChange}
            comments={{
                "Help": {
                    color: Colors.cyan,
                    height: 50,
                    width: 600,
                    x: 10,
                    y:10,
                    text:"Press right click to add a new node. For every valid data output node a new database entry will be created.",
                    id: "help",
                    isNew: false
                }
            }}
        />
    </div>)
}