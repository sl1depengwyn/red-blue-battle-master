import React from 'react';
import ReactDOM from 'react-dom';
import {Router, Route } from 'react-router-dom'
import * as serviceWorker from './serviceWorker';
import './index.css';
import board from './components/board/board'

const history = require("history").createBrowserHistory()

ReactDOM.render((
    <Router history={history}>
        <div>
            <Route exact path="/" component={board}/>
        </div>
    </Router>

), document.getElementById('root'));

serviceWorker.unregister();
