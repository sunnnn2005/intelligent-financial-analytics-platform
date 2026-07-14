def render_dashboard():
    return """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Financial Analytics Dashboard</title>
    <style>
      :root {
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        background: #f6f7f9;
        color: #172033;
      }

      body {
        margin: 0;
      }

      main {
        max-width: 1120px;
        margin: 0 auto;
        padding: 40px 24px;
      }

      header {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 24px;
        margin-bottom: 28px;
      }

      h1 {
        margin: 0 0 8px;
        font-size: 34px;
        line-height: 1.1;
      }

      p {
        margin: 0;
        color: #667085;
      }

      button {
        border: 0;
        border-radius: 8px;
        background: #1570ef;
        color: white;
        font-weight: 700;
        padding: 12px 16px;
        cursor: pointer;
      }

      .grid {
        display: grid;
        grid-template-columns: repeat(5, minmax(0, 1fr));
        gap: 14px;
      }

      .card {
        background: white;
        border: 1px solid #d9e1ec;
        border-radius: 8px;
        padding: 18px;
        box-shadow: 0 12px 28px rgba(20, 32, 54, 0.06);
      }

      .wide {
        grid-column: span 2;
      }

      .label {
        color: #667085;
        font-size: 12px;
        font-weight: 800;
        text-transform: uppercase;
      }

      .value {
        margin-top: 10px;
        font-size: 26px;
        font-weight: 800;
      }

      table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 12px;
        font-size: 14px;
      }

      th,
      td {
        border-bottom: 1px solid #edf1f6;
        padding: 10px 0;
        text-align: left;
      }

      th {
        color: #667085;
        font-size: 12px;
        text-transform: uppercase;
      }

      @media (max-width: 900px) {
        header {
          display: block;
        }

        button {
          margin-top: 18px;
          width: 100%;
        }

        .grid {
          grid-template-columns: 1fr;
        }

        .wide {
          grid-column: auto;
        }
      }
    </style>
  </head>
  <body>
    <main>
      <header>
        <div>
          <h1>Financial Analytics Dashboard</h1>
          <p>Mock Plaid-style transaction data, cleaned and summarized through FastAPI analytics endpoints.</p>
        </div>
        <button id="seed">Seed demo data</button>
      </header>

      <section class="grid">
        <article class="card">
          <div class="label">Total spend</div>
          <div class="value" id="total">$0</div>
        </article>
        <article class="card">
          <div class="label">Transactions</div>
          <div class="value" id="count">0</div>
        </article>
        <article class="card">
          <div class="label">Top category</div>
          <div class="value" id="category">-</div>
        </article>
        <article class="card">
          <div class="label">Top merchant</div>
          <div class="value" id="merchant">-</div>
        </article>
        <article class="card">
          <div class="label">Anomalies</div>
          <div class="value" id="anomalies">0</div>
        </article>
        <article class="card wide">
          <div class="label">Category summary</div>
          <table id="category-table"></table>
        </article>
        <article class="card wide">
          <div class="label">Recent transactions</div>
          <table id="transaction-table"></table>
        </article>
      </section>
    </main>

    <script>
      const currency = new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" });

      function table(selector, headers, rows) {
        document.querySelector(selector).innerHTML = [
          "<thead><tr>" + headers.map((header) => "<th>" + header + "</th>").join("") + "</tr></thead>",
          "<tbody>" + rows.join("") + "</tbody>"
        ].join("");
      }

      async function refresh() {
        const [summary, categories, transactions] = await Promise.all([
          fetch("/analytics/dashboard").then((response) => response.json()),
          fetch("/analytics/category-summary").then((response) => response.json()),
          fetch("/transactions").then((response) => response.json())
        ]);

        document.querySelector("#total").textContent = currency.format(summary.total_spend);
        document.querySelector("#count").textContent = summary.transaction_count;
        document.querySelector("#category").textContent = summary.top_category || "-";
        document.querySelector("#merchant").textContent = summary.top_merchant || "-";
        document.querySelector("#anomalies").textContent = summary.anomaly_count;

        table(
          "#category-table",
          ["Category", "Spend", "Count"],
          categories.map((row) => "<tr><td>" + row.category + "</td><td>" + currency.format(row.total_spend) + "</td><td>" + row.transaction_count + "</td></tr>")
        );

        table(
          "#transaction-table",
          ["Merchant", "Category", "Amount"],
          transactions.slice(0, 6).map((row) => "<tr><td>" + row.merchant_name + "</td><td>" + row.category + "</td><td>" + currency.format(row.amount) + "</td></tr>")
        );
      }

      document.querySelector("#seed").addEventListener("click", async () => {
        await fetch("/seed", { method: "POST" });
        await refresh();
      });

      refresh();
    </script>
  </body>
</html>"""
