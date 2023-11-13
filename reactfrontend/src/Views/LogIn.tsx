import React, {FormEventHandler, useContext, useEffect, useState} from 'react';
import '../LogIn.css';
import {Alert, Button, Checkbox, FormControlLabel, FormGroup, TextField} from "@mui/material";
import {BackendApi} from "../backendApi";
import axios from "../axios";
import {useNavigate} from "react-router-dom";
import {UserDispatchContext} from "../UserContext";


function LogIn(props:any){
    const [user, setUser] = useState(null);
    const updateUser = useContext(UserDispatchContext);
    const navigate = useNavigate();
    const [errorMessage, setErrorMessage] = useState('');
    const handleSubmit:FormEventHandler=($event:any)=>{
        BackendApi.login({
            username: $event.target.username.value,
            password: $event.target.password.value
        }).then(response=>{
            console.log(response.data)
            localStorage.setItem('access',response.data.access)
            localStorage.setItem('refreshToken',response.data.refresh)
            updateUser(response.data.user)
            navigate('/')
        }).catch((error)=>{
            if (error.response.data.detail) {
                console.log(error.response.data.detail);
                setErrorMessage(error.response.data.detail)
            }
            localStorage.clear();
            BackendApi.register({
                username: $event.target.username.value,
                email: $event.target.username.value+'@test.com',
                password:$event.target.password.value
            }).then(response=>{
                localStorage.setItem('access',response.data.access)
                localStorage.setItem('refreshToken',response.data.refresh)
                axios.defaults.headers.common['Authorization'] = `Bearer ${localStorage.getItem('access')}`;
                updateUser(response.data.user)
                navigate('/')
            });
        })
        $event.preventDefault();
    }
    useEffect(()=>{
        if (localStorage.getItem('access')) {

        }
    });
    return (
        <div id={"loginWrapper"}>
            <form onSubmit={handleSubmit} method={"POST"}>
                <div className= "window">
                    <h2 className="headLine">Log In</h2>
                <div className= "login-input-wrap">
                    <TextField name={"username"}
                               required={true}
                               className="login-input"
                               label="Username"
                               variant="outlined"/>
                </div>
                <div className= "login-input-wrap">
                    <TextField name={"password"}
                               required={true}
                               className="login-input"
                               type="password"
                               label="Password"
                               variant="outlined"/>
                </div>
                <div className= "remember">
                    <FormGroup>
                        <FormControlLabel control={<Checkbox />} label="Remember me" />
                    </FormGroup>
                </div>
                <div className= "sign-in">
                    <Button className="button" type={"submit"} variant="contained">
                        Sign In
                    </Button>
                </div>
                <div className="error-message">
                    {errorMessage&&<Alert severity="error">{errorMessage}</Alert>}
                </div>
            </div>
            </form>
        </div>
    );
}

export default LogIn;

