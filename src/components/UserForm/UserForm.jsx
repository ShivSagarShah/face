import react, { useState, useEffect, useRef } from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import InputLabel from '@mui/material/InputLabel';
import InputAdornment from '@mui/material/InputAdornment';
import AccountCircle from '@mui/icons-material/AccountCircle';
import PhotoCamera from '@mui/icons-material/PhotoCamera';
import RestartAltIcon from '@mui/icons-material/RestartAlt';
import IconButton from '@mui/material/IconButton';
import Grid from '@mui/material/Grid';
import axios from 'axios';
import Alert from '@mui/material/Alert';
import "./style.css";
const UserForm = ({ form }) => {
    const [username, setUsername] = useState("");
    const [imageData, setImageData] = useState(null);
    const [message, setMessage] = useState(null);
    const [severity, setSeverity] = useState(null);
    const canvasRef = useRef(null);
    const videoRef = useRef(null);
    const [streamTracks, setStreamTracks] = useState(null);
    const [streamInterval, setStreamInterval] = useState(null);
    const handleSubmit = (e) => {
        e.preventDefault();
        axios.post(`http://localhost:5000/${form.toLowerCase()}`, { username, "imageData": imageData }).then((res) => {
            if (res.data.success) {
                setMessage(res.data.message);
                setSeverity("success");
            } else {
                setMessage(res.data.message);
                setSeverity("error");
            }
        }).catch((err)=>{
            setMessage("Something went wrong");
            setSeverity("error");
        })
    }

    const start = () => {
        if (canvasRef.current) {
            setImageData(null);
            const canvas = canvasRef.current;
            const ctx = canvas.getContext("2d");
            ctx.fillStyle = "black";
            ctx.fillRect(0, 0, 300, 300);
            const usermedia = navigator.mediaDevices.getUserMedia({ video: { width: 300, height: 300, frameRate: { ideal: 20, max: 30 } } });
            usermedia.then((stream) => {
                videoRef.current.srcObject = stream;
                videoRef.current.play();
                setStreamTracks(stream);
                let sI = setInterval(() => {
                    ctx.drawImage(videoRef.current, 0, 0, 300, 300);
                }, 1000 / 30);
                setStreamInterval(sI);
            })
        }
    }
    const capture = () => {
        // Stop Video
        if (streamInterval) {
            let si = streamInterval;
            clearInterval(si);
            setStreamInterval(null);
        }
        if (streamTracks) {
            let st = streamTracks;
            st.getTracks()[0].stop();
            setStreamTracks(null);
        }
        if (videoRef.current) {
            videoRef.current.srcObject = null;
        }
        if (canvasRef.current) {
            let ctx = canvasRef.current.getContext("2d");
            let img = ctx.getImageData(0, 0, 300, 300);
            let data = img.data.filter((_, i) => (i + 1) % 4);
            setImageData(data);
        }
    }
    useEffect(() => {
        start();
    }, [])
    return (
        <div className="user_form">
            <form action="" onSubmit={handleSubmit}>
                <Grid container spacing={2}>
                    <video ref={videoRef} style={{ display: "none" }}></video>
                    <Grid item md={12} textAlign="center" variant="primary">
                        <h1>{form} Form</h1>
                    </Grid>
                    <Grid item md={12}>
                        <InputLabel color="primary">Username</InputLabel>
                        <TextField
                            id="username"
                            fullWidth
                            InputProps={{
                                startAdornment: (
                                    <InputAdornment position="start">
                                        <AccountCircle color="primary" />
                                    </InputAdornment>
                                ),
                            }}
                            size="standard"
                            variant="standard"
                            onChange={(e) => { setUsername(e.target.value) }}
                            value={username}
                        />
                    </Grid>
                    <Grid item md={12} textAlign="center" justifyContent={"center"}>
                        <canvas width={300} height={300} ref={canvasRef}>

                        </canvas>
                        <br />
                        {
                            (
                                imageData ?
                                    <IconButton color="primary" aria-label="upload picture" component="label" onClick={start}>
                                        <RestartAltIcon />
                                    </IconButton>
                                    :
                                    <IconButton color="primary" aria-label="upload picture" component="label" onClick={capture}>
                                        <PhotoCamera />
                                    </IconButton>
                            )
                        }
                    </Grid>
                    <Grid item md={12} textAlign="center" justifyContent={"center"}>
                        <Button variant="contained" type="submit" onClick={handleSubmit} disabled={!Boolean(username && imageData)}>Submit</Button>
                    </Grid>
                    {
                        (

                            message && severity ?
                                <Grid item md={12} textAlign="center" justifyContent={"center"}>
                                    <Alert severity={severity}>{message}</Alert>
                                </Grid> : null
                        )
                    }
                </Grid>
            </form>
        </div>
    )
};

export default UserForm;