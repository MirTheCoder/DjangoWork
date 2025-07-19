import React, { Component } from "react";
import RoomJoinPage from "./RoomJoinPage";
import CreateRoomPage from "./CreateRoomPage";
import Room from "./Room";
/* Make sure to use this BrowserRouter import format to import the React routes if you are using react-router-dom v6 or
* higher */
import { BrowserRouter as Router, Routes, Route, Link, Redirect} from "react-router-dom"
import Room from "./Room";
/* This component will be used to render our homepage */
export default class HomePage extends Component {
  render() {
    return (
      <Router>
        <Routes>
          <Route path='/' element={<p>This is the home page</p>} />
          <Route path='/join' element={<RoomJoinPage />} />
          <Route path='/create' element={<CreateRoomPage />} />
            {/* the '/:' just notifies the computer that an argument or variable will be passed in the url request*/}
            <Route path='/room/:roomCode' element={<Room />} />
        </Routes>
      </Router>
    );
  }
}