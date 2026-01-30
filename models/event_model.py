from datetime import datetime
from typing import Optional, Dict, Any

class Event:
    """Event model representing a GitHub webhook event"""
    
    def __init__(
        self,
        request_id: str,
        author: str,
        action: str,
        to_branch: str,
        from_branch: Optional[str] = None,
        timestamp: Optional[str] = None
    ):
        self.request_id = request_id
        self.author = author
        self.action = action
        self.from_branch = from_branch
        self.to_branch = to_branch
        self.timestamp = timestamp or datetime.utcnow().isoformat() + 'Z'
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary for MongoDB storage"""
        return {
            'request_id': self.request_id,
            'author': self.author,
            'action': self.action,
            'from_branch': self.from_branch,
            'to_branch': self.to_branch,
            'timestamp': self.timestamp
        }


class WebhookProcessor:
    """Process GitHub webhook events"""
    
    @staticmethod
    def process_push_event(payload: Dict[str, Any]) -> Optional[Event]:
        """Process PUSH event from GitHub"""
        commit = payload.get('head_commit', {})
        if not commit:
            return None
        
        author = (
            commit['author']['name'] 
            if commit.get('author') 
            else payload.get('pusher', {}).get('name', 'Unknown')
        )
        
        return Event(
            request_id=commit['id'][:7],
            author=author,
            action='PUSH',
            from_branch=None,
            to_branch=payload['ref'].replace('refs/heads/', '')
        )
    
    @staticmethod
    def process_pull_request_event(payload: Dict[str, Any]) -> Optional[Event]:
        """Process PULL_REQUEST event from GitHub"""
        pr = payload['pull_request']
        pr_action = payload['action']
        
        if pr_action not in ['opened', 'closed']:
            return None
        
        if pr_action == 'opened':
            return Event(
                request_id=str(pr['number']),
                author=pr['user']['login'],
                action='PULL_REQUEST',
                from_branch=pr['head']['ref'],
                to_branch=pr['base']['ref']
            )
        
        elif pr_action == 'closed' and pr.get('merged', False):
            author = pr.get('merged_by', {}).get('login', pr['user']['login'])
            return Event(
                request_id=str(pr['number']),
                author=author,
                action='MERGE',
                from_branch=pr['head']['ref'],
                to_branch=pr['base']['ref']
            )
        
        return None
    
    @staticmethod
    def process_event(event_type: str, payload: Dict[str, Any]) -> Optional[Event]:
        """Main processor that routes to specific event handlers"""
        if event_type == 'push':
            return WebhookProcessor.process_push_event(payload)
        elif event_type == 'pull_request':
            return WebhookProcessor.process_pull_request_event(payload)
        return None