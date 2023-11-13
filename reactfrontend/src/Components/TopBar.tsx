import NavTabs from "./NavTabs";
import Button from "@mui/material/Button";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import React, {useContext, useEffect, useState} from "react";
import {UserContext, UserDispatchContext} from "../UserContext";
import {useNavigate} from "react-router-dom";

export default function TopBar(props:any) {
    const updateUser = useContext(UserDispatchContext);
    const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
    const navigate = useNavigate();
    const handleLogout = () => {
        updateUser(null);
        localStorage.clear()
        navigate('/login')
    };

    const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
        setAnchorEl(event.currentTarget);
    };
    const handleClose = () => {
        setAnchorEl(null);
    };

    const open = Boolean(anchorEl);
    useEffect(()=>{

    },[props.tabs])

    return(
    <div className={"topBarFlex"}>
        <div className={"bar"}>
            <NavTabs userTabs={props.tabs}></NavTabs>
        </div>
        <div className={"profil"}>
            <div>
                <Button
                    id="basic-button"
                    aria-controls={open ? 'basic-menu' : undefined}
                    aria-haspopup="true"
                    aria-expanded={open ? 'true' : undefined}
                    onClick={handleClick}>
                    <p className={"pro"}>Profil</p>
                </Button>
                <Menu id="basic-menu"
                      anchorEl={anchorEl}
                      open={open}
                      onClose={handleClose}
                      MenuListProps={{'aria-labelledby': 'basic-button'}}>
                    <MenuItem onClick={handleClose}>Username: {props.username}</MenuItem>
                    <MenuItem onClick={handleLogout}>Logout</MenuItem>
                </Menu>
            </div>
        </div>
    </div>
    )
};