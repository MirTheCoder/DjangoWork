import React, { Component } from "react";

export default class Room extends Component {
    constructor(props) {
        super(props);
        this.state = {
            votesToSkip: 2,
            guestCanPause: false,
            isHost: false,
        }
        /* This will allow us to get the room code of the room from the code variable that is passed into
        * the url */
        this.roomCode = this.props.match.params.roomCode
    }
    render() {
            return <div>
                <h3>{this.roomCode}</h3>
                <p>Votes: {this.state.votesToSkip}</p>
                <p>Guest Can Pause: {this.state.guestCanPause}</p>
                <p>is Host: {this.state.isHost}</p>
            </div>
        }
}