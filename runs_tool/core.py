"""Original bounded concept exercise with supplied synthetic data only."""


def fields(value, required, optional=()):
    if not isinstance(value, dict) or not set(required) <= value.keys() or not value.keys() <= set(required) | set(optional):
        raise ValueError("Unexpected or missing object fields")


def integer(value, low=0, high=10**12):
    if type(value) is not int or not low <= value <= high:
        raise ValueError("Integer outside the supported range")
    return value


def label(value):
    if not isinstance(value, str) or not value.strip() or len(value) > 80 or any(ord(c) < 32 for c in value):
        raise ValueError("Expected a nonblank label of at most 80 characters")
    return value.strip()


def sequence(value, maximum):
    if not isinstance(value, list) or len(value) > maximum:
        raise ValueError("Expected a bounded list")
    return value


def day(value):
    from datetime import date
    import re
    if not isinstance(value,str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}",value):
        raise ValueError("Use YYYY-MM-DD")
    return date.fromisoformat(value)


def text(value,maximum=10000):
    if not isinstance(value,str) or len(value)>maximum:
        raise ValueError("Expected bounded text")
    return value

def evaluate(data):
    fields(data,("runs",))
    seen,totals=set(),{}
    for run in sequence(data["runs"],1000):
        fields(run,("id","model","input_tokens","output_tokens","latency_ms","passed"))
        ident,model=label(run["id"]),label(run["model"])
        incoming,outgoing,latency=integer(run["input_tokens"],0,10**7),integer(run["output_tokens"],0,10**7),integer(run["latency_ms"],0,10**7)
        if ident in seen or type(run["passed"]) is not bool:
            raise ValueError("Repeated run ID or nonboolean assertion outcome")
        seen.add(ident)
        row=totals.setdefault(model,{"model":model,"runs":0,"input_tokens":0,"output_tokens":0,"latency_ms_total":0,"passed":0})
        row["runs"]+=1;row["input_tokens"]+=incoming;row["output_tokens"]+=outgoing
        row["latency_ms_total"]+=latency;row["passed"]+=int(run["passed"])
    rows=[]
    for model in sorted(totals):
        row=totals[model]
        rows.append({**row,"average_latency_ms":round(row["latency_ms_total"]/row["runs"],3),"pass_rate":round(row["passed"]/row["runs"],6)})
    return {"models":rows}
