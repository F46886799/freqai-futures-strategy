# AI Agent Workflow Guide

**مخاطب:** AI Coding Agents (Claude, GPT, Copilot, etc.)  
**تاریخ:** 13 اکتبر 2025  
**هدف:** راهنمای گام‌به‌گام برای کار با GitHub Project Management System

---

## 🎯 خلاصه یک‌خطی

این پروژه یک **RL-powered trading strategy** است که از **GitHub Issues برای tracking** و **CI/CD برای enforcement** استفاده می‌کند.

---

## 📋 Context: پروژه چیست؟

### هدف نهایی
ایجاد یک **self-learning AI trader** برای فیوچرز که با **Reinforcement Learning** بهتر می‌شود.

### معماری فعلی
```
FreqAI Strategy (baseline)
  ├─ LightGBM/CatBoost models
  ├─ Governance system (risk management)
  ├─ Signal audit (diagnostics)
  └─ Evaluation protocol (validation)

Next: Add RL layer on top ↑
```

### Timeline
- **Q4 2025:** Foundation (Sprint 1-2) ✅ Sprint 1 done
- **Q1 2026:** Contextual Bandit (Sprint 3-7)
- **Q2 2026:** Actor-Critic + PPO (Sprint 8-12)
- **Q3 2026:** Production Deployment (Sprint 13-16)

---

## 🔄 Workflow: چطور کار کنیم؟

### Phase 1: فهم Task (Understanding)

#### 1.1 چک کردن Sprint فعلی
```powershell
# بررسی Sprint 2 issues
python scripts/sprint_burndown.py --sprint 2
```

**Output مورد انتظار:**
```
📊 Sprint 2 Burndown Report
====================================================================
Milestone: Sprint 2
Due Date: 2025-11-10
Total Issues: 2

⏳ #XX: [US 1.4] Increase Test Coverage to 60%+ (13 pts)
⏳ #YY: [US 1.5] Documentation Update (5 pts)

====================================================================
📈 Total Story Points: 18
✅ Completed: 0 (0.0%)
🔄 In Progress: 0 (0.0%)
⏳ Remaining: 18 (100.0%)
📅 Days Remaining: 28
🔥 Required Burn Rate: 0.6 pts/day
====================================================================
```

#### 1.2 خواندن Issue مربوطه در GitHub
- Go to: https://github.com/aminak58/freqai-futures-strategy/issues
- Open issue (e.g., #XX for US 1.4)
- Read:
  - **Acceptance Criteria** ← چه چیزی باید تحویل شود
  - **Technical Tasks** ← چه کارهایی باید انجام شود
  - **Definition of Done** ← چطور می‌فهمیم تمام شده

#### 1.3 فهم Context کد فعلی
```powershell
# ساختار پروژه را ببین
tree /F /A

# Coverage فعلی
pytest tests/ --cov=src --cov=diagnostics --cov=monitoring --cov-report=term

# کدهای موجود را بخوان
# src/evaluation_protocol.py - تازه اضافه شده در Sprint 1
# diagnostics/signal_audit.py - تازه اضافه شده در Sprint 1
# user_data/strategies/FreqAIHybridStrategy.py - strategy اصلی (نیاز به test!)
```

---

### Phase 2: برنامه‌ریزی (Planning)

#### 2.1 شکستن Task به Sub-tasks
برای US 1.4 (Test Coverage 60%+):

```markdown
Sub-tasks:
1. ✅ فهم strategy کد (FreqAIHybridStrategy.py)
2. ✅ شناسایی critical paths (entry/exit logic, gating funnel, governance)
3. ✅ نوشتن test برای entry logic
4. ✅ نوشتن test برای exit logic
5. ✅ نوشتن test برای gating funnel
6. ✅ نوشتن test برای governance integration
7. ✅ نوشتن test برای regime detection
8. ✅ نوشتن edge case tests
9. ✅ نوشتن integration tests
10. ✅ اجرا و رفع باگ‌ها
11. ✅ بررسی coverage (باید ≥ 60%)
12. ✅ Commit + Push + PR
```

#### 2.2 تخمین زمان
- **US 1.4:** 13 story points ≈ 10-12 روز
- **US 1.5:** 5 story points ≈ 3-4 روز
- **Total Sprint 2:** 18 points ≈ 2 هفته

---

### Phase 3: Implementation (اجرا)

#### 3.1 ایجاد Branch
```powershell
# Update master
git checkout master
git pull origin master

# Create feature branch
git checkout -b feature/us-1-4-test-coverage
```

#### 3.2 نوشتن Code + Tests
**قانون طلایی:** همیشه test قبل از code یا همزمان با code!

```powershell
# Example: Testing strategy entry logic
# File: tests/test_strategy_entry.py

import pytest
from user_data.strategies.FreqAIHybridStrategy import FreqAIHybridStrategy

def test_populate_entry_trend_basic():
    """Test basic entry signal generation"""
    strategy = FreqAIHybridStrategy()
    dataframe = create_test_dataframe()  # helper
    
    result = strategy.populate_entry_trend(dataframe, metadata={'pair': 'BTC/USDT'})
    
    assert 'enter_long' in result.columns
    assert 'enter_short' in result.columns
    assert result['enter_long'].sum() >= 0
    # ... more assertions

def test_entry_with_governance_halt():
    """Test that entries are blocked when governance halts"""
    strategy = FreqAIHybridStrategy()
    # ... setup governance halt scenario
    # ... assert no entries
```

#### 3.3 اجرای Tests به صورت مداوم
```powershell
# Run specific test file
pytest tests/test_strategy_entry.py -v

# Run all tests with coverage
pytest tests/ --cov=src --cov=diagnostics --cov=user_data/strategies --cov-report=term

# Check if coverage meets target
# Target for Sprint 2: 60%
```

#### 3.4 Commit Changes (به صورت تدریجی)
```powershell
# Commit each logical unit
git add tests/test_strategy_entry.py
git commit -m "[US 1.4] Add entry logic tests (coverage +5%)"

git add tests/test_strategy_exit.py
git commit -m "[US 1.4] Add exit logic tests (coverage +4%)"

# ... continue until all tests written
```

---

### Phase 4: Quality Check (کیفیت)

#### 4.1 Local Testing
```powershell
# 1. Run all tests
pytest tests/ -v

# 2. Check coverage
pytest tests/ --cov=src --cov=diagnostics --cov=user_data/strategies --cov-report=html
# Open: htmlcov/index.html in browser

# 3. Linting
flake8 src/ tests/ diagnostics/ --max-line-length=120
black src/ tests/ diagnostics/

# 4. Type checking
mypy src/ --ignore-missing-imports

# 5. Security scan
bandit -r src/ diagnostics/
```

#### 4.2 بررسی Acceptance Criteria
بازگشت به issue در GitHub و چک کردن:
- [ ] Overall coverage ≥ 60%? ← **CHECK!**
- [ ] Strategy coverage ≥ 60%? ← **CHECK!**
- [ ] All critical paths tested? ← **CHECK!**
- [ ] All tests passing? ← **CHECK!**

---

### Phase 5: Pull Request (PR)

#### 5.1 Push Branch
```powershell
git push origin feature/us-1-4-test-coverage
```

#### 5.2 Create PR در GitHub
1. Go to: https://github.com/aminak58/freqai-futures-strategy/pulls
2. Click "New pull request"
3. Base: `master`, Compare: `feature/us-1-4-test-coverage`
4. Title: `[US 1.4] Increase test coverage to 60%+`
5. Body: Use PR template (auto-filled), complete checklist:

```markdown
## Description
Added comprehensive tests for FreqAIHybridStrategy covering entry/exit logic, 
gating funnel, governance integration, and edge cases.

## Related Issue
Closes #XX

## Type of Change
- [x] New feature (tests)
- [ ] Bug fix
- [ ] Breaking change

## Sprint
**Sprint:** Sprint 2
**Epic:** Epic 1 - Foundation
**Story Points:** 13

## Checklist

### Code Quality
- [x] Code follows project style guidelines
- [x] Self-review completed
- [x] Comments added for complex logic
- [x] No unnecessary code or files

### Testing
- [x] Unit tests added/updated
- [x] All tests passing locally (37/37 ✅)
- [x] Coverage meets sprint target (≥ 60%, actual: 62%)
- [x] Edge cases covered
- [x] Integration tests added

### Documentation
- [x] Code docstrings updated
- [x] README updated (N/A)
- [x] Architecture docs updated (N/A)
- [x] CHANGELOG updated

### CI/CD
- [ ] All CI checks passing (will check after push)
- [x] No merge conflicts
- [x] Branch up-to-date with base

### Security
- [x] No sensitive data exposed
- [x] No security vulnerabilities introduced
- [x] Dependencies updated (N/A)

### Review
- [x] Ready for review
- [x] Assigned reviewers (self-review for solo dev)
- [x] Linked to issue/milestone
```

6. Create pull request

#### 5.3 Wait for CI Checks
CI will automatically run:
- ✅ **lint** - Code style check
- ✅ **security** - Bandit scan
- ✅ **test** - All tests
- ✅ **coverage-check** - Enforce 60%+ coverage
- ✅ **build** - Import validation

**Expected:** همه 5 check باید pass شوند ✅

#### 5.4 اگر CI Fail شد
```powershell
# Pull latest changes
git pull origin feature/us-1-4-test-coverage

# Fix issues locally
# ... fix code ...

# Re-test
pytest tests/ -v
flake8 src/ tests/

# Commit fix
git add .
git commit -m "[US 1.4] Fix linting issues"
git push origin feature/us-1-4-test-coverage

# CI will re-run automatically
```

---

### Phase 6: Merge & Cleanup

#### 6.1 Merge PR
- After all CI checks pass ✅
- Click "Merge pull request" در GitHub
- Confirm merge
- Delete branch: `feature/us-1-4-test-coverage`

#### 6.2 Update Local
```powershell
git checkout master
git pull origin master
git branch -d feature/us-1-4-test-coverage
```

#### 6.3 Update Issue
- GitHub automatically closes issue when PR merges (if "Closes #XX" in PR body)
- Verify issue is closed: https://github.com/aminak58/freqai-futures-strategy/issues

#### 6.4 Check Progress
```powershell
# Sprint 2 progress
python scripts/sprint_burndown.py --sprint 2

# Team velocity
python scripts/velocity_tracking.py
```

---

## 🤖 AI Agent Guidelines

### برای Claude/GPT/Copilot:

#### **چه وقت از کدام tool استفاده کنی:**

1. **فهم پروژه:**
   - `read_file` → خواندن strategy, tests, docs
   - `grep_search` → جستجو در codebase
   - `semantic_search` → یافتن related code

2. **نوشتن Code:**
   - `create_file` → تست جدید
   - `replace_string_in_file` → اصلاح test موجود
   - `run_in_terminal` → اجرای pytest

3. **Quality Check:**
   - `run_in_terminal` → pytest, flake8, black, mypy
   - `get_errors` → دیدن errors در VS Code

4. **Git:**
   - `run_in_terminal` → git add, commit, push
   - نکته: همیشه **descriptive commit messages**

#### **Best Practices:**

1. **Test Coverage:**
   - هر function public باید test داشته باشد
   - Edge cases را test کن (empty, null, extreme values)
   - Integration tests برای critical flows

2. **Code Quality:**
   - Follow PEP 8
   - Type hints برای functions
   - Docstrings برای classes/functions
   - Comments برای logic پیچیده

3. **Git Workflow:**
   - Branch naming: `feature/us-X-Y-description`
   - Commit messages: `[US X.Y] Description`
   - Small, frequent commits
   - Always pull before push

4. **CI/CD:**
   - همیشه local test قبل از push
   - اگر CI fail شد، سریع fix کن
   - Coverage باید ≥ target باشد

---

## 📚 Key Files (مهم‌ترین فایل‌ها)

### Documentation
- `GITHUB_SETUP_GUIDE.md` ← راهنمای setup اولیه
- `GITHUB_PROJECT_MANAGEMENT.md` ← معماری کامل سیستم
- `FUTURE_SPRINTS_ROADMAP.md` ← نقشه 16 اسپرینت
- `SCRUM_FRAMEWORK.md` ← فرآیند Scrum
- **این فایل:** `AI_AGENT_WORKFLOW_GUIDE.md` ← راهنمای گام‌به‌گام

### Source Code
- `src/evaluation_protocol.py` ← validation methods (Sprint 1)
- `diagnostics/signal_audit.py` ← gating funnel tracker (Sprint 1)
- `user_data/strategies/FreqAIHybridStrategy.py` ← main strategy
- `src/governance_system.py` ← risk management
- `monitoring/` ← metrics extraction

### Tests
- `tests/test_evaluation_protocol.py` ← 20 tests (Sprint 1)
- `tests/test_signal_audit.py` ← 17 tests (Sprint 1)
- `tests/test_strategy_logic.py` ← strategy tests (needs expansion!)
- `tests/test_integration.py` ← integration tests (needs expansion!)

### Configuration
- `.github/workflows/ci.yml` ← CI/CD pipeline
- `.github/ISSUE_TEMPLATE/` ← issue templates
- `.github/PULL_REQUEST_TEMPLATE.md` ← PR template
- `requirements.txt` ← production dependencies
- `requirements-dev.txt` ← development dependencies

### Scripts
- `scripts/create_milestones.py` ← ایجاد milestones
- `scripts/create_sprint_issues.py` ← ایجاد issues
- `scripts/sprint_burndown.py` ← گزارش پیشرفت
- `scripts/velocity_tracking.py` ← سرعت تیم

---

## 🎯 Sprint 2 Focus (فعلی)

### US 1.4: Test Coverage 60%+ (13 pts, P1) 🔴

**هدف:** افزایش coverage از 45% به 60%+

**Files to Test:**
1. `user_data/strategies/FreqAIHybridStrategy.py` (main priority!)
   - `populate_entry_trend()`
   - `populate_exit_trend()`
   - Gating funnel integration
   - Governance integration
   - Regime detection

2. `src/governance_system.py` (if not already 80%+)
   - Risk calculations
   - Halt logic
   - Position sizing

3. Integration tests:
   - Full backtest workflow
   - FreqAI pipeline
   - Governance runtime

**Acceptance Criteria:**
- [ ] Coverage ≥ 60% overall
- [ ] Strategy coverage ≥ 60%
- [ ] All critical paths tested
- [ ] All tests passing

### US 1.5: Documentation Update (5 pts, P2) 🟡

**هدف:** همگام‌سازی docs با Sprint 1 changes

**Files to Update:**
1. `README.md` - Add Sprint 1 achievements
2. `UNIFIED_ARCHITECTURE.md` - Add evaluation protocol, signal audit
3. `CI_CD_GUIDE.md` - Add new CI/CD workflow
4. Create `RL_INTEGRATION_PLAN.md` - Plan for Sprints 3-16
5. Fix broken links

**Acceptance Criteria:**
- [ ] All docs updated
- [ ] No broken links
- [ ] RL roadmap documented

---

## ❓ FAQ برای AI Agents

### Q1: چگونه بفهمم issue بعدی چیست؟
```powershell
python scripts/sprint_burndown.py --sprint 2
# یا
# GitHub > Issues > Filter by "sprint-2" label
```

### Q2: چگونه بفهمم coverage فعلی چقدر است؟
```powershell
pytest tests/ --cov=src --cov=diagnostics --cov=user_data/strategies --cov-report=term
```

### Q3: اگر test fail شد چه کنم؟
1. خواندن error message
2. اجرای test به صورت مجزا: `pytest tests/test_xyz.py::test_function -v`
3. Debug با pdb: `pytest tests/test_xyz.py::test_function --pdb`
4. Fix code یا test
5. Re-run

### Q4: اگر CI fail شد چه کنم؟
1. چک کردن GitHub PR > Checks tab
2. خواندن error log
3. Fix local: `flake8`, `black`, `pytest`
4. Commit + Push (CI re-runs automatically)

### Q5: چگونه PR ایجاد کنم؟
```powershell
git push origin feature/us-X-Y-description
# سپس GitHub UI > New Pull Request
# Fill in template
```

### Q6: چگونه branch protection را bypass کنم؟
**جواب:** نمی‌توانی! (و نباید!) Branch protection برای quality است.
اگر CI fail می‌کند، باید fix کنی.

### Q7: چگونه issue جدید ایجاد کنم (برای Sprint 3+)?
```python
# Edit scripts/create_sprint_issues.py
# Add Sprint 3 stories to SPRINT_STORIES dict
python scripts/create_sprint_issues.py --sprint 3
```

### Q8: Coverage target برای هر sprint چقدر است؟
- Sprint 1: Baseline (45%)
- Sprint 2: 60%+ ← **فعلی**
- Sprint 3+: 65%+
- Sprint 8+: 70%+
- Sprint 13+: 75%+ (production)

---

## ✅ Checklist: آیا من (AI Agent) آماده‌ام؟

قبل از شروع کار، این موارد را بررسی کن:

- [ ] خواندم: `GITHUB_SETUP_GUIDE.md`
- [ ] خواندم: `FUTURE_SPRINTS_ROADMAP.md`
- [ ] خواندم: این فایل (`AI_AGENT_WORKFLOW_GUIDE.md`)
- [ ] فهمیدم: Sprint 2 چه می‌خواهد (US 1.4 + US 1.5)
- [ ] می‌دانم: چگونه branch بسازم
- [ ] می‌دانم: چگونه test بنویسم
- [ ] می‌دانم: چگونه coverage بررسی کنم
- [ ] می‌دانم: چگونه PR ایجاد کنم
- [ ] می‌دانم: چگونه CI checks را بررسی کنم

اگر همه ✅ است، **آماده شروع کار هستی!** 🚀

---

## 🎬 مثال: یک Session کامل

```powershell
# 1. Check current sprint
python scripts/sprint_burndown.py --sprint 2

# 2. Read issue in GitHub
# https://github.com/aminak58/freqai-futures-strategy/issues/XX

# 3. Create branch
git checkout master
git pull origin master
git checkout -b feature/us-1-4-test-coverage

# 4. Check current coverage
pytest tests/ --cov=src --cov=user_data/strategies --cov-report=term
# Result: 45%

# 5. Read strategy code
# VS Code: Open user_data/strategies/FreqAIHybridStrategy.py

# 6. Write first test
# VS Code: Create tests/test_strategy_entry.py
# ... write tests ...

# 7. Run test
pytest tests/test_strategy_entry.py -v
# ✅ All pass

# 8. Check coverage increase
pytest tests/ --cov=src --cov=user_data/strategies --cov-report=term
# Result: 50% (+5%)

# 9. Commit
git add tests/test_strategy_entry.py
git commit -m "[US 1.4] Add entry logic tests (coverage +5%)"

# 10. Continue until coverage ≥ 60%
# ... write more tests ...

# 11. Final check
pytest tests/ -v --cov=src --cov=user_data/strategies --cov-report=html
# Result: 62% ✅

# 12. Linting
black tests/
flake8 tests/ --max-line-length=120

# 13. Push
git push origin feature/us-1-4-test-coverage

# 14. Create PR in GitHub UI
# Fill in template, link issue

# 15. Wait for CI
# ✅ All 5 checks pass

# 16. Merge PR

# 17. Update local
git checkout master
git pull origin master
git branch -d feature/us-1-4-test-coverage

# 18. Celebrate! 🎉
python scripts/sprint_burndown.py --sprint 2
# US 1.4: ✅ DONE!
```

---

## 🔚 خلاصه برای AI Agents

این پروژه یک **workflow واضح و enforceable** دارد:

1. **Issues** = Tasks (با acceptance criteria واضح)
2. **Branches** = Feature development (isolated work)
3. **Tests** = Quality gate (coverage ≥ target)
4. **CI/CD** = Automated validation (5 checks must pass)
5. **PR** = Code review + merge (with template checklist)
6. **Metrics** = Progress tracking (burndown, velocity)

**قانون طلایی:** 
- همیشه test بنویس
- همیشه CI را pass کن
- همیشه docs را update کن
- همیشه commit message واضح بنویس

**تو به عنوان AI agent:**
- Task را بفهم (read issue)
- Code بنویس (with tests!)
- Quality را check کن (local testing)
- PR ایجاد کن (with template)
- CI را monitor کن (fix if fails)
- Merge کن (celebrate! 🎉)

**این workflow برای solo developer + AI agents بهینه شده است!** 🤖✨

---

**سوال داری؟** این فایل را بخوان: `GITHUB_PROJECT_MANAGEMENT.md` (جزئیات بیشتر)

**آماده شروع؟** `python scripts/sprint_burndown.py --sprint 2` را اجرا کن!

**Go build something awesome! 🚀**
