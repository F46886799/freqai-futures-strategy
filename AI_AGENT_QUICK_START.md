# 🚀 AI Agent Quick Start Card

**به پروژه FreqAI Futures Strategy خوش آمدید!**

---

## ⚡ 30-Second Briefing

- **Project:** AI-powered futures trading bot (adding RL layer)
- **Your Task:** Increase test coverage from 45% to 60%+ (Sprint 2, Issue #13)
- **Timeline:** ~3-4 hours of work
- **Tech:** Python 3.11, pytest, FreqAI, Freqtrade

---

## 📖 MUST READ (30 minutes total)

### Step 1: Context (5 min)
```
Open: SETUP_COMPLETE_SUMMARY.md
```
→ Understand: What was done, what's next

### Step 2: Workflow (20 min)
```
Open: AI_AGENT_WORKFLOW_GUIDE.md
```
→ Learn: How to work (6 phases step-by-step)

### Step 3: Your Task (5 min)
```
Browser: https://github.com/aminak58/freqai-futures-strategy/issues/13
```
→ Read: Acceptance criteria, technical tasks, definition of done

---

## ✅ Quick Setup Checklist

```powershell
# 1. Check Python
python --version  # Should be 3.11.x

# 2. Activate venv (if not active)
.\.venv\Scripts\Activate.ps1

# 3. Install deps
pip install -r requirements-dev.txt

# 4. Run tests
pytest tests/ -v

# 5. Check current coverage
pytest tests/ --cov=src --cov=user_data/strategies --cov-report=term
# Current: ~45% → Target: 60%+

# 6. Check sprint status
python scripts/sprint_burndown.py --sprint 2

# ✅ If all above works, you're ready!
```

---

## 🎯 Your Mission (Issue #13)

**Goal:** Write tests for `user_data/strategies/FreqAIHybridStrategy.py`

**What to test:**
- Entry/exit logic
- Gating funnel (8 stages)
- Governance integration
- Regime detection
- Edge cases (empty data, extreme values, etc.)

**How many tests:** ~20-30 tests needed

**Success criteria:**
- Coverage ≥ 60%
- All tests passing
- No linting errors

---

## 🔄 Workflow (TL;DR)

```powershell
# 1. Create branch
git checkout -b feature/us-1-4-test-coverage

# 2. Write test
code tests/test_strategy_entry.py
# ... write test ...

# 3. Run & check
pytest tests/test_strategy_entry.py -v
pytest tests/ --cov=user_data/strategies --cov-report=term

# 4. Commit
git add tests/
git commit -m "[US 1.4] Add entry tests (coverage +5%)"

# 5. Repeat until coverage ≥ 60%

# 6. Push & PR
git push origin feature/us-1-4-test-coverage
# Create PR in GitHub

# 7. Wait for CI, merge, done! 🎉
```

---

## 📚 Full Documentation (if you need more details)

**Onboarding (This is for you!):**
- `AI_AGENT_ONBOARDING_GUIDE.md` ← **START HERE if you're new**

**Workflow:**
- `AI_AGENT_WORKFLOW_GUIDE.md` ← Detailed 6-phase workflow

**System:**
- `GITHUB_PROJECT_MANAGEMENT.md` ← System architecture
- `SETUP_COMPLETE_SUMMARY.md` ← Current status

**Project:**
- `FUTURE_SPRINTS_ROADMAP.md` ← 16-sprint roadmap
- `SCRUM_FRAMEWORK.md` ← Scrum process

---

## ❓ Quick FAQ

**Q: Where do I start?**  
A: Read `SETUP_COMPLETE_SUMMARY.md` (5 min), then `AI_AGENT_WORKFLOW_GUIDE.md` (20 min)

**Q: What do I need to do?**  
A: Write tests until coverage goes from 45% → 60%+

**Q: How do I know what to test?**  
A: Read Issue #13 in GitHub (acceptance criteria tells you everything)

**Q: What if tests fail?**  
A: Read error, debug with `-v` or `--pdb`, fix, re-run

**Q: What if CI fails?**  
A: Check GitHub PR > Checks tab, read logs, fix locally, push again

**Q: How many tests needed?**  
A: Probably 20-30 tests to reach 60% coverage

**Q: I don't understand the strategy code!**  
A: That's OK! Just test the behavior (black box testing)

---

## 🎯 Success Looks Like This

```
✅ Coverage: 62% (was 45%)
✅ Tests: 42 passing (was 17)
✅ CI: All 5 checks passing
✅ PR: Merged to master
✅ Issue #13: CLOSED
✅ Sprint 2: 13/18 points done (72%)
🎉 Mission accomplished!
```

---

## 🚀 You're Ready! Let's Go!

**First command:**
```powershell
code AI_AGENT_ONBOARDING_GUIDE.md
```

**Then follow:** Phase 0 → Phase 1 → Phase 2 → Phase 3

**Timeline:**
- Phase 0 (Context): 30 min
- Phase 1 (Setup): 5 min
- Phase 2 (Dev): 2-3 hours
- Phase 3 (PR): 30 min

**Total:** ~4 hours from zero to done ✅

---

**Questions?** All answers are in `AI_AGENT_WORKFLOW_GUIDE.md`

**Let's build something awesome! 🚀**
