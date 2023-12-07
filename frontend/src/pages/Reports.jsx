import '../styles/Reports.css';
import axios from 'axios';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';


function Reports(){
    const [route, setRoute] = useState('');
    const [images, setImages] = useState([]); 

    const [selectedImage, setSelectedImage] = useState(null); 
    const [modalOpen, setModalOpen] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = (e) => {
        e.preventDefault();
        axios.get('http://18.117.141.89:8000/api/getPics?path=' + route)
            .then((response) => {
                if(response.data.status === 'success'){
                    setImages(response.data.result.sort((a, b) => a.name.localeCompare(b.name)));
                } else {
                    alert(response.data.error);
                }
            }).catch((error) => {
                alert(error);
            });
    }

    const handleLogout = (e) => {
        e.preventDefault();
        axios.post('http://18.117.141.89:8000/api/logout')
            .then((response) => {
                if(response.data.status === 'success'){
                    navigate('/');
                } else {
                    alert(response.data.error);
                    navigate('/');
                }
            }).catch((error) => {
                alert(error);
            });
    }

    const handleImageClick = (image) => {
        setSelectedImage(image);
        setModalOpen(true); 
    }


    return (
        <div className='reports'>
            <div className="header-reports">
                <input className='input-search' type="text" placeholder="Ruta" value={route} onChange={(e) => {setRoute(e.target.value)}}/>
                <button className="button-search" onClick={handleSubmit}>Buscar</button>
                <button className="button-warning" id='btn-logout' onClick={handleLogout}>Cerrar Sesión</button>
            </div>
            <div className="body-reports">
                {images.map((image, index) => (
                    <div className="image-container" onClick={() => handleImageClick(image)}>
                        <div key={index}>
                            <img className='image' src={`data:${image.mime};base64,${image.base64}`} alt={image.name}/>
                        </div>
                        <p className='img-name'>{image.name}</p>
                    </div>
                ))}
            </div>
            {modalOpen && selectedImage && (
                <div className="modal">
                    <div className='modal-image'>
                        <img className='image-full' src={`data:${selectedImage.mime};base64,${selectedImage.base64}`} alt={selectedImage.name}/>
                        <button className='button-warning' id='btn-close' onClick={() => setModalOpen(false)}>Cerrar</button>
                    </div>
                </div>
            )}
        </div>
    )
}

export default Reports;