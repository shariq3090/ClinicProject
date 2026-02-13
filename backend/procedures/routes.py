from flask import Blueprint, abort, render_template
from .services import get_all_procedures, get_procedure_by_id

procedure_bp = Blueprint(
    "procedures",
    __name__
)

@procedure_bp.route("/procedures")
def procedure_list():
    procedures = get_all_procedures()
    return render_template("procedures/procedure-list.html", procedures=procedures)

@procedure_bp.route("/procedures/<int:procedure_id>")
def procedure_detail(procedure_id):
    procedure_detail = get_procedure_by_id(procedure_id)
    if not procedure_detail:
        abort(404) 

    return render_template(
        "procedures/procedure-detail.html",
        procedure=procedure_detail["procedure"]
        #schedules=doctor_detail["schedules"]
    )    
        

