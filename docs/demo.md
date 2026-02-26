# Demo Script

1. **Lookup patient**
   - Prompt: `Find patient Alicia`  
2. **List appointments**
   - Prompt: `Show appointments for p001`
3. **Attempt confirmation (no explicit confirm)**
   - Prompt: `Confirm appointment a001`
   - Expected: assistant asks for explicit confirmation / tool returns confirmation_required.
4. **Confirm explicitly**
   - Prompt: `Confirm appointment a001 confirm`
5. **Create follow-up task**
   - Prompt: `Create a follow up task for p001 to call after cleaning due 2026-01-12 confirm`
6. **Send notification**
   - Prompt: `Send sms reminder to p001 that their appointment is tomorrow confirm`
