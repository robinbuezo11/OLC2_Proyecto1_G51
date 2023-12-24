import { ListItemIcon, ListItemButton } from "@mui/material";
import colorConfigs from "../../configs/colorConfigs";
// import { Link } from "react-router-dom";
import { useSelector } from "react-redux";

const SidebarItem = ({item}) => {
  const { appState } = useSelector((state) => state.appState);

    return (
        item.sidebarProps ? (
            <ListItemButton
                // component={Link}
                // to={item.path}
                sx={{
                    "&: hover": {
                        backgroundColor: colorConfigs.sidebar.hoverBg
                    },
                    backgroundColor: appState === item.state ? colorConfigs.sidebar.activeBg : "unset",
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
              {item.sidebarProps.displayText}
            </ListItemButton>
        ) : null
    );
};

export default SidebarItem;