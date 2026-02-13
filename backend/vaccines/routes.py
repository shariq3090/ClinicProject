from flask import Blueprint, abort, render_template
from .services import get_all_vaccines, get_vaccine_by_id

vaccine_bp = Blueprint(
    "vaccines",
    __name__
)

@vaccine_bp.route("/vaccines")
def vaccine_list():
    vaccines = get_all_vaccines()
    return render_template("vaccines/vaccine-list.html", vaccines=vaccines)

@vaccine_bp.route("/vaccines/<int:vaccine_id>")
def vaccine_detail(vaccine_id):
    vaccine_detail = get_vaccine_by_id(vaccine_id)
    if not vaccine_detail:
        abort(404) 

    return render_template(
        "vaccines/vaccine-detail.html",
        vaccine=vaccine_detail["vaccine"]
        #schedules=doctor_detail["schedules"]
    )    
        

