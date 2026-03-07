# 🚀 Quick Start Guide

Get your Real Estate Agent running in 5 minutes!

## Step 1: Get Your API Keys (2 minutes)

### Google Gemini API Key (Required)
1. Go to https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy your API key

### LangSmith API Key (Optional - for monitoring)
1. Go to https://smith.langchain.com/
2. Sign up for free
3. Go to Settings → API Keys
4. Create new API key

## Step 2: Install Dependencies (1 minute)

```bash
# Install Python packages
pip install -r requirements.txt --break-system-packages

# Or install individually
pip install langchain langgraph langsmith langchain-google-genai flask flask-cors --break-system-packages
```

## Step 3: Configure Environment (30 seconds)

Create a `.env` file:

```bash
# Copy example file
cp .env.example .env

# Edit with your favorite editor
nano .env
```

Add your keys:
```env
GOOGLE_API_KEY=your_actual_google_api_key_here
LANGCHAIN_API_KEY=your_langsmith_key_here  # Optional
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=real-estate-agent-darija
```

## Step 4: Test the Agent (30 seconds)

```bash
python real_estate_agent.py
```

You should see:
```
✓ LangSmith configured successfully
✓ Gemini model configured
✓ Real Estate Agent initialized

📱 Demo Conversation:
👤 Customer: سلام، بغيت نشري شقة في الدار البيضاء
🤖 Agent: مرحبا بيك! واخا، بغيت نعاونك...
```

## Step 5: Try the Web Interface (1 minute)

Open `chat_interface.html` in your browser:

```bash
# On macOS
open chat_interface.html

# On Linux
xdg-open chat_interface.html

# On Windows
start chat_interface.html
```

## Alternative: Run API Server

```bash
python api_server.py
```

Then test with curl:
```bash
curl -X POST http://localhost:5000/api/message \
  -H "Content-Type: application/json" \
  -d '{"message": "سلام، بغيت نشري دار", "customer_id": "test_123"}'
```

## Next Steps

### Customize the Agent
- Edit `real_estate_agent.py` to modify responses
- Update property database in `fetch_property_recommendations()`
- Adjust Darija dialect in system prompts

### Add Integrations
- See `advanced_examples.py` for CRM integration
- Add WhatsApp webhook in `api_server.py`
- Connect to your property database

### Deploy to Production
- Use Docker (see README.md)
- Deploy to Render, Railway, or Heroku
- Set up domain and SSL certificate

## Common Issues

### Issue: "No module named 'langchain'"
**Solution:**
```bash
pip install -r requirements.txt --break-system-packages
```

### Issue: "GOOGLE_API_KEY not found"
**Solution:**
Make sure `.env` file exists and contains your API key:
```bash
cat .env  # Should show your keys
```

### Issue: "Rate limit exceeded"
**Solution:**
- Check your Gemini API quota at https://makersuite.google.com/
- Wait a few minutes and try again
- Upgrade to paid tier if needed

### Issue: Network error when using web_search
**Solution:**
- The basic version doesn't use web search
- If you added web search, ensure network is enabled
- Check your internet connection

## Tips for Best Results

1. **Be Specific in Darija**
   - ✅ "بغيت شقة ف الدار البيضاء ب 3 بيوت و ميزانية مليون و نص"
   - ❌ "بغيت شي حاجة"

2. **Use Natural Language**
   - The agent understands Moroccan dialect variations
   - Mix of Arabic and French terms is fine

3. **Test Different Scenarios**
   - Buying: "بغيت نشري"
   - Renting: "بغيت نكري"
   - Selling: "بغيت نبيع"
   - Questions: "شحال؟", "فين؟"

## Resources

- 📖 Full documentation: `README.md`
- 🔧 Advanced features: `advanced_examples.py`
- 🌐 API reference: See `api_server.py`
- 💬 Web interface: `chat_interface.html`

## Support

Need help? Check:
- README.md for detailed docs
- GitHub issues for common problems
- LangSmith traces for debugging

---

**You're all set! 🎉**

Start chatting with your AI real estate agent in Moroccan Darija!
