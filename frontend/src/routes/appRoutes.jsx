import HomePage from "../pages/home/HomePage"
import DashboardOutlinedIcon from '@mui/icons-material/DashboardOutlined';
import FormatListBulletedOutlinedIcon from '@mui/icons-material/FormatListBulletedOutlined';

const appRoutes = [
    {
        index: true,
        element: <HomePage />,
        state: "home"
    },
    {
        path: "/dashboard",
        element: '',
        state: "dashboard",
        sidebarProps: {
            displayText: "Dashboard",
            icon: <DashboardOutlinedIcon />
        },
        child: [
            {
                index: true,
                element: '',
                state: "dashboard.index"
            },
            {
                path: "/dashboard/default",
                element: '',
                state: "dashboard.default",
                sidebarProps: {
                    displayText: "Default"
                }
            },
            {
                path: "/dashboard/analytics",
                element: '',
                state: "dashboard.analytics",
                sidebarProps: {
                    displayText: "AnalyticsPage"
                }
            },
            {
                path: "/dashboard/saas",
                element: '',
                state: "dashboard.saas",
                sidebarProps: {
                    displayText: "SaasPage"
                }
            }
        ]
    },
    {
        path: "/changelog",
        element: '',
        state: "changelog",
        sidebarProps: {
            displayText: "ChangeLog",
            icon: <FormatListBulletedOutlinedIcon />
        }
    }
]

export default appRoutes;