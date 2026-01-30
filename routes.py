from flask import Blueprint, request, jsonify, render_template
from datetime import datetime
from models import WebhookProcessor
from database import Database


webhook_bp = Blueprint('webhook', __name__)
api_bp = Blueprint('api', __name__)

db = None

def init_routes(database: Database):
    """Initialize routes with database instance"""
    global db
    db = database


# ============= Webhook Routes =============

@webhook_bp.route('/webhook', methods=['POST'])
def handle_webhook():
    """Receive and process GitHub webhooks"""
    try:
        event_type = request.headers.get('X-GitHub-Event')
        payload = request.json
        
        print(f"Received {event_type} event")
        
        if event_type in ['push', 'pull_request']:
            event = WebhookProcessor.process_event(event_type, payload)
            
            if event:
                success = db.insert_event(event.to_dict())
                if success:
                    print(f"Stored event: {event.to_dict()}")
                    return jsonify({'status': 'success'}), 200
        
        return jsonify({'status': 'ignored'}), 200
    
    except Exception as e:
        print(f"Error processing webhook: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 400


# ============= API Routes =============

@api_bp.route('/')
def home():
    """Render home page"""
    return render_template('index.html')

@api_bp.route('/api/events', methods=['GET'])
def get_events():
    """API endpoint to fetch events"""
    try:
        limit = int(request.args.get('limit', 20))
        events = db.get_events(limit)
        return jsonify(events)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    })