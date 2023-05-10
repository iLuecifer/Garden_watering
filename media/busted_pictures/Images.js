import React, { useState, useEffect } from 'react';

export default function ImageList() {
    const [images, setImages] = useState([]);

    useEffect(() => {
        fetch('http://127.0.0.1:8999/api/images/')
            .then(response => response.json())
            .then(data => setImages(data.images))
            .catch(error => console.error(error));
    }, []);

    return (
        <div>
        {images.map(image => (
            <div key={image.name}>
                <img src={'http://127.0.0.1:8999/media/busted_pictures/' + image.name} alt={image.name} />
                <p>{image.name}</p>
            </div>
        ))}
    </div>
    
    
    
    );
}

