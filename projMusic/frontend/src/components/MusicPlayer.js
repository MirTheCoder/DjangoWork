import React, { Component } from 'react';
import { Grid, Typography, Card, IconButton, LinearProgress } from "@mui/material";
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import SkipNextIcon from '@mui/icons-material/SkipNext';
import PauseIcon from '@mui/icons-material/Pause';
import {useParams} from "react-router-dom";


class MusicPlayer extends Component{
    constructor(props){
        super(props)
        this.pauseSong = this.pauseSong.bind(this)
    }

    pauseSong(){
        const requestOption = {
            method: 'PUT',
            headers: {"Content-Type": "application/json"},
        };
        fetch("/spotify/pause", requestOption).then((response) => response.json()
        ).then((data) => {
            console.log(data.pause)
        })
    }

    playSong(){
        const requestOption = {
            method: 'PUT',
            headers: {"Content-Type": "application/json"},
        };
        fetch("/spotify/play", requestOption).then((response) => response.json()
        ).then((data) => {
            console.log(data.play)
        });
    }

    skipSong(){
        const requestOptions = {
            method: 'POST',
            headers: {"Content-Type": "application/json"},
        };
        fetch('/spotify/skip', requestOptions);
    }

    render(){
        /* Our linear progress will show how far we are throughout the song, but we need to send it a value
        * out of 100, so we are converting out time stamp and duration proportions into something out 100 so that
        * out linear progress will be able to read it*/
        var songProgress
        if(this.props.song.time) {
             songProgress = (this.props.song.time / this.props.song.duration) * 100
        } else {
            songProgress = 0
        }

        /* Cards are like a nice styled box with rounded off corners that appear on the screen*/
        return(
            <Card>
               <Grid container alignItems="center" direction="column">
                   {/* We have xs = to 4 so that the album cover is aligned to the left, takes up 1/3 of the grid*/}
                   <Grid item align="center" xs={4}>
                       <img src={this.props.song.image_url?this.props.song.image_url: null} height="80%" width="80%"/>
                   </Grid>
                   {/* This will take up 2/3 of the grid*/}
                   <Grid item align="center" xs={8}>
                       <Typography component="h5" variant="h5">
                           {this.props.song.title?this.props.song.title: "Title Not Given"}
                       </Typography>
                       <Typography color="textSecondary" variant="subtitle1">
                           {this.props.song.artist?this.props.song.artist: "Artist Not Provided"}
                       </Typography>
                       <div>
                           <IconButton onClick={() => {this.props.song.is_playing?this.pauseSong() : this.playSong()}}>
                               {this.props.song.is_playing ? <PauseIcon/>: <PlayArrowIcon/>}
                           </IconButton>
                           {/* We use the arrow functions in order to bypass needing to bind our function to the this key word so that we can by default just use the this keyword*/}
                            <IconButton onClick={() => this.skipSong()}>
                               {<SkipNextIcon/>}  {this.props.song.votes}/{this.props.song.votes_required}
                           </IconButton>
                       </div>
                   </Grid>
               </Grid>
               <LinearProgress variant="determinate" value={songProgress}/>
            </Card>
        )
    }
}

export default function MusicPlayerWrapper(props){
    return <MusicPlayer {...props}/>
}