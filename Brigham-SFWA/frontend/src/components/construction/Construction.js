import "./Construction.css";

import React, { useState, useEffect } from "react";
import axios from "axios";

import { getPaperTarget, getPaperStats } from "../../utils/helpers";
import MsgBanner from "../shared/MsgBanner";
import ConstructionAddRow from "./ConstructionAddRow";
import ConstructionProcess from "./ConstructionProcess";
import { Content } from "../shared/SharedStyles";

export const Construction = (props) => {
  const [errorMsg, setErrorMsg] = useState(null);
  const [apiSecurities, setApiSecurities] = useState([]);
  const [paperTarget, setPaperTarget] = useState(getPaperTarget());
  const [liveTarget, setLiveTarget] = useState([]);
  const [paperStats, setPaperStats] = useState(getPaperStats());
  const [liveStats, setLiveStats] = useState([]);
  const [hasProcessed, setHasProcessed] = useState(false);

  useEffect(() => {
    localStorage.setItem("paperTarget", JSON.stringify(paperTarget));
  }, [paperTarget]);

  useEffect(() => {
    localStorage.setItem("paperStats", JSON.stringify(paperStats));
  }, [paperStats]);

  const resetToLive = () => {
    setPaperTarget(liveTarget);
    setPaperStats(liveStats);
    setHasProcessed(true);
  };

  const getApiSecurities = () => {
    axios
      .get("api/securities/r3000/")
      .then((response) => {
        console.log("Securities", response.data);
        setApiSecurities(response.data);
      })
      .catch((error) => {
        console.log(error);
        setErrorMsg(
          "Uh oh! Something went wrong on our end (failed to load positions data).  If this error persists, contact support."
        );
      });
  };

  const getApiLiveTarget = () => {
    axios
      .get("api/live-target-portfolio/latest/")
      .then((response) => {
        console.log("Live Target Portfolio", response.data);
        // change json key 'asset' to 'asset_id'
        response.data.forEach((el) => {
          el["asset_id"] = el["asset"];
          delete el["asset"];
        });
        setLiveTarget(response.data);
      })
      .catch((error) => {
        console.log(error);
        setErrorMsg(
          "Uh oh! Something went wrong on our end (failed to load live target porfolio data).  If this error persists, contact support."
        );
      });
  };

  const getApiLiveStats = () => {
    axios
      .get("api/portfolio-stats/latest/")
      .then((response) => {
        console.log("Latest Portfolio Stats", response.data);
        setLiveStats(response.data);
      })
      .catch((error) => {
        console.log(error);
        setErrorMsg(
          "Uh oh! Something went wrong on our end (failed to load portfolio stats data).  If this error persists, contact support."
        );
      });
  };

  useEffect(() => {
    getApiSecurities();
    getApiLiveTarget();
    getApiLiveStats();
  }, []);

  const removePosition = (tickerToRemove) => {
    setHasProcessed(false);
    const tempArrObj = paperTarget.filter((el) => el.ticker !== tickerToRemove);
    setPaperTarget(tempArrObj);
  };

  const onChangeAER = (ticker, value) => {
    setErrorMsg(null);
    setHasProcessed(false);

    let tempArrObj = [...paperTarget];
    tempArrObj.forEach((el) => {
      if (el.ticker === ticker) {
        el.annualized_er = value;
      }
    });
    setPaperTarget(tempArrObj);
  };

  return (
    <>
      <MsgBanner msg={errorMsg} setMsg={(value) => setErrorMsg(value)} />
      <Content>
        <table className="table-with-select">
          <thead>
            <tr>
              <th className="top-left-cell" style={{ width: "400px" }}>
                <button
                  className="btn white-btn my-2 mx-4 float-left"
                  onClick={resetToLive}
                >
                  Reset To Live
                </button>
                <span className="float-right my-3">Ticker</span>
              </th>
              <th>Model E[r]</th>
              <th>Annualized E[r]</th>
              <th>Beta to Benchmark</th>
              <th>Alpha</th>
              <th>Optimal Active Weight</th>
              <th>Weight in Benchmark</th>
              <th>Our Current Weight</th>
              <th>Backlog</th>
              <th className="top-right-cell">Backlog Risk</th>
              <th className="clear-cell" style={{ width: "85px" }} />
            </tr>
          </thead>
          <tbody>
            {/* Benchmark */}
            <tr>
              <td className="table-subtitle-container clear-cell">
                <h5 className="table-subtitle">Benchmark</h5>
              </td>
            </tr>
            <tr>
              <td>VOO</td>
              <td>0.10</td>
              <td>0.10</td>
              <td>1.0</td>
              <td>0.0</td>
              <td>1.00</td>
              <td className="blank-cell">N/A</td>
              <td>0.82</td>
              <td className="blank-cell">N/A</td>
              <td className="blank-cell">N/A</td>
            </tr>
            {/* Active Positions */}
            <tr>
              <td className="table-subtitle-container clear-cell">
                <h5 className="table-subtitle">Active Positions</h5>
              </td>
            </tr>
            {paperTarget.map((el) => (
              <tr key={el.ticker}>
                <td>{el.ticker}</td>
                <td className={!hasProcessed ? "blank-cell" : undefined}>
                  {el.model_er}
                </td>
                <td className={!hasProcessed ? "blank-cell" : undefined}>
                  <input
                    style={{ width: "100%" }}
                    className={
                      !hasProcessed
                        ? (el.annualized_er === ""
                            ? "bolded-cell"
                            : undefined) ||
                          (el.annualized_er < -1 ? "error-cell" : undefined) ||
                          (el.annualized_er > 1 ? "warning-cell" : undefined)
                        : undefined
                    }
                    type="number"
                    step="0.01"
                    min="-1"
                    max="1"
                    placeholder="Enter Decimal"
                    value={el.annualized_er}
                    onChange={(e) => onChangeAER(el.ticker, e.target.value)}
                  />
                </td>
                <td className={!hasProcessed ? "blank-cell" : undefined}>
                  {el.beta_to_b}
                </td>
                <td className={!hasProcessed ? "blank-cell" : undefined}>
                  {el.alpha}
                </td>
                <td className={!hasProcessed ? "blank-cell" : undefined}>
                  {el.oa_weight}
                </td>
                <td className={!hasProcessed ? "blank-cell" : undefined}>
                  {el.b_weight}
                </td>
                <td className={!hasProcessed ? "blank-cell" : undefined}>
                  {el.c_weight}
                </td>
                <td className={!hasProcessed ? "blank-cell" : undefined}>
                  {el.backlog}
                </td>
                <td className={!hasProcessed ? "blank-cell" : undefined}>
                  {el.backlog_risk}
                </td>
                <td className="clear-cell">
                  <button
                    className="btn delete-table-row-btn"
                    onClick={() => removePosition(el.ticker)}
                  >
                    🞬
                  </button>
                </td>
              </tr>
            ))}
            <ConstructionAddRow
              apiSecurities={apiSecurities}
              setErrorMsg={(value) => setErrorMsg(value)}
              paperTarget={paperTarget}
              setPaperTarget={(value) => setPaperTarget(value)}
              setHasProcessed={(value) => setHasProcessed(value)}
            />
          </tbody>
        </table>
        <br />
        <ConstructionProcess
          paperTarget={paperTarget}
          setPaperTarget={(value) => setPaperTarget(value)}
          liveTarget={liveTarget}
          setLiveTarget={(value) => setLiveTarget(value)}
          hasProcessed={hasProcessed}
          setHasProcessed={(value) => setHasProcessed(value)}
          setErrorMsg={(value) => setErrorMsg(value)}
          username={props.username}
          paperStats={paperStats}
          setPaperStats={(value) => setPaperStats(value)}
          setLiveStats={(value) => setLiveStats(value)}
        />
      </Content>
    </>
  );
};

export default Construction;
