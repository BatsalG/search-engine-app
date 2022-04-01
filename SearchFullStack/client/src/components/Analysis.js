import React from 'react';
import { useLocation } from 'react-router-dom';
import Results from './Results';
import { useNavigate } from "react-router-dom";
import './css/Analysis.css'
import Sentiment from './Sentiment';

const Analysis = () => {
    const location = useLocation()
    const navigate = useNavigate();

    return (
        <div>
            <div className="keyword_name">
                <span className="back_button">
                    <a onClick={() => navigate(-1)}>← Go Back </a>
                </span>
                <span className="kw_name">{location.state.keyword}</span>
                <span className="res_search"> Search Results </span>
            </div>

            <Results res={location.state} cols_num="single_result" group="results_group" />
            <Sentiment res={location.state} />
        </div>
    )
}

export default Analysis;