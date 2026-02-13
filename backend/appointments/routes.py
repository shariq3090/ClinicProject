from flask import Blueprint, abort, jsonify, redirect, render_template, request, url_for
from .services import get_available_slots, get_doctor_by_id, save_appointment, appointment_success


appointment_bp = Blueprint(
    "appointments",
    __name__
)

@appointment_bp.route("/appointments/<int:doctor_id>")
def appointment_list(doctor_id):  
    data = get_doctor_by_id(doctor_id)        
    if not data:
        abort(404)
       
    return render_template(
        "appointments/bookappointment.html", doctor=data['doctor']
    )

@appointment_bp.route("/appointments/<int:doctor_id>/available-slots")
def available_slots(doctor_id): 
    #print("Inside appointment doctor", doctor_id)
    date = request.args.get("date")
    #print("Appointment route: ", doctor_id, date)
    slots = get_available_slots(doctor_id, date)    
    #slots= "1, 2, 3"
    return jsonify(slots)

@appointment_bp.route("/doctors/<int:doctor_id>/book", methods=["GET", "POST"])
def saveappointment(doctor_id):
    if request.method == "POST":        
        appointment_id=save_appointment(doctor_id)                
        data=appointment_success(appointment_id)        
        return render_template("appointments/appointment_success.html", appointment=data        
        )        

@appointment_bp.route("/appointment-success/<int:appointment_id>")
def appointment_success123(appointment_id):
    #appointment1 = appointment_success(appointment_id)
    return render_template(
        "appointments.appointment_success.html", appointment_id = appointment_id          
    )