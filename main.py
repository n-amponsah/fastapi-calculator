import logging
import logging.config
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from operations import add, subtract, multiply, divide, power, modulo

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "detailed": {
            "format": "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "detailed",
            "level": "DEBUG",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "calculator.log",
            "formatter": "detailed",
            "level": "INFO",
        },
    },
    "root": {"level": "DEBUG", "handlers": ["console", "file"]},
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

app = FastAPI(title="Calculator API", version="1.0.0")


class CalculationRequest(BaseModel):
    a: float
    b: float


class CalculationResponse(BaseModel):
    operation: str
    a: float
    b: float
    result: float


@app.get("/", response_class=HTMLResponse)
async def root():
    logger.info("Serving calculator UI")
    return HTML_CONTENT


@app.post("/add", response_model=CalculationResponse)
async def route_add(req: CalculationRequest):
    logger.info(f"POST /add  a={req.a} b={req.b}")
    result = add(req.a, req.b)
    return CalculationResponse(operation="add", a=req.a, b=req.b, result=result)


@app.post("/subtract", response_model=CalculationResponse)
async def route_subtract(req: CalculationRequest):
    logger.info(f"POST /subtract  a={req.a} b={req.b}")
    result = subtract(req.a, req.b)
    return CalculationResponse(operation="subtract", a=req.a, b=req.b, result=result)


@app.post("/multiply", response_model=CalculationResponse)
async def route_multiply(req: CalculationRequest):
    logger.info(f"POST /multiply  a={req.a} b={req.b}")
    result = multiply(req.a, req.b)
    return CalculationResponse(operation="multiply", a=req.a, b=req.b, result=result)


@app.post("/divide", response_model=CalculationResponse)
async def route_divide(req: CalculationRequest):
    logger.info(f"POST /divide  a={req.a} b={req.b}")
    try:
        result = divide(req.a, req.b)
    except ValueError as exc:
        logger.warning(f"Division error: {exc}")
        raise HTTPException(status_code=400, detail=str(exc))
    return CalculationResponse(operation="divide", a=req.a, b=req.b, result=result)


@app.post("/power", response_model=CalculationResponse)
async def route_power(req: CalculationRequest):
    logger.info(f"POST /power  a={req.a} b={req.b}")
    result = power(req.a, req.b)
    return CalculationResponse(operation="power", a=req.a, b=req.b, result=result)


@app.post("/modulo", response_model=CalculationResponse)
async def route_modulo(req: CalculationRequest):
    logger.info(f"POST /modulo  a={req.a} b={req.b}")
    try:
        result = modulo(req.a, req.b)
    except ValueError as exc:
        logger.warning(f"Modulo error: {exc}")
        raise HTTPException(status_code=400, detail=str(exc))
    return CalculationResponse(operation="modulo", a=req.a, b=req.b, result=result)


HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<title>FastAPI Calculator</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Syne:wght@700;800&display=swap" rel="stylesheet"/>
<style>
  :root { --bg: #0d0d0d; --surface: #161616; --border: #2a2a2a; --accent: #c8f135; --accent2: #4fffb0; --text: #f0f0f0; --muted: #666; --error: #ff5c5c; }
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: var(--bg); color: var(--text); font-family: 'DM Mono', monospace; min-height: 100vh; display: flex; flex-direction: column; align-items: center; padding: 3rem 1rem; }
  header { text-align: center; margin-bottom: 3rem; }
  header h1 { font-family: 'Syne', sans-serif; font-size: clamp(2.2rem, 6vw, 4rem); font-weight: 800; letter-spacing: -2px; background: linear-gradient(90deg, var(--accent) 0%, var(--accent2) 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
  header p { color: var(--muted); font-size: .85rem; margin-top: .4rem; letter-spacing: 2px; text-transform: uppercase; }
  .card { width: 100%; max-width: 480px; background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 2rem; }
  .field { margin-bottom: 1.25rem; }
  label { display: block; font-size: .75rem; text-transform: uppercase; letter-spacing: 1.5px; color: var(--muted); margin-bottom: .5rem; }
  input[type=number], select { width: 100%; background: var(--bg); border: 1px solid var(--border); border-radius: 4px; color: var(--text); font-family: 'DM Mono', monospace; font-size: 1rem; padding: .65rem .85rem; transition: border-color .2s; -moz-appearance: textfield; }
  input:focus, select:focus { outline: none; border-color: var(--accent); }
  select option { background: #1e1e1e; }
  button { width: 100%; background: var(--accent); color: #0d0d0d; border: none; border-radius: 4px; font-family: 'Syne', sans-serif; font-weight: 700; font-size: 1rem; padding: .8rem; cursor: pointer; margin-top: .5rem; }
  button:hover { opacity: .88; }
  .result-box { margin-top: 1.75rem; padding: 1.25rem; background: var(--bg); border: 1px solid var(--border); border-radius: 4px; }
  .result-box .label { font-size: .7rem; text-transform: uppercase; letter-spacing: 2px; color: var(--muted); }
  .result-box .value { font-family: 'Syne', sans-serif; font-size: 2rem; font-weight: 800; color: var(--accent2); }
  .result-box .value.error { color: var(--error); font-size: 1rem; font-family: 'DM Mono', monospace; font-weight: 400; }
  .history { width: 100%; max-width: 480px; margin-top: 1.5rem; }
  .history h2 { font-family: 'Syne', sans-serif; font-size: .9rem; letter-spacing: 2px; text-transform: uppercase; color: var(--muted); margin-bottom: .75rem; }
  .history-list { list-style: none; display: flex; flex-direction: column; gap: .4rem; }
  .history-list li { background: var(--surface); border: 1px solid var(--border); border-radius: 4px; padding: .5rem .85rem; font-size: .82rem; color: var(--muted); display: flex; justify-content: space-between; }
  .history-list li span { color: var(--accent); font-weight: 500; }
</style>
</head>
<body>
<header><h1>CALCULATOR</h1><p>FastAPI Powered</p></header>
<div class="card">
  <div class="field"><label for="numA">Number A</label><input id="numA" type="number" value="0" step="any"/></div>
  <div class="field"><label for="numB">Number B</label><input id="numB" type="number" value="0" step="any"/></div>
  <div class="field"><label for="op">Operation</label>
    <select id="op">
      <option value="add">Add ( + )</option>
      <option value="subtract">Subtract ( - )</option>
      <option value="multiply">Multiply ( x )</option>
      <option value="divide">Divide ( / )</option>
      <option value="power">Power ( ^ )</option>
      <option value="modulo">Modulo ( % )</option>
    </select>
  </div>
  <button id="calcBtn" onclick="calculate()">CALCULATE</button>
  <div class="result-box"><div class="label">Result</div><div class="value" id="resultValue">-</div></div>
</div>
<div class="history" id="historySection" style="display:none">
  <h2>History</h2><ul class="history-list" id="historyList"></ul>
</div>
<script>
const history = [];
async function calculate() {
  const a = parseFloat(document.getElementById('numA').value);
  const b = parseFloat(document.getElementById('numB').value);
  const op = document.getElementById('op').value;
  if (isNaN(a) || isNaN(b)) { showResult('Invalid input', true); return; }
  try {
    const res = await fetch('/' + op, { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({a, b}) });
    const data = await res.json();
    if (!res.ok) { showResult(data.detail || 'Error', true); return; }
    showResult(data.result, false);
    addHistory(a, op, b, data.result);
  } catch (e) { showResult('Network error', true); }
}
function showResult(value, isErr) {
  const el = document.getElementById('resultValue');
  el.textContent = isErr ? value : parseFloat(value.toFixed(10)).toString();
  el.className = 'value' + (isErr ? ' error' : '');
}
const symbols = {add:'+', subtract:'-', multiply:'x', divide:'/', power:'^', modulo:'%'};
function addHistory(a, op, b, res) {
  history.unshift({a, op, b, res});
  if (history.length > 8) history.pop();
  document.getElementById('historySection').style.display = 'block';
  document.getElementById('historyList').innerHTML = history.map(h => `<li>${h.a} ${symbols[h.op]} ${h.b} = <span>${h.res}</span></li>`).join('');
}
document.addEventListener('keydown', e => { if (e.key === 'Enter') calculate(); });
</script>
</body>
</html>"""


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
