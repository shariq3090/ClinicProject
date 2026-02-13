from flask import Blueprint, abort, render_template
from .services import get_all_doctors, get_doctor_by_id

doctor_bp = Blueprint(
    "doctors",
    __name__
)

@doctor_bp.route("/doctors")
def doctor_list():
    doctors = get_all_doctors()
    return render_template("doctors/doctor-list.html", doctors=doctors)

@doctor_bp.route("/doctors/<int:doctor_id>")
def doctor_detail(doctor_id):
    doctor_detail = get_doctor_by_id(doctor_id)
    if not doctor_detail:
        abort(404) 

    return render_template(
        "doctors/doctor-detail.html",
        doctor=doctor_detail["doctor"],
        schedules=doctor_detail["schedules"]
    )    
        

