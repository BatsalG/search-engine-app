import React, { useState, useEffect } from 'react';
import './css/Results.css';
import { Link, useNavigate } from 'react-router-dom';


const Results = ({ res, cols_num, group }, props) => {
    // const navigate = useNavigate();
    const [disp, setDisp] = useState({ display: 'none' });
    // const toAnalysis = () => {
    //     navigate('/analysis', res);
    // }
    const origin = (res.url).match("^(?:http:\/\/|www\.|https:\/\/)([^\/]+)")[0];

    return (

        <div 
            className={group}
            onMouseEnter={e => {
                setDisp({ display: 'block' })
            }}
            onMouseLeave={e => {
                setDisp({ display: 'none' })
            }}>

            <div className={cols_num}>
                <div className="res_url">{res.url}</div>

                <div className="title_result">
                    <a href={res.url} target="_blank">{res.title}</a>
                </div>

                <div className="date_publisher">
                    <p className="publisher_">{res.publisher}</p>
                    <p className="date_">{res.published_date}</p>
                </div>

                <div className="description">
                    {(res.description).substring(0, 150) + '...'}
                </div>

                <div className="button_div" style={disp} >
                    <Link
                        to='/analysis'
                        state={res}
                    >
                        Analysis
                    </Link>
                    <span className="origin">
                        <a href = {origin} target = "_blank">Publisher</a>
                    </span>
                </div>


            </div>
        </div>
    )
}

export default Results;