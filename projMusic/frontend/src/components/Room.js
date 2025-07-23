import React, { Component } from "react";
import { useParams, Link } from "react-router-dom";
import { Grid, Button, Typography} from "@mui/material"

class Room extends Component {
    constructor(props) {
        super(props);
        this.state = {
            votesToSkip: 2,
            guestCanPause: false,
            isHost: false,
        };
        //We get the room code that is passed into our props and store it as the room code for this page
        this.roomCode = props.roomCode;
        //We call this function in order to receive all the room details based off of that code
        this.getRoomDetails()// passed from wrapper
        this.leaveButtonPressed = this.leaveButtonPressed.bind(this)
    }

    leaveButtonPressed(){
        const reqeustOptions = {
            method: "POST",
            heders: {'Content-Type': 'application/json'}
        };
        fetch('/api/leave-room', reqeustOptions
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
                    this.props.leaveRoomCallback();
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
            });
    }

    render() {
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
export default function RoomWrapper() {
    const { roomCode } = useParams();
    return <Room roomCode={roomCode} />;
}
