# from .get_cep_details import get_cep_details
# from .get_weather import get_weather
from agents.clima.tools.get_cep_details import get_cep_details
from agents.clima.tools.get_weather import get_weather
from agents.clima.tools.execute_tool import execute_tool

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_cep_details",
            "description": "Obter detalhes de um CEP",
            "parameters": {
                "type": "object",
                "properties": {
                    "cep": {
                        "type": "string",
                        "description": "CEP com ou sem hífen. No formato 00000000 ou 00000-000.",
                    }
                },
                "required": ["cep"],
                "additionalProperties": False,
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Obter temperatura atual em uma localização.",
            "parameters": {
                "type": "object",
                "properties": {
                    "cidade": {
                        "type": "string",
                        "description": "Cidade ou país, exemplo: Bogotá, Colombia",
                    },
                    "uf": {
                        "type": "string",
                        "description": "Unidade federativa ou estado, exemplo: SC, para Santa Catarina"
                    }
                },
                "required": ["cidade", "uf"],
                "additionalProperties": False,
            },
        },
        "strict": True,
    },
]

__all__ = ["tools", "get_cep_details", "get_weather", "execute_tool"]