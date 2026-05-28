import sys, os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import get_image_generation_completion
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import time
app = Flask(__name__)
CORS(app)
stories_db = []
@app.get('/health')
def health():
    return jsonify(status='ok')
# Story 1: Casual Reader
@app.route("/api/locations/suggest", methods=["GET"])
def api_locations_suggest_story1():
    q = (request.args.get("q") or "").strip().lower()
    if not q:
        return jsonify({"suggestions": []}), 200

    pool = [
        "Silent Pines, Oregon",
        "Blackwater Bay, Maine",
        "Ashen Hollow, Scotland",
        "Ravenmoor, Yorkshire",
        "Dead Man's Crossing, Nevada",
        "Fogreach Harbor, Washington",
        "Cinderfield, West Virginia",
        "Harrowgate, Massachusetts",
        "Gloamwood Forest, Ontario",
        "The Old Quarter, Prague",
    ]
    suggestions = [p for p in pool if q in p.lower()][:8]
    return jsonify({"suggestions": suggestions}), 200


@app.route("/api/generate", methods=["POST"])
def api_generate_story1():
    data = request.get_json(silent=True) or {}
    location = (data.get("location") or "").strip()
    if not location:
        return jsonify({"error": "location is required"}), 400

    tone = (data.get("tone") or "classic").strip().lower()
    length = (data.get("length") or "medium").strip().lower()

    # Hardcoded placeholder horror stories (2-4 sentences), lightly varied by tone/length
    base_story = (
        f"In {location}, the fog arrives early and stays too long, swallowing streetlamps one by one. "
        "A voice calls your name from behind locked doors, repeating it until the wood begins to breathe. "
        "When you finally look back, your footprints end at a fresh set that leads away without you."
    )
    bleak_story = (
        f"{location} looks normal at noon, but the shadows there remember faces. "
        "You find a postcard of the place in your pocket—dated tomorrow—with your own obituary printed beneath the skyline. "
        "The ink is still wet when you read it aloud."
    )
    campy_story = (
        f"At {location}, the souvenir shop sells 'authentic' cursed keys for five bucks. "
        "You laugh—until every door you pass clicks open by itself, and the keys jingle in your stomach like teeth. "
        "The clerk waves from the reflection behind you, even though the store is miles away."
    )

    if tone in ("bleak", "grim", "serious"):
        story = bleak_story
    elif tone in ("campy", "fun", "pulp"):
        story = campy_story
    else:
        story = base_story

    if length in ("short", "tiny"):
        story = " ".join(story.split(" ")[:40]).rstrip(".") + "."
    elif length in ("long", "extended"):
        story = story + " The last thing you hear is the fog learning your voice."

    prompt = (
        f"A dark, eerie, cinematic horror scene at {location}: haunted, foggy, unsettling atmosphere; "
        f"tone={tone}; ominous shadows, distressed textures, low-key lighting, high contrast, realistic, terrifying"
    )
    try:
        file_path, image_url = get_image_generation_completion(
            prompt, None, "qwen/qwen-image-2512", "apifree"
        )
    except Exception:
        image_url = None

    if not image_url:
        image_url = f"https://picsum.photos/seed/{int(time.time())}/1024/768"

    story_id = str(int(time.time() * 1000))
    record = {
        "id": story_id,
        "location": location,
        "tone": tone,
        "length": length,
        "story": story,
        "image_url": image_url,
        "created_at": int(time.time()),
        "status": "active",  # active/hidden/deleted
        "safe_mode": False,
        "reports": [],
        "shares": 0,
    }
    stories_db.append(record)
    return jsonify(record), 201


# Story 2: Travel Blogger
@app.route("/api/presets", methods=["GET"])
def api_get_presets_story2():
    return jsonify(
        {
            "tones": [
                {"id": "classic", "label": "Classic Gothic"},
                {"id": "bleak", "label": "Bleak / Serious"},
                {"id": "campy", "label": "Campy Pulp"},
            ],
            "lengths": [
                {"id": "short", "label": "Short"},
                {"id": "medium", "label": "Medium"},
                {"id": "long", "label": "Long"},
            ],
        }
    ), 200


@app.route("/api/generate/custom", methods=["POST"])
def api_generate_custom_story2():
    data = request.get_json(silent=True) or {}
    location = (data.get("location") or "").strip()
    tone = (data.get("tone") or "classic").strip().lower()
    length = (data.get("length") or "medium").strip().lower()

    if not location:
        return jsonify({"error": "location is required"}), 400
    if tone not in ("classic", "bleak", "campy"):
        return jsonify({"error": "tone must be one of: classic, bleak, campy"}), 400
    if length not in ("short", "medium", "long"):
        return jsonify({"error": "length must be one of: short, medium, long"}), 400

    story_variants = {
        "classic": (
            f"The air in {location} tastes of rust and rain, as if the sky is bleeding quietly. "
            "You follow a lantern glow down a lane that shouldn't exist, and every window reflects a stranger wearing your face. "
            "When the lantern goes out, the stranger smiles first."
        ),
        "bleak": (
            f"In {location}, the local map has a blank spot that everyone pretends not to see. "
            "You step into it anyway, and the world becomes soundless, like a photograph holding its breath. "
            "Hours later you return, but your friends swear you never arrived."
        ),
        "campy": (
            f"{location} has a charming little inn with complimentary mints and a complimentary curse. "
            "At midnight the hallway wallpaper peels itself into grinning faces, offering room service in a dead language. "
            "You tip them anyway; they keep the coin and take the hand."
        ),
    }
    story = story_variants[tone]

    if length == "short":
        story = " ".join(story.split(" ")[:45]).rstrip(".") + "."
    elif length == "long":
        story = story + " At dawn, the checkout receipt lists your name under 'lost and found'."

    prompt = (
        f"A dark, eerie, cinematic horror scene at {location}: haunted, foggy, unsettling atmosphere; "
        f"{tone} vibe; cinematic framing, volumetric fog, ominous silhouettes, realistic detail, scary"
    )
    try:
        file_path, image_url = get_image_generation_completion(
            prompt, None, "qwen/qwen-image-2512", "apifree"
        )
    except Exception:
        image_url = None
    if not image_url:
        image_url = f"https://picsum.photos/seed/{int(time.time())}/1024/768"

    story_id = str(int(time.time() * 1000))
    record = {
        "id": story_id,
        "location": location,
        "tone": tone,
        "length": length,
        "story": story,
        "image_url": image_url,
        "created_at": int(time.time()),
        "status": "active",
        "safe_mode": False,
        "reports": [],
        "shares": 0,
    }
    stories_db.append(record)
    return jsonify(record), 201


# Story 3: Casual Reader
@app.route("/api/stories", methods=["GET"])
def api_get_all_stories_story3():
    # Frontend history feature depends on returning ALL stored stories
    return jsonify(stories_db), 200


@app.route("/api/stories/<story_id>/share", methods=["POST"])
def api_share_story_link_story3(story_id):
    base_url = (request.host_url or "").rstrip("/")
    for s in stories_db:
        if s.get("id") == story_id and s.get("status") != "deleted":
            s["shares"] = int(s.get("shares", 0)) + 1
            return (
                jsonify(
                    {
                        "id": s["id"],
                        "share_url": f"{base_url}/share/{s['id']}",
                        "story": s["story"],
                        "image_url": s["image_url"],
                        "shares": s["shares"],
                    }
                ),
                200,
            )
    return jsonify({"error": "story not found"}), 404


# Story 4: User
@app.route("/api/stories/<story_id>/report", methods=["POST"])
def api_report_story_story4(story_id):
    data = request.get_json(silent=True) or {}
    reason = (data.get("reason") or "").strip()
    details = (data.get("details") or "").strip()

    if not reason:
        return jsonify({"error": "reason is required"}), 400

    for s in stories_db:
        if s.get("id") == story_id and s.get("status") != "deleted":
            report = {
                "report_id": str(int(time.time() * 1000)),
                "story_id": story_id,
                "reason": reason,
                "details": details,
                "created_at": int(time.time()),
                "status": "open",  # open/triaged/closed
            }
            s.setdefault("reports", []).append(report)
            return jsonify({"message": "report submitted", "report": report}), 201

    return jsonify({"error": "story not found"}), 404


# Story 5: Moderator
@app.route("/mod/reports", methods=["GET"])
def mod_list_reports_story5():
    status = (request.args.get("status") or "").strip().lower()  # optional filter
    out = []
    for s in stories_db:
        if s.get("status") == "deleted":
            continue
        for r in s.get("reports", []) or []:
            if status and (r.get("status") or "").lower() != status:
                continue
            out.append(
                {
                    "report_id": r.get("report_id"),
                    "story_id": s.get("id"),
                    "location": s.get("location"),
                    "reason": r.get("reason"),
                    "details": r.get("details"),
                    "report_status": r.get("status"),
                    "story_status": s.get("status"),
                    "created_at": r.get("created_at"),
                }
            )
    return jsonify(out), 200


@app.route("/mod/stories/<story_id>/action", methods=["POST"])
def mod_story_action_story5(story_id):
    data = request.get_json(silent=True) or {}
    action = (data.get("action") or "").strip().lower()
    block_trigger = (data.get("block_trigger") or "").strip().lower()
    report_id = (data.get("report_id") or "").strip()
    note = (data.get("note") or "").strip()

    allowed = {"hide", "delete", "regenerate_safe", "block_trigger", "close_report", "triage_report"}
    if action not in allowed:
        return jsonify({"error": f"action must be one of: {', '.join(sorted(allowed))}"}), 400

    # Find story
    story_rec = None
    for s in stories_db:
        if s.get("id") == story_id:
            story_rec = s
            break
    if not story_rec:
        return jsonify({"error": "story not found"}), 404

    # Ensure moderation metadata exists
    story_rec.setdefault("moderation", {"blocked_triggers": [], "log": []})
    story_rec["moderation"].setdefault("blocked_triggers", [])
    story_rec["moderation"].setdefault("log", [])

    # Apply actions
    if action == "hide":
        story_rec["status"] = "hidden"
        story_rec["moderation"]["log"].append(
            {"ts": int(time.time()), "action": "hide", "note": note}
        )
        return jsonify({"message": "story hidden", "id": story_id, "story": story_rec["story"], "image_url": story_rec["image_url"]}), 200

    if action == "delete":
        story_rec["status"] = "deleted"
        story_rec["moderation"]["log"].append(
            {"ts": int(time.time()), "action": "delete", "note": note}
        )
        return jsonify({"message": "story deleted", "id": story_id}), 200

    if action == "block_trigger":
        if not block_trigger:
            return jsonify({"error": "block_trigger is required for action=block_trigger"}), 400
        if block_trigger not in story_rec["moderation"]["blocked_triggers"]:
            story_rec["moderation"]["blocked_triggers"].append(block_trigger)
        story_rec["moderation"]["log"].append(
            {"ts": int(time.time()), "action": "block_trigger", "trigger": block_trigger, "note": note}
        )
        return jsonify(
            {
                "message": "trigger blocked",
                "id": story_id,
                "blocked_triggers": story_rec["moderation"]["blocked_triggers"],
            }
        ), 200

    if action in ("close_report", "triage_report"):
        if not report_id:
            return jsonify({"error": "report_id is required for report actions"}), 400
        updated = False
        for r in story_rec.get("reports", []) or []:
            if r.get("report_id") == report_id:
                r["status"] = "closed" if action == "close_report" else "triaged"
                updated = True
                break
        if not updated:
            return jsonify({"error": "report not found"}), 404

        story_rec["moderation"]["log"].append(
            {"ts": int(time.time()), "action": action, "report_id": report_id, "note": note}
        )
        return jsonify({"message": "report updated", "report_id": report_id, "status": r["status"]}), 200

    # action == regenerate_safe
    location = story_rec.get("location") or "an unknown place"
    tone = (story_rec.get("tone") or "classic").strip().lower()

    # Safe-mode placeholder story (2-4 sentences)
    safe_story = (
        f"In {location}, the night feels heavy, but the danger stays at the edge of sight. "
        "You hear distant footsteps in the fog and choose the brighter street, refusing to follow the whispers. "
        "By morning, the town looks ordinary again—yet the air still remembers something watching."
    )
    story_rec["story"] = safe_story
    story_rec["safe_mode"] = True
    story_rec["status"] = "active"

    prompt = (
        f"A dark, eerie, cinematic horror scene at {location}: haunted, foggy, unsettling atmosphere; "
        f"SAFE MODE; no gore; spooky silhouettes, moody lighting, cinematic realism, scary but non-graphic; tone={tone}"
    )
    try:
        file_path, image_url = get_image_generation_completion(
            prompt, None, "qwen/qwen-image-2512", "apifree"
        )
    except Exception:
        image_url = None
    if not image_url:
        image_url = f"https://picsum.photos/seed/{int(time.time())}/1024/768"
    story_rec["image_url"] = image_url

    story_rec["moderation"]["log"].append(
        {"ts": int(time.time()), "action": "regenerate_safe", "note": note}
    )
    return jsonify(
        {
            "message": "story regenerated in safe mode",
            "id": story_id,
            "story": story_rec["story"],
            "image_url": story_rec["image_url"],
            "safe_mode": True,
        }
    ), 200
# Serve frontend
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5005)