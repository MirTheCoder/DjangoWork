import React, { Component } from "react";
import { useParams, Link } from "react-router-dom";
import { Grid, Button, Typography} from "@mui/material"
import CreateRoomPage from "./CreateRoomPage";
import CreateRoomPageWrapper from "./CreateRoomPage";
import MusicPlayerWrapper from "./MusicPlayer"

class Room extends Component {
    constructor(props) {
        super(props);
        this.state = {
            votesToSkip: 2,
            guestCanPause: false,
            isHost: false,
            showSettings: false,
            spotifyAuthenticated: false,
            members: {},
            /* Here we will store song within our state*/
            song: {}
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
            this.getCurrentSong = this.getCurrentSong.bind(this)
            this.getUsersInRoom = this.getUsersInRoom.bind(this)
            this.renderUsersInRoom = this.renderUsersInRoom.bind(this)
            this.getRoomDetails();
            this.getCurrentSong();
            this.authenticateSpotify = this.authenticateSpotify.bind(this)
        }

        /* This will allow us to check the details of the current song playing so that we can accurately display the current
        * status of the song within the playlist that we have access to*/
    componentDidMount() {
        /* here we are asking th file to call this.current song every 1000 milliseconds in order for it to provide
        * a routine check on teh song within the users playlist*/
            this.interval = setInterval(() => {
                this.getCurrentSong();
                this.getUsersInRoom()
            }, 1000);
        }


    /* This will be used to stop the interval once the component 'Room.js' is closed or stopped*/
    componentWillUnmount() {
        clearInterval(this.interval);
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

    getCurrentSong(){
        fetch('/spotify/current-song').then((response) => {
            if(!response.ok){
                console.log("No song data")
                return {}
            } else {
                return response.json()
            }
        }).then((data) => {
            this.setState({song: data});
            console.log(data)
        });
    }

    getUsersInRoom(){
        const requestOptions = {
            method: "POST",
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                code: this.roomCode
            }),
        }

        fetch('/api/users-in-room', requestOptions)
            .then((response) => {
                if(response.ok){
                    return response.json()
                }else{
                    return {}
                }

            })
            .then((data) => {
                this.setState({
                    members: data
                })
            }) .catch((error) => {
                console.log("Request was unsuccessful: ", error)
        })
    }

    renderUsersInRoom(){
        const items = []
        for (let i = 0; i < this.members.length; i++) {
            items.push(
                <li value={this.members[i]} key={i}>User {this.members[i]}</li>
            );
        }
        return(
            <div>
                <ul>items</ul>
            </div>
        )
    }

    getRoomDetails() {
        //Here we have the call to the api, sending it the room code in exchange for the information pertaining to the
        //room with that code
        fetch("/api/get-room?code=" + this.roomCode)
            .then((response) => {
                /* If we don't get a match for the roomCode, then we will just send the user back to the home page*/
                if(!response.ok){
                    console.log("Room Not Found")
                    this.props.leaveRoomCallBack();
                    window.location.href = "/"
                } else {
                    /* make sure to jsonify the response in order to obtain the data from it*/
                    return response.json()
                }
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
        fetch('/spotify/is-authenticated').then((response) => response.json()
        ).then((data) =>{
            /* set the spotify is authenticated state to whatever the api call gives us*/
            this.setState({
                spotifyAuthenticated: data.status
            })
            console.log("Already Authenticated")
            /* if the user is not authenticated, then we will authenticate them */
            if(data.status){
                console.log(data.status)
            } else {
                fetch('/spotify/get-auth-url'
                ).then((response) => response.json()
                ).then((data) => {
                    console.log("you have now been authenticated")
                    /* Here we will redirect the user to the spotify callback */
                    window.location.replace(data.url)
                })
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
                {/* This will ensure that we first get the song details before rendering the Music Player*/}
                {this.state.song? (<MusicPlayerWrapper song = {this.state.song}/>):(
                    <Typography>Loading current song...</Typography>
                )
                }
                {this.state.isHost ? this.renderSettingsButton() : null}
                {this.state.members ? this.renderUsersInRoom(): null}
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
