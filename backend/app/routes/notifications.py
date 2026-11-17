from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from app.extensions import db
from app.models.notification import Notification

notifications = Blueprint("notifications", __name__)


def _serialize_notification(notification):
    return {
        "id": notification.id,
        "title": notification.title,
        "message": notification.message,
        "type": notification.type,
        "is_read": notification.is_read,
        "created_at": notification.created_at.isoformat()
        if notification.created_at
        else None,
    }


@notifications.get("")
@login_required
def list_notifications():
    limit = max(1, min(request.args.get("limit", 20, type=int), 100))
    cursor = request.args.get("cursor", type=int)  # last id seen
    unread_only = request.args.get("unread") == "true"

    q = Notification.query.filter_by(user_id=current_user.id)
    if unread_only:
        q = q.filter(Notification.is_read.is_(False))
    if cursor is not None:
        q = q.filter(Notification.id < cursor)

    items = q.order_by(Notification.id.desc()).limit(limit + 1).all()
    has_more = len(items) > limit
    items = items[:limit]

    return jsonify({
        "items": [_serialize_notification(n) for n in items],
        "next_cursor": items[-1].id if has_more else None,
    })


@notifications.get("/unread-count")
@login_required
def unread_count():
    count = Notification.query.filter_by(
        user_id=current_user.id, is_read=False
    ).count()
    return jsonify({"count": count})


@notifications.patch("/<int:notif_id>/read")
@login_required
def mark_read(notif_id):
    n = Notification.query.filter_by(
        id=notif_id, user_id=current_user.id
    ).first_or_404()
    if not n.is_read:
        n.is_read = True
        db.session.commit()
    return jsonify(_serialize_notification(n))


@notifications.post("/read-all")
@login_required
def mark_all_read():
    updated = (
        Notification.query
        .filter_by(user_id=current_user.id, is_read=False)
        .update({"is_read": True})
    )
    db.session.commit()
    return jsonify({"updated": updated})


@notifications.delete("/<int:notif_id>")
@login_required
def delete_notification(notif_id):
    n = Notification.query.filter_by(
        id=notif_id, user_id=current_user.id
    ).first_or_404()
    db.session.delete(n)
    db.session.commit()
    return "", 204