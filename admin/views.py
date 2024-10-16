from flask import Blueprint, render_template
from flask_login import login_required
from models import User


admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


@admin_blueprint.route('/admin')
@login_required
def admin():
    return render_template('admin/admin.html')


@admin_blueprint.route('/view_all_users', methods=['POST'])
@login_required
def view_all_users():
    return render_template('admin/admin.html', registered_users=User.query.all())


@admin_blueprint.route('/logs', methods=['POST'])
@login_required
def logs():
    return render_template('admin/admin.html')