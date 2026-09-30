from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from knowledge.elements.registry import all_elements


WEB_ROOT = Path(__file__).parent


def element_payload():
    elements = []

    for element in all_elements():
        elements.append(
            {
                "atomic_number": element.atomic_number,
                "name": element.name,
                "symbol": element.symbol,
                "period": element.period,
                "group": element.group,
                "block": element.block,
                "category": element.category.value,
            }
        )

    return tuple(elements)


INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>ZamCan Software Chemistry</title>

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    background: #f3f4f6;
    color: #171717;
}

header {
    background: white;
    border-bottom: 1px solid #d4d4d4;
    padding: 24px;
}

header h1 {
    margin: 0;
    font-size: 28px;
}

header p {
    margin: 5px 0 0;
    color: #666;
}

main {
    max-width: 1700px;
    margin: auto;
    padding: 20px;
}

.toolbar {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 18px;
}

input,
select,
button {
    border: 1px solid #cfcfcf;
    border-radius: 8px;
    padding: 10px 12px;
    background: white;
    font-size: 14px;
}

input {
    min-width: 280px;
    flex: 1;
}

button {
    cursor: pointer;
}

button:hover {
    border-color: #111;
}

.status {
    margin: 12px 0;
    color: #555;
}

.periodic-wrapper {
    overflow-x: auto;
    padding-bottom: 12px;
}

.periodic-table {
    min-width: 1150px;
    display: grid;
    grid-template-columns: repeat(18, minmax(55px, 1fr));
    grid-template-rows: repeat(7, 82px);
    gap: 5px;
}

.element {
    position: relative;
    border: 1px solid #bbb;
    border-radius: 7px;
    background: white;
    padding: 6px;
    cursor: pointer;
    min-width: 0;
    transition: transform .12s, border-color .12s;
}

.element:hover {
    transform: translateY(-2px);
    border-color: #111;
    z-index: 2;
}

.number {
    font-size: 10px;
    color: #666;
}

.symbol {
    font-size: 23px;
    line-height: 25px;
    font-weight: 750;
}

.name {
    font-size: 9px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.category {
    font-size: 8px;
    margin-top: 2px;
    color: #555;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.placeholder {
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px dashed #aaa;
    border-radius: 7px;
    color: #777;
    font-size: 11px;
    text-align: center;
}

.f-block {
    min-width: 900px;
    margin-top: 18px;
    display: grid;
    grid-template-columns: 70px repeat(15, minmax(55px, 1fr));
    gap: 5px;
}

.f-label {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    color: #666;
}

.first20 {
    margin: 24px 0;
}

.first20 h2,
.details h2 {
    margin-top: 0;
}

.quick-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
}

.quick {
    border: 1px solid #ccc;
    background: white;
    border-radius: 6px;
    padding: 7px 9px;
    cursor: pointer;
}

.quick:hover {
    border-color: #111;
}

.details {
    display: none;
    margin-top: 20px;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 10px;
    background: white;
}

.details-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 10px;
}

.data-card {
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 7px;
    background: #fafafa;
}

.data-label {
    font-size: 11px;
    color: #666;
}

.data-value {
    font-weight: 650;
    margin-top: 4px;
}

.warning {
    margin-top: 16px;
    color: #666;
    font-size: 13px;
}

.legend {
    display: flex;
    flex-wrap: wrap;
    gap: 7px;
    margin: 16px 0;
}

.legend-item {
    border: 1px solid #ccc;
    border-radius: 6px;
    padding: 5px 8px;
    background: white;
    font-size: 11px;
}

.mode-info {
    margin: 12px 0;
    padding: 12px;
    border-left: 3px solid #777;
    background: white;
    font-size: 13px;
}

</style>
</head>

<body>

<header>
    <h1>ZamCan Software Chemistry</h1>
    <p>Software Chemistry Model — Scientific Periodic Table</p>
</header>

<main>

<div class="toolbar">

    <input
        id="search"
        type="search"
        placeholder="Search element, symbol, or atomic number..."
    >

    <select id="viewMode">
        <option value="category">Category / Classification</option>
        <option value="group">Groups & Periods</option>
        <option value="electronegativity">Electronegativity</option>
        <option value="electropositivity">Electropositivity</option>
        <option value="atomicRadius">Atomic Radius</option>
        <option value="ionizationEnergy">Ionization Energy</option>
    </select>

    <button id="reset">Reset</button>

</div>

<div id="modeInfo" class="mode-info"></div>

<div id="status" class="status">
    Loading SCM element registry...
</div>

<div class="legend" id="legend"></div>

<section class="periodic-wrapper">
    <div id="table" class="periodic-table"></div>
</section>

<section class="f-block">

    <div class="f-label">
        Lanthanides
    </div>

    <div id="lanthanides"></div>

</section>

<section class="f-block">

    <div class="f-label">
        Actinides
    </div>

    <div id="actinides"></div>

</section>

<section class="first20">

    <h2>First 20 Elements</h2>

    <div id="first20" class="quick-grid"></div>

</section>

<section id="details" class="details"></section>

</main>

<script>

let elements = [];

const categoryDescriptions = {

    "alkali_metal": "Alkali metals",
    "alkaline_earth_metal": "Alkaline earth metals",
    "transition_metal": "Transition metals",
    "post_transition_metal": "Post-transition metals",
    "metalloid": "Metalloids",
    "nonmetal": "Nonmetals",
    "halogen": "Halogens",
    "noble_gas": "Noble gases",
    "lanthanide": "Lanthanides",
    "actinide": "Actinides",
    "unknown": "Unknown / not classified"

};

const categorySymbols = {

    "alkali_metal": "AM",
    "alkaline_earth_metal": "AE",
    "transition_metal": "TM",
    "post_transition_metal": "PT",
    "metalloid": "ML",
    "nonmetal": "NM",
    "halogen": "HG",
    "noble_gas": "NG",
    "lanthanide": "LN",
    "actinide": "AN",
    "unknown": "?"

};

async function loadElements() {

    const response = await fetch("/api/elements");

    if (!response.ok) {
        throw new Error("Failed to load SCM element registry");
    }

    elements = await response.json();

    renderLegend();
    renderFirst20();
    render(elements);

    document.getElementById("status").textContent =
        `${elements.length} elements loaded from SCM knowledge registry.`;

    updateModeInfo();

}

function createElementCard(element) {

    const card = document.createElement("article");

    card.className = "element";

    card.dataset.atomicNumber =
        element.atomic_number;

    card.dataset.category =
        element.category;

    card.innerHTML = `
        <div class="number">
            ${element.atomic_number}
        </div>

        <div class="symbol">
            ${element.symbol}
        </div>

        <div class="name">
            ${element.name}
        </div>

        <div class="category">
            ${categoryDescriptions[element.category]
                || element.category}
        </div>
    `;

    card.onclick = () => showDetails(element);

    return card;

}

function placeElement(card, element) {

    if (
        element.period >= 1 &&
        element.period <= 7 &&
        element.group !== null
    ) {

        card.style.gridColumn =
            String(element.group);

        card.style.gridRow =
            String(element.period);

        return true;
    }

    return false;
}

function render(items) {

    const table =
        document.getElementById("table");

    table.innerHTML = "";

    const visible = new Set(
        items.map(
            element => element.atomic_number
        )
    );

    for (const element of elements) {

        if (!visible.has(element.atomic_number)) {
            continue;
        }

        if (
            element.group === null ||
            element.period >= 8
        ) {
            continue;
        }

        const card =
            createElementCard(element);

        if (placeElement(card, element)) {
            table.appendChild(card);
        }

    }

    renderFBlock(items);

}

function renderFBlock(items) {

    const lanthanides =
        document.getElementById("lanthanides");

    const actinides =
        document.getElementById("actinides");

    lanthanides.innerHTML = "";
    actinides.innerHTML = "";

    lanthanides.style.display =
        "grid";

    actinides.style.display =
        "grid";

    lanthanides.style.gridTemplateColumns =
        "repeat(15, minmax(55px, 1fr))";

    actinides.style.gridTemplateColumns =
        "repeat(15, minmax(55px, 1fr))";

    lanthanides.style.gap = "5px";
    actinides.style.gap = "5px";

    for (const element of items) {

        if (
            element.atomic_number >= 57 &&
            element.atomic_number <= 71
        ) {

            lanthanides.appendChild(
                createElementCard(element)
            );

        }

        if (
            element.atomic_number >= 89 &&
            element.atomic_number <= 103
        ) {

            actinides.appendChild(
                createElementCard(element)
            );

        }

    }

}

function renderFirst20() {

    const container =
        document.getElementById("first20");

    container.innerHTML = "";

    for (const element of elements.slice(0, 20)) {

        const item =
            document.createElement("button");

        item.className = "quick";

        item.textContent =
            `${element.atomic_number} ${element.symbol}`;

        item.onclick =
            () => showDetails(element);

        container.appendChild(item);

    }

}

function renderLegend() {

    const legend =
        document.getElementById("legend");

    legend.innerHTML = "";

    const categories =
        [...new Set(
            elements.map(
                element => element.category
            )
        )];

    for (const category of categories) {

        const item =
            document.createElement("div");

        item.className = "legend-item";

        item.textContent =
            `${categorySymbols[category] || "?"} — ${
                categoryDescriptions[category]
                || category
            }`;

        legend.appendChild(item);

    }

}

function showDetails(element) {

    const details =
        document.getElementById("details");

    details.style.display =
        "block";

    details.innerHTML = `

        <h2>
            ${element.name}
            (${element.symbol})
        </h2>

        <div class="details-grid">

            <div class="data-card">
                <div class="data-label">
                    Atomic number
                </div>
                <div class="data-value">
                    ${element.atomic_number}
                </div>
            </div>

            <div class="data-card">
                <div class="data-label">
                    Period
                </div>
                <div class="data-value">
                    ${element.period}
                </div>
            </div>

            <div class="data-card">
                <div class="data-label">
                    Group
                </div>
                <div class="data-value">
                    ${element.group ?? "Not assigned"}
                </div>
            </div>

            <div class="data-card">
                <div class="data-label">
                    Block
                </div>
                <div class="data-value">
                    ${element.block}
                </div>
            </div>

            <div class="data-card">
                <div class="data-label">
                    Classification
                </div>
                <div class="data-value">
                    ${
                        categoryDescriptions[
                            element.category
                        ] || element.category
                    }
                </div>
            </div>

        </div>

        <p class="warning">
            Scientific property values are displayed only
            after authoritative source ingestion.
            The SCM never invents missing scientific data.
        </p>
    `;

    details.scrollIntoView({
        behavior: "smooth",
        block: "nearest"
    });

}

function updateModeInfo() {

    const mode =
        document.getElementById("viewMode").value;

    const info =
        document.getElementById("modeInfo");

    const descriptions = {

        category:
            "Classification view. Categories are derived from the SCM element registry.",

        group:
            "Universal periodic-table view using periods 1–7 and groups 1–18.",

        electronegativity:
            "Electronegativity visualization is prepared for authoritative property data. Values are not inferred or invented.",

        electropositivity:
            "Electropositivity visualization is prepared for authoritative property data. Values are not inferred or invented.",

        atomicRadius:
            "Atomic-radius visualization is prepared for authoritative property data.",

        ionizationEnergy:
            "Ionization-energy visualization is prepared for authoritative property data."

    };

    info.textContent =
        descriptions[mode];

}

document
    .getElementById("search")
    .addEventListener("input", event => {

        const query =
            event.target.value
                .trim()
                .toLowerCase();

        if (!query) {

            render(elements);

            document.getElementById("status").textContent =
                `${elements.length} elements loaded from SCM knowledge registry.`;

            return;
        }

        const filtered =
            elements.filter(element =>
                element.name
                    .toLowerCase()
                    .includes(query)

                || element.symbol
                    .toLowerCase()
                    .includes(query)

                || String(
                    element.atomic_number
                ) === query
            );

        render(filtered);

        document.getElementById("status").textContent =
            `${filtered.length} matching element(s).`;

    });

document
    .getElementById("viewMode")
    .addEventListener(
        "change",
        updateModeInfo
    );

document
    .getElementById("reset")
    .addEventListener("click", () => {

        document.getElementById("search").value = "";

        document.getElementById("viewMode").value =
            "category";

        render(elements);

        document.getElementById("status").textContent =
            `${elements.length} elements loaded from SCM knowledge registry.`;

        updateModeInfo();

    });

loadElements().catch(error => {

    document.getElementById("status").textContent =
        `ERROR: ${error.message}`;

});

</script>

</body>
</html>
"""



def create_app():
    class Handler(BaseHTTPRequestHandler):

        def do_GET(self):
            if self.path == "/":
                body = INDEX_HTML.encode("utf-8")

                self.send_response(200)
                self.send_header(
                    "Content-Type",
                    "text/html; charset=utf-8",
                )
                self.send_header(
                    "Content-Length",
                    str(len(body)),
                )
                self.end_headers()
                self.wfile.write(body)
                return

            if self.path == "/api/elements":
                body = json.dumps(
                    element_payload()
                ).encode("utf-8")

                self.send_response(200)
                self.send_header(
                    "Content-Type",
                    "application/json; charset=utf-8",
                )
                self.send_header(
                    "Content-Length",
                    str(len(body)),
                )
                self.end_headers()
                self.wfile.write(body)
                return

            self.send_response(404)
            self.end_headers()

        def log_message(self, format, *args):
            return

    return Handler


def main():
    server = ThreadingHTTPServer(
        ("0.0.0.0", 8000),
        create_app(),
    )

    print(
        "ZamCan Software Chemistry UI running at "
        "http://127.0.0.1:8000"
    )

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
