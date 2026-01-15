from forms.forms import ContactForm
from flask import Blueprint, jsonify, request
from config import db
from models.models import ContactMessage

test_bp = Blueprint('test_bp', __name__)

@test_bp.route('/', methods=['POST'])
def test():
    return "Contact Form Test Blueprint is working!"

@test_bp.route('/test', methods=['POST'])
def test_contact_form():
    """Test contact form submission"""
    try:
        form = ContactForm(meta={"csrf": False})

        if request.is_json:
            form.process(data=request.get_json())
        else:
            form.process(formdata=request.form)

        if not form.validate():
            return jsonify({"error": "validation failed", "details": form.errors}), 400

        contact_message = ContactMessage(
            fname=form.fname.data,
            lname=form.lname.data,
            email=form.email.data,
            subject=form.subject.data,
            message=form.message.data,
        )

        db.session.add(contact_message)
        db.session.commit()

        return jsonify({"message": "contact message submitted", "data": {
            "fname": contact_message.fname,
            "lname": contact_message.lname,
            "email": contact_message.email,
            "subject": contact_message.subject,
            "message": contact_message.message,
            "created_at": contact_message.created_at.isoformat() 
        }}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error submitting contact message: {e}"}), 500


@test_bp.route('/messages', methods=['GET'])
def get_contact_messages():
    """Retrieve all contact messages"""
    try:
        messages = ContactMessage.query.all()
        messages_data = [{
            "id": msg.id,
            "fname": msg.fname,
            "lname": msg.lname,
            "email": msg.email,
            "subject": msg.subject,
            "message": msg.message,
            "created_at": msg.created_at.isoformat()
        } for msg in messages]

        return jsonify({"messages": messages_data}), 200

    except Exception as e:
        return jsonify({"error": f"Error retrieving contact messages: {e}"}), 500

@test_bp.route('/messages/<int:message_id>', methods=['GET'])
def get_contact_message(message_id):
    """Retrieve a specific contact message by ID"""
    try:
        msg = ContactMessage.query.get(message_id)
        if not msg:
            return jsonify({"error": "Contact message not found"}), 404

        message_data = {
            "id": msg.id,
            "fname": msg.fname,
            "lname": msg.lname,
            "email": msg.email,
            "subject": msg.subject,
            "message": msg.message,
            "created_at": msg.created_at.isoformat()
        }

        return jsonify({"message": message_data}), 200

    except Exception as e:
        return jsonify({"error": f"Error retrieving contact message: {e}"}), 500


@test_bp.route('/messages/<int:message_id>', methods=['DELETE'])
def delete_contact_message(message_id):
    """Delete a specific contact message by ID"""
    try:
        msg = ContactMessage.query.get(message_id)
        if not msg:
            return jsonify({"error": "Contact message not found"}), 404

        db.session.delete(msg)
        db.session.commit()

        return jsonify({"message": "Contact message deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error deleting contact message: {e}"}), 500


@test_bp.route('/messages', methods=['DELETE'])
def delete_all_contact_messages():
    '''Delete all contact messages'''
    try:
        num_deleted = db.session.query(ContactMessage).delete()
        db.session.commit()

        return jsonify({"message": f"All contact messages deleted successfully. Total deleted: {num_deleted}"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error deleting contact messages: {e}"}), 500