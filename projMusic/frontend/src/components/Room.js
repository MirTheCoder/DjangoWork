import React, { Component } from "react";
import { useParams, Link } from "react-router-dom";
import { Grid, Button, Typography} from "@mui/material"
import CreateRoomPage from "./CreateRoomPage";
import CreateRoomPageWrapper from "./CreateRoomPage";

class Room extends Component {
    constructor(props) {
        super(props);
        this.state = {
            votesToSkip: 2,
            guestCanPause: false,
            isHost: false,
            showSettings: false,
            spotifyAuthenticated: false,
        };
        //We get the room code that is passed into our props and store it as the room code for this page
        this.roomCode = props.roomCode;
        //We call this function in order to receive all the room details based off of that code
        this.getRoomDetails()// passed from wrapper
        this.leaveButtonPressed = this.leaveButtonPressed.bind(this)
        this.updateShowSettings = this.updateShowSettings.bind(this)
        this.renderSettingsButton = this.renderSettingsButton.bind(this)
        this.renderSettings = this.renderSettings.bind(this)
        this.getRoomDetails = this.getRoomDetails.bind(this)
        this.getRoomDetails()
        this.authenticateSpotify = this.authenticateSpotify.bind(this)
    }

    leaveButtonPressed(){
        const requestOptions = {
            method: "POST",
            headers: {'Content-Type': 'application/json'}
        };
        fetch('/api/leave-room', requestOptions
        ).then((response) =>{
            if (response.ok){
                /* after the user leaves the room, we will remove the room code from our homepage component so that
                * the user does not accidentally get redirected back to the room page after leaving the room*/
                this.props.leaveRoomCallBack();
                window.location.href = "/"
            } else {
                console.log("You are not currently in a room")
            }

        }).catch((error) => {
            console.log(error)
        })
    };

    getRoomDetails() {
        //Here we have the call to the api, sending it the room code in exchange for the information pertaining to the
        //room with that code
        fetch("/api/get-room?code=" + this.roomCode)
            .then((response) => {
                /* If we don't get a match for the roomCode, then we will just send the user back to the home page*/
                if(!response.ok){
                    this.props.leaveRoomCallBack();
                    window.location.href = "/"
                }
                /* make sure to jsonify the response in order to obtain the data from it*/
                return response.json()
            }).then((data) => {
                console.log(data)
                this.setState({
                    votesToSkip: data.votes_to_skip,
                    guestCanPause: data.guest_can_pause,
                    isHost: data.is_host,
                });
                if(this.state.isHost) {
                    this.authenticateSpotify()
                }
            });
    }

    updateShowSettings(value){
        this.setState({
            showSettings: value
        })
    }
    /* We are doing an arrow function for the onclick for the button so that the button will only render once the
    * function modifies the showSettings*/
    renderSettingsButton(){
        return(
            <Grid item xs={12} align="center">
                <Button variant="contained" color="primary" onClick={() => this.updateShowSettings(true)}>
                    Settings
                </Button>
            </Grid>
        )
    }

    renderSettings(){
        return(
            <Grid container spacing={1} direction="column">
                <Grid item xs={12} align="center">
                    <CreateRoomPageWrapper update={true} votesToSkip={this.state.votesToSkip}
                                           guestCanPause={this.state.guestCanPause}
                    roomCode={this.roomCode} updateCallBack={this.getRoomDetails}/>
                </Grid>
                <Grid item xs={12} align="center">
                    <Button variant="contained" color="secondary" onClick={() => this.updateShowSettings(false)}>
                        Close
                    </Button>
                </Grid>
            </Grid>
        )
    }

    authenticateSpotify(){
        /* Here we are going to check and see if the user is authenticated or not*/
        fetch('/spotify/is-authenticated').then((response) => response.json
        ).then((data) =>{
            /* set the spotify is authenticated state to whatever the api call gives us*/
            this.setState({
                spotifyAuthenticated: data.status
            })
            /* if the user is not authenticated, then we will authenticate them */
            if(!data.status){
                fetch('/spotify/get-auth-url'
                ).then((response) => response.json()
                ).then((data) => {
                    console.log("you have now been authenticated")
                    /* Here we will redirect the user to the spotify callback */
                    window.location.replace(data.url)
                })
            } else {
                console.log("True")
            }
        })
    }

    render() {
        if(this.state.showSettings){
            return this.renderSettings()
        }
        return (
            <Grid container spacing={1} direction="column">
                <Grid item xs={12} align='center'>
                    <Typography variant="h4" component="h4">
                        Code: {this.roomCode}
                    </Typography>
                </Grid>
                <Grid item xs={12} align='center'>
                    <Typography variant="h6" component="h6">
                        Votes: {this.state.votesToSkip}
                    </Typography>
                </Grid>
                <Grid item xs={12} align='center'>
                    <Typography variant="h6" component="h6">
                        Guest Can Pause: {this.state.guestCanPause.toString()}
                    </Typography>
                </Grid>
                <Grid item xs={12} align='center'>
                    <Typography variant="h6" component="h6">
                        Is Host: {this.state.isHost.toString()}
                    </Typography>
                </Grid>
                {this.state.isHost ? this.renderSettingsButton() : null}
                <Grid item xs={12} align='center'>
                    <Button color="secondary" variant="contained" onClick={this.leaveButtonPressed}>
                        Leave Room
                    </Button>
                </Grid>
            </Grid>

        );
    }
}

/* We use this function to pass the room code into our component*/
/* make sure to add props as a parameter so that you can pass the data and if that we receive from the homepage.js
* to the Room.js file */
export default function RoomWrapper(props) {
    const { roomCode } = useParams();
    /* This will allow us to ensure that we pass the function from the homepage.js to our Room component*/
    return <Room {...props} roomCode={roomCode} />;
}
