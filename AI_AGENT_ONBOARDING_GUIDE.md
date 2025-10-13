# AI Agent Onboarding Guide - From Zero to Productive

**مخاطب:** AI Agent جدید (Claude, GPT, Copilot) بدون هیچ پیش‌زمینه‌ای از پروژه  
**هدف:** تبدیل AI agent به یک contributor مستقل و productive در 30 دقیقه  
**تاریخ:** 13 اکتبر 2025

---

## 🎯 خلاصه 30 ثانیه‌ای (TL;DR)

این پروژه یک **AI-powered trading bot** است که روی **futures trading** کار می‌کند.  
تو باید **test coverage را به 60%+ برسانی** (Sprint 2, Issue #13).  
راهنمای کامل: `AI_AGENT_WORKFLOW_GUIDE.md`

---

## 📖 Phase 0: Context Loading (10 دقیقه)

### Step 1: فهم پروژه در سطح بالا

**این پروژه چیست؟**

یک **Reinforcement Learning-powered trading strategy** برای **crypto futures** که:
- از **FreqAI** (machine learning framework for Freqtrade) استفاده می‌کند
- یک **governance system** برای risk management دارد
- در حال **افزودن RL layer** است برای self-learning

**معماری کلی:**
```
┌─────────────────────────────────────────────┐
│         Freqtrade Trading Bot               │
│                                             │
│  ┌───────────────────────────────────────┐ │
│  │  FreqAI (ML Framework)                │ │
│  │  ├─ LightGBM/CatBoost models          │ │
│  │  ├─ Feature engineering               │ │
│  │  └─ Prediction pipeline               │ │
│  └───────────────────────────────────────┘ │
│                                             │
│  ┌───────────────────────────────────────┐ │
│  │  FreqAIHybridStrategy (Main)          │ │
│  │  ├─ Entry/Exit logic                  │ │
│  │  ├─ Gating funnel (8 stages)          │ │
│  │  ├─ Regime detection                  │ │
│  │  └─ Position sizing                   │ │
│  └───────────────────────────────────────┘ │
│                                             │
│  ┌───────────────────────────────────────┐ │
│  │  Governance System (Risk Mgmt) ✅     │ │
│  │  ├─ Real-time risk monitoring         │ │
│  │  ├─ Drawdown protection               │ │
│  │  ├─ Position limits                   │ │
│  │  └─ Halt mechanism                    │ │
│  └───────────────────────────────────────┘ │
│                                             │
│  ┌───────────────────────────────────────┐ │
│  │  NEW: RL Layer (In Progress)          │ │
│  │  ├─ Contextual Bandit (Q1 2026)       │ │
│  │  ├─ Actor-Critic + PPO (Q2 2026)      │ │
│  │  └─ Production Deploy (Q3 2026)       │ │
│  └───────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

**Status فعلی:**
- ✅ **Sprint 1 Complete** (Oct 14-27):
  - Evaluation Protocol ✅
  - Signal Audit Diagnostics ✅
  - Code Baseline ✅
- ⏳ **Sprint 2 Active** (Oct 28 - Nov 10):
  - **Issue #13:** Test Coverage 60%+ ← **تو اینجا کار می‌کنی**
  - **Issue #14:** Documentation Update

---

### Step 2: خواندن راهنماها (ترتیب مهم است!)

**این فایل‌ها را به ترتیب بخوان:**

#### 1. **SETUP_COMPLETE_SUMMARY.md** (5 دقیقه) ✅ مهم
**چرا:** فهم سریع از وضعیت فعلی پروژه

```powershell
# Open in VS Code
code SETUP_COMPLETE_SUMMARY.md
```

**چه چیزی یاد می‌گیری:**
- ✅ Sprint 1 چه تحویل داد
- ✅ Sprint 2 چه می‌خواهد
- ✅ GitHub integration چطور کار می‌کند
- ✅ Token معتبر است

---

#### 2. **AI_AGENT_WORKFLOW_GUIDE.md** (15 دقیقه) ✅✅ خیلی مهم
**چرا:** این فایل **قلب سیستم** است - همه چیزی که نیاز داری اینجاست

```powershell
# Open in VS Code
code AI_AGENT_WORKFLOW_GUIDE.md
```

**چه چیزی یاد می‌گیری:**
- ✅ **Phase 1:** چطور task را بفهمی (Understanding)
- ✅ **Phase 2:** چطور plan کنی (Planning)
- ✅ **Phase 3:** چطور code بنویسی (Implementation)
- ✅ **Phase 4:** چطور quality check کنی (Quality)
- ✅ **Phase 5:** چطور PR ایجاد کنی (Pull Request)
- ✅ **Phase 6:** چطور merge کنی (Cleanup)
- ✅ **Example session:** یک workflow کامل از شروع تا پایان

**این فایل را با دقت بخوان - 80% سوالاتت را جواب می‌دهد!**

---

#### 3. **FUTURE_SPRINTS_ROADMAP.md** (5 دقیقه) ⚡ Context
**چرا:** فهم اینکه Sprint 2 در کل پروژه کجا قرار دارد

```powershell
code FUTURE_SPRINTS_ROADMAP.md
```

**چه چیزی یاد می‌گیری:**
- ✅ 16-sprint roadmap (Q4 2025 - Q3 2026)
- ✅ Sprint 2 details (Test Coverage + Docs)
- ✅ Next sprints (Contextual Bandit, Actor-Critic, Production)

---

#### 4. **Optional (فقط اگر نیاز بود):**

**GITHUB_PROJECT_MANAGEMENT.md** - معماری کامل سیستم (advanced)  
**BASELINE_METRICS.md** - وضعیت کد قبل از RL (reference)  
**SCRUM_FRAMEWORK.md** - فرآیند Scrum (process details)

---

### Step 3: بررسی Issue فعلی در GitHub

**Issue #13: Test Coverage 60%+**

```
1. Go to: https://github.com/aminak58/freqai-futures-strategy/issues/13

2. Read carefully:
   - User Story ← WHY we need this
   - Acceptance Criteria ← WHAT defines success
   - Technical Tasks ← WHAT to do
   - Definition of Done ← HOW to know it's complete
```

**نکته مهم:** همه چیزی که باید بکنی در issue نوشته شده است!

---

### Step 4: بررسی Codebase (Quick Tour)

```powershell
# See project structure
tree /F /A

# Key directories:
# - src/ ← Main source code
# - tests/ ← Tests (need expansion!)
# - user_data/strategies/ ← Trading strategy (main target for testing!)
# - diagnostics/ ← Diagnostics tools (Sprint 1)
# - monitoring/ ← Metrics extraction
# - scripts/ ← Automation scripts
```

**فایل‌های کلیدی برای Sprint 2:**

1. **`user_data/strategies/FreqAIHybridStrategy.py`** ← **MAIN TARGET**
   - Trading strategy logic
   - Entry/exit signals
   - **Needs 60%+ coverage!**

2. **`tests/test_strategy_logic.py`** ← **EXPAND THIS**
   - Current basic tests
   - Need more comprehensive tests

3. **`src/governance_system.py`**
   - Risk management
   - Should have good coverage already

4. **`src/evaluation_protocol.py`** (Sprint 1)
   - Already has 20 tests ✅

5. **`diagnostics/signal_audit.py`** (Sprint 1)
   - Already has 17 tests ✅

---

## 🚀 Phase 1: Environment Setup (5 دقیقه)

### Step 1: بررسی Environment

```powershell
# Check Python version
python --version
# Should be: Python 3.11.x

# Check if in venv
where python
# Should show: C:\freqai-futures-strategy\.venv\Scripts\python.exe

# If not in venv, activate:
.\.venv\Scripts\Activate.ps1
```

---

### Step 2: نصب Dependencies

```powershell
# Install/update dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Verify key packages
python -c "import pytest; import pandas; import numpy; print('✅ Core packages OK')"
python -c "from github import Github; print('✅ PyGithub OK')"
```

---

### Step 3: Run Tests (بررسی وضعیت فعلی)

```powershell
# Run all tests
pytest tests/ -v

# Check current coverage
pytest tests/ --cov=src --cov=diagnostics --cov=user_data/strategies --cov-report=term

# Expected: ~45% coverage
# Target: 60%+ coverage
```

**Output مهم:**
```
===== Coverage Report =====
src/                        XX%
diagnostics/                XX%
user_data/strategies/       XX%  ← Focus here!
===========================
TOTAL                      45%  ← Need to increase to 60%+
```

---

### Step 4: بررسی GitHub Token

```powershell
# Check if token is set
$env:GITHUB_TOKEN

# Test token validity
python -c "from github import Github; g = Github('$env:GITHUB_TOKEN'); print(f'✅ Token valid for: {g.get_user().login}')"

# Expected: ✅ Token valid for: aminak58
```

**اگر token نبود:** پیام بده، من token را می‌دهم.

---

## 🎯 Phase 2: First Task Execution (مثال عملی)

### مثال: شروع کار روی Issue #13 (Test Coverage)

#### Step 1: بررسی Sprint Progress

```powershell
python scripts/sprint_burndown.py --sprint 2
```

**Output:**
```
📊 Sprint 2 Burndown Report
====================================================
⏳ #13: [US 1.4] Test Coverage 60%+ (13 pts)
⏳ #14: [US 1.5] Documentation Update (5 pts)

Total: 18 pts | Remaining: 18 pts | Days: 27
====================================================
```

---

#### Step 2: فهم Strategy Code

```powershell
# Open main strategy file
code user_data/strategies/FreqAIHybridStrategy.py

# Read the code and understand:
# - What does populate_entry_trend() do?
# - What does populate_exit_trend() do?
# - What is the gating funnel?
# - How does governance integrate?
```

**سوالاتی که باید جواب بدی:**
- ✅ چه شرایطی باعث long entry می‌شود؟
- ✅ چه شرایطی باعث short entry می‌شود؟
- ✅ چه شرایطی باعث exit می‌شود؟
- ✅ گیتینگ فانل چیست و چطور کار می‌کند؟
- ✅ Governance چطور signals را block می‌کند؟

---

#### Step 3: شناسایی Test Gaps

```powershell
# Check current strategy tests
code tests/test_strategy_logic.py

# Run coverage for strategy only
pytest tests/test_strategy_logic.py --cov=user_data/strategies --cov-report=term

# Identify what's NOT tested:
# - Entry logic edge cases?
# - Exit logic edge cases?
# - Gating funnel stages?
# - Governance integration?
# - Regime detection?
```

**Example Test Gaps:**
```python
# Current: Basic test exists ✅
def test_populate_indicators():
    # ... basic test

# Missing:
# ❌ test_entry_with_all_signals_positive()
# ❌ test_entry_blocked_by_governance()
# ❌ test_entry_blocked_by_di_filter()
# ❌ test_entry_blocked_by_regime()
# ❌ test_exit_on_stop_loss()
# ❌ test_exit_on_take_profit()
# ❌ test_gating_funnel_stage_1()
# ❌ test_gating_funnel_stage_2()
# ... etc
```

---

#### Step 4: نوشتن اولین Test

```powershell
# Create/edit test file
code tests/test_strategy_entry.py
```

**Example Test:**
```python
import pytest
import pandas as pd
from user_data.strategies.FreqAIHybridStrategy import FreqAIHybridStrategy

@pytest.fixture
def strategy():
    """Fixture to create strategy instance"""
    config = {
        'stake_currency': 'USDT',
        'dry_run': True,
        # ... minimal config
    }
    return FreqAIHybridStrategy(config)

def test_populate_entry_trend_basic(strategy):
    """Test basic entry signal generation"""
    # Create test dataframe
    dataframe = pd.DataFrame({
        'date': pd.date_range('2025-01-01', periods=100, freq='5min'),
        'open': [100] * 100,
        'high': [101] * 100,
        'low': [99] * 100,
        'close': [100] * 100,
        'volume': [1000] * 100,
        # Add required indicators
        'DI_values': [26] * 100,  # Above threshold
        '&-s_close': [100] * 100,
        # ... other required columns
    })
    
    metadata = {'pair': 'BTC/USDT'}
    result = strategy.populate_entry_trend(dataframe, metadata)
    
    # Assertions
    assert 'enter_long' in result.columns
    assert 'enter_short' in result.columns
    assert result['enter_long'].dtype == 'int64'
    assert result['enter_short'].dtype == 'int64'
    # Check at least one entry signal exists (if conditions met)
    # ...

def test_entry_blocked_by_governance(strategy):
    """Test that entries are blocked when governance halts trading"""
    # Setup: Create scenario where governance should halt
    # ... setup dataframe with high risk conditions
    
    # Mock governance to return halt status
    # ... mock governance_system
    
    # Execute
    result = strategy.populate_entry_trend(dataframe, metadata)
    
    # Assert: No entries should be generated
    assert result['enter_long'].sum() == 0
    assert result['enter_short'].sum() == 0

# Add more tests...
```

---

#### Step 5: اجرای Test

```powershell
# Run single test
pytest tests/test_strategy_entry.py::test_populate_entry_trend_basic -v

# Run all new tests
pytest tests/test_strategy_entry.py -v

# Check coverage increase
pytest tests/ --cov=user_data/strategies --cov-report=term
```

**Expected:**
```
tests/test_strategy_entry.py::test_populate_entry_trend_basic PASSED
tests/test_strategy_entry.py::test_entry_blocked_by_governance PASSED

Coverage: 52% (+7% from 45%)
```

---

#### Step 6: Commit Progress

```powershell
git add tests/test_strategy_entry.py
git commit -m "[US 1.4] Add entry logic tests (coverage +7%)"
```

---

#### Step 7: تکرار تا رسیدن به 60%+

```
Repeat Steps 4-6:
1. نوشتن test جدید
2. اجرا و بررسی coverage
3. Commit
4. بررسی coverage کل
5. اگر < 60%, به Step 1 برگرد
6. اگر ≥ 60%, به Phase 3 برو
```

---

## 🎯 Phase 3: Quality & PR (آماده‌سازی برای Merge)

### Step 1: Final Quality Checks

```powershell
# 1. All tests pass
pytest tests/ -v
# Expected: All PASSED

# 2. Coverage meets target
pytest tests/ --cov=src --cov=diagnostics --cov=user_data/strategies --cov-report=html
# Expected: ≥ 60%
# Open: htmlcov/index.html to see details

# 3. Linting
flake8 src/ tests/ diagnostics/ user_data/ --max-line-length=120
# Expected: No errors

# 4. Format check
black tests/ --check
# Expected: All files formatted

# 5. Type check
mypy src/ --ignore-missing-imports
# Expected: No errors

# 6. Security scan
bandit -r src/ diagnostics/
# Expected: No high-severity issues
```

---

### Step 2: Create Branch & Push

```powershell
# Create branch (if not done already)
git checkout -b feature/us-1-4-test-coverage

# Add all test files
git add tests/

# Final commit
git commit -m "[US 1.4] Complete test coverage to 62% (target: 60%+)

- Added comprehensive tests for FreqAIHybridStrategy
- Tests for entry/exit logic
- Tests for gating funnel stages
- Tests for governance integration
- Tests for edge cases
- All 45 tests passing
- Coverage: 62% (up from 45%)

Closes #13"

# Push to GitHub
git push origin feature/us-1-4-test-coverage
```

---

### Step 3: Create Pull Request

```
1. Go to: https://github.com/aminak58/freqai-futures-strategy/pulls

2. Click "New Pull Request"

3. Base: master, Compare: feature/us-1-4-test-coverage

4. Title: [US 1.4] Increase test coverage to 60%+

5. Fill in PR template (auto-loads):
   - [x] All acceptance criteria met
   - [x] Coverage ≥ 60% (actual: 62%)
   - [x] All tests passing (45/45)
   - [x] Linting pass
   - [x] No security issues
   - Closes #13

6. Create Pull Request
```

---

### Step 4: Wait for CI & Merge

```
1. CI automatically runs 5 checks:
   ✅ lint
   ✅ security
   ✅ test
   ✅ coverage-check
   ✅ build

2. Wait ~5-10 minutes for all checks to pass

3. If all green ✅, click "Merge pull request"

4. Delete branch: feature/us-1-4-test-coverage

5. Update local:
   git checkout master
   git pull origin master
   git branch -d feature/us-1-4-test-coverage
```

---

### Step 5: Verify & Celebrate

```powershell
# Check sprint progress
python scripts/sprint_burndown.py --sprint 2

# Expected:
# ✅ #13: [US 1.4] Test Coverage 60%+ (13 pts) DONE
# ⏳ #14: [US 1.5] Documentation Update (5 pts)

# 🎉 Sprint 2: 13/18 points complete!
```

---

## 📚 Reference: Key Commands

### Git Workflow
```powershell
# Update master
git checkout master
git pull origin master

# Create feature branch
git checkout -b feature/us-X-Y-description

# Stage changes
git add .

# Commit with message
git commit -m "[US X.Y] Description"

# Push to GitHub
git push origin feature/us-X-Y-description

# After merge, cleanup
git checkout master
git pull origin master
git branch -d feature/us-X-Y-description
```

### Testing
```powershell
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_xyz.py -v

# Run specific test function
pytest tests/test_xyz.py::test_function -v

# Run with coverage
pytest tests/ --cov=src --cov=diagnostics --cov=user_data/strategies --cov-report=term

# Generate HTML coverage report
pytest tests/ --cov=src --cov=diagnostics --cov=user_data/strategies --cov-report=html
# Open: htmlcov/index.html
```

### Code Quality
```powershell
# Linting
flake8 src/ tests/ --max-line-length=120

# Format code
black src/ tests/

# Type checking
mypy src/ --ignore-missing-imports

# Security scan
bandit -r src/ diagnostics/
```

### Project Management
```powershell
# Sprint burndown
python scripts/sprint_burndown.py --sprint 2

# Team velocity
python scripts/velocity_tracking.py

# Create sprint issues (for future sprints)
python scripts/create_sprint_issues.py --sprint 3
```

---

## ❓ FAQ: سوالات متداول

### Q1: من از کجا شروع کنم؟
**A:** از `SETUP_COMPLETE_SUMMARY.md` شروع کن (5 دقیقه)، بعد `AI_AGENT_WORKFLOW_GUIDE.md` (15 دقیقه).

### Q2: چگونه بفهمم چه کاری باید انجام دهم؟
**A:** Issue #13 در GitHub را بخوان. همه چیز در Acceptance Criteria و Technical Tasks نوشته شده.

### Q3: Coverage فعلی چقدر است؟
**A:** ~45%. هدف: 60%+. چک کن با: `pytest tests/ --cov=... --cov-report=term`

### Q4: چگونه test بنویسم؟
**A:** نگاه کن به `tests/test_evaluation_protocol.py` (20 tests) یا `tests/test_signal_audit.py` (17 tests) به عنوان مثال.

### Q5: اگر test fail شد چه کنم؟
**A:** 
1. خواندن error message
2. اجرای test با `-v` برای جزئیات بیشتر
3. Debug با `--pdb`
4. Fix code یا test
5. Re-run

### Q6: اگر CI fail شد چه کنم؟
**A:**
1. Check GitHub PR > Checks tab
2. خواندن error log
3. Fix local
4. Commit + Push (CI re-runs auto)

### Q7: چگونه PR ایجاد کنم؟
**A:** `git push origin feature/...` سپس GitHub UI > New PR > Fill template

### Q8: Coverage target برای Sprint 2 چیست؟
**A:** 60%+. بعد از Sprint 2: 65%+, بعد از Sprint 8: 70%+, بعد از Sprint 13: 75%+

### Q9: من نمی‌دانم strategy چطور کار می‌کند!
**A:** نگرانی نداشته باش! تو فقط باید **test بنویسی**. Strategy را به عنوان black box ببین و behavior آن را test کن.

### Q10: چند test باید بنویسم؟
**A:** به اندازه‌ای که coverage از 45% به 60%+ برسد. احتمالاً 20-30 test.

---

## ✅ Checklist: آیا آماده شروع هستم؟

قبل از شروع کار، این موارد را چک کن:

### Phase 0: Context ✅
- [ ] خواندم: `SETUP_COMPLETE_SUMMARY.md` (5 min)
- [ ] خواندم: `AI_AGENT_WORKFLOW_GUIDE.md` (15 min)
- [ ] خواندم: Issue #13 در GitHub
- [ ] فهمیدم: پروژه چیست، Sprint 2 چه می‌خواهد

### Phase 1: Setup ✅
- [ ] Python 3.11 نصب است
- [ ] venv فعال است
- [ ] Dependencies نصب شد (`pip install -r requirements-dev.txt`)
- [ ] Tests اجرا می‌شود (`pytest tests/ -v`)
- [ ] Coverage فعلی 45% است
- [ ] GitHub token معتبر است

### Phase 2: Ready to Code ✅
- [ ] Strategy code را خواندم (`FreqAIHybridStrategy.py`)
- [ ] Test gaps را شناسایی کردم
- [ ] می‌دانم چه tests باید بنویسم
- [ ] Branch ایجاد کردم (`feature/us-1-4-test-coverage`)

اگر همه ✅ است، **آماده شروع کار هستی!** 🚀

---

## 🎬 مثال: یک Session کامل از صفر تا صد

```powershell
# ========================================
# PHASE 0: Context Loading (10 min)
# ========================================

# 1. Read documentation
code SETUP_COMPLETE_SUMMARY.md           # 5 min
code AI_AGENT_WORKFLOW_GUIDE.md          # 15 min

# 2. Check GitHub issue
# Browser: https://github.com/aminak58/freqai-futures-strategy/issues/13

# 3. Check sprint progress
python scripts/sprint_burndown.py --sprint 2

# ========================================
# PHASE 1: Environment Setup (5 min)
# ========================================

# 4. Verify environment
python --version                          # 3.11.x
where python                              # .venv\Scripts\python.exe

# 5. Install dependencies
pip install -r requirements-dev.txt

# 6. Run tests & check coverage
pytest tests/ -v                          # All pass?
pytest tests/ --cov=user_data/strategies --cov-report=term
# Result: 45% (need to reach 60%+)

# ========================================
# PHASE 2: Development (2-3 hours)
# ========================================

# 7. Create branch
git checkout master
git pull origin master
git checkout -b feature/us-1-4-test-coverage

# 8. Read strategy code
code user_data/strategies/FreqAIHybridStrategy.py

# 9. Write first test
code tests/test_strategy_entry.py
# ... write test_populate_entry_trend_basic() ...

# 10. Run test
pytest tests/test_strategy_entry.py -v
# ✅ PASSED

# 11. Check coverage
pytest tests/ --cov=user_data/strategies --cov-report=term
# 50% (+5%)

# 12. Commit
git add tests/test_strategy_entry.py
git commit -m "[US 1.4] Add entry logic tests (coverage +5%)"

# 13-20. Repeat: Write more tests
# test_entry_blocked_by_governance()
# test_entry_blocked_by_di()
# test_exit_on_stop_loss()
# ... continue until coverage ≥ 60% ...

# 21. Final coverage check
pytest tests/ --cov=src --cov=diagnostics --cov=user_data/strategies --cov-report=html
# Result: 62% ✅ TARGET MET!

# ========================================
# PHASE 3: Quality & PR (30 min)
# ========================================

# 22. Quality checks
pytest tests/ -v                          # All pass?
flake8 tests/ --max-line-length=120       # No errors?
black tests/ --check                      # Formatted?

# 23. Final commit
git add tests/
git commit -m "[US 1.4] Complete test coverage to 62%

- Added 25 new tests for FreqAIHybridStrategy
- Coverage increased from 45% to 62%
- All 42 tests passing

Closes #13"

# 24. Push
git push origin feature/us-1-4-test-coverage

# 25. Create PR
# Browser: GitHub > New PR > Fill template > Create

# 26. Wait for CI (5-10 min)
# All 5 checks pass ✅

# 27. Merge PR
# Browser: Merge pull request > Confirm

# 28. Cleanup
git checkout master
git pull origin master
git branch -d feature/us-1-4-test-coverage

# 29. Verify
python scripts/sprint_burndown.py --sprint 2
# ✅ #13 DONE! 13/18 points complete

# 🎉 SUCCESS! Sprint 2 is 72% complete!
```

---

## 🚀 تو الان کجایی؟

### اگر تازه شروع کردی:
👉 **Start:** `SETUP_COMPLETE_SUMMARY.md` (5 دقیقه)

### اگر context را خواندی:
👉 **Next:** Setup environment, run tests, check coverage

### اگر environment آماده است:
👉 **Next:** Read strategy code, identify test gaps, write first test

### اگر tests را شروع کردی:
👉 **Next:** Continue until coverage ≥ 60%, then create PR

### اگر PR ایجاد کردی:
👉 **Next:** Wait for CI, merge, celebrate! 🎉

---

## 📞 Need Help?

### Documentation:
- **Quick Start:** این فایل (`AI_AGENT_ONBOARDING_GUIDE.md`)
- **Detailed Workflow:** `AI_AGENT_WORKFLOW_GUIDE.md`
- **System Architecture:** `GITHUB_PROJECT_MANAGEMENT.md`
- **Sprint Roadmap:** `FUTURE_SPRINTS_ROADMAP.md`

### Common Issues:
- **Tests failing?** Check error message, read `AI_AGENT_WORKFLOW_GUIDE.md` FAQ
- **Coverage not increasing?** Write more tests, check what's not covered
- **CI failing?** Check GitHub PR > Checks tab, read error logs
- **Don't understand strategy?** That's OK! Test behavior, not implementation

### Tools:
```powershell
# Sprint progress
python scripts/sprint_burndown.py --sprint 2

# Coverage report
pytest tests/ --cov=... --cov-report=html

# Run specific test
pytest tests/test_xyz.py::test_function -v
```

---

## 🎯 تو الان چه می‌دانی؟

بعد از خواندن این فایل، تو باید بدانی:

✅ **Context:** این پروژه چیست (AI trading bot با RL)  
✅ **Status:** Sprint 1 complete, Sprint 2 active  
✅ **Task:** Test coverage از 45% به 60%+  
✅ **How:** نوشتن tests برای `FreqAIHybridStrategy`  
✅ **Workflow:** Phase 0 → 1 → 2 → 3 (Context → Setup → Dev → PR)  
✅ **Tools:** pytest, git, GitHub issues, CI/CD  
✅ **Success:** Coverage ≥ 60%, all tests pass, PR merged  

---

**تو الان 100% آماده‌ای! شروع کن!** 🚀

**First command:** `code SETUP_COMPLETE_SUMMARY.md`  
**Then:** Follow Phase 0 → Phase 1 → Phase 2 → Phase 3  
**Result:** Sprint 2 Issue #13 ✅ DONE!

**Good luck! You got this! 🎉**
