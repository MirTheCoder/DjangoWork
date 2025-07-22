import React, { Component } from "react";
import {TextField, Button, Grid, Typography} from '@mui/material';
import {Link} from "react-router-dom"
/* Component that will be used for joining a room*/
export default class RoomJoinPage extends Component{
    constructor(props) {
        super(props);
        this.state = {
            roomCode: " ",
            error: " ",
        }
        /* Remember to add this so that you can use the "this" key word to reference the components state */
        this.changeCode = this.changeCode.bind(this);
        this.roomButtonPressed = this.roomButtonPressed.bind(this);
    }

    changeCode(e){
        this.setState({
            roomCode: e.target.value
        })
            this.setState({
                error: " ",
            })

    }

    roomButtonPressed(){
        const requestOptions = {
            method:  'POST',
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                code: this.state.roomCode
            })
        };
        fetch('/api/join-room', requestOptions
        ).then((response) => {
            if (response.ok){
                window.href.location = "/room/" + this.state.roomCode
            } else {
                this.setState({error: "Room Code Not Found"})
                this.setState({roomCode: " "})
            }
        }) . catch((error) => {
            console.log(error);
        })
    }

    render(){
        return <Grid container spacing={1}>
            <Grid item xs={12} align="center">
                <Typography variant="h4" component="h4">
                    Join a Room
                </Typography>
            </Grid>
            <Grid item xs={12} align="center">
                <TextField
                    type={"text"}
                    error = {this.state.error}
                    label="Code"
                    placeholder = "Enter a room code"
                    value={this.state.roomCode}
                    onChange={this.changeCode}
                    helperText={this.state.error}
                    variant="outlined"
                />
            </Grid>
            <Grid item xs={12} align="center">
                <Button variant="contained" color="primary" onClick={this.roomButtonPressed}>
                    Enter Room
                </Button>
            </Grid>
            <Grid item xs={12} align="center">
                <Button variant="contained" color="secondary" to="/" component={Link}>
                    Back
                </Button>
            </Grid>
        </Grid>
    }
}