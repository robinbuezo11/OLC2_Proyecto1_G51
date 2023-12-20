import React from "react";
import { AppBar, Toolbar} from "@mui/material";
import sizeConfigs from "../../configs/sizeConfigs";
import colorConfigs from "../../configs/colorConfigs";
import TopbarItems from "./TopbarItems";
import TopbarItem from "./TopbarItem";
import "../../styles/Topbar.css"

const Topbar = ({props}) => {
    return (
        <AppBar
            position="fixed"
            sx={{
                width: `calc(100% - ${sizeConfigs.sidebar.width})`,
                height: sizeConfigs.topbar.height,
                ml: sizeConfigs.sidebar.width,
                boxShadow: "unset",
                backgroundColor: colorConfigs.topbar.bg,
                color: colorConfigs.topbar.color,
            }}
        >
            <Toolbar>
                <nav /*style={{height: sizeConfigs.topbar.height}}*/> 
                    <ul className="menus">
                        {
                            TopbarItems.map((item, index) => {
                                const depthLevel = 0;
                                return <TopbarItem item={item} key={index} depthLevel={depthLevel} func={props[item.id]}/>
                            })
                        }
                    </ul>
                </nav>
            </Toolbar>
        </AppBar>
    )
};

export default Topbar;