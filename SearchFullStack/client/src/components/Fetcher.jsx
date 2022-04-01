import React, { useEffect, useState } from 'react';
import { Container, Row, Button, Form, Col, CloseButton } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';


const Analysis = () => {
    const [timeInterval, setTimeInterval] = useState(0)
    const [numberResults, setNumberResults] = useState(0)
    const [currKw, setCurrKw] = useState('')
    const [listKw, setListKw] = useState([])
    const [kwIdentifier, setKwIdentifier] = useState('')
    const [successKw, setsuccessKw] = useState('')

    const handleAddKw = () => {
        if (currKw === "") {

        } else if (listKw.includes(currKw)) { } else {
            setListKw((prevListKw) => [
                ...prevListKw,
                currKw
            ]);
            setCurrKw('')

        }
    }
    function handleDelKw(id) {
        const newList = listKw.filter((item) => item !== id);
        setListKw(newList);
    }

    function handleSubmitInfo() {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                interval: timeInterval,
                results: numberResults,
                listKw: listKw,
                kwID: kwIdentifier
            })
        };
        fetch('/fetchdata/', requestOptions);
    }

    function handleKwPush() {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                kwID: kwIdentifier,
                listKw: listKw
            })
        };
        fetch('/kwpersist/', requestOptions).then(setsuccessKw('Successful Insertion'));
    }

    useEffect(() => {
        setsuccessKw('')
    }, [kwIdentifier])


    return (
        <Container fluid>
            <Form
                onSubmit={(e) => {
                    handleSubmitInfo();
                }}
            >
                <Container fluid className="p-3">
                    <Row>
                        <Col md={2}></Col>
                        <Col md={4} className="mt-3">
                            <Form.Label className="font-weight-bold"><strong className="font-weight-bold">Interval</strong></Form.Label>
                            <Form.Control
                                type="number"
                                name="intervals"
                                value={timeInterval}
                                onChange={(e) => (setTimeInterval(e.target.value))}
                                min="1"
                            />
                            <Form.Text className="text-muted">
                                Enter the frequency of interval in integer hours.
                            </Form.Text>
                        </Col>
                        <Col md={4} className="mt-3">
                            <Form.Label><strong>Results</strong></Form.Label>
                            <Form.Control
                                type="number"
                                name="results"
                                value={numberResults}
                                onChange={(e) => (setNumberResults(e.target.value))}
                                min="1"
                            />
                            <Form.Text className="text-muted">
                                Enter the number of results to collect.
                            </Form.Text>
                        </Col>
                        <Col md={5}></Col>
                    </Row>
                </Container>
                <Container fluid className="p-3">
                    <Row>
                        <Col md={3}></Col>
                        <Col md="auto" className="mt-2"><Form.Label><strong>Keyword</strong></Form.Label></Col>
                        <Col md={4} className="mt-2">
                            <Form.Control
                                type="test"
                                name="cur_kw"
                                placeholder='Enter a Keyword'
                                value={currKw}
                                onChange={(e) => (setCurrKw(e.target.value))}
                            />
                            <Form.Text className="text-muted">
                                Enter the keyword to search for.
                            </Form.Text>
                        </Col>
                        <Col md="auto" className="mt-2">
                            <Button type='button' onClick={handleAddKw} variant="outline-danger" >
                                Add Keyword
                            </Button>
                        </Col>
                    </Row>
                    <Row>
                        <Button type='submit' className="mt-4 border-0" style={{ backgroundColor: "#1e6091" }}>
                            ⦿ Start Fetching
                        </Button>
                    </Row>
                </Container>
            </Form >
            <Form onSubmit={(e) => {
                e.preventDefault();
                handleKwPush();
            }}>
                <Row>
                    <Col lg={2}></Col>
                    <Col md="auto">
                        <Form.Label className="mt-3 font-weight-bold"><strong className="font-weight-bold">Store Keywords</strong></Form.Label>
                    </Col>
                    <Col>
                        <Form.Control
                            type="text"
                            name="kw_iden"
                            value={kwIdentifier}
                            onChange={(e) => (setKwIdentifier(e.target.value))}
                            className="mt-2"
                        />
                        <Form.Text className="text-muted">
                            Enter the unique identifier for your keyword.
                        </Form.Text>
                    </Col>
                    <Col md="auto" className="mt-2">
                        <Button type='submit' variant="outline-primary">
                            ➤ Push Data
                        </Button>
                    </Col>
                    <Col md="auto" className="mt-2"> <h6 className='badge badge-pill badge-success bg-success'>{successKw}</h6> </Col>
                    <Col lg={2}></Col>
                </Row>

            </Form>
            <Row xs="auto" className="m-5">
                {listKw.map((kws) => (
                    <Col md="auto" className="m-2 rounded border border-warning ">
                        {kws}
                        <CloseButton
                            variant="danger"
                            type='button'
                            className="rounded-circle, m-2"
                            onClick={() => handleDelKw(kws)}
                        >
                        </CloseButton >
                    </Col>
                ))}
            </Row>
        </Container >
    )
}

export default Analysis;