import React from 'react';
import { Switch, Route } from 'react-router-dom';
import axios from 'axios';
import UserList from './components/userlist';
import About from './components/about';
import NavBar from './components/nav_bar';
import Form from './components/form';
import Logout from './components/logout';
import UserStatus from './components/user_status';


export default class App extends React.Component {
    constructor() {
        super();
        this.state = {
            users: [],
            title: 'React Frame',
            isAuthenticated: false,
            formData: {
                username: '',
                email: '',
                password: '',
            }
        }
    }

    componentDidMount() {
        this.getUsers();
    }

    getUsers() {
        console.log(`get service url ---> ${process.env.REACT_APP_USERS_SERVICE_URL}/users`);
        axios.get(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`)
            .then((res) => {
                console.log(res.data.data.users);
                this.setState({ users: res.data.data.users });
            })
    }

    logoutUser() {
        window.localStorage.removeItem('authToken');
        this.setState({ isAuthenticated: false });
    }

    handleChange(evt) {
        const obj = this.state.formData;
        obj[evt.target.name] = evt.target.value;
        this.setState(obj);
    }

    handleSubmit(evt) {
        evt.preventDefault();
        const formType = window.location.href.split('/').reverse()[0];
        let data;
        if (formType === 'login') {
            data = {
                email: this.state.email,
                password: this.state.password,
            };
        } else if (formType === 'register') {
            data = {
                username: this.state.username,
                email: this.state.email,
                password: this.state.password,
            };
        }
        const url = `${process.env.REACT_APP_USERS_SERVICE_URL}/auth/${formType}`;
        axios.post(url, data)
            .then((res) => {
                this.setState({
                    formData: { username: '', password: '', email: '' },
                    isAuthenticated: true
                });
                window.localStorage.setItem('authToken', res.data.auth_token);
                this.getUsers();
            })
            .catch((error) => { console.log(error)})
    }

    render() {
        return (
            <div>
                <NavBar title={this.state.title} isAuthenticated={this.state.isAuthenticated} />
                <div className="container">
                    <div className="row">
                        <div className="col-md-6">
                            <br/>
                            <Switch>
                                <Route exact path="/" render={() => (
                                    <UserList users={this.state.users} />
                                )}/>
                                <Route exact path="/register" render={() => (
                                    <Form
                                        formType="Register"
                                        formData={this.state.formData}
                                        handleFormChange={this.handleChange.bind(this)}
                                        handleFormSubmit={this.handleSubmit.bind(this)}
                                        isAuthenticated={this.state.isAuthenticated}
                                    />
                                )}/>
                                <Route exact path="/login" render={() => (
                                    <Form
                                        formType="Login"
                                        formData={this.state.formData}
                                        handleFormChange={this.handleChange.bind(this)}
                                        handleFormSubmit={this.handleSubmit.bind(this)}
                                        isAuthenticated={this.state.isAuthenticated}
                                    />
                                )}/>
                                <Route exact path="/about" render={About} />
                                <Route exact path="/status" component={() =>(
                                    <UserStatus isAuthenticated={this.state.isAuthenticated}/>
                                )} />
                                <Route exact path="/logout" render={() => (
                                    <Logout
                                        logoutUser={this.logoutUser.bind(this)}
                                        isAuthenticated={this.state.isAuthenticated}
                                    />
                                )} />
                            </Switch>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}
