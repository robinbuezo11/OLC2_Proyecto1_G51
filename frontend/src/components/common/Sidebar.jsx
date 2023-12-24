import { Avatar, Drawer, List, Stack, Toolbar, Typography } from "@mui/material";
import { Link } from "react-router-dom";
import sizeConfigs from "../../configs/sizeConfigs";
import assets from "../../assets";
import colorConfigs from "../../configs/colorConfigs";
// import appRoutes from "../../routes/appRoutes";
import structDB from "./StructDB";
import SidebarItem from "./SidebarItem";
import SidebarItemCollapse from "./SidebarItemCollapse";

const Sidebar = () => {
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