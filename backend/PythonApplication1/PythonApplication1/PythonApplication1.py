from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import csv
import os

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# 用户表
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))


# 通讯录表
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# 初始化数据库
with app.app_context():
    db.create_all()


# 注册接口
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({'success': False, 'message': 'Username already exists'})

    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'success': True})


# 登录接口
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username, password=password).first()
    if user:
        return jsonify({'success': True, 'user_id': user.id})
    else:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401


# 获取联系人
@app.route('/api/contacts/<int:user_id>', methods=['GET'])
def get_contacts(user_id):
    contacts = Contact.query.filter_by(user_id=user_id).all()
    return jsonify([{'id': c.id, 'name': c.name, 'phone': c.phone} for c in contacts])


# 添加联系人
@app.route('/api/contacts', methods=['POST'])
def add_contact():
    data = request.get_json()
    new_contact = Contact(name=data['name'], phone=data['phone'], user_id=data['user_id'])
    db.session.add(new_contact)
    db.session.commit()
    return jsonify({'success': True})


# 修改联系人
@app.route('/api/contacts/<int:id>', methods=['PUT'])
def update_contact(id):
    data = request.get_json()
    contact = Contact.query.get(id)
    if not contact:
        return jsonify({'success': False, 'message': 'Contact not found'})
    contact.name = data['name']
    contact.phone = data['phone']
    db.session.commit()
    return jsonify({'success': True})


# 删除联系人
@app.route('/api/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    contact = Contact.query.get(id)
    if not contact:
        return jsonify({'success': False, 'message': 'Contact not found'})
    db.session.delete(contact)
    db.session.commit()
    return jsonify({'success': True})

from flask import send_file

@app.route('/api/export/<int:user_id>', methods=['GET'])
def export_contacts(user_id):
    contacts = Contact.query.filter_by(user_id=user_id).all()
    filename = f'contacts_user_{user_id}.csv'
    filepath = os.path.join(os.getcwd(), filename)

    # 写入 CSV
    with open(filepath, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Name', 'Phone'])
        for c in contacts:
            writer.writerow([c.name, c.phone])

    # 用 send_file 直接让浏览器下载
    return send_file(
        filepath,
        as_attachment=True,
        download_name=filename,
        mimetype='text/csv'
    )


if __name__ == '__main__':
    app.run(debug=True)

