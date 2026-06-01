# Tomorrow Project Plan

## Goal

Stabilize the backend and local development workflow before doing a larger frontend redesign.

## Why this comes first

The app is already running, but a more stable backend and cleaner local setup will make UI work faster, safer, and less frustrating. The main idea is to reduce file-sync noise, tighten input handling, improve test coverage, and keep normal app usage mostly read-only.

## Recommended order

1. Move the repo out of OneDrive
2. Verify the app still launches from the new location
3. Harden backend validation
4. Improve backend error responses
5. Add more API and integration tests
6. Review dependency weight and cleanup opportunities
7. Revisit the frontend flow and redesign from an address-first experience

## Step 1: Move the repo out of OneDrive

### Suggested new location

- `C:\dev\HousingApp`

### Reason

OneDrive can create noise for:

- `.venv`
- `node_modules`
- `housing_app.db`
- live reload watchers

Moving the project to a normal local dev folder should make startup and file watching more predictable.

## Step 2: Verify launch flow after moving

### Check these

- Backend starts cleanly
- Frontend starts cleanly
- `http://127.0.0.1:8000/health` works
- `http://127.0.0.1:5173` works
- lookup for a sample address still works

### Sample address

- `101 Cedar Elm Street`

## Step 3: Harden backend validation

### Add or tighten validation for

- blank address strings
- negative square footage
- negative taxes, rent, or maintenance
- `down_payment_percent < 0`
- `down_payment_percent > 1`
- negative interest rates
- invalid holding periods
- invalid renovation quantities or costs

### Desired outcome

Bad input should return clean validation errors instead of confusing failures.

## Step 4: Improve backend error responses

### Focus areas

- property not found
- bad renovation payload
- bad investment payload
- startup/config issues

### Desired outcome

All major API failures should return predictable, user-friendly JSON responses.

## Step 5: Add more tests

### Priority tests

- `GET /api/report/property/{id}`
- property lookup miss case
- invalid renovation payload
- invalid investment payload
- repeated requests return stable response shapes

### Desired outcome

More confidence before deeper UI and workflow changes.

## Step 6: Review backend weight and cleanup

### Review

- whether `pandas` is needed in active request paths
- whether any mock/demo paths can be simplified
- whether startup scripts should be further simplified

### Desired outcome

Keep the project lighter and easier to run locally.

## Step 7: Frontend/product direction after backend hardening

### Product flow

The app should become address-first:

1. Welcome page focused only on the address
2. After lookup, route to a property options hub
3. Let the user choose what to explore next

### Design direction

- sky and white color palette
- keep the current typography tone
- simpler landing page
- less dashboard clutter on first view

### Recommended post-address options

- `Home Value`
- `Renovation ROI`
- `Investor Analysis`
- `Full Property Report`

## Nice-to-have tomorrow if time allows

- add a favicon so `/favicon.ico` stops 404ing
- add a single launch script for stable startup in the new folder
- add a short developer troubleshooting section to the README

## Definition of success for tomorrow

- repo moved out of OneDrive
- backend and frontend launch cleanly
- validation is stronger
- API tests expanded
- app is ready for a cleaner address-first UI redesign
