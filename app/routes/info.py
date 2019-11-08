from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from app.modules.db import DbConnection
import json
bp = Blueprint('info', __name__, url_prefix='/info')

@bp.route('/AllStrategies', methods=['GET'])
def AllStrategies():
    # db = DbConnection.getInstance()

    # available_symbols = db.get_symbols()
    # available_strategies = db.get_strategies()
    # available_symbols = [s[0] for s in available_symbols]
    # available_strategies = [s[0] for s in available_strategies]
    return render_template('info/all_strategies.html')

@bp.route('/AllSymbols', methods=['GET'])
def AllSymbols():
    db = DbConnection.getInstance()

    available_symbols = db.get_full_symbols()
    available_symbols = [s[0] for s in available_symbols]
    print(available_symbols)
    json_strings = {}
    json_other = {}
    for symbol in available_symbols:
        symbol_info = {
        "symbol":symbol,
         "width": "100%",
         "height": "100%",
        "colorTheme": "dark",
        "isTransparent": False,
          "locale": "en"
        }
        
        tech_info = {
      "interval": "1D",
      "width": "100%",
      "colorTheme": "dark",
      "isTransparent": False,
      "height": 450,
      "symbol": symbol,
      "showIntervalTabs": "true",
      "locale": "en"
            }
        json_strings[symbol] = json.dumps(symbol_info)
        json_other[symbol] = json.dumps(tech_info)
    print(json_strings)
    print(json_other)
    return render_template('info/all_symbols.html', available_symbols=available_symbols, symbol_info = json_strings, tech_info = json_other)