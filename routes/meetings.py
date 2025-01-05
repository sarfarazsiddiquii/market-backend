from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from config import Config

meetings_bp = Blueprint('meetings', __name__)

@meetings_bp.route('/create_meeting', methods=['POST'])
@jwt_required()
def create_meeting():
    current_user = get_jwt_identity()

    data = request.json
    title = data.get('title')
    meeting_time = data.get('meeting_time')  # Expected format: "YYYY-MM-DD HH:MM:SS"

    if not title or not meeting_time:
        return jsonify({"error": "Title and meeting time are required"}), 400

    try:
        meeting_time = datetime.strptime(meeting_time, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return jsonify({"error": "Invalid meeting time format. Use 'YYYY-MM-DD HH:MM:SS'"}), 400

    # Insert the meeting into the collection
    Config.meetings_collection.insert_one({
        'username': current_user,
        'title': title,
        'meeting_time': meeting_time
    })

    return jsonify({"message": "Meeting created successfully!"}), 201

@meetings_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    current_user = get_jwt_identity()
    now = datetime.now()

    meetings = list(Config.meetings_collection.find(
        {'username': current_user, 'meeting_time': {'$gte': now}}
    ))

    return jsonify({
        "username": current_user,
        "meetings": [{
            "id": str(meeting["_id"]),
            "title": meeting["title"],
            "time": meeting["meeting_time"].strftime("%Y-%m-%d %H:%M:%S")
        } for meeting in meetings]
    }), 200