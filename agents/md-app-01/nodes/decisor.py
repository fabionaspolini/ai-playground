from schema.calc_state import CalcState
from typing import Literal


def decisor(state: CalcState) -> CalcState:
    return {"num1": state["num1"], "num2": state["num2"], "operation": state["operation"], "result": None}


def decide_operacao(state: CalcState) -> Literal["somar", "subtrair", "multiplicar"]:
    return state["operation"]
