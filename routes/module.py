from flask import Blueprint, render_template
from services.module_service import find_module, list_fields_for_module

module_bp = Blueprint("module", __name__)  # Module Blueprint

# @module_bp.route("/eating", methods=["GET"])  # Route for the eating module
# def get_eating_module_and_fields():
#     module = find_module(1)
#     if not module:
#         return render_template("module_not_found.html"), 404
#     fields = list_fields_for_module(1)
#     return render_template("eating.html", module=module, fields=fields)