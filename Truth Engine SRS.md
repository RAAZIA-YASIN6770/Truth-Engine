**Software Requirements Specification (SRS)**

**Truth Engine**

**1. Introduction**

**1.1 Purpose**

This document provides a detailed **Software Requirements Specification
(SRS)** for the *Truth Engine* game. The SRS follows **IEEE 830 / IEEE
29148** standards and is intended for:

-   Software developers

-   System architects

-   Academic evaluators

-   Industry reviewers

Truth Engine is designed as a **browser-based logical reasoning system**
implemented using Python, focusing on contradiction detection rather
than traditional gameplay mechanics.

**1.2 Scope**

Truth Engine is a single-player web application where users analyze
system-based scenarios and identify logically impossible statements. The
system emphasizes:

-   Logical consistency

-   Critical reasoning

-   Rule-based system understanding

The application is positioned as:

-   An educational tool

-   A cognitive assessment system

-   A professional-grade logic evaluation platform

**1.3 Definitions, Acronyms, and Abbreviations**

  -----------------------------------------------------------------------
  **Term**    **Description**
  ----------- -----------------------------------------------------------
  SRS         Software Requirements Specification

  UI          User Interface

  API         Application Programming Interface

  RBES        Rule-Based Evaluation System

  Scenario    A logical problem consisting of rules and facts
  -----------------------------------------------------------------------

**1.4 References**

-   IEEE 830-1998 SRS Standard

-   IEEE 29148-2018 Systems and Software Engineering

-   ISO/IEC 25010 Software Quality Model

**1.5 Overview**

This document is organized into overall system description, functional
requirements, non-functional requirements, system models, and
constraints.

**2. Overall Description**

**2.1 Product Perspective**

Truth Engine operates as a **standalone web-based system** built on a
client-server architecture:

-   Frontend: Browser-based UI

-   Backend: Python-based logic engine

The system does not rely on external game engines or real-time
interaction frameworks.

**2.2 Product Functions**

Major system functions include:

-   Scenario presentation

-   Logical contradiction evaluation

-   Attempt tracking

-   Scenario locking after rule violation

-   Progress control

**2.3 User Classes and Characteristics**

  -----------------------------------------------------------------------
  **User Class**        **Description**
  --------------------- -------------------------------------------------
  Student               Learners in CS, IT, logic, AI

  Professional          Engineers, analysts, auditors

  Evaluator             Recruiters and assessors
  -----------------------------------------------------------------------

No prior gaming experience is required.

**2.4 Operating Environment**

-   Client: Modern web browsers (Chrome, Firefox, Edge)

-   Server: Python runtime (3.10+)

-   OS: Platform-independent

**2.5 Design and Implementation Constraints**

-   Python must be used for core logic

-   No randomization in scenario outcomes

-   Deterministic logic evaluation

-   Browser-based interaction only

**2.6 User Documentation**

-   Onboarding instructions

-   Scenario introduction text

-   System rule explanations

**2.7 Assumptions and Dependencies**

-   Users possess basic reading comprehension

-   Internet connection required

-   Scenarios are pre-validated

**3. Specific Requirements**

**3.1 Functional Requirements**

**FR-1: Scenario Display**

The system shall display one scenario at a time including context and
statements.

**FR-2: Statement Selection**

The system shall allow the user to select exactly one statement per
attempt.

**FR-3: Logical Validation**

The system shall evaluate the selected statement against predefined
contradiction rules.

**FR-4: Attempt Limitation**

The system shall allow a maximum of three incorrect attempts per
scenario.

**FR-5: Scenario Reset**

The system shall reset the scenario upon an incorrect selection.

**FR-6: Scenario Locking**

The system shall lock the scenario after three failed attempts.

**FR-7: Progression Control**

The system shall allow progression only upon correct logical
identification.

**3.2 Non-Functional Requirements**

**3.2.1 Performance Requirements**

-   Scenario evaluation response time \< 200 ms

-   Page load time \< 2 seconds

**3.2.2 Reliability Requirements**

-   99% logical consistency accuracy

-   No state corruption on refresh

**3.2.3 Usability Requirements**

-   Minimalist UI

-   No hints or suggestions

-   Clear typography

**3.2.4 Security Requirements**

-   No user data persistence by default

-   Secure session handling

**3.2.5 Maintainability Requirements**

-   Modular scenario definitions

-   Easily extendable logic rules

**3.3 Logical Database Requirements**

Each scenario shall include:

-   Unique ID

-   Category

-   Difficulty level

-   Statements

-   Exactly one logically false statement

**4. System Models**

**4.1 Use Case Diagram (Textual)**

**Actor:** Player

**Use Cases:**

-   Start scenario

-   Analyze statements

-   Select contradiction

-   Receive evaluation

-   Progress or reset

**4.2 Process Flow**

1.  Load scenario

2.  Display statements

3.  Accept selection

4.  Validate logic

5.  Apply system rules

**5. External Interface Requirements**

**5.1 User Interface**

-   Web-based interface

-   Keyboard and mouse input

**5.2 Software Interface**

-   REST API for scenario delivery

-   Python-based logic engine

**6. Quality Attributes (ISO/IEC 25010)**

-   Functional suitability

-   Usability

-   Reliability

-   Maintainability

-   Portability

**7. Future Enhancements**

-   Explanation-based validation

-   Scenario authoring tool

-   Enterprise assessment dashboards

**8. Approval**

This document serves as the formal SRS for the Truth Engine system and
can be used for academic submission, industry evaluation, and
professional portfolio presentation.

**End of Document**
