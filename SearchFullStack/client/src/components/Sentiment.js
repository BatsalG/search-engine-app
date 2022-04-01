import React from 'react'
import { useState, useEffect } from 'react';
import MainSentiment from './MainSentiment';
import ClipLoader from "react-spinners/ClipLoader";

const Sentiment = ({ res }) => {
    const [doc_sentiment, setDocSentiment] = useState(0);
    const [kw_sentiment, setKwSentiment] = useState(0);
    const [keyword, setkeyword] = useState('');
    const [text_char, settext_char] = useState(0);
    const [document_emotions, setdocument_emotions] = useState({});
    const [kw_emotions, setkw_emotions] = useState({});
    const [kw_list, setkw_list] = useState([]);
    const [entities, setentities] = useState([]);
    const [loading, setLoading] = useState(true);

    const sentiment_analysis = (res) => {
        setLoading(false);
        const fetchAPI = '/sentiment/' + res.keyword + '/' + res.url;
        fetch(fetchAPI)
            .then(res => res.json())
            .then(data => {
                console.log(data)
                if (data.sentiment) {
                    setDocSentiment(data.sentiment.document.score);
                    if (data.sentiment.targets) {
                        setKwSentiment((data.sentiment.targets)['0'].score);
                        setkeyword((data.sentiment.targets)['0'].text);
                    }
                } else {
                    setDocSentiment(0);
                    setKwSentiment(0);
                    setkeyword(keyword);
                }
                settext_char(data.usage.text_characters);

                if (data.emotion){
                    setdocument_emotions(data.emotion.document.emotion);
                    setkw_emotions(data.emotion.targets['0'].emotion);    
                }
                setkw_list(data.keywords);
                setentities(data.entities);
                setLoading(true)
            }
            )
    };

    useEffect(() => {
        sentiment_analysis(res)
    }, []);

    return (
        <div>
            <div class="loader_circle">
                <ClipLoader color="red" loading={!loading} size={150} />
            </div>
            
            {
                loading &&
                <MainSentiment
                    doc_sentiment={doc_sentiment}
                    kw_sentiment={kw_sentiment}
                    keyword={keyword}
                    text_char={text_char}
                    document_emotions={document_emotions}
                    kw_emotions={kw_emotions}
                    kw_list={kw_list}
                    entities={entities}
                />
            }


        </div>

    )
}


export default Sentiment;
