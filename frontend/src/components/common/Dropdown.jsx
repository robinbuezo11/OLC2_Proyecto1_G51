import TopbarItem from "./TopbarItem";

const Dropdown = ({submenus, dropdown, depthLevel, props}) => {
    depthLevel = depthLevel + 1;
    const dropdownClass = depthLevel > 1 ? 'dropdown-submenu' : '';


    return (
        <ul className={`dropdown ${dropdownClass} ${dropdown ? "show" : ""}`}>
        {
            submenus.map((submenu, index) => (
              <TopbarItem item={submenu} key={index} depthLevel={depthLevel} props={props}/>
            ))
        }
        </ul>
    )
}

export default Dropdown;
