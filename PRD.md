# Product Requirements Document: AI WhatsApp Assistant for Superyacht Services Guide (SSG)

**Version:** 1.0
**Date:** October 1, 2025
**Author:** Eric Tech
**Client:** Superyacht Publications Limited
**Development Partner:** Serenity Digital (API Development)

---

## 1. Project Overview & Goal

### 1.1. The Problem
Yacht captains and crew are highly mobile and need immediate access to reliable service information. The current website search, while functional, requires users to navigate to the site and use structured filters, which can be inefficient for users on the go.

### 1.2. The Solution
We will build an AI-powered assistant that lives on WhatsApp, a platform already used extensively by the target audience. This chatbot will allow users to find services in the SSG directory by simply asking questions in natural, conversational language.

### 1.3. Business Goal
The primary goal is to significantly increase user engagement by providing a valuable, convenient tool for yacht crew. This will solidify SSG's position as the most useful resource in the industry, drive qualified traffic to the website, and provide a new channel for promoting premium listings.

---

## 2. Target Audience

**Primary User:** Yacht Captains and Crew Members

**Key Needs:**
- Fast, hands-free access to information while on board or in port
- Reliable, curated results from a trusted source (SSG)
- An intuitive interface that doesn't require learning a new app
- Ability to search using photos or voice messages

---

## 3. Core Features & User Stories

### 3.1. Natural Language Search
**User Story:** As a captain, I want to ask "Find me rigging services in Antigua" so that I can get a list of relevant companies without using filters.

**Implementation:**
- Bot extracts intent (category: "rigging", location: "Antigua")
- Queries SSG API with extracted parameters
- Returns 3-4 relevant results formatted for WhatsApp

### 3.2. Multimedia Support
**User Story:** As a crew member, I want to send a photo of a broken engine part or a voice note asking for help so that I can get recommendations even if I don't know the exact terminology.

**Supported Formats:**
- **Images:** Bot analyzes image and generates text description of what's shown
- **Voice Messages:** Bot transcribes audio to text and processes the query
- **Text:** Standard conversational text queries

**NOT Supported:**
- **Video:** Explicitly excluded due to high token consumption

**Technical Note:** All multimedia is converted to text before being stored in conversation memory.

### 3.3. Conversation Memory
**User Story:** As a user, I want the bot to remember my previous questions and my role/vessel size so that I don't have to repeat myself and the conversation feels personal.

**Memory Storage:**
- User identification: Phone number
- Stored data: User role, vessel size, conversation history
- Database: Supabase (text-based storage)
- Retrieval: Bot queries memory before each response to maintain context

**Initial Questions Bot Asks:**
1. User's position/role on the yacht
2. Vessel size/length
3. Current or typical operating location

### 3.4. Prioritized Results
**User Story:** As a business, we want the chatbot to always recommend premium advertisers first for relevant queries so that it aligns with our existing business model.

**Result Presentation Logic:**
- **Premium Advertisers (Top 2 Tiers):**
  - Company name
  - One-sentence description
  - Website link to SSG listing page

- **Free Listings:**
  - Company name
  - Website link to SSG listing page
  - NO description (tier differentiation)

**Presentation Format:**
- Return 3-4 results per query
- Always prioritize top 2 advertising tiers first
- Results sent as formatted WhatsApp message with clickable links

---

## 4. Technical Architecture

### 4.1. Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Workflow Automation | n8n | Orchestrates entire chatbot logic and integrations |
| AI Models | OpenRouter | Cost-effective AI model access (DeepSeek, Claude, etc.) |
| Database | Supabase | User memory, conversation history, analytics storage |
| WhatsApp Integration | WhatsApp Business API | Production messaging channel |
| API Authentication | Bearer Token | Secure SSG API access |

**Key Decision:** OpenRouter chosen over OpenAI for:
- Cheaper pricing for image/audio processing
- Access to multiple AI models
- Better cost control during testing phase

**Key Decision:** Supabase chosen over Airtable for:
- Lower cost for database storage
- Better suited for production-scale data
- More flexible querying capabilities

### 4.2. Memory System Architecture

**Storage Method:**
- Text-only storage in Supabase
- Indexed by user phone number
- Conversation history maintains context across sessions

**Data Flow:**
1. User sends message → Bot retrieves user memory by phone number
2. Bot processes query with context awareness
3. Bot generates response
4. Bot saves new conversation data to memory

**Privacy:** User-specific isolation ensures conversations remain private.

---

## 5. SSG API Integration Specifications

### 5.1. API Endpoints Required

**Developed by:** Serenity Digital (James Gunn)

**Development Status:** API endpoints need to be built - not currently available.

**Development Workaround:** During initial chatbot development, sample data will be provided as CSV file for testing and workflow development. Once API is complete, workflow will be updated to use live API endpoints.

#### Authentication
- **Method:** Bearer Token in request header
- **Header:** `Authorization: Bearer {API_KEY}`

#### Endpoint 1: Category Lookup
```
GET /api/categories
Response: {"10": "Rigging", "11": "Marinas", "56": "Marina", ...}
```

#### Endpoint 2: Location Lookup
```
GET /api/locations
Response: {"63": "Spain", "45": "Antigua", ...}
```

#### Endpoint 3: Search
```
GET /api/search?category_id={id}&location_id={id}&search_term={text}

Parameters:
- category_id: Category ID from lookup endpoint
- location_id: Location ID from lookup endpoint
- search_term: Free text search (optional, for brand names or specific terms)

Response Format:
[
  {
    "company_name": "Example Marina",
    "description": "Full-service marina in the town center",
    "website_link": "https://superyachtservicesguide.com/listing/123",
    "advertising_tier": "Premium" | "Standard" | "Free"
  },
  ...
]
```

**Search Algorithm:** Utilizes same ranking logic as SSG website search.

**Update Frequency:** Website updated weekly with new companies. API must return live data, not cached results.

#### Sample Data for Development
**Format:** CSV file
**Contents:** Representative sample of categories, locations, and company listings with all required fields
**Purpose:** Enable workflow development and testing before API completion

### 5.2. Future Endpoint (Phase 2 - Subscription Model)

#### Endpoint 4: User Status Check
```
GET /api/user/status?phone={phone_number}

Response Format:
{
  "status": "free" | "premium",
  "daily_queries_left": 3,
  "account_exists": true
}
```

**Purpose:** Enable usage limits and subscription tier enforcement.

---

## 6. Analytics & Tracking

### 6.1. Data Collection
**Stored in Supabase:**
- Total queries per user (indexed by phone number)
- Query types and patterns
- Popular services/locations
- Conversation flow analysis
- Response quality indicators
- User profile data (role, vessel size, location)
- Timestamp data for all interactions

**Data Structure:**
- Stored in relational tables (similar to Excel: rows and columns)
- Multiple tables for different data types
- Phone number as primary unique identifier across all tables

### 6.2. Click Tracking
**Strategy:** Bot sends SSG website links (not direct phone/email contact info)

**Benefits:**
- Website analytics can track WhatsApp referral traffic
- Attribution of leads generated by chatbot
- Measurement of click-through rates

**Implementation:** Google Analytics (or similar) tracks incoming traffic from WhatsApp source.

### 6.3. Admin Dashboard (Future Enhancement)
**Purpose:** Provide user-friendly interface for managing chatbot data and subscriptions

**Potential Features:**
- Visual dashboard showing conversation analytics
- User management (view users, subscription status, usage patterns)
- Conversation history viewer
- Subscription management interface
- Revenue tracking for paid tiers
- Popular query analysis
- User engagement metrics

**Technical Options:**
- Build custom admin interface on top of Supabase data
- Import Supabase data into existing SSG CMS
- Use third-party analytics/admin tools

**Decision Point:** Whether to integrate with existing SSG website CMS or maintain separate admin system for chatbot. This decision impacts:
- Data architecture
- User account management
- Subscription billing integration
- Development complexity

**Priority:** Phase 2+ (after successful testing and initial rollout)

---

## 7. User Subscription Model (Phased Approach)

### Phase 1: Testing Period (Current)
- **Access:** Unlimited queries for all users
- **Features:** Full access to all capabilities (text, image, voice)
- **Purpose:** Thorough testing, data collection, user feedback
- **Duration:** TBD based on testing results
- **No restrictions** during this phase

### Phase 2: Free Tier Implementation
- **Access Options (to be decided based on Phase 1 data):**
  - Option A: Daily usage limit (similar to ChatGPT free tier)
  - Option B: Specific number of questions per day
  - Option C: Combination of query limit + feature restrictions
- **Feature Restrictions:**
  - Text queries: Limited by daily quota
  - Image uploads: May be restricted to paid tier only
  - Voice messages: May be restricted to paid tier only
- **User Identification:** Phone number-based accounts (prevents account sharing)
- **Verification:** User-status API endpoint checks subscription level
- **Account Creation:** Bot prompts users to create account with phone number
- **Privacy:** Users consent to data collection when they engage with the bot

### Phase 3: Paid Tier Launch
- **Access:** Unlimited queries
- **Premium Features:**
  - Unlimited text queries
  - Photo upload capability (identify parts, brands, damage)
  - Voice message support
  - Priority response times
- **Pricing:** TBD
- **Payment:** Stripe integration (separate from website subscriptions)
- **Database:** Subscription data stored in dedicated system (TBD: CMS vs. separate database)

### Example Use Case: Premium Photo Feature
**Scenario:** User on yacht takes photo of broken Miele dishwasher filter
**Bot Actions:**
1. Analyzes image to identify brand (Miele) and part type (dishwasher filter)
2. Extracts context from conversation (user's location)
3. Searches SSG database for "Miele technicians" or "appliance repair" near user's location
4. Returns 3-4 local technicians who service Miele appliances

**Business Value:** This premium feature justifies paid subscription by solving urgent, high-value problems for yacht crew.

**Critical Implementation Note:** Bot must check user status before processing queries once subscription model is active. Phone number serves as unique identifier to prevent account sharing abuse.

---

## 8. Error Handling & Edge Cases

### 8.1. Unsupported Content
- **Video Messages:** Bot responds: "Sorry, I can't process video messages. Please send a photo or voice note instead."

### 8.2. API Failures
- **API Unavailable:** "I'm having trouble connecting to our directory right now. Please try again in a few minutes."
- **No Results Found:** "I couldn't find any services matching your request. Try broadening your search or asking in a different way."

### 8.3. Rate Limiting
- **Spam Protection:** TBD - Even during testing phase, consider implementing basic rate limits to prevent abuse

---

## 9. Success Metrics

### 9.1. Adoption Metrics
- Number of unique users interacting with chatbot monthly
- Growth rate of active users
- User retention rate

### 9.2. Engagement Metrics
- Total successful queries handled
- Average queries per user
- Conversation completion rate

### 9.3. Quality Metrics
- User feedback and testimonials
- Response accuracy rate
- Time to resolution

### 9.4. Business Metrics (Future)
- Click-through rate on website links
- Conversion rate (clicks → contact)
- Premium listing exposure via chatbot

---

## 10. Future Enhancements (Phase 2+)

### 10.1. Intelligent Website Search
Replace current website search filters with a single, intelligent search bar powered by the same AI technology used in the chatbot.

### 10.2. Expanded Communication Channels
- Facebook Messenger integration
- Website chat widget using same AI backend

### 10.3. Advanced Features
- Proactive recommendations based on user location
- Integration with yacht management systems
- Multilingual support for international crews

---

## 11. Project Dependencies & Assumptions

### 11.1. Dependencies
- **Critical:** Timely delivery of API endpoints by Serenity Digital
- **Required:** WhatsApp Business API account and production phone number
- **Assumed:** Users will grant permissions for multimedia content sharing

### 11.2. Assumptions
- WhatsApp is the primary communication platform for target audience
- Users are comfortable interacting with AI chatbots
- Internet connectivity available for users (standard for yacht crew)
- SSG directory data quality is maintained by existing editorial processes

---

## 12. Team Responsibilities

### 12.1. Eric Tech (AI Chatbot Developer)
- n8n workflow development
- AI model integration via OpenRouter
- Supabase database setup and management
- WhatsApp Business API integration
- Memory system implementation
- Testing and quality assurance

### 12.2. James Gunn / Serenity Digital (API Development)
- Build and deploy 3 core API endpoints (categories, locations, search)
- Implement Bearer Token authentication
- Ensure API returns live data (weekly updates reflected immediately)
- Future: User status endpoint for subscription model

### 12.3. Tristan Blatter / SSG (Client)
- Requirements definition and validation
- Business logic decisions
- User testing coordination
- Premium advertiser prioritization rules
- Subscription pricing and model decisions

---

## 12.4. Development Kickoff Requirements

**Items Required from Client to Begin Development:**

### Immediate Requirements (Phase 1 Start)
1. **n8n Account Access**
   - Client to sign up for n8n developer program
   - Provide developer access to Eric Tech
   - **Status:** In progress (signup scheduled)

2. **OpenRouter Account**
   - Client account created
   - Minimum $3-5 credit balance loaded for testing
   - API credentials shared with Eric Tech
   - **Status:** Account created, needs credit top-up

3. **Sample Data (CSV Format)**
   - Representative sample of categories (with IDs and names)
   - Representative sample of locations (with IDs and names)
   - Sample company listings with all required fields:
     - Company name
     - Description
     - Website link
     - Advertising tier
   - **Purpose:** Enable workflow development while API is being built
   - **Status:** To be provided by client

4. **WhatsApp Testing Setup**
   - **Option A:** Use existing WhatsApp test number (already created by client)
   - **Option B:** Use personal WhatsApp numbers for initial development
   - **Decision:** Start with personal numbers, integrate client test number when workflow is ready
   - **Production Number:** To be acquired after successful testing

### Future Requirements (Before Production)
5. **API Endpoints**
   - Developed by Serenity Digital
   - To replace CSV sample data once complete
   - Required before production launch

6. **Privacy Policy**
   - Data collection consent mechanism
   - Required before external user testing

7. **Production WhatsApp Number**
   - Virtual number from approved provider
   - Required for public launch

---

## 13. Testing Strategy

### Phase 1: Internal Testing
- Unlimited access for development team
- Functionality validation (text, image, voice)
- Memory system accuracy testing
- API integration verification

### Phase 2: Beta Testing
- Select group of yacht crews
- Real-world usage scenarios
- Feedback collection
- Performance monitoring

### Phase 3: Data Analysis
- Query pattern identification
- Popular service/location trends
- Response quality assessment
- Usage threshold determination for free tier

### Phase 4: Production Launch
- Implement usage limits based on Phase 3 insights
- Monitor system performance
- Iterate based on user feedback

---

## 14. Open Questions & Decisions Needed

### 14.1. Subscription Model Questions
1. **Free Tier Limit:** What is the appropriate daily query limit for free users?
   - Option A: Daily usage limit (like ChatGPT)
   - Option B: Specific number of questions per day
   - Option C: Combination of query limit + feature restrictions
   - **Decision Timeline:** After Phase 1 testing data analysis

2. **Feature Restrictions:** Should free tier have access to multimedia features?
   - Should image uploads be premium-only?
   - Should voice messages be premium-only?
   - Or should free tier have limited multimedia usage?
   - **Decision Timeline:** After Phase 1 testing data analysis

3. **Subscription Pricing:** What should the premium tier cost?
   - **Dependent on:** Value validation during testing, competitive analysis
   - **Decision Timeline:** After successful Phase 1 completion

### 14.2. Technical Architecture Questions
4. **CMS Integration:** Should chatbot subscriptions be integrated with website CMS or remain separate?
   - **Option A:** Integrate with existing SSG website CMS (unified user accounts)
   - **Option B:** Separate system for chatbot (independent management)
   - **Impacts:** Data architecture, user account management, billing integration, development complexity
   - **Decision Timeline:** Before Phase 2 subscription launch

5. **Admin Dashboard:** What tool/approach should be used for admin interface?
   - **Option A:** Custom-built dashboard on Supabase
   - **Option B:** Import data into existing CMS
   - **Option C:** Third-party analytics/admin platform
   - **Decision Timeline:** Phase 2 planning

6. **Privacy Policy:** What level of data collection consent is needed?
   - Need clear privacy policy for users engaging with bot
   - What data can be collected and for what purposes?
   - How long to retain conversation data?
   - **Decision Timeline:** Before Phase 1 testing with external users

### 14.3. Operational Questions
7. **Rate Limiting:** What spam protection measures should be implemented?
   - Even during testing phase, need basic abuse prevention
   - **Decision Timeline:** Before Phase 1 external testing

8. **WhatsApp Production Number:** What virtual number provider to use?
   - Cost considerations
   - Reliability requirements
   - **Decision Timeline:** After successful internal testing

9. **Multi-language Support:** Should the bot support languages beyond English in Phase 1?
   - Target audience language preferences
   - Resource requirements for multilingual support
   - **Decision Timeline:** Phase 2+ consideration

---

**Document Status:** Living document - will be updated as decisions are made and new requirements emerge.
