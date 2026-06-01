import { useEffect, useState } from "react";

export default function AddressSearch({
  initialAddress = "",
  onSearch,
  loading = false,
  buttonLabel = "Analyze property",
}) {
  const [address, setAddress] = useState(initialAddress);

  useEffect(() => {
    setAddress(initialAddress);
  }, [initialAddress]);

  function handleSubmit(event) {
    event.preventDefault();
    onSearch(address);
  }

  return (
    <form className="search-panel" onSubmit={handleSubmit}>
      <label className="eyebrow" htmlFor="address-input">
        Address lookup
      </label>
      <div className="search-row">
        <input
          id="address-input"
          value={address}
          onChange={(event) => setAddress(event.target.value)}
          placeholder="Try 101 Cedar Elm Street"
        />
        <button type="submit" disabled={loading || !address.trim()}>
          {loading ? "Loading..." : buttonLabel}
        </button>
      </div>
    </form>
  );
}
