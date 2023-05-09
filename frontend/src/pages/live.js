import { useState, useEffect } from "react";

const LiveCam = () => {
  const [videoSrc, setVideoSrc] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("token");
    console.log(token)
    if (token) {
      setVideoSrc(`http://127.0.0.1:8999/api/live/?token=${token}`);
    } else {
      console.error("No token found");
    }
  }, []);

  return (
    <div>
      {videoSrc ? (
        <img src={videoSrc} alt="Live stream" />
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default LiveCam;
