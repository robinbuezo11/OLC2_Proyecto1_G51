import { useState, useEffect, useRef } from 'react'
import Dropdown from './Dropdown'

const TopbarItem = ({item, depthLevel, props}) => {
    const [dropdown, setDropdown] = useState(false)
    let ref = useRef();
    const func = props[item.id];

    useEffect(()=>{
        const handler = (event) => {
            if (dropdown && ref.current && !ref.current.contains(event.target)) {
                setDropdown(false);
            }
        };
        document.addEventListener("mousedown", handler);
        document.addEventListener("touchstart", handler);
        return () => {
            document.removeEventListener("mousedown", handler);
            document.removeEventListener("touchstart", handler);
        };
    }, [dropdown]);

    const onMouseEnter = () => {
        window.innerWidth > 960 && setDropdown(true)
    };

    const onMouseLeave = () => {
        window.innerWidth > 960 && setDropdown(false)
    };

    return (
        <li
            className="menu-items"
            onMouseEnter={onMouseEnter}
            onMouseLeave={onMouseLeave}
            ref={ref}
        >
            {
                item.items ? (
                    <>
                        <button 
                            type = "button" 
                            aria-haspopup = "menu" 
                            aria-expanded = {dropdown  ? "true" : "false"}
                            onClick={()=> setDropdown(!dropdown)}
                        >
                            {item.label + " "}
                            {depthLevel > 0 ? <span> &raquo; </span> : <span className='arrow' />}
                        </button>
                        <Dropdown depthLevel={depthLevel} dropdown={dropdown} submenus={item.items} props={props} />
                    </>
                ) : (
                    func ?  <a href='/#' onClick={func}>{item.label}</a>
                    :   <a href='/#'>{item.label}</a>
                )

            }
        </li>
    )
}

export default TopbarItem