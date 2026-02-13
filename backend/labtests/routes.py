from flask import Blueprint, abort, render_template
from .services import get_all_labtests, get_labtest_by_id

labtest_bp = Blueprint(
    "labtests",
    __name__
)

@labtest_bp.route("/labtests")
def labtest_list():
    labtests = get_all_labtests()
    return render_template("labtests/labtest-list.html", labtests=labtests)

@labtest_bp.route("/labtests/<int:labtest_id>")
def labtest_detail(labtest_id):
    labtest_detail = get_labtest_by_id(labtest_id)
    if not labtest_detail:
        abort(404) 

    return render_template(
        "labtests/labtest-detail.html",
        labtest=labtest_detail["labtest"]
        #schedules=doctor_detail["schedules"]
    )    
        

