import React from 'react';
import { Switch, Route } from 'react-router-dom';
import axios from 'axios';
import { UserList, DomainList } from './components/userlist';
import About from './components/about';
import NavBar from './components/nav_bar';
import { Form, DomainForm } from './components/form';
import Logout from './components/logout';
import UserStatus from './components/user_status';


export default class App extends React.Component {
    constructor() {
        super();
        this.state = {
            users: [],
            curretnUser: null,
            domains: [],
            title: 'React Frame',
            isAuthenticated: false,
            formData: {
                username: '',
                email: '',
                password: '',
            },
            domainData: {
                domain: '',
                ip: '',
                master: 0,
            },
        };
    }

    componentDidMount() {
        this.getUsers();
        this.getDomains();
    }

    getUsers() {
        axios.get(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`)
            .then((res) => {
                console.log(res.data.data.users);
                this.setState({ users: res.data.data.users });
            });
    }

    getDomains() {
        axios.get(`${process.env.REACT_APP_USERS_SERVICE_URL}/domains`)
            .then((res) => {
                this.setState({ domains: res.data.data.domains });
            });
    }

    logoutUser() {
        window.localStorage.removeItem('authToken');
        this.setState({ isAuthenticated: false });
    }

    handleDomainChange(evt) {
        const obj = this.state.domainData;
        obj[evt.target.name] = evt.target.value;
        this.setState(obj);
    }

    handleAddDomainSubmit(evt) {
        evt.preventDefault();
        const data = {
            ip: this.state.domainData.ip,
            domain: this.state.domainData.domain,
            master: this.state.currentUser.user_id,
        };
        const url = `${process.env.REACT_APP_USERS_SERVICE_URL}/domains`;
        axios.post(url, { Authorization: `Bearer ${window.localStorage.getItem('authToken')}` }, data)
            .then(() => {
                this.setState({
                    domainData: { domain: '', ip: '', master: 0 },
                });
                this.getDomains();
            })
            .catch((error) => { console.log(error); });
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
                email: this.state.formData.email,
                password: this.state.formData.password,
            };
        } else if (formType === 'register') {
            data = {
                username: this.state.formData.username,
                email: this.state.formData.email,
                password: this.state.formData.password,
            };
        }
        const url = `${process.env.REACT_APP_USERS_SERVICE_URL}/auth/${formType}`;
        axios.post(url, data)
            .then((res) => {
                this.setState({
                    formData: { username: '', password: '', email: '' },
                    isAuthenticated: true,
                    currentUser: res.data.user,
                });
                window.localStorage.setItem('authToken', res.data.auth_token);
                this.getUsers();
            })
            .catch((error) => { console.log(error); });
    }

    render() {
        return (
            <div>
                <NavBar title={this.state.title} isAuthenticated={this.state.isAuthenticated} />
                <div className="container">
                    <div className="row">
                        <div className="col-md-12">
                            <br />
                            <Switch>
                                <Route
                                    exact
                                    path="/"
                                    render={() => (
                                        <UserList users={this.state.users} />
                                    )}
                                />
                                <Route
                                    exact
                                    path="/register"
                                    render={() => (
                                        <Form
                                            formType="Register"
                                            formData={this.state.formData}
                                            handleFormChange={this.handleChange.bind(this)}
                                            handleFormSubmit={this.handleSubmit.bind(this)}
                                            isAuthenticated={this.state.isAuthenticated}
                                        />
                                    )}
                                />
                                <Route
                                    exact
                                    path="/login"
                                    render={() => (
                                        <Form
                                            formType="Login"
                                            formData={this.state.formData}
                                            handleFormChange={this.handleChange.bind(this)}
                                            handleFormSubmit={this.handleSubmit.bind(this)}
                                            isAuthenticated={this.state.isAuthenticated}
                                        />
                                    )}
                                />
                                <Route
                                    exact
                                    path="/about"
                                    render={About}
                                />
                                <Route
                                    exact
                                    path="/status"
                                    component={() => (
                                        <UserStatus isAuthenticated={this.state.isAuthenticated} />
                                    )}
                                />
                                <Route
                                    exact
                                    path="/logout"
                                    render={() => (
                                        <Logout
                                            logoutUser={this.logoutUser.bind(this)}
                                            isAuthenticated={this.state.isAuthenticated}
                                        />
                                    )}
                                />
                                <Route
                                    exact
                                    path="/domains"
                                    render={() => (
                                        <DomainList domains={this.state.domains} />
                                    )}
                                />
                                <Route
                                    exact
                                    path="/domain/add"
                                    render={() => (
                                        <DomainForm
                                            formData={this.state.domainData}
                                            handleFormChange={this.handleDomainChange.bind(this)}
                                            handleFormSubmit={this.handleAddDomainSubmit.bind(this)}
                                            isAuthenticated={this.state.isAuthenticated}
                                        />
                                    )}
                                />
                            </Switch>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}
