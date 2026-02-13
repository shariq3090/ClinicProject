from flask import Blueprint, abort, render_template
from .services import get_all_accreditions, get_accredition_by_id

accredition_bp = Blueprint(
    "accreditions",
    __name__
)

@accredition_bp.route("/accreditions")
def accredition_list():
    accreditions = get_all_accreditions()
    return render_template("accreditions/accredition-list.html", accreditions=accreditions)

@accredition_bp.route("/accreditions/<int:accredition_id>")
def accredition_detail(accredition_id):
    accredition_detail = get_accredition_by_id(accredition_id)
    if not accredition_detail:
        abort(404) 

    return render_template(
        "accreditions/accredition-detail.html",
        accredition=accredition_detail["accredition"]
        #schedules=doctor_detail["schedules"]
    )    
        

