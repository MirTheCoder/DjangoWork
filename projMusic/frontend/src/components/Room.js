import React, { Component } from "react";
import { useParams } from "react-router-dom";

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
    }



    getRoomDetails() {
        //Here we have the call to the api, sending it the room code in exchange for the information pertaining to the
        //room with that code
        fetch("/api/get-room?code=" + this.roomCode)
            .then((response) => response.json())
            .then((data) => {
                this.setState({
                    votesToSkip: data.votes_to_skip,
                    guestCanPause: data.guest_can_pause,
                    isHost: data.is_host,
                });
            });
    }

    render() {
        return (
            <div>
                <h3>{this.roomCode}</h3>
                <p>Votes: {this.state.votesToSkip}</p>
                <p>Guest Can Pause: {this.state.guestCanPause.toString()}</p>
                <p>Is Host: {this.state.isHost.toString()}</p>
            </div>
        );
    }
}

/* We use this function to pass the room code into our component*/
export default function RoomWrapper() {
    const { roomCode } = useParams();
    return <Room roomCode={roomCode} />;
}
