import HomePage from "../pages/home/HomePage"
import DashboardPageLayout from "../pages/dashboard/DashboardPageLayout"
import DashboardOutlinedIcon from '@mui/icons-material/DashboardOutlined';
import DefaultPage from "../pages/dashboard/DefaultPage";
import DashboardIndex from "../pages/dashboard/DashboardIndex";
import ChangeLogPage from "../pages/changelog/ChangelogPage";
import AnalyticsPage from "../pages/dashboard/AnalyticsPage";
import SaasPage from "../pages/dashboard/SaasPage";
import FormatListBulletedOutlinedIcon from '@mui/icons-material/FormatListBulletedOutlined';

const appRoutes = [
    {
        index: true,
        element: <HomePage />,
        state: "home"
    },
    {
        path: "/dashboard",
        element: <DashboardPageLayout />,
        state: "dashboard",
        sidebarProps: {
            displayText: "Dashboard",
            icon: <DashboardOutlinedIcon />
        },
        child: [
            {
                index: true,
                element: <DashboardIndex />,
                state: "dashboard.index"
            },
            {
                path: "/dashboard/default",
                element: <DefaultPage />,
                state: "dashboard.default",
                sidebarProps: {
                    displayText: "Default"
                }
            },
            {
                path: "/dashboard/analytics",
                element: <AnalyticsPage />,
                state: "dashboard.analytics",
                sidebarProps: {
                    displayText: "AnalyticsPage"
                }
            },
            {
                path: "/dashboard/saas",
                element: <SaasPage />,
                state: "dashboard.saas",
                sidebarProps: {
                    displayText: "SaasPage"
                }
            }
        ]
    },
    {
        path: "/changelog",
        element: <ChangeLogPage />,
        state: "changelog",
        sidebarProps: {
            displayText: "ChangeLog",
            icon: <FormatListBulletedOutlinedIcon />
        }
    }
]

export default appRoutes;