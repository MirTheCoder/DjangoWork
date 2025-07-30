import React, {useState, useEffect} from "react";
import { Grid, Button, Typography, IconButton} from "@mui/material";
import NavigateBeforeIcon from "@mui/icons-material/NavigateBefore"
import NavigateNextIcon from "@mui/icons-material/NavigateNext"
import { Link } from "react-router-dom"

/* this will give our state variable two things which are join and create, which are defined by the value within their
* string*/
const pages = {
    JOIN: "pages.join",
    CREATE: "pages.create",
}
/* This is a functional component*/
export default function Info(props){
    /* Here we put the name of our state and the second thing we put in this array is the function that updates it*/
    /* Use state will provide us the base value or default value for our state variable*/
    const [page, setPage] = useState(pages.JOIN)

    /* When you define the functions within the functional component, they automatically have access to the state
    * variables of the functional component */
    function joinInfo(){
        return "Join page"
    }

    function createInfo(){
        return "Create Info"
    }

    /* This will allow you to automatically run a function once the component is called to render*/
    useEffect(() => {
        console.log("ran");
        /* When we unmount component (or stop rendering the page), this return statement will run which is also need in
        * order to do  unmount*/
        return () => console.log("cleanup");
    }, [page]); /* Make sure to add  the dependencies, even if it is an empty array, in this case you should add
    page so that when you change the contents of page, the useEffect will know that it has to listen for the page change
    in order to mount or unmount*/


    return(
        <Grid container spacing={1} direction="column">
            <Grid item xs={12} align="center" >
                <Typography component="h4" variant="h4">
                    What is House Party
                </Typography>
            </Grid>
            <Grid item xs={12} align="center">
                <Typography variant="body1">
                    {/* Remember to use 3 '=' signs to create a comparison for the state and its values*/}
                    { page === pages.JOIN ? joinInfo(): createInfo()}
                </Typography>
            </Grid>
            <Grid item xs={12} align="center">
                {/* This will be used to call page renderings based on what is showing when the button is clicked*/}
                <IconButton onClick={() => {page === pages.CREATE ? setPage(pages.JOIN): setPage(pages.CREATE)}}>
                    {/* This will show a navigation bar depending on what the page is on or set to*/}
                    {page === pages.CREATE ?
                        (<NavigateBeforeIcon/>)
                        :(<NavigateNextIcon/>)
                    }
                </IconButton>
            </Grid>
            <Grid item xs={12} align="center">
                <Button color="secondary" variant="contained" to="/" component={Link}>
                    Back
                </Button>
            </Grid>
        </Grid>
    )
}