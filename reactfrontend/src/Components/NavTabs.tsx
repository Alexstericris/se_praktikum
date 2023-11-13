import * as React from 'react';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import {tabData} from "../types";
import {useNavigate} from "react-router-dom";
import {ThemeProvider} from '@mui/material/styles';
import {tabTheme} from "../globalStyle"
import { useLocation } from "react-router-dom";



export default function NavTabs(props:{userTabs:tabData[]}){
    const [value, setValue] = React.useState<number>(0);
    // create list of tab components from tabData
    const tabs = props.userTabs.map((tab, index) =>
        <Tab key={"navtab-" + index} label={tab.title} disabled={tab.isDisabled}/>
    );

    const navigate = useNavigate();

    const handleChange = (event: React.SyntheticEvent, newValue: number) => {
        // Navigate to selected page when clicking on tab and set indicator accordingly
        setValue(newValue);
        props.userTabs[newValue].active=true
        navigate(props.userTabs[newValue].path)
    };

    // Update Tab Indicator when navigating via back/forwards arrows
    const locate = useLocation();
    window.onpopstate = (event) => {
        const previousPath: string = locate.pathname;
        const previousValue = props.userTabs.map((tab, index) => (tab.path==previousPath)? index: -1)
            .filter(index => index != -1)[0];
        setValue(previousValue);
    };

    return (
        <ThemeProvider theme={tabTheme}>
            <Tabs value={value} onChange={handleChange} aria-label="disabled tabs example">
                {tabs}
            </Tabs>
        </ThemeProvider>

    );
}
