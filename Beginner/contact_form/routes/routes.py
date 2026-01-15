from flask import Blueprint, flash, redirect, render_template, url_for

from config import db
from forms.forms import ContactForm
from models.models import ContactMessage


contact_bp = Blueprint('contact_bp', __name__)


@contact_bp.route('/', methods=['GET'])
def home():
	return redirect(url_for('contact_bp.submit_contact_form'))


@contact_bp.route('/contact', methods=['GET', 'POST'])
def submit_contact_form():
    form = ContactForm()

    if form.validate_on_submit():
        try:
            contact_message = ContactMessage(
                fname=form.fname.data,
                lname=form.lname.data,
                email=form.email.data,
                subject=form.subject.data,
                message=form.message.data,
            )
            db.session.add(contact_message)
            db.session.commit()

            flash("Message sent successfully.", "success")
            return redirect(url_for('contact_bp.submit_contact_form'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error submitting contact message: {e}", "error")
            return render_template('contact.html', form=form), 500

    return render_template('contact.html', form=form)