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
        /* what this.state does is that whenever the fields within the component are updated, this.state will force
        * the component to update its values according to the users input, and when the user clicks create room,
        * it will then save the values that the user had inputted */
        this.state = {
            guestCanPause: true,
            votesToSkip: this.defaultVotes
        }
        /* binding the method to this class allows whatever value that calls the button press method to have access to
        * the 'this' keyword*/
        this.handleRoomButtonPressed = this.handleRoomButtonPressed.bind(this)
        this.handleVotesChange = this.handleVotesChange.bind(this)
        this.handleGuestCanPauseChange = this.handleGuestCanPauseChange.bind(this)
    }
    handleVotesChange(e) {
                this.setState({
                    votesToSkip: e.target.value,
                });
            }

            handleGuestCanPauseChange(e) {
                this.setState({
                    /* Checks to see if the string input is true, and if not then we will set guestCanPause to false*/
                   guestCanPause: e.target.value === "true",
                });
            }

            handleRoomButtonPressed(){
                const requestOptions = {
                    method: 'POST',
                    /* This just tells us the type of data we are passing via request*/
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        votes_To_Skip: this.state.votesToSkip,
                        guest_Can_Pause: this.state.guestCanPause,
                    }),
                };
                /* here is where we call the create room method from the frontend and feed it the data that the user has
                * typed in so that the api cna create the room*/
                fetch('/api/create-room', requestOptions). then((response) => response.json()
                ). then((data) => console.log(data))
            }

    render(){
        /* A grid is used in material UI to align items horizontally or vertically, (kind of like flexbox in css)*/
        /* This by default would align the items vertically and the spacing shows how much space we put between each
        * item in the Grid. (1 means 8 pixels, 2 means 16 pixels, 3 means 32 pixels, and so on*/
        return (
            <Grid container direction="column" spacing={2}>
            {/* When the size of the screen is extra small, then we want to let the computer know that this item should
            *be size 12. We basically are using this to fill out the maximum grid space */}
            <Grid item xs={12} align='center'>
                {/* This is used to create a title for the page rendering */}
                <Typography component= 'h4' variant='h4'>
                    Create A Room
                </Typography>
            </Grid>
            <Grid item xs={12} align='center'>
                {/* This is where we will put the form */}
                <FormControl component="fieldset">
                    <FormHelperText>
                        <div align="center">
                            Guest Control of Play Back State
                        </div>
                    </FormHelperText>
                    {/* This is where we will store our radio buttons, and we will have them lined up in a row*/}
                    <RadioGroup row defaultValue="true" onChange={this.handleGuestCanPauseChange}>
                        {/* We use this to add a label to our radio buttons*/}
                        {/* We will have two radio buttons with one having a value of true and one being false
                        that they don't have control*/}
                        <FormControlLabel value="true" control={<Radio color="primary"/>} label="Play/Pause"
                        labelPlacement="bottom">
                        </FormControlLabel>
                        {/* In this one we are creating a button that the user cna select if they don't want the users to have
                        control over pausing or playing the music*/}
                        <FormControlLabel value="false" control={<Radio color="secondary"/>} label="No control"
                        labelPlacement="bottom">
                        </FormControlLabel>

                    </RadioGroup>
                </FormControl>
            </Grid>
                <Grid item xs={12} align='center'>
                    {/* This is where we will have the user input the number of votes needed to skip a song*/}
                    {/* Form control is like a form wrapper that wraps elements that require user input and collect
                    data input by the user*/}
                    <FormControl>
                        <TextField required={true} type={"number"} onChange={this.handleVotesChange}
                                   defaultValue={this.defaultVotes}
                        inputProps={{
                            min:1,
                            style: { textAlign: "center"},
                        }} />
                        <FormHelperText>
                            <div align="center">
                                <b>Votes to Skip A Song</b>
                            </div>
                        </FormHelperText>
                    </FormControl>
                </Grid>
                <Grid item xs={12} align="center">
                    <Button color="secondary" variant="contained" onClick={this.handleRoomButtonPressed}>
                        Create A Room
                    </Button>
                </Grid>
                <Grid item xs={12} align="center">
                    <Button color="primary" variant="contained" to="/" component={Link}>
                        Back
                    </Button>
                </Grid>
            </Grid>

        );
    }
}