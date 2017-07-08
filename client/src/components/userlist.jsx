import React from 'react';
import { Table } from 'react-bootstrap';


const UserList = (props) => {
    return (
        <div>
            <h1>All Users</h1>
            <hr />
            <br />
            <Table striped bordered condensed hover>
                <thead>
                    <tr>
                        <th>User ID</th>
                        <th>Email</th>
                        <th>Username</th>
                        <th>Created Date</th>
                    </tr>
                </thead>
                <tbody>{
                    props.users.map((user) => {
                        return (
                            <tr key={user.id}>
                                <td>{user.id}</td>
                                <td>{user.email}</td>
                                <td>{user.username}</td>
                                <td>{user.created_at}</td>
                            </tr>
                        );
                    })
                }
                </tbody>
            </Table>
        </div>
    );
};

const DomainList = (props) => {
    return (
        <div>
            <h1>All Domains</h1>
            <hr />
            <br />
            <Table striped bordered condensed hover>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Domain</th>
                        <th>IP</th>
                        <th>Master</th>
                    </tr>
                </thead>
                <tbody>{
                    props.domains.map((domain) => {
                        return (
                            <tr key={domain.id}>
                                <td>{domain.id}</td>
                                <td>{domain.domain}</td>
                                <td>{domain.ip}</td>
                                <td>{domain.master}</td>
                            </tr>
                        );
                    })
                }
                </tbody>
            </Table>
        </div>
    );
};

export { DomainList, UserList };
