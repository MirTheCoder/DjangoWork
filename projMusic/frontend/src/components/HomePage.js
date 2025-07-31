import React, { Component } from "react";
import RoomJoinPage from "./RoomJoinPage";
import CreateRoomPage from "./CreateRoomPage";
/* Make sure to use this BrowserRouter import format to import the React routes if you are using react-router-dom v6 or
* higher */
import { BrowserRouter as Router, Routes, Route, Link, Redirect, Navigate} from "react-router-dom"
import Room from "./Room";
/* We will need this in order to obtain any functions that are passed from the home page into the components rendering*/
import RoomWrapper from "./Room";
import {ButtonGroup, Button, Grid, Typography} from '@mui/material';
import CreateRoomPageWrapper from "./CreateRoomPage";
/* Make sure to import your components with the first letter being upper case*/
import Info from "./info"
/* This component will be used to render our homepage */
export default class HomePage extends Component {

  constructor(props) {
    super(props);
    this.state = {
      /* Since we have '/room/roomCode' as one of our routes, we have to set the roomCode equal to null so that
      * we are not redirected to the room page yet, until the user joins a room, so tha then the user will instantly be
      * redirected to the room they are in when the home page is rendered*/
      roomCode: null
    }
    this.clearRoomCode = this.clearRoomCode.bind(this)
  }

  /* This is a life cycle method that allows us to make an action before the page renders.
  * We add async so that this function can run in the background, allowing the component
  * to continue on with other processes*/
  /*async componentDidMount(){
    fetch('/api/user-in-room'
    ).then((response) => response.json()
    ).then((data) => {
      this.setState({
        roomCode: data.code
      })
    })
  }*/

  /* This will allow us to reset the room code to null for the homepage's 'this.roomCode' */
  clearRoomCode(){
    this.setState({
      roomCode: null,
    })
  }

  /* Here we have created a function called renderHomepage which holds the details that we want to render from this
  * component. We will call it from the render itself in order to fill out the information of our render with
  * what we have inside of this function*/
  renderHomePage(){
/* Make sure to add "direction='column' " in order to organize the grid vertically */
    return(

        <Grid container spacing={3} direction="column">
          <Grid item xs={12} align='center'>
            <Typography variant="h3" component="h3">
              House Party
            </Typography>
          </Grid>
          <Grid item xs={12} align='center'>
            <ButtonGroup disableElevation variant="contained" color="primary">
              <Button color="primary" to='/join' component={Link}>
                Join a Room
              </Button>
              <Button color="default" to='/info' component={Link}>
                Info
              </Button>
              <Button color="secondary" to='/create' component={Link}>
                Create a Room
              </Button>
            </ButtonGroup>
          </Grid>
        </Grid>
    );
  }

  render() {
    return (
      <Router>
        <Routes>
          <Route
          path="/"
          element={
            this.state.roomCode
              ? <Navigate to={`/room/${this.state.roomCode}`} />
              : this.renderHomePage()
          }
        />
          <Route path='/join' element={<RoomJoinPage />} />
          <Route path='/info' element={<Info/>}/>
          <Route path='/create' element={<CreateRoomPageWrapper />} />
            {/* the '/:' just notifies the computer that an argument or variable will be passed in the url request*/}
            <Route
                path='/room/:roomCode'
                element={<RoomWrapper leaveRoomCallBack={this.clearRoomCode} />}
            />
        </Routes>
      </Router>
    );
  }
}