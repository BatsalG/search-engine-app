import { useState } from "react"
import './css/KeywordForm.css'

const KeywordForm = ({ refreshResults, loading }) => {
    const [kywrd, setKW] = useState('');
    const [engine, setEngine] = useState('Google');
    const [logo_, setLogo] = useState('https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/48px-Google_%22G%22_Logo.svg.png');
    const logoHandler = (kw) => {
        if (kw === "Google") {
            setLogo('https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/48px-Google_%22G%22_Logo.svg.png');
        } else if (kw === "Bing") {
            setLogo('https://logos-world.net/wp-content/uploads/2021/02/Bing-Logo.png');
        } else {
            setLogo('https://upload.wikimedia.org/wikipedia/commons/thumb/b/bd/VisualEditor_-_Icon_-_Search-big_-_white.svg/1200px-VisualEditor_-_Icon_-_Search-big_-_white.svg.png');
        }
    };

    return (
        <div className="form_div">
            <div className="search_title_bar">
                SERPs Analyzer
            </div>
            <form
                className="form_form"
                onSubmit={(e) => {
                    e.preventDefault();
                    refreshResults(kywrd, engine);
                }}>
                <label className="search_label"> </label>
                <input
                    type="text"
                    required
                    value={kywrd}
                    onChange={(e) => (setKW(e.target.value))
                    }
                    className="input_box"
                    placeholder='🔎︎'
                />
                <br />
                <label className="engine_label"></label>
                <select
                    className="select_box"
                    onChange={(e) => {
                        setEngine(e.target.value);
                        logoHandler(e.target.value);
                    }}>
                    <option value="Google" > Google</option>
                    <option value="Bing"> Bing</option>
                    <option value="Both">Both</option>
                </select>
                <button type="submit" className="submit_button">Search</button>
            </form>
            <SearchHeading kywrd={kywrd} logo_={logo_} engine={engine} />
        </div>
    )
}

const SearchHeading = ({ kywrd, logo_, engine }) => {
    return (
        <div>
            <div className="search_heading">
                <p> <span className="search_for">Search for : </span> <span className="keyword_">{kywrd}</span> in  <span className="engine_"> <img src={logo_} alt="" height="20px" /> {engine}</span></p>
            </div>

        </div>
    )
}

export default KeywordForm;
