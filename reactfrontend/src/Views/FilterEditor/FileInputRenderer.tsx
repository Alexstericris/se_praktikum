import {Button} from "@mui/material";
import React, {useState} from "react";
import ColumnPopup from "./ColumnPopup";

export default function ColumnInputPopupButton(props: { data: any, onChange: (newData: any) => void }) {
    const [isOpen, setIsOpen] = useState(false)

    const open = () => setIsOpen(true)
    const close = () => setIsOpen(false)
    return (
        <div>
            <Button onClick={open} variant={"outlined"}>{"Select Column"}</Button>
            <ColumnPopup handleCancel={close} handleSubmit={(newData) => {console.log(newData);props.onChange(newData); close()}} isOpen={isOpen}></ColumnPopup>
        </div>
    )
}