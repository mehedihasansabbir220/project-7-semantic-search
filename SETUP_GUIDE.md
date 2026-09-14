# Complete Setup Guide - Task 06 & 07

## 📋 Folder Structure (CORRECT)

```
project-7-semantic-search/        ← ROOT folder
├── backend/                       ← Backend folder
│   ├── venv/                      ← ✅ Backend virtual env HERE
│   ├── main.py
│   ├── requirements.txt
│   ├── api/
│   ├── services/
│   ├── ingestion/
│   └── data/
│
├── frontend/                      ← Frontend folder
│   ├── package.json
│   ├── app/
│   ├── components/
│   └── lib/
│
└── README.md
```

## 🚀 Setup Instructions

### Step 1: Backend Setup (5 minutes)

```bash
# Navigate to backend folder
cd /Users/mohammedmehedi/Documents/workspace/AI_LEARING_PROJECT/project-7-semantic-search/backend

# Create virtual environment (if not done)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed sentence-transformers torch fastapi uvicorn pydantic ...
```

### Step 2: Start Backend (Terminal 1)

```bash
cd /Users/mohammedmehedi/Documents/workspace/AI_LEARING_PROJECT/project-7-semantic-search/backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
Uvicorn running on http://0.0.0.0:8000
Application startup complete
✓ API READY - Listening on http://localhost:8000
```

✅ **Backend is running** - Keep this terminal open!

### Step 3: Frontend Setup (5 minutes)

In a **NEW terminal**:

```bash
# Navigate to frontend folder
cd /Users/mohammedmehedi/Documents/workspace/AI_LEARING_PROJECT/project-7-semantic-search/frontend

# Install Node.js dependencies (first time only)
npm install
```

**Expected output:**
```
added 250+ packages
```

### Step 4: Start Frontend (Terminal 2)

```bash
cd /Users/mohammedmehedi/Documents/workspace/AI_LEARING_PROJECT/project-7-semantic-search/frontend
npm run dev
```

**Expected output:**
```
> semantic-search-frontend@1.0.0 dev
> next dev

▲ Next.js 14.0.0
- Local:        http://localhost:3000
- Environments: .env.local

✓ Ready in 2.1s
```

✅ **Frontend is running** - Keep this terminal open!

### Step 5: Test the System (Terminal 3)

```bash
# Check backend health
curl http://localhost:8000/health

# Test search
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "machine learning", "top_k": 5}'
```

**Expected responses:**
```json
{"status": "healthy", "model_loaded": true, "chunks_indexed": 57}
```

---

## 📱 Access the Application

### Backend API
- Health: **http://localhost:8000/health**
- API Docs: **http://localhost:8000/docs**
- ReDoc: **http://localhost:8000/redoc**

### Frontend
- Website: **http://localhost:3000**

---

## ⚠️ Common Issues & Fixes

### Issue 1: "venv: command not found"

**Cause:** Virtual environment not activated

**Fix:**
```bash
cd backend
source venv/bin/activate
# You should see (venv) at start of terminal line
```

### Issue 2: "ModuleNotFoundError: No module named 'fastapi'"

**Cause:** Dependencies not installed

**Fix:**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### Issue 3: "Address already in use" (port 8000)

**Cause:** Another process using port 8000

**Fix:**
```bash
# Find process using port 8000
lsof -i :8000

# Kill it (replace PID)
kill -9 <PID>

# Or use different port
uvicorn main:app --port 8001
```

### Issue 4: "API Unavailable" in frontend

**Cause:** Backend not running

**Fix:**
```bash
# In Terminal 1:
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

### Issue 5: "Cannot find module 'next'" in frontend

**Cause:** Dependencies not installed

**Fix:**
```bash
cd frontend
npm install
npm run dev
```

### Issue 6: pydantic-core build error

**Cause:** Python version incompatibility

**Fix:**
```bash
cd backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install --no-cache-dir -r requirements.txt
```

---

## 📊 Terminal Setup (Recommended)

You need **3 terminals** running simultaneously:

```
┌─────────────────────────────┐
│ Terminal 1: BACKEND         │
│ $ source venv/bin/activate  │
│ $ uvicorn main:app --reload │
│ Running on :8000            │
└─────────────────────────────┘

┌─────────────────────────────┐
│ Terminal 2: FRONTEND        │
│ $ npm run dev               │
│ Running on :3000            │
└─────────────────────────────┘

┌─────────────────────────────┐
│ Terminal 3: TESTING/COMMANDS │
│ $ curl http://localhost:... │
│ $ npm run build             │
│ $ git status                │
└─────────────────────────────┘
```

---

## ✅ Verification Checklist

### Backend Ready?

- [ ] Terminal shows "Application startup complete"
- [ ] http://localhost:8000/health returns `{"status": "healthy", ...}`
- [ ] http://localhost:8000/docs loads Swagger UI
- [ ] curl search command returns results

### Frontend Ready?

- [ ] Terminal shows "Ready in X.Xs"
- [ ] http://localhost:3000 loads in browser
- [ ] Page shows "Semantic Search" title
- [ ] Green "Connected" indicator appears
- [ ] Search input is visible

### Full System Ready?

- [ ] Type a search query in frontend
- [ ] Click search
- [ ] Results appear within 2 seconds
- [ ] Scores show (0.85-0.99 range)
- [ ] No errors in browser console

---

## 🎯 Quick Commands Reference

### Backend

```bash
# Navigate & activate
cd backend && source venv/bin/activate

# Start
uvicorn main:app --reload

# Stop
Ctrl + C

# Install packages
pip install -r requirements.txt

# Deactivate venv
deactivate
```

### Frontend

```bash
# Navigate
cd frontend

# Install dependencies (first time)
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Stop
Ctrl + C
```

### Testing

```bash
# Health check
curl http://localhost:8000/health

# Test search
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "machine learning", "top_k": 5}'

# Check frontend is running
curl http://localhost:3000

# View backend API docs
open http://localhost:8000/docs
```

---

## 🚀 Full Local Testing Procedure

### 1. Prepare (5 min)

```bash
# Terminal 1
cd /Users/mohammedmehedi/Documents/workspace/AI_LEARING_PROJECT/project-7-semantic-search/backend
source venv/bin/activate
# Wait for prompt: (venv) backend $
```

### 2. Start Backend (1 min)

```bash
# Terminal 1
uvicorn main:app --reload
# Wait for: ✓ API READY
```

### 3. Start Frontend (Terminal 2)

```bash
cd /Users/mohammedmehedi/Documents/workspace/AI_LEARING_PROJECT/project-7-semantic-search/frontend
npm run dev
# Wait for: ✓ Ready in Xs
```

### 4. Open Browser

- Frontend: http://localhost:3000
- Backend Docs: http://localhost:8000/docs

### 5. Test Search

1. Type: "machine learning"
2. Click: Search
3. Wait: 1-2 seconds
4. Expect: 2-3 results with scores

### 6. Test Multiple Queries

- "deep neural networks"
- "natural language processing"
- "transformer models"

### 7. Test Error States

**Stop backend:** Ctrl+C in Terminal 1
- Frontend should show: "API Unavailable"

**Restart backend:** `uvicorn main:app --reload`
- Frontend should show: "Connected"

---

## 📱 Environment Files

### Frontend `.env.local`

```bash
cd frontend
echo 'NEXT_PUBLIC_API_URL=http://localhost:8000' > .env.local
```

Or manually create `frontend/.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 🎉 Success Indicators

### ✅ Backend Success

```
Uvicorn running on http://0.0.0.0:8000
Application startup complete
[STEP 1/3] Loading documents...
✓ Loaded 3 documents
[STEP 2/3] Chunking documents...
✓ Created 57 chunks
[STEP 3/3] Generating embeddings...
✓ Generated 57 embeddings
✓ API READY - Listening on http://localhost:8000
```

### ✅ Frontend Success

```
▲ Next.js 14.0.0
- Local:        http://localhost:3000
- Environments: .env.local

✓ Ready in 2.1s
```

### ✅ Full System Success

- Page loads at http://localhost:3000
- Search works and returns results
- Scores appear (0.85+)
- No console errors
- "Connected" indicator shows

---

## 🔧 Advanced Commands

### Rebuild Backend Index

```bash
cd backend && source venv/bin/activate
python3 -c "from services.search_service import initialize_search_service; initialize_search_service('data/sample_documents')"
```

### Clear Frontend Build

```bash
cd frontend
rm -rf .next node_modules/.cache
npm run dev
```

### Check Python Version

```bash
python3 --version
# Should be: Python 3.9+
```

### Check Node Version

```bash
node --version
# Should be: v18+
npm --version
# Should be: v9+
```

---

## 📚 Next Steps After Setup

1. ✅ Both running locally
2. 🔍 Test all search queries
3. 📝 Add custom documents to `backend/data/sample_documents/`
4. 🎨 Customize frontend styling
5. 🚀 Deploy to production (Vercel + Railway)

---

**Setup Complete! Happy searching!** 🔍

