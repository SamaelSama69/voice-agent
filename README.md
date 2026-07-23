# 2Care Voice AI Agent

An AI-powered voice receptionist for Yashoda Hospital that enables patients to book, reschedule, cancel, and manage appointments through natural voice conversations.

---

# Project Overview

2Care Voice AI is a production-oriented healthcare voice agent built using DeepAgents, LangChain, FastAPI, and Vapi.

The system allows patients to interact naturally over voice while the backend performs real appointment management operations using live hospital data.

Supported capabilities:

* Appointment booking
* Appointment rescheduling
* Appointment cancellation
* Appointment lookup
* Doctor recommendation
* Speciality-based doctor search
* Emergency symptom detection
* Error recovery and clarification
* Patient verification and privacy protection

---

# Why Vapi

Vapi was selected because it provides:

* Low-latency voice conversations
* Reliable speech-to-text and text-to-speech
* Easy telephony integration
* Real-time tool calling support
* Natural conversational experience

---

# Architecture

```text
Patient Call
      ↓
Vapi Voice Platform
      ↓
FastAPI API Server
      ↓
DeepAgents Agent
      ↓
LangChain Tools
      ↓
SQLite Database
```

---

# Tech Stack

| Component       | Technology           |
| --------------- | -------------------- |
| Voice Platform  | Vapi                 |
| Agent Framework | DeepAgents           |
| LLM Framework   | LangChain            |
| Backend API     | FastAPI              |
| Database        | SQLite               |
| ORM             | SQLAlchemy           |
| Deployment      | Render               |
| Model Provider  | OpenRouter           |
| Monitoring      | LangSmith  |

---

# Real Hospital Data

This project uses real doctor information collected from Yashoda Hospital, including:

* Doctor names
* Departments
* Specialities
* Experience
* OPD timings
* Languages spoken
* Hospital locations

No placeholder doctors or synthetic hospital data were used.

---

# Features

### Appointment Booking

* Doctor selection
* Speciality search
* Slot availability checking
* Confirmation workflow
* Duplicate prevention

### Appointment Management

* Appointment lookup
* Cancellation
* Rescheduling
* Conflict resolution

### Safety Features

* Patient verification
* Privacy protection
* Prompt injection resistance
* SQL injection protection
* Emergency symptom detection

---

# Deployment

### Live API

--link to be update

### Swagger Documentation

--link to be update

# Live Voice Demo

The deployed voice agent can be tested using the following Vapi link:

--link to be update

Please use the following example prompts:

- Book a cardiologist appointment tomorrow.
- Show available cardiologists.
- Cancel my appointment.
- Reschedule my appointment.
- Show my appointments.

---

# Evaluation Harness

The evaluation framework was designed to measure the reliability and robustness of the voice agent under real-world hospital receptionist scenarios.

The evaluation suite consists of six independent categories.

## Evaluation Categories

| Category            | Result |
| ------------------- | ------ |
| Booking             | 7/7    |
| Cancellation        | 3/3    |
| Rescheduling        | 5/5    |
| Appointment Lookup  | 3/3    |
| Emergency Detection | 3/3    |
| Security            | 3/3    |

### Overall Results

* Total Test Cases: 24
* Successful Tests: 24
* Success Rate: 100%

---

# Booking Evaluation

The booking evaluation measures:

* Doctor selection
* Speciality-based search
* Slot selection
* Duplicate booking prevention
* Missing information handling
* Language preference handling
* Confirmation workflow

Result: 7/7 Passed

---

# Cancellation Evaluation

Measures:

* Patient verification
* Appointment identification
* Confirmation requirement
* Invalid appointment handling

Result: 3/3 Passed

---

# Rescheduling Evaluation

Measures:

* Slot availability
* Alternative slot suggestions
* Same-day rescheduling
* Appointment verification
* User cancellation handling

Result: 5/5 Passed

---

# Appointment Lookup Evaluation

Measures:

* Patient authentication
* Appointment retrieval
* Missing information handling

Result: 3/3 Passed

---

# Emergency Detection Evaluation

Measures:

* Chest pain detection
* Breathing difficulty detection
* Emergency escalation
* Non-emergency symptom handling

Result: 3/3 Passed

---

# Security Evaluation

Measures:

* SQL injection attacks
* Prompt injection attacks
* Unauthorized patient data access

Result: 3/3 Passed

---

# Evaluation Metrics

| Metric                   | Value |
| ------------------------ | ----- |
| Total Test Cases         | 24    |
| Successful Tests         | 24    |
| Success Rate             | 100%  |
| Booking Success Rate     | 100%  |
| Security Success Rate    | 100%  |
| Emergency Detection Rate | 100%  |

---

# Latency

Average response latency:

* Voice response: 2–5 seconds
* Tool execution: 1–3 seconds
* End-to-end appointment booking: approximately 90 seconds

---

# Known Limitations

* SQLite is currently used as the database.
* Speech recognition quality depends on the voice provider.
* Multi-language support is limited.
* Extremely noisy environments were not evaluated.
* Human satisfaction metrics are not included.

---

# Future Improvements

* PostgreSQL database
* Multi-language support
* Call recording
* Appointment reminders
* SMS notifications
* Human handoff workflow
* Analytics dashboard
* Expanded evaluation framework

---

# Reproducibility

The evaluation harness is fully reproducible.

Evaluation scenarios are available in:

```text
evals/
├── booking.json
├── cancellation.json
├── emergency.json
├── lookup.json
├── reschedule.json
└── security.json
```

The evaluation suite can be independently executed by reviewers to verify system behavior.

---

# Author

Peetha Raghavendra

AI Engineer | Applied Machine Learning | Generative AI | Voice AI Systems
