/* We are going to import the Component class from our React module that we installed via npm*/
/* The import system in javascript is like python but in reverse and the item being imported must be put within "{ }"*/
import React, { Component } from "react";
/* instead of using 'import { render } from "react-dom";" since we are using react 19 we have to use the import below*/
import { createRoot } from 'react-dom/client';


/* Here we will be setting up an App class that extends to the parent class Component
* and we are also making this class the default export of this file */
export default class App extends Component{
    /* Here is our constructor that takes in one argument in order to create an instance of this class*/
    constructor(props) {
        super(props);
    }


    render(){
        return(<h1>Testing the React Code</h1>)
    }
}

/* This will get the div with element id "app" and render the stuff within our React file in the div class*/
const appDiv = document.getElementById('app')
/* This creates a root to the div class that we will input the stuff in our React file into when we render the page */
const root = createRoot(appDiv)
/* Here we are just placing the App class in the div class in our index html labeled app so that whatever we render
* in our App class will be rendered in the div class*/
root.render(<App />, appDiv)