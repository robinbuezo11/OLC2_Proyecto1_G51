import React, {useEffect, useState} from "react";
import { ListItemIcon, ListItemButton, ListItemText, Typography, Collapse, List } from "@mui/material";
import colorConfigs from "../../configs/colorConfigs";
import ExpandLessOutlinedIcon from '@mui/icons-material/ExpandLessOutlined';
import ExpandMoreOutlinedIcon from '@mui/icons-material/ExpandMoreOutlined';
import SidebarItem from "./SidebarItem";
import { useSelector } from "react-redux";

const SidebarItemCollapse = ({item}) => {
    const [open, setOpen] = useState(false);

    const { appState } = useSelector((state) => state.appState);

    useEffect(() => {
        if(appState.includes(item.state)) {
            setOpen(true);
        }
    }, [appState, item]);

    return (
        item.sidebarProps ? (
            <>
                <ListItemButton
                    onClick={() => setOpen(!open)}
                    sx={{
                        "&: hover": {
                            backgroundColor: colorConfigs.sidebar.hoverBg
                        },
                        paddingY: "12px",
                        paddingLeft: `${12 * item.level + 12}px`,
                        paddingRight: '12px',
                    }}
                >
                    <ListItemIcon sx={{
                        color: colorConfigs.sidebar.color
                    }}>
                        {item.sidebarProps.icon && item.sidebarProps.icon}
                    </ListItemIcon>
                    <ListItemText
                        disableTypography
                        primary={
                            <Typography>
                                {item.sidebarProps.displayText}
                            </Typography>
                        }
                    />
                    {open ? <ExpandLessOutlinedIcon /> : <ExpandMoreOutlinedIcon />}
                </ListItemButton>
                <Collapse in={open} timeout="auto">
                    <List>
                        {item.child.map((child, index) => (
                            child.sidebarProps ? (
                                child.child ? (
                                <SidebarItemCollapse item={child} key={index} />
                                ) : (
                                <SidebarItem item={child} key={index} />
                                )
                        ) : null
                        ))}
                    </List>
                </Collapse>
            </>
        ) : null
    );
};

export default SidebarItemCollapse;