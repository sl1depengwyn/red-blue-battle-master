import React, { Component } from "react";
import '../board/board.css';

class Line extends Component {
    
    componentDidMount (){
    
    }
    render() {
        var stl = '"position: absolute; margin-top: 13px; margin-left:"' + this.props.pos + '%"'
        return(
        <div class="line">
        <img src="./switcher.png" style={{position: absolute, marginTop: 13, marginLeft: this.props.pos}} height="90" width="35"/>
        <img src="./line.png" height="50" width="500" style="margin-top: 40px;"/>
        </div>
        )}
}
export default Line;