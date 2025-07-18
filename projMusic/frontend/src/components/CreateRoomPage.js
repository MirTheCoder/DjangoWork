import React, { Component } from "react";
import Button from '@mui/material/Button'
import Grid from '@mui/material/Grid'
import Typography from '@mui/material/Typography'
import TextField from '@mui/material/TextField'
import FormHelperText from '@mui/material/FormHelperText'
import FormControl from '@mui/material/FormControl'
import { Link } from 'react-router-dom'
import Radio from '@mui/material/Radio'
import RadioGroup from '@mui/material/RadioGroup'
import FormControlLabel from '@mui/material/FormControlLabel'
import RoomJoinPage from "./RoomJoinPage";
/* Component that will be used for creating a room*/


export default class CreateRoomPage extends Component{

    defaultVotes = 2;
    constructor(props) {
        super(props);
    }

    render(){
        /* A grid is used in material UI to align items horizontally or vertically, (kind of like flexbox in css)*/
        /* This by default would align the items vertically and the spacing shows how much space we put between each
        * item in the Grid. (1 means 8 pixels, 2 means 16 pixels, 3 means 32 pixels, and so on*/
        return <Grid container spacing={1}>
            <!-- When the size of the screen is extra small, then we want to let the computer know that this item should
            be size 12. We basicallly are using this to fill out the maximum grid space-->
            <Grid item xs={12} align='center'>
                <!-- This is used to create a title for the page rendering -->
                <Typography component= 'h4' variant='h4'>
                    Create A Room
                </Typography>
            </Grid>
        </Grid>
    }
}