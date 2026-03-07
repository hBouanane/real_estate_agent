"""
Advanced Real Estate Agent Examples
Demonstrates custom extensions and integrations
"""

import os
from real_estate_agent import RealEstateAgent, AgentState
from langchain_core.messages import HumanMessage
from datetime import datetime, timedelta


# ==================== EXAMPLE 1: CUSTOM PROPERTY DATABASE ====================

class PropertyDatabase:
    """
    Example of integrating with a real property database
    Replace with your actual database (PostgreSQL, MongoDB, etc.)
    """
    
    def __init__(self):
        # In production, connect to real database
        self.connection = None
    
    def search_properties(self, filters: dict) -> list:
        """
        Search properties with advanced filters
        
        Args:
            filters: {
                'location': str,
                'min_price': float,
                'max_price': float,
                'bedrooms': int,
                'property_type': str,
                'amenities': list
            }
        """
        # Example SQL query (adjust for your database)
        # query = """
        #     SELECT * FROM properties
        #     WHERE location LIKE %s
        #     AND price BETWEEN %s AND %s
        #     AND bedrooms >= %s
        # """
        
        # Simulated results
        return [
            {
                "id": 1,
                "type": "شقة",
                "location": filters.get('location', 'الدار البيضاء'),
                "price": "1,200,000 درهم",
                "bedrooms": filters.get('bedrooms', 3),
                "area": "120 متر مربع",
                "amenities": ["مصعد", "موقف سيارات", "حمام سباحة"],
                "images": ["url1.jpg", "url2.jpg"],
                "agent_contact": "+212 6XX-XXXXXX"
            }
        ]
    
    def get_property_details(self, property_id: int) -> dict:
        """Get detailed information about a specific property"""
        # In production, query database
        return {
            "id": property_id,
            "full_description": "شقة فاخرة في موقع استراتيجي...",
            "virtual_tour_url": "https://tour.example.com/property/1",
            "documents": ["plan.pdf", "title_deed.pdf"]
        }


# ==================== EXAMPLE 2: CRM INTEGRATION ====================

class CRMIntegration:
    """
    Example CRM integration for customer relationship management
    Works with HubSpot, Salesforce, or custom CRM
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def create_lead(self, customer_data: dict) -> str:
        """
        Create a new lead in CRM
        
        Args:
            customer_data: {
                'name': str,
                'phone': str,
                'email': str,
                'intent': str,
                'budget': str,
                'preferences': dict
            }
            
        Returns:
            lead_id: Unique identifier for the lead
        """
        # Example: HubSpot API call
        # requests.post(
        #     'https://api.hubapi.com/contacts/v1/contact',
        #     json=customer_data,
        #     headers={'Authorization': f'Bearer {self.api_key}'}
        # )
        
        print(f"📝 Created CRM lead for {customer_data.get('name', 'Unknown')}")
        return "LEAD_12345"
    
    def log_interaction(self, lead_id: str, interaction: dict):
        """Log customer interaction in CRM"""
        print(f"📊 Logged interaction for lead {lead_id}")
    
    def schedule_follow_up(self, lead_id: str, follow_up_date: datetime):
        """Schedule automated follow-up"""
        print(f"🗓️ Scheduled follow-up for {follow_up_date.strftime('%Y-%m-%d')}")


# ==================== EXAMPLE 3: SCHEDULING INTEGRATION ====================

class CalendarIntegration:
    """
    Example calendar integration for property viewings
    Works with Google Calendar, Outlook, or custom system
    """
    
    def __init__(self):
        # In production, authenticate with calendar service
        pass
    
    def check_availability(self, date: datetime, duration_minutes: int = 60) -> list:
        """
        Check available time slots for property viewing
        
        Returns:
            List of available time slots
        """
        # In production, query actual calendar
        available_slots = [
            "10:00 AM",
            "2:00 PM",
            "4:00 PM"
        ]
        return available_slots
    
    def schedule_viewing(
        self, 
        property_id: int, 
        customer_name: str,
        customer_phone: str,
        date_time: datetime
    ) -> str:
        """
        Schedule a property viewing
        
        Returns:
            confirmation_id: Booking confirmation number
        """
        # In production, create calendar event and send notifications
        confirmation_id = f"VIEW_{property_id}_{date_time.strftime('%Y%m%d%H%M')}"
        
        print(f"✅ Scheduled viewing for {customer_name}")
        print(f"   Property: {property_id}")
        print(f"   Date: {date_time.strftime('%Y-%m-%d %H:%M')}")
        print(f"   Confirmation: {confirmation_id}")
        
        # Send SMS/Email confirmation
        self.send_confirmation(customer_phone, confirmation_id)
        
        return confirmation_id
    
    def send_confirmation(self, phone: str, confirmation_id: str):
        """Send SMS/Email confirmation"""
        message = f"""
        تأكيد الموعد
        
        رقم التأكيد: {confirmation_id}
        سنتصل بك قبل الموعد بـ 24 ساعة
        
        شكرا لثقتك
        """
        print(f"📱 Sent confirmation to {phone}")


# ==================== EXAMPLE 4: NOTIFICATION SYSTEM ====================

class NotificationService:
    """
    Multi-channel notification system
    Supports SMS, Email, WhatsApp, and Push notifications
    """
    
    def send_sms(self, phone: str, message: str):
        """Send SMS via Twilio or similar service"""
        # from twilio.rest import Client
        # client = Client(account_sid, auth_token)
        # client.messages.create(to=phone, from_=from_number, body=message)
        
        print(f"📱 SMS to {phone}: {message[:50]}...")
    
    def send_email(self, email: str, subject: str, body: str):
        """Send email via SendGrid or similar service"""
        # import sendgrid
        # sg = sendgrid.SendGridAPIClient(api_key)
        # sg.send(message)
        
        print(f"📧 Email to {email}: {subject}")
    
    def send_whatsapp(self, phone: str, message: str, media_url: str = None):
        """Send WhatsApp message via Twilio or Meta API"""
        print(f"💬 WhatsApp to {phone}: {message[:50]}...")
    
    def send_property_brochure(self, email: str, property_id: int):
        """Generate and send property PDF brochure"""
        # Use reportlab or weasyprint to generate PDF
        print(f"📄 Sent property brochure for property {property_id} to {email}")


# ==================== EXAMPLE 5: ENHANCED AGENT WITH INTEGRATIONS ====================

class EnhancedRealEstateAgent(RealEstateAgent):
    """
    Extended agent with CRM, scheduling, and notifications
    """
    
    def __init__(self):
        super().__init__()
        
        # Initialize integrations
        self.property_db = PropertyDatabase()
        self.crm = CRMIntegration(api_key=os.getenv('CRM_API_KEY', 'demo'))
        self.calendar = CalendarIntegration()
        self.notifications = NotificationService()
        
        print("✓ Enhanced Real Estate Agent initialized with integrations")
    
    def process_message_with_actions(
        self, 
        message: str, 
        customer_id: str,
        customer_phone: str = None,
        customer_email: str = None
    ) -> dict:
        """
        Process message and trigger appropriate actions
        """
        # Get base response from parent agent
        result = super().process_message(message, thread_id=customer_id)
        
        # Trigger actions based on intent and stage
        intent = result['intent']
        stage = result['stage']
        sentiment = result['sentiment']
        
        # Create CRM lead on first contact
        if stage == 'greeting':
            lead_id = self.crm.create_lead({
                'customer_id': customer_id,
                'phone': customer_phone,
                'email': customer_email,
                'intent': intent,
                'first_contact': datetime.now().isoformat()
            })
            result['lead_id'] = lead_id
        
        # Send property brochures when presenting
        if stage == 'presenting' and customer_email:
            for prop in result['properties']:
                self.notifications.send_property_brochure(
                    customer_email, 
                    prop['id']
                )
        
        # Schedule follow-up for urgent customers
        if sentiment == 'urgent' or result['follow_up_needed']:
            follow_up_date = datetime.now() + timedelta(hours=2)
            self.crm.schedule_follow_up(customer_id, follow_up_date)
            
            # Send immediate notification to sales team
            self.notifications.send_sms(
                '+212 6XX-XXXXXX',  # Sales team number
                f"Urgent lead: {customer_id} - Intent: {intent}"
            )
        
        # Offer scheduling in negotiating stage
        if stage == 'negotiating':
            available_slots = self.calendar.check_availability(
                datetime.now() + timedelta(days=1)
            )
            result['available_viewing_slots'] = available_slots
        
        return result
    
    def schedule_property_viewing(
        self,
        customer_id: str,
        property_id: int,
        preferred_datetime: datetime,
        customer_name: str,
        customer_phone: str
    ) -> dict:
        """
        Handle property viewing scheduling
        """
        # Check availability
        available = self.calendar.check_availability(
            preferred_datetime,
            duration_minutes=60
        )
        
        if not available:
            return {
                'success': False,
                'message': 'الوقت المختار غير متاح. اختار وقت آخر من فضلك.',
                'available_slots': available
            }
        
        # Schedule the viewing
        confirmation_id = self.calendar.schedule_viewing(
            property_id=property_id,
            customer_name=customer_name,
            customer_phone=customer_phone,
            date_time=preferred_datetime
        )
        
        # Send confirmations
        self.notifications.send_whatsapp(
            customer_phone,
            f"تأكيد موعد الزيارة\nالعقار: {property_id}\nالموعد: {preferred_datetime.strftime('%Y-%m-%d %H:%M')}\nرقم التأكيد: {confirmation_id}"
        )
        
        # Log in CRM
        self.crm.log_interaction(customer_id, {
            'type': 'viewing_scheduled',
            'property_id': property_id,
            'datetime': preferred_datetime.isoformat(),
            'confirmation_id': confirmation_id
        })
        
        return {
            'success': True,
            'confirmation_id': confirmation_id,
            'message': f'تم تأكيد الموعد! رقم التأكيد: {confirmation_id}'
        }


# ==================== EXAMPLE 6: ANALYTICS AND REPORTING ====================

class AgentAnalytics:
    """
    Advanced analytics for agent performance
    """
    
    def __init__(self):
        self.metrics = {
            'total_conversations': 0,
            'conversion_rate': 0.0,
            'average_response_time': 0.0,
            'customer_satisfaction': 0.0
        }
    
    def track_conversation(self, conversation_data: dict):
        """Track conversation metrics"""
        self.metrics['total_conversations'] += 1
        # Calculate conversion rate, response time, etc.
    
    def generate_daily_report(self) -> dict:
        """Generate daily performance report"""
        return {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'metrics': self.metrics,
            'top_intents': ['buy', 'rent'],
            'busiest_hours': ['10:00-12:00', '14:00-16:00'],
            'recommendations': [
                'زيادة التركيز على شقق الكراء في فترة المساء',
                'تحسين وقت الرد في ساعات الذروة'
            ]
        }


# ==================== DEMO OF ENHANCED FEATURES ====================

def demo_enhanced_features():
    """
    Demonstrate all advanced features
    """
    print("=" * 70)
    print("🚀 ENHANCED REAL ESTATE AGENT - ADVANCED FEATURES DEMO")
    print("=" * 70)
    print()
    
    # Initialize enhanced agent
    agent = EnhancedRealEstateAgent()
    
    # Example 1: Process message with full integration
    print("📱 Example 1: Customer Inquiry with CRM Integration")
    print("-" * 70)
    
    result = agent.process_message_with_actions(
        message="بغيت نشري فيلا في الرباط بميزانية 3 مليون",
        customer_id="CUST_001",
        customer_phone="+212 6XX-XXXXXX",
        customer_email="customer@example.com"
    )
    
    print(f"Response: {result['response']}")
    print(f"Lead ID: {result.get('lead_id', 'N/A')}")
    print()
    
    # Example 2: Schedule property viewing
    print("📅 Example 2: Schedule Property Viewing")
    print("-" * 70)
    
    viewing_result = agent.schedule_property_viewing(
        customer_id="CUST_001",
        property_id=101,
        preferred_datetime=datetime.now() + timedelta(days=2, hours=14),
        customer_name="محمد الأمين",
        customer_phone="+212 6XX-XXXXXX"
    )
    
    print(f"Scheduling: {viewing_result['message']}")
    print()
    
    # Example 3: Analytics
    print("📊 Example 3: Agent Analytics")
    print("-" * 70)
    
    analytics = AgentAnalytics()
    report = analytics.generate_daily_report()
    
    print(f"Date: {report['date']}")
    print(f"Total Conversations: {report['metrics']['total_conversations']}")
    print(f"Recommendations: {report['recommendations'][0]}")
    print()
    
    print("=" * 70)
    print("✅ Demo completed successfully!")


if __name__ == "__main__":
    # Set environment variables first:
    # export GOOGLE_API_KEY="your-key"
    # export CRM_API_KEY="your-crm-key"
    
    demo_enhanced_features()
