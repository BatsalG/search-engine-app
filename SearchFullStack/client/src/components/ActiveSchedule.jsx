import 'bootstrap/dist/css/bootstrap.min.css';
import React, { useEffect, useRef, useState } from 'react';

import './css/Analysis.css'
import { Container, Row, Button, Form, Col, CloseButton, Card, Overlay, Popover } from 'react-bootstrap';


const ActiveSchedule = () => {
    const [activeSch, setActiveSch] = useState([])
    const [count, setcount] = useState(0)
    const [show, setShow] = useState(false);
    const [target, setTarget] = useState(null);
    const [kw_identifier, setKw_identifier] = useState('')
    const ref = useRef(null);

    const handleClick = (event) => {
        setShow(!show);
        setTarget(event.target);
    };

    useEffect(() => {
        console.log("HERE")
        fetch('/activeschedules/')
            .then(res => res.json())
            .then(data =>
                setActiveSch(data)
            )
    }, [count])

    function handleDelConn(id) {
        setcount(count + 1);
        id = id[0];
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                jid: id
            })
        };
        fetch('/activeschedules/', requestOptions);
    }

    function handleKwSearch() {
        const api_search = '/searchschedules/'+kw_identifier
        fetch(api_search)
            .then (res => res.json())
            .then(data =>
                setActiveSch(data)
            )
    }

    return (
        <Container fluid className="p-5">
            <Row>
                <Col>
                    <h1>Actively Running Jobs</h1>
                </Col>
                <Col>
                    <Form onSubmit={(e) => {
                        e.preventDefault();
                        handleKwSearch();
                    }}>
                        <Row>
                            <Col lg={2}></Col>
                            <Col>
                                <Form.Control
                                    type="text"
                                    name="kw_iden"
                                    value={kw_identifier}
                                    onChange={(e) => (setKw_identifier(e.target.value))}
                                    className="mt-2"
                                />
                                <Form.Text className="text-muted">
                                    Search a keyword identifier.
                                </Form.Text>
                            </Col>
                            <Col md="auto" className="mt-2">
                                <Button type='submit' variant="outline-primary">
                                    ➤ Search
                                </Button>
                            </Col>
                        </Row>

                    </Form>
                </Col>
            </Row>

            <Row xs="auto">
                {activeSch.map((id) => (
                    <Card style={{ width: '18rem' }} className="m-2" >

                        <Card.Body>
                            <Card.Title> <strong>ID: </strong> {id[0]} </Card.Title>
                            <Card.Subtitle className="mb-2 text-muted"> Runs every <strong>{id[2]}</strong> hour </Card.Subtitle>
                            <Card.Subtitle className="mb-2 text-muted"> <strong>{id[3]}</strong> Results are collected </Card.Subtitle>
                            <Card.Text>
                                {id[1].substring(1, 30) + '...'}
                            </Card.Text>
                            <Button type='button' onClick={() => handleDelConn(id)} variant="outline-danger" >
                                Stop
                            </Button>

                        </Card.Body>
                    </Card>
                ))}
            </Row>
        </Container>
    )
}

export default ActiveSchedule;