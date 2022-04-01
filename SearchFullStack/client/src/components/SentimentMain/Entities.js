import React from 'react';
import '../css/Entities.css'

const Entities = ({ type, text, sentiment, relevance, confidence }) => {
    return (
        <div className="entity">
            <div className="type">
                <span className="type_main">{type}</span>
            </div>
            <div className="text">
                <span className="text_main">{text}</span>
            </div>
            <div className="sentiment">
                <span className="sentiment_txt">Sentiment </span>
                <span className="sentiment_main">{sentiment}</span>
            </div>
            <div className="relevance">
                <span className="relevance_txt">Relevance </span>
                <span className="relevance_main">{relevance}</span>
            </div>
        </div>
    )
}

export default Entities;
