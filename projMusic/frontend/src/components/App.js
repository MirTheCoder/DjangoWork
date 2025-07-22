/* We are going to import the Component class from our React module that we installed via npm*/
/* The import system in javascript is like python but in reverse and the item being imported must be put within "{ }"*/
import React, { Component } from "react";
/* instead of using 'import { render } from "react-dom";" since we are using react 19 we have to use the import below*/
import { createRoot } from 'react-dom/client';
import HomePage from "./HomePage";
import RoomJoinPage from "./RoomJoinPage";
import CreateRoomPage from "./CreateRoomPage";

/* This App javascript file will serve as our base Component where we will render the details stored in other
* components*/


/* Here we will be setting up an App class that extends to the parent class Component
* and we are also making this class the default export of this file */
export default class App extends Component{
    /* Here is our constructor that takes in one argument in order to create an instance of this class*/
    /* we can also pass props from one component to another as well */
    constructor(props) {
        super(props);
    }

    /*This right here is telling our main app component to render the details of our */
    render(){
        /* We must use a div class if we want to return multiple components because we can only technically pass
        * one item into our rendering at a time, so our div class will just basically wrap all the components into
        * one element kind of*/

        /* This is how we can render multiple component pages from our base component page */
        return <div className="center"><HomePage></HomePage></div>
    }
}

/* This will get the div with element id "app" and render the stuff within our React file in the div class*/
const appDiv = document.getElementById('app')
/* This creates a root to the div class that we will input the stuff in our React file into when we render the page */
const root = createRoot(appDiv)
/* Here we are just placing the App class in the div class in our index html labeled app so that whatever we render
* in our App class will be rendered in the div class*/
root.render(<App />, appDiv)