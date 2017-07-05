import React from 'react';
import axios from 'axios';


export default class UserStatus extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            id: '',
            username: '',
            email: '',
            created_at: '',
        }
    }

    componentDidMount() {
        if (this.props.isAuthenticated) {
            this.getUserStatus();
        }
    }

    getUserStatus() {
        const options = {
            url: `${process.env.REACT_APP_USERS_SERVICE_URL}/auth/status`,
            method: 'get',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${window.localStorage.authToken}`
            }
        };
        return axios(options)
            .then((res) => {
                this.setState({
                    id: res.data.data.id,
                    username: res.data.data.username,
                    email: res.data.data.email,
                    created_at: res.data.data.created_at,
                });
            })
            .catch((error) => {
                console.log(error);
            })
    };

    render() {
        if (!this.props.isAuthenticated) {
            return <p>User not logged in</p>
        }
        return (
            <div>
                <ul>
                    <li><strong>User ID: </strong>{this.state.id}</li>
                    <li><strong>Username: </strong>{this.state.username}</li>
                    <li><strong>Email: </strong>{this.state.email}</li>
                    <li><strong>Create at: </strong>{this.state.created_at}</li>
                </ul>
            </div>
        )
    }
}
