"""
Flask API Server for Real Estate Agent
Provides REST endpoints for messaging integration
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os
from dotenv import load_dotenv
import logging

from real_estate_agent import RealEstateAgent

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the agent
agent = RealEstateAgent()

# In-memory conversation storage (use Redis/MongoDB in production)
conversations = {}


# ==================== API ENDPOINTS ====================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "real-estate-agent",
        "timestamp": datetime.now().isoformat()
    })


@app.route('/api/message', methods=['POST'])
def handle_message():
    """
    Handle incoming customer messages
    
    Request body:
    {
        "message": "customer message in Darija",
        "customer_id": "unique_customer_id",
        "platform": "whatsapp|facebook|website"
    }
    """
    try:
        data = request.get_json()
        
        # Validate request
        if not data or 'message' not in data:
            return jsonify({"error": "Message is required"}), 400
        
        message = data['message']
        customer_id = data.get('customer_id', 'anonymous')
        platform = data.get('platform', 'api')
        
        logger.info(f"Processing message from {customer_id} on {platform}")
        
        # Process the message through the agent
        result = agent.process_message(message, thread_id=customer_id)
        
        # Store conversation
        if customer_id not in conversations:
            conversations[customer_id] = []
        
        conversations[customer_id].append({
            "timestamp": result['timestamp'],
            "customer_message": message,
            "agent_response": result['response'],
            "metadata": {
                "intent": result['intent'],
                "sentiment": result['sentiment'],
                "stage": result['stage']
            }
        })
        
        # Return response
        return jsonify({
            "success": True,
            "response": result['response'],
            "metadata": {
                "intent": result['intent'],
                "sentiment": result['sentiment'],
                "conversation_stage": result['stage'],
                "properties_count": len(result['properties']),
                "follow_up_needed": result['follow_up_needed']
            },
            "properties": result['properties'],
            "timestamp": result['timestamp']
        })
        
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/conversation/<customer_id>', methods=['GET'])
def get_conversation_history(customer_id):
    """
    Retrieve conversation history for a customer
    """
    history = conversations.get(customer_id, [])
    
    return jsonify({
        "success": True,
        "customer_id": customer_id,
        "message_count": len(history),
        "conversation": history
    })


@app.route('/api/webhook/whatsapp', methods=['POST'])
def whatsapp_webhook():
    """
    Webhook endpoint for WhatsApp Business API integration
    """
    try:
        data = request.get_json()
        
        # Extract WhatsApp message data
        # Format varies by provider (Twilio, Meta, etc.)
        # This is a generic example
        
        if 'messages' in data:
            for msg_data in data['messages']:
                customer_phone = msg_data.get('from', 'unknown')
                message_text = msg_data.get('text', {}).get('body', '')
                
                if message_text:
                    # Process through agent
                    result = agent.process_message(message_text, thread_id=customer_phone)
                    
                    # Here you would send the response back via WhatsApp API
                    # This depends on your WhatsApp provider
                    logger.info(f"WhatsApp response: {result['response']}")
                    
                    return jsonify({
                        "success": True,
                        "response_sent": True
                    })
        
        return jsonify({"success": True})
        
    except Exception as e:
        logger.error(f"WhatsApp webhook error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/webhook/facebook', methods=['POST'])
def facebook_webhook():
    """
    Webhook endpoint for Facebook Messenger integration
    """
    try:
        data = request.get_json()
        
        # Facebook Messenger webhook format
        if data.get('object') == 'page':
            for entry in data.get('entry', []):
                for messaging_event in entry.get('messaging', []):
                    
                    sender_id = messaging_event.get('sender', {}).get('id')
                    message_text = messaging_event.get('message', {}).get('text')
                    
                    if sender_id and message_text:
                        # Process through agent
                        result = agent.process_message(message_text, thread_id=sender_id)
                        
                        # Send response via Facebook Send API
                        logger.info(f"Facebook response: {result['response']}")
        
        return jsonify({"success": True})
        
    except Exception as e:
        logger.error(f"Facebook webhook error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """
    Get analytics on conversations
    """
    total_conversations = len(conversations)
    total_messages = sum(len(conv) for conv in conversations.values())
    
    # Calculate intent distribution
    intent_counts = {}
    sentiment_counts = {}
    
    for conv_history in conversations.values():
        for msg in conv_history:
            intent = msg.get('metadata', {}).get('intent', 'unknown')
            sentiment = msg.get('metadata', {}).get('sentiment', 'unknown')
            
            intent_counts[intent] = intent_counts.get(intent, 0) + 1
            sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1
    
    return jsonify({
        "total_conversations": total_conversations,
        "total_messages": total_messages,
        "intent_distribution": intent_counts,
        "sentiment_distribution": sentiment_counts,
        "timestamp": datetime.now().isoformat()
    })


@app.route('/api/broadcast', methods=['POST'])
def broadcast_message():
    """
    Broadcast a message to specific customers (for marketing)
    
    Request body:
    {
        "message": "promotional message",
        "customer_ids": ["id1", "id2", ...] or "all"
    }
    """
    try:
        data = request.get_json()
        
        message = data.get('message')
        target_customers = data.get('customer_ids', 'all')
        
        if not message:
            return jsonify({"error": "Message is required"}), 400
        
        sent_count = 0
        
        if target_customers == 'all':
            target_customers = list(conversations.keys())
        
        # In production, this would queue messages for asynchronous sending
        for customer_id in target_customers:
            # Here you would send via the appropriate channel
            # (WhatsApp, SMS, Email, etc.)
            logger.info(f"Broadcasting to {customer_id}: {message}")
            sent_count += 1
        
        return jsonify({
            "success": True,
            "message_sent": sent_count,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Broadcast error: {str(e)}")
        return jsonify({"error": str(e)}), 500


# ==================== MAIN ====================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting Real Estate Agent API on port {port}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
