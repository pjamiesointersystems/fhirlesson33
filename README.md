Lesson 33 – Lab: Using Structured Data Capture (SDC)

This repository accompanies Lesson 33 of the FHIR Course: Using Structured Data Capture (SDC).
It contains exercises, examples, and code to support the lecture and lab activities.

📂 Repository: fhirlesson33

📖 Lesson Overview

Structured Data Capture (SDC) is an HL7 FHIR Implementation Guide that standardizes the creation and use of forms in healthcare. It enables interoperability, consistency, and reusability of forms and responses across systems.

Key Concepts:

Questionnaire → Defines the form.

QuestionnaireResponse → Captures the completed form.

Features:

Conditional logic (enableWhen)

Constraints & validations

Calculations with FHIRPath/expressions

Modular/derived forms for reuse

Pre-population with $populate

Extraction of structured data into FHIR resources (Observations, Conditions, etc.)

Lab Using Structured Data Captu…

🏥 Why SDC Matters

Forms are everywhere: admissions, assessments, checklists, clinical trials.

Without SDC: inconsistent data, manual re-entry, poor interoperability.

With SDC:

Consistent rendering & workflow

Automation (pre-filled forms)

Standardized, computable data

Interoperability across FHIR servers and applications

Lab Using Structured Data Captu…

⚙️ Tools Used in This Lab

NLM Form Builder
 → Create FHIR Questionnaires.

NLM Form Viewer (LHC-Forms)
 → Render and complete Questionnaires.

SDC SMART App → Launch forms in clinical workflows.

InterSystems IRIS for Health → Store Questionnaires and QuestionnaireResponses.

FHIR SQL Builder + Pandas → Analyze QuestionnaireResponses as structured data

Lab Using Structured Data Captu…

.

🧑‍💻 Lab Challenges
Challenge 1 – Building a Questionnaire

Use NLM Form Builder to create a questionnaire:

Smoking Status (Yes/No)

Average cigarettes/day (conditional numeric)

Age started smoking (numeric)

Export as FHIR Questionnaire (.json).

Post to FHIR server.

Challenge 2 – Capturing Responses

Load the Questionnaire in NLM Form Viewer.

Fill out realistic patient responses.

Export as FHIR QuestionnaireResponse.

Post to FHIR server and verify submission.

Repeat for 10 patients to generate analyzable data.

Challenge 3 – Analyzing Structured Data

Use FHIR SQL Builder to project QuestionnaireResponse data into relational tables.

Analyze with Python Pandas in Jupyter:

List patients who answered “Yes” to smoking.

Show their average reported cigarettes/day.

Discuss use of structured data for research & clinical studies

Lab Using Structured Data Captu…

.

🚀 Getting Started

Clone the Repository

git clone https://github.com/pjamiesointersystems/fhirlesson33.git
cd fhirlesson33


Set Up Environment

Python 3.9+ recommended

Install dependencies:

pip install -r requirements.txt


Run Examples

Post a Questionnaire to the FHIR server.

Submit QuestionnaireResponses.

Query responses with SQL Builder and analyze with Pandas.

📌 Key Takeaways

SDC standardizes healthcare forms with FHIR.

Questionnaires and QuestionnaireResponses provide computable, interoperable data.

Tools like NLM Form Builder, NLM Form Viewer, and FHIR SQL Builder streamline creation, capture, and analysis.

Structured responses enable analytics, research, and patient engagement.

📚 Additional Resources

FHIR Structured Data Capture (SDC) Implementation Guide

NLM Form Builder

LHC-Forms Viewer

FHIR Standard

🧾 License

This project is licensed under the MIT License. See the LICENSE
 file for details.

Would you like me to also include a workflow diagram (mermaid) showing how forms move from Form Builder → Viewer → FHIR Server → SQL Builder/Pandas for Lesson 33? That would visually reinforce the lab flow.