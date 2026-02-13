from flask import Blueprint, abort, render_template
from .services import get_all_opdservices, get_opdservice_by_id

opdservice_bp = Blueprint(
    "opdservices",
    __name__
)

@opdservice_bp.route("/opdservices")
def opdservice_list():
    opdservices = get_all_opdservices()
    return render_template("opdservices/opdservice-list.html", opdservices=opdservices)

@opdservice_bp.route("/opdservices/<int:opdservice_id>")
def opdservice_detail(opdservice_id):
    opdservice_detail = get_opdservice_by_id(opdservice_id)
    if not opdservice_detail:
        abort(404) 

    return render_template(
        "opdservices/opdservice-detail.html",
        opdservice=opdservice_detail["opdservice"]
        #schedules=doctor_detail["schedules"]
    )    
        

