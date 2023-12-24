import StorageOutlinedIcon from '@mui/icons-material/StorageOutlined';
import TableChartOutlinedIcon from '@mui/icons-material/TableChartOutlined';
import axios from "axios";

const structDB = await axios.get("http://localhost:4000/api/getStruct")
    .then((response) => {
        return response.data.success ? setStructDB(response.data.result) : [];
    }
    ).catch((error) => {
        console.log(error);
    });

function setStructDB(data) {
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
        }
        if (item.child) {
            item.child = setStructDB(item.child);
        }
    });
    
    return data;
};

export default structDB;