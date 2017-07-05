import React from 'react';
import { Link } from 'react-router-dom';


export default class Logout extends React.Component {
    componentDidMount() {
        this.props.logoutUser();
    }

    render() {
        return (
            <div>
                <p>You are now logged out. Click <Link to="/login">here</Link> to log back in.</p>
            </div>
        )
    }
}
