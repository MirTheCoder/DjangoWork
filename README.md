Required pip installations for Django Projects
1. django-crispy-forms
2. django
3. pillow
4. crispy-bootstrap4

Required Steps for projAuction
1. If you are using Python interpreter 3.12 or higher, make sure to open your terminal and run "/Applications/Python\ 3.12/Install\ Certificates.command, to manually install the required certifications for using Gmail from your website to send stuff
2. You will also need to generate an app password that you will use as your Gmail account (the one you will allow your website to use to send emails) password for the website to have access to.
3. Here is the link to generate the required app password: https://myaccount.google.com/apppasswords

Required Pip Installations for projMusic
1. django
2. rest_framework
3. You need to install Node.js and npm(Node Package Manager), use this link to install [
](https://nodejs.org/)
- Run "npm -v" and "node -v" to make sure that you have successfully installed both packages (if installed correctly, this should return the version of each)
- Make sure to run in terminal "npm init -y" to have npm create all the necessary modules needed for the frontend project
- Also, in terminal, make sure to run "npm install webpack webpack-cli --save-dev" to install webpack, which will be needed to bundle all our JavaScript into one file
- Next, we need to go into the terminal and run "npm i @babel/core babel-loader @babel/preset-env @babel/preset-react --save-dev"
, which will be required to translate our code so that it can also run on older browsers
-Next, you need to run "npm install react@18.2.0 react-dom@18.2.0" to install React itself
- Next, install "npm install @material-ui/core" for some built-in webpage styling  (install "npm install @mui/material @emotion/react @emotion/styled
"If you are using React 18 or 19, as the new Reacts need the newer version of Material UI
- Next, you need to install "npm install @babel/plugin-proposal-class-properties" to use async and await in our JavaScript code
- Next, we will install "npm install react-router-dom@6.11.2", which will allow us to reroute our pages so that we can navigate to different pages from React
- Next, we need to install "npm install @mui/icons-material" to get the icons required
- Next, we need to install "npm install @mui/lab" to create alerts in our renderings
- Next, install 'python-dotenv' by running "pip install python-dotenv"


More on ProjMusic
- Make sure to change your directory to the frontend app within your project (your package.json file and package-lock.json should both be in that frontend app file) before you run "npm run dev" or anything
  with npm
- Make sure that when you are installing react and react-dom, you are installing a version no newer or later than 18.2, since that is the latest version that is stable enough for this project. If you installed anything higher, you can run "npm install react@18.2.0 react-dom@18.2.0" to replace the newer version that you were using
- Also, make sure to delete mode_modules and package.jason-lock if you had accidentally installed the newest version of React and installed a downgrade to fix the issue. Once you delete both, reinstall by typing "npm install"
- To run on the local network or to allow connections to this website from other devices, run "python manage.py runserver 0.0.0.0:8000"

  
- Remember, to add the client_id and client_secret as environment variables, you can do this by creating a .env text file, which will hold all the true values of your variables
- Write this:

from dotenv import load_dotenv
import os

load_dotenv()

-to load all the environment variables within your .env file

Connection with Spotify:
- Make sure to register your application with Spotify to request and access data on Spotify
- You then also need to have the users of your application grant the application access to their Spotify data
- When registering your application with Spotify, you need to present the scope (basically what exact info you want to get from Spotify) so that the user can grant the information
- When the user gives the application access to their Spotify information, a token is formed so that the application can access their Spotify details whenever they log in


Link to connect or register application with spotify:
https://developer.spotify.com/
