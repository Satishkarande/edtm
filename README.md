**Overview**

Event-Driven Task Manager is a fully serverless backend system built on AWS.
It demonstrates real-world backend architecture using asynchronous event processing, workflow orchestration, failure handling, and CI/CD automation.

This project focuses on backend engineering concepts.

Architecture Summary:

Flow :-
	1.	Client sends POST /tasks
	2.	API Gateway (HTTP API) invokes Task API Lambda
	3.	Task is stored in DynamoDB
	4.	Event is published to SQS Main Queue
	5.	Event Processor Lambda consumes the message
	6.	AWS Step Functions workflow is triggered
	7.	Workflow completes business steps

Failure Path:
	•	If processing fails after retries → message moves to DLQ (Dead Letter Queue)

**** AWS Services Used****
	•	API Gateway (HTTP API)
	•	AWS Lambda
	•	Task API Lambda (sync)
	•	Event Processor Lambda (async)
	•	Amazon DynamoDB – task persistence
	•	Amazon SQS
	•	Main Queue
	•	Dead Letter Queue (DLQ)
	•	AWS Step Functions – workflow orchestration
	•	AWS IAM – least-privilege roles
	•	AWS CodePipeline + CodeBuild – CI/CD automation
	•	SSM Parameter Store – configuration management

**Event-Driven Design (Why This Matters)**
	•	Loose coupling between services
	•	Scalable: API traffic and processing scale independently
	•	Fault tolerant with retries + DLQ
	•	Production-grade pattern used in real systems

This is not CRUD-only Lambda — it models how real backend systems work.

** Security Design**
	•	IAM roles follow least privilege
	•	Each Lambda has only required permissions
	•	No hardcoded secrets
	•	Environment variables + SSM parameters used properly

** CI/CD Pipeline**

Trigger:
	•	Push to main branch

Pipeline Steps:
	1.	Source → GitHub
	2.	Build → CodeBuild
	3.	Package Lambdas
	4.	Deploy updated Lambda code automatically

How to test:-curl -X POST https://ypnjm0us4i.execute-api.<region>.amazonaws.com/dev/tasks \
  -H "Content-Type: application/json" \
  -d '{"taskID":"task-173"}'
  Verify:
	•	DynamoDB item created
	•	SQS message sent
	•	Step Function execution started
	•	DLQ empty 

**  What This Project Demonstrates**
	•	Event-driven backend architecture
	•	Async processing with SQS
	•	Workflow orchestration using Step Functions
	•	Proper error handling with DLQ
	•	CI/CD for serverless applications
	•	AWS architectural thinking (not just services)
