import React, { useState, useEffect } from "react";
import '../../styles/Sidebar.css'
import { Avatar, Drawer, List, Stack, Toolbar, Typography } from "@mui/material";
import { Link } from "react-router-dom";
import sizeConfigs from "../../configs/sizeConfigs";
import assets from "../../assets";
import colorConfigs from "../../configs/colorConfigs";
// import appRoutes from "../../routes/appRoutes";
// import structDB from "./StructDB";
import SidebarItem from "./SidebarItem";
import SidebarItemCollapse from "./SidebarItemCollapse";
import RefreshIcon from '@mui/icons-material/Refresh';
import StorageOutlinedIcon from '@mui/icons-material/StorageOutlined';
import TableChartOutlinedIcon from '@mui/icons-material/TableChartOutlined';
import CompareArrowsIcon from '@mui/icons-material/CompareArrows';
import CodeIcon from '@mui/icons-material/Code';
import FolderIcon from '@mui/icons-material/Folder';
import axios from "axios";

const Sidebar = () => {
  const [structDB, setStructDB] = useState([]);
  const [rotateIcon, setRotateIcon] = useState(false);

  const fetchStructDB = async () => {
    try{
      setRotateIcon(true);
      const response = await axios.get("http://localhost:4000/api/getStruct");
      if (response.data.success) {
        const updatedStructDB = setStructDBData(response.data.result);
        setStructDB(updatedStructDB);
        console.log(updatedStructDB)
      }
    } catch (error) {
      console.log(error);
    } finally {
      setTimeout(() => {
        setRotateIcon(false);
      }, 1000);
    }
  };

  const setStructDBData = (data) => {
    data.forEach((item) => {
      if (item.type === 'database') {
        item.sidebarProps = {
          displayText: item.name,
          icon: <StorageOutlinedIcon />
        }
      } else if (item.type === 'table') {
        item.sidebarProps = {
          displayText: item.name,
          icon: <TableChartOutlinedIcon />
        }
      } else if (item.type === 'column') {
        item.sidebarProps = {
          displayText: item.name + " (" + item.dataType + ")",
        }
      } else if (item.type === 'function') {
        item.sidebarProps = {
          displayText: item.name,
          icon: <CompareArrowsIcon />
        }
      } else if (item.type === 'procedure') {
        item.sidebarProps = {
          displayText: item.name,
          icon: <CodeIcon />
        }
      } else if (item.type === 'tables' || item.type === 'functions' || item.type === 'procedures') {
        item.sidebarProps = {
          displayText: item.name,
          icon: <FolderIcon />
        }
      }
      if (item.child) {
        item.child = setStructDBData(item.child);
      }
    });
    return data;
  };

  useEffect(() => {
    fetchStructDB();
  }, []);

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: sizeConfigs.sidebar.width,
        flexShrink: 0,
        "& .MuiDrawer-paper": {
          width: sizeConfigs.sidebar.width,
          boxSizing: "border-box",
          borderRight: "0px",
          backgroundColor: colorConfigs.sidebar.bg,
          color: colorConfigs.sidebar.color,
        },
      }}
    >
      <List disablePadding>
        <Toolbar sx={{
          marginBottom: "20px"
        }}>
          <Stack
            sx={{ width: "100%", marginTop: "20px" }}
            direction="column"
            justifyContent="center"
            alignItems="center"
          >
            <Link to="/">
              <Avatar src={assets.images.logo} />
            </Link>
            <Typography variant="h6" sx={{ marginTop: "20px" }}>
              Bases de Datos 
            </Typography>
            <RefreshIcon onClick={fetchStructDB} sx={{ cursor: "pointer", animation: rotateIcon ? "rotate 1s infinite linear" : "none" }} />
          </Stack>
        </Toolbar>
        {structDB.map((item, index) => (
          item.sidebarProps ? (
            item.child ? (
              <SidebarItemCollapse item={item} key={index} />
            ) : (
              <SidebarItem item={item} key={index} />
            )
          ) : null
        ))}
      </List>
    </Drawer>
  );
};

export default Sidebar;