# Getting Started with ConvoScope v2.0

Welcome to ConvoScope! This guide will help you get up and running with the new web interface in just a few minutes.

## Prerequisites

Before you begin, make sure you have:

- **Python 3.8+** installed ([Download Python](https://www.python.org/downloads/))
- **Node.js 18+** and npm installed ([Download Node.js](https://nodejs.org/))
- Your Claude AI conversation export JSON file (see below if you don't have it yet)

## Step 1: Get Your Claude Conversation Data

1. Go to [Claude.ai](https://claude.ai)
2. Click your profile icon → Settings
3. Click the "Privacy" tab
4. Click "Download my data"
5. Confirm your email address
6. Wait 1-3 days for the email with your data
7. Download and extract the `conversations.json` file

**Don't have your data yet?** No problem! You can set up ConvoScope now and come back when you receive your export.

## Step 2: Install ConvoScope

```bash
# Clone the repository
git clone https://github.com/yourusername/ConvoScope-v2.git
cd ConvoScope-v2

# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install
cd ..
```

## Step 3: Start the Backend Server

Open a terminal and run:

```bash
python backend/app.py
```

You should see:

```
Starting ConvoScope backend on port 5000
CORS enabled for: ['http://localhost:3000', ...]
* Running on http://127.0.0.1:5000
```

**Keep this terminal open!** The backend needs to stay running.

## Step 4: Start the Frontend

Open a **new terminal** (keep the backend running) and run:

```bash
cd frontend
npm run dev
```

You should see:

```
VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

## Step 5: Open ConvoScope in Your Browser

1. Open your web browser
2. Go to **http://localhost:3000**
3. You should see the ConvoScope upload page!

## Step 6: Upload Your Data

1. Drag and drop your `conversations.json` file onto the upload zone
   - Or click to browse and select the file
2. ConvoScope will validate the file and show you a preview:
   - Number of conversations
   - Total messages
   - Date range
3. Click "Start Analysis"
4. Watch the real-time progress updates!
5. Explore your insights when analysis completes ✨

## What Happens During Analysis?

ConvoScope analyzes your conversations to identify:

- **Topics** - What you talk to Claude about (Technical, AI/ML, Creative, etc.)
- **Sentiment** - The emotional tone of conversations
- **Quality** - Task completion rates, collaboration patterns
- **Patterns** - When you use Claude, conversation streaks, trends over time
- **Failures** - Model issues like hallucinations, context loss, etc.

**All processing happens locally on your computer** - your data never leaves your machine!

## Privacy Guarantee

ConvoScope automatically:

- ✅ Redacts personal information (emails, phone numbers, addresses, etc.)
- ✅ Processes everything locally (no cloud, no external servers)
- ✅ Shows you exactly what data is being redacted
- ✅ Lets you verify no network traffic via the Privacy dashboard

You can check the network monitor in your browser's developer tools - you'll see zero external requests!

## Troubleshooting

### Backend won't start

**Error: "No module named 'flask'"**
```bash
pip install -r requirements.txt
```

**Error: "Port 5000 is already in use"**
```bash
# Find and kill the process using port 5000
# On Mac/Linux:
lsof -ti:5000 | xargs kill -9

# On Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Frontend won't start

**Error: "Cannot find module"**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Error: "Port 3000 is already in use"**
```bash
# The frontend will automatically try port 3001
# Or specify a different port:
npm run dev -- --port 3001
```

### File upload fails

**Error: "Invalid file format"**
- Make sure you're uploading the `conversations.json` file from Claude
- Check that the file isn't corrupted (should be valid JSON)
- File must be under 100MB

**Error: "No conversations found"**
- Your export might be empty
- Try re-requesting your data from Claude.ai

### Analysis gets stuck

- Check the backend terminal for error messages
- Refresh the page and try again
- For large files (>10,000 messages), analysis may take 2-3 minutes

### Page is blank or broken

- Clear your browser cache
- Try a different browser (Chrome, Firefox, Safari, Edge all work)
- Check browser console for errors (F12 → Console tab)

## Next Steps

Now that you have ConvoScope running:

1. **Explore the Dashboard** - See your conversation overview
2. **Browse Topics** - Drill down into specific categories
3. **Check Quality** - Understand your collaboration patterns
4. **View Timeline** - See your activity patterns over time
5. **Read the Privacy Dashboard** - Verify data stays local
6. **Export Insights** - Share (privacy-safe) visualizations

## Helpful Resources

- 📖 [User Experience Walkthrough](docs/USER_EXPERIENCE_WALKTHROUGH.md) - Detailed tour of the interface
- 🎨 [UX Improvement Plan](docs/UX_IMPROVEMENT_PLAN.md) - Our design vision
- 🔒 [Privacy & Security Guide](docs/PRIVACY.md) - How we protect your data
- 💻 [Frontend Architecture](docs/architecture/FRONTEND_ARCHITECTURE.md) - Technical details
- 🐍 [Backend Architecture](docs/architecture/BACKEND_ARCHITECTURE.md) - API documentation

## Get Help

If you're stuck:

1. Check the [troubleshooting section](#troubleshooting) above
2. Search [GitHub Issues](https://github.com/yourusername/ConvoScope-v2/issues)
3. Ask in [Discussions](https://github.com/yourusername/ConvoScope-v2/discussions)
4. Open a new issue with:
   - Your OS and Python/Node versions
   - Complete error message
   - Steps to reproduce
   - Screenshots if relevant

## Contributing

Want to help improve ConvoScope?

- 🐛 Report bugs
- 💡 Suggest features
- 📝 Improve documentation
- 💻 Submit code contributions

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

**Ready to analyze your conversations?** 🚀

Start the backend, start the frontend, and discover insights about how you use Claude AI!

Remember: **All analysis happens locally. Your data never leaves your computer.** 🔒
