import { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { lookupProperty } from "../api/client";
import AddressSearch from "../components/AddressSearch";
import ComparableSalesTable from "../components/ComparableSalesTable";
import ConfidenceScore from "../components/ConfidenceScore";
import DataSourceProvenance from "../components/DataSourceProvenance";
import FormulaBreakdown from "../components/FormulaBreakdown";
import InvestmentSummary from "../components/InvestmentSummary";
import MarketTrendChart from "../components/MarketTrendChart";
import PropertySummary from "../components/PropertySummary";
import RenovationScenarios from "../components/RenovationScenarios";
import ValueEstimateCard from "../components/ValueEstimateCard";

export default function PropertyReport() {
  const [params] = useSearchParams();
  const navigate = useNavigate();
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const address = params.get("address") || "";

  useEffect(() => {
    if (!address) {
      return;
    }

    async function loadReport() {
      setLoading(true);
      setError("");
      try {
        const payload = await lookupProperty(address);
        setReport(payload);
      } catch (loadError) {
        setError(loadError.message);
      } finally {
        setLoading(false);
      }
    }

    loadReport();
  }, [address]);

  function handleSearch(nextAddress) {
    navigate(`/report?address=${encodeURIComponent(nextAddress)}`);
  }

  return (
    <div className="stack-layout">
      <AddressSearch initialAddress={address} onSearch={handleSearch} loading={loading} buttonLabel="Generate report" />

      {!address && <section className="card"><p>Search for an address to generate a property report.</p></section>}
      {error && <section className="card error-card"><p>{error}</p></section>}
      {report?.matched_property == null && !loading && address && (
        <section className="card">
          <p>No matching property was found in the seeded dataset. Try `101 Cedar Elm Street` or `12 Harbor Point Drive`.</p>
        </section>
      )}

      {report?.matched_property && (
        <>
          <ValueEstimateCard
            estimatedValue={report.estimated_value}
            lowEstimate={report.low_estimate}
            highEstimate={report.high_estimate}
          />
          <ConfidenceScore score={report.confidence_score} explanation={report.confidence_explanation} />
          <PropertySummary property={report.matched_property} />
          <FormulaBreakdown
            components={report.valuation_components}
            weights={report.valuation_breakdown}
            explanation={report.formula_explanation}
          />
          <ComparableSalesTable comparables={report.comparable_sales} />
          <RenovationScenarios scenarios={report.renovation_scenarios} />
          <MarketTrendChart trend={report.market_trends} />
          <InvestmentSummary summary={report.investment_summary} />
          <DataSourceProvenance sources={report.data_sources_used} />
        </>
      )}
    </div>
  );
}
