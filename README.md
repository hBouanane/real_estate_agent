# 🏠 Real Estate Agent - Moroccan Darija

An intelligent real estate agent powered by **Google Gemini 3 Pro**, **LangChain**, **LangGraph**, and **LangSmith** that responds to customer inquiries in Moroccan Darija (Moroccan Arabic dialect).

## 🌟 Features

### Core Capabilities
- **🗣️ Moroccan Darija Communication**: Natural conversations in the local dialect
- **🤖 AI-Powered Intelligence**: Leverages Google Gemini 3 Pro for contextual understanding
- **📊 Smart Intent Analysis**: Automatically detects customer intent (buy/rent/sell/inquiry)
- **😊 Sentiment Detection**: Analyzes emotional tone (positive/neutral/negative/urgent)
- **🏢 Property Matching**: Recommends properties based on customer preferences
- **📈 Conversation Stage Tracking**: Manages sales funnel stages (greeting → qualifying → presenting → negotiating → closing)
- **💾 Memory & Context**: Maintains conversation history using LangGraph checkpointing
- **📡 Multi-Platform Support**: Webhooks for WhatsApp, Facebook Messenger, and custom integrations
- **📊 Analytics Dashboard**: Track conversations, intents, and sentiment distribution
- **🔍 LangSmith Monitoring**: Full observability and debugging capabilities

### Creative Features
- **Contextual Responses**: Adapts tone based on conversation stage and customer sentiment
- **Dynamic Property Recommendations**: Matches properties using intelligent filtering
- **Follow-up Management**: Automatically flags conversations needing follow-up
- **Multi-turn Conversations**: Maintains context across multiple messages
- **Bilingual Support**: Seamlessly handles Arabic and French terms

## 🏗️ Architecture

### LangGraph State Machine

```
┌─────────────┐
│   Analyze   │  ← Extract intent, sentiment, preferences
│   Intent    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Determine  │  ← Identify conversation stage
│    Stage    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    Fetch    │  ← Query property database
│ Properties  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Generate   │  ← Create response in Darija
│  Response   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    Check    │  ← Determine follow-up needs
│  Follow-up  │
└─────────────┘
```

### State Schema

```python
class AgentState(TypedDict):
    messages: List[BaseMessage]          # Conversation history
    customer_intent: str                 # buy/rent/sell/inquiry
    property_preferences: dict           # location, budget, type, etc.
    sentiment: str                       # positive/neutral/negative/urgent
    conversation_stage: str              # Current funnel stage
    recommended_properties: list         # Matched properties
    follow_up_needed: bool              # Flag for CRM
```

## 📦 Installation

### Prerequisites
- Python 3.9+
- Google API Key (for Gemini)
- LangSmith API Key (optional, for monitoring)

### Setup

1. **Clone or download the project files**

2. **Install dependencies**
```bash
pip install -r requirements.txt --break-system-packages
```

3. **Configure API keys**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API keys
nano .env
```

Required keys:
- `GOOGLE_API_KEY`: Get from https://makersuite.google.com/app/apikey
- `LANGCHAIN_API_KEY`: Get from https://smith.langchain.com/ (optional)

4. **Test the agent**
```bash
python real_estate_agent.py
```

## 🚀 Usage

### Method 1: Direct Python Usage

```python
from real_estate_agent import RealEstateAgent

# Initialize agent
agent = RealEstateAgent()

# Process a message
result = agent.process_message(
    message="بغيت نشري شقة في الدار البيضاء",
    thread_id="customer_123"
)

print(result['response'])
# Output: "مزيان! واش عندك فكرة على المنطقة..."
```

### Method 2: Flask API Server

Start the API server:
```bash
python api_server.py
```

Send a message via REST API:
```bash
curl -X POST http://localhost:5000/api/message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "سلام، بغيت نشري دار",
    "customer_id": "customer_123",
    "platform": "website"
  }'
```

### Method 3: Web Interface

Open `chat_interface.html` in your browser for a beautiful interactive chat interface.

## 🔌 API Endpoints

### POST `/api/message`
Process a customer message and get AI response

**Request:**
```json
{
  "message": "بغيت نكري شقة",
  "customer_id": "unique_id",
  "platform": "whatsapp"
}
```

**Response:**
```json
{
  "success": true,
  "response": "مرحبا! واش كتقلب على شقة ولا فيلا؟...",
  "metadata": {
    "intent": "rent",
    "sentiment": "positive",
    "conversation_stage": "qualifying",
    "properties_count": 2,
    "follow_up_needed": false
  },
  "properties": [...],
  "timestamp": "2024-01-15T10:30:00"
}
```

### GET `/api/conversation/{customer_id}`
Retrieve conversation history

### POST `/api/webhook/whatsapp`
WhatsApp Business API webhook

### POST `/api/webhook/facebook`
Facebook Messenger webhook

### GET `/api/analytics`
Get conversation analytics and statistics

### POST `/api/broadcast`
Send broadcast messages to customers

## 🎯 Intent Detection

The agent automatically detects customer intent:

| Intent | Example Phrases (Darija) |
|--------|-------------------------|
| **Buy** | "بغيت نشري دار", "كنقلب على شقة للشراء" |
| **Rent** | "بغيت نكري شقة", "كنقلب على دار للكراء" |
| **Sell** | "بغيت نبيع عقار", "عندي دار بغيت نبيعها" |
| **Inquiry** | "شحال التمن؟", "فين كاينة؟" |

## 📊 Conversation Stages

The agent manages conversations through these stages:

1. **Greeting**: Welcome and initial engagement
2. **Qualifying**: Understanding customer needs
3. **Presenting**: Showing matching properties
4. **Negotiating**: Discussing details and pricing
5. **Closing**: Scheduling visits or finalizing

## 🔍 LangSmith Monitoring

View real-time traces and debugging:

1. Set your `LANGCHAIN_API_KEY` in `.env`
2. Run the agent
3. Visit https://smith.langchain.com/
4. View traces under project "real-estate-agent-darija"

Benefits:
- Debug conversation flows
- Monitor token usage
- Analyze response quality
- Track error rates
- Optimize prompts

## 🌐 Integration Examples

### WhatsApp Business API (Twilio)

```python
from twilio.rest import Client

def send_whatsapp_response(to_number, message):
    client = Client(account_sid, auth_token)
    
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=message,
        to=f'whatsapp:{to_number}'
    )
```

### Facebook Messenger

```python
import requests

def send_facebook_message(recipient_id, message):
    url = f"https://graph.facebook.com/v18.0/me/messages"
    
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message}
    }
    
    headers = {"Authorization": f"Bearer {page_access_token}"}
    requests.post(url, json=payload, headers=headers)
```

## 🎨 Customization

### Add Custom Property Sources

Modify `fetch_property_recommendations()` in `real_estate_agent.py`:

```python
def fetch_property_recommendations(state: AgentState) -> AgentState:
    # Connect to your database
    properties = db.query("SELECT * FROM properties WHERE ...")
    
    state["recommended_properties"] = properties
    return state
```

### Modify Response Style

Update the system prompts in `generate_response()`:

```python
stage_prompts = {
    "greeting": """Your custom greeting prompt in Darija...""",
    "qualifying": """Your custom qualifying prompt...""",
    # ... etc
}
```

### Add New Conversation Stages

Extend the state machine in `create_agent_graph()`:

```python
workflow.add_node("send_contract", send_contract_node)
workflow.add_edge("negotiating", "send_contract")
```

## 📈 Performance Tips

1. **Use Vector Database**: For large property catalogs, use Pinecone or Weaviate
2. **Cache Responses**: Implement Redis for frequently asked questions
3. **Async Processing**: Use Celery for background tasks
4. **Rate Limiting**: Protect API endpoints with rate limits
5. **Load Balancing**: Deploy multiple instances behind a load balancer

## 🧪 Testing

Run the demo conversation:
```bash
python real_estate_agent.py
```

Test specific scenarios:
```python
# Test intent detection
result = agent.process_message("بغيت نشري فيلا ب 3 مليون")
assert result['intent'] == 'buy'

# Test sentiment analysis
result = agent.process_message("مستعجل بزاف!")
assert result['sentiment'] == 'urgent'
```

## 🔐 Security Best Practices

- Never commit `.env` file to version control
- Use environment variables for all sensitive data
- Implement rate limiting on API endpoints
- Validate and sanitize all user inputs
- Use HTTPS in production
- Implement authentication for admin endpoints

## 📱 Deployment

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "api_server.py"]
```

Build and run:
```bash
docker build -t real-estate-agent .
docker run -p 5000:5000 --env-file .env real-estate-agent
```

### Cloud Deployment (Render, Railway, Heroku)

1. Create `Procfile`:
```
web: python api_server.py
```

2. Set environment variables in platform dashboard
3. Deploy from GitHub repository

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- [ ] Add more Moroccan cities to property database
- [ ] Implement image recognition for property photos
- [ ] Add voice message support
- [ ] Multi-language support (French, English)
- [ ] CRM integration (HubSpot, Salesforce)
- [ ] Calendar integration for property visits
- [ ] PDF brochure generation
- [ ] Email notifications

## 📄 License

MIT License - feel free to use for commercial projects

## 🙏 Acknowledgments

- **Google Gemini**: Advanced language understanding
- **LangChain**: Powerful LLM framework
- **LangGraph**: State machine orchestration
- **LangSmith**: Debugging and monitoring
- **Anthropic**: For the opportunity to build this

## 📞 Support

For questions or issues:
- Create an issue on GitHub
- Email: support@youragency.com
- WhatsApp: +212 XXX-XXXXXX

---

**Built with ❤️ for the Moroccan real estate market**

🇲🇦 Made in Morocco | مصنوع في المغرب
