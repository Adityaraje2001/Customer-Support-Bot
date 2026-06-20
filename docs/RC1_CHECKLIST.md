# RC-1 Production Readiness Checklist

## Authentication Tests
- [ ] Register
- [ ] Login
- [ ] JWT generation
- [ ] Token expiration
- [ ] `/auth/me`
- [ ] Protected routes
- [ ] Logout
- [ ] Role loading

## RBAC Tests
- [ ] Customer cannot access Knowledge Base Admin APIs
- [ ] Customer cannot access Admin Ticket APIs
- [ ] Customer cannot access Analytics APIs
- [ ] Admin can access all

## Chat Tests
- [ ] Question submission
- [ ] Conversation creation
- [ ] Conversation persistence
- [ ] Conversation history retrieval
- [ ] Agent routing
- [ ] Session handling

## RAG Tests
- [ ] Document retrieval
- [ ] Embedding search
- [ ] Chroma connectivity
- [ ] Retrieved document count
- [ ] Active document filtering
- [ ] Archived document exclusion
- [ ] Deleted document exclusion

## Knowledge Base Tests
- [ ] Upload document
- [ ] Activate document
- [ ] Archive document
- [ ] Delete document
- [ ] Document listing
- [ ] Search
- [ ] Version history
- [ ] Rollback
- [ ] Audit trail

## Document Versioning Tests
- [ ] Auto version increment
- [ ] Single active version
- [ ] Rollback
- [ ] Audit records
- [ ] History endpoint

## Ticket Tests
- [ ] Create ticket
- [ ] Status lookup
- [ ] My tickets
- [ ] Open tickets
- [ ] Resolved tickets
- [ ] Close ticket

## Feedback Tests
- [ ] Helpful feedback
- [ ] Not helpful feedback
- [ ] Feedback storage
- [ ] Feedback analytics
- [ ] MLflow logging

## Database Tests
- [ ] PostgreSQL connectivity
- [ ] CRUD operations
- [ ] Connection pooling
- [ ] Health endpoint

## Celery Tests
- [ ] Task creation
- [ ] Redis connectivity
- [ ] Document ingestion
- [ ] Status transitions
- [ ] Retry logic

## MLflow Tests
- [ ] Run creation
- [ ] Metrics logging
- [ ] Parameters logging
- [ ] Databricks visibility
- [ ] Trace creation

## Frontend Tests
- [ ] Dashboard
- [ ] Chat UI
- [ ] Knowledge Base UI
- [ ] Conversation History
- [ ] Profile
- [ ] Feedback UI
- [ ] Responsive design
