import React, { Component } from "react";
import '../board/board.css';

class Task extends Component {
    render() {
        if (this.props.state === 101){
        return (
            <div class='task_up'>
                <h3 class="h">{this.props.name}</h3>
                <h4 class="h">Flags: {this.props.flags} <br/> Uptime: {this.props.uptime}</h4>
            </div>
        )}
        if (this.props.state === 103){
            return (
                <div class='task_mumble'>
                    <h3 class="h">{this.props.name}</h3>
                    <h4 class="h">Flags: {this.props.flags} <br/> Uptime: {this.props.uptime}</h4>
                </div>
            )}
        if (this.props.state === 102){
            return (
                <div class='task_corrupt'>
                    <h3 class="h">{this.props.name}</h3>
                    <h4 class="h">Flags: {this.props.flags} <br/> Uptime: {this.props.uptime}</h4>
                </div>
            )}
        if (this.props.state === 104){
                return (
                    <div class='task_down'>
                        <h3 class="h">{this.props.name}</h3>
                        <h4 class="h">Flags: {this.props.flags} <br/> Uptime: {this.props.uptime}</h4>
                    </div>
                )}
        else{
            return (
                <div class='task_down'>
                    <h3 class="h">{this.props.name}</h3>
                    <h4 class="h">Flags: {this.props.flags} <br/> Uptime: {this.props.uptime}</h4>
                </div>
            )}
        }
        
}

export default Task;