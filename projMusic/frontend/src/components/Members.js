import React, {Component} from "react";
import { useParams, Link } from "react-router-dom";
import { Grid, Button, Typography} from "@mui/material"
import CreateRoomPage from "./CreateRoomPage";
import CreateRoomPageWrapper from "./CreateRoomPage";
import MusicPlayerWrapper from "./MusicPlayer"
import RoomWrapper from "./Room";


class Members extends Component {
    constructor(props) {
        super(props);
        this.state = {
            members : {}
        }
        this.roomCode = this.props.roomCode
        this.backButtonPressed = this.backButtonPressed.bind(this)
        this.getUsersInRoom = this.getUsersInRoom.bind(this)
    }
    /* Every second we will check and see the members within the room*/
    componentDidMount() {
        this.interval = setInterval(() => {
                this.getUsersInRoom();
            }, 1000);
    }

    componentWillUnmount() {
        clearInterval(this.interval)
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
                    console.log("Unable to receive valid response ")
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

    /* Here we are going to return a list of users within the room*/
    renderUsersInRoom(){
        const items = []
        for (let i = 0; i < this.state.members.length; i++) {
            items.push(
                <li value={this.members[i]} key={i}>User {this.members[i]}</li>
            );
        }
        return (
            <Grid item xs={12} align="center">
            <div>
                <ul>{items}</ul>
            </div>
            </Grid>
        )
    }

    backButtonPressed(){
        fetch("room/" + this.roomCode).then((response) => response.json())
            .then((data) => {
                console.log(data)
            })
            .catch((error) => {
                console.log("Error:", error)
            })
    }

    render() {
        return(
            <Grid container spacing={1} direction="column">
                {/* This will ensure that we will display the member list only if the room has at least one member in it*/}
                {this.members ? this.renderUsersInRoom():
                    <Grid item xs={12} align="center">
                        <Typography component="h4" variant="h4">
                            You currently have no users in the room
                        </Typography>
                    </Grid>}
                <Grid items xs={12} align="center">
                    <Button color="primary" variant="contained" onClick={this.backButtonPressed}>
                        Back
                    </Button>
                </Grid>
            </Grid>
        )
    }

}



export default function MembersWrapper(props){
    return <Members {...props} />;
}