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
/* Allows you to show something on the screen*/
import  Collapse  from "@mui/material/Collapse"
/* Alert has been moved to the '@mui/material' package instead of the '@mui/lab' package */
import Alert from "@mui/material/Alert"
/* Component that will be used for creating a room*/


class CreateRoomPage extends Component{

    defaultVotes = 2;
    constructor(props) {
        super(props);
        /* what this.state does is that whenever the fields within the component are updated, this.state will force
        * the component to update its values according to the users input, and when the user clicks create room,
        * it will then save the values that the user had inputted */
        this.state = {
            guestCanPause: true,
            votesToSkip: this.defaultVotes,
            successMsg: false,
            errorMsg: false,
            admit: false
        }
        /* binding the method to this class allows whatever value that calls the button press method to have access to
        * the 'this' keyword*/
        this.handleRoomButtonPressed = this.handleRoomButtonPressed.bind(this)
        this.handleVotesChange = this.handleVotesChange.bind(this)
        this.handleGuestCanPauseChange = this.handleGuestCanPauseChange.bind(this)
        this.renderUpdateButtons = this.renderUpdateButtons.bind(this)
        this.renderCreateButton = this.renderCreateButton.bind(this)
        this.handleUpdateButtonPressed = this.handleUpdateButtonPressed.bind(this)
        this.handleAdmitChange = this.handleAdmitChange.bind(this)
        if(props.update){
            this.update = props.update
        }
        if(props.votesToSkip){
            this.setState({
                votesToSkip: props.votesToSkip
            })
        }
        if(props.guestCanPause){
            this.setState({
                guestCanPause: props.guestCanPause
            })
        }
        if(props.roomCode){
            this.roomCode = props.roomCode
        }
        if(props.admit){
            this.setState({
                admit: props.admit
            })
        }
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

            handleAdmitChange(e) {
                this.setState({
                    /* Checks to see if the string input is true, and if not then we will set guestCanPause to false*/
                   admit: e.target.value === "true",
                });
            }

            handleRoomButtonPressed(){
                const requestOptions = {
                    method: 'POST',
                    /* This just tells us the type of data we are passing via request*/
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        votes_to_skip: this.state.votesToSkip,
                        guest_can_pause: this.state.guestCanPause,
                        admit_required: this.state.admit,
                    }),
                };
                /* here is where we call the create room method from the frontend and feed it the data that the user has
                * typed in so that the api cna create the room*/
                fetch('/api/create-room', requestOptions)
                .then((response) => {
                    console.log("Raw request body:", response.body)
                    return response.json()
                })
                .then((data) => {
                    console.log("Parsed request data:", data)
                    window.location.href="/room/" + data.code
                }).catch((error) => console.error('Error:', error));

            }

    renderCreateButton(){
        return(<Grid container spacing={1} direction="column">
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
        </Grid>)
    }

    handleUpdateButtonPressed(){
        const requestOptions = {
                    method: 'PATCH',
                    /* This just tells us the type of data we are passing via request*/
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        votes_to_skip: this.state.votesToSkip,
                        guest_can_pause: this.state.guestCanPause,
                        code: this.roomCode,
                        admit: this.state.admit,
                    }),
                };
                /* here is where we call the create room method from the frontend and feed it the data that the user has
                * typed in so that the api cna create the room*/
                fetch('/api/update-room', requestOptions)
                .then((response) => {
                    if(response.ok) {
                        this.setState({
                            successMsg: "Room Updated successfully"
                        })
                    } else{
                        this.setState({
                            errorMsg: "Error updating room..."
                        })
                        console.log("You are not authorized to edit this room")
                    }
                    /* Make sure to add this within the last '.then' statement so that it doesn't mess up the
                    * fetch method*/
                    this.props.updateCallBack()
                })


    }

    renderUpdateButtons(){
        return(
            <Grid item xs={12} align="center">
                    <Button color="primary" variant="contained" onClick={this.handleUpdateButtonPressed}>
                        Update Room
                    </Button>
                </Grid>
        )
    }

    render(){

        const title = this.props.update ? "Update Room" : "Create A Room"
        /* A grid is used in material UI to align items horizontally or vertically, (kind of like flexbox in css)*/
        /* This by default would align the items vertically and the spacing shows how much space we put between each
        * item in the Grid. (1 means 8 pixels, 2 means 16 pixels, 3 means 32 pixels, and so on*/
        return (
            <Grid container direction="column" spacing={2}>
            {/* When the size of the screen is extra small, then we want to let the computer know that this item should
            *be size 12. We basically are using this to fill out the maximum grid space */}
                <Grid item xs={12} align='center'>
                <Collapse in={Boolean(this.state.errorMsg) || Boolean(this.state.successMsg)}>
                    {this.state.successMsg ?
                        (<Alert severity="success" onClose={() => {this.setState({successMsg: false})}}>{this.state.successMsg}</Alert>): (<Alert severity="error" onClose={() => {this.setState({errorMsg: false})}}>{this.state.errorMsg}</Alert>)}
                </Collapse>
            </Grid>
            <Grid item xs={12} align='center'>
                {/* This is used to create a title for the page rendering */}
                <Typography component= 'h4' variant='h4'>
                    {title}
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
                    <RadioGroup row defaultValue={this.state.guestCanPause.toString()} onChange={this.handleGuestCanPauseChange}>
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
                    {/* This will handle the users choice for whether not they would want a public or private room*/}
                    <FormHelperText>
                        <div align="center">
                            Control of room being public or private
                        </div>
                    </FormHelperText>
                    <RadioGroup row defaultValue={this.state.admit.toString()} onChange={this.handleAdmitChange}>
                        {/* We use this to add a label to our radio buttons*/}
                        {/* We will have two radio buttons with one having a value of true and one being false
                        that they don't have control*/}
                        <div align="center">
                        <FormControlLabel value="true" control={<Radio color="primary"/>} label="private"
                        labelPlacement="bottom">
                        </FormControlLabel>
                        {/* In this one we are creating a button that the user cna select if they don't want the users to have
                        control over pausing or playing the music*/}
                        <FormControlLabel value="false" control={<Radio color="secondary"/>} label="public"
                        labelPlacement="bottom">
                        </FormControlLabel>
                        </div>

                    </RadioGroup>
                </FormControl>
            </Grid>
                <Grid item xs={12} align='center'>
                    {/* This is where we will have the user input the number of votes needed to skip a song*/}
                    {/* Form control is like a form wrapper that wraps elements that require user input and collect
                    data input by the user*/}
                    <FormControl>
                        <TextField required={true} type={"number"} onChange={this.handleVotesChange}
                                   defaultValue={this.state.votesToSkip}
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
                {this.update ? this.renderUpdateButtons() : this.renderCreateButton()}
            </Grid>

        );
    }
}

export default function CreateRoomPageWrapper(props){
    return <CreateRoomPage {...props} />
}