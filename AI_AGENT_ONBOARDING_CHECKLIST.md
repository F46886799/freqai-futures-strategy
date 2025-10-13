# AI Agent Onboarding Checklist

**نام AI Agent:** _____________  
**تاریخ شروع:** _____________  
**Sprint:** Sprint 2  
**Issue:** #13 - Test Coverage 60%+

---

## 📋 Phase 0: Context Loading (30 دقیقه)

### Documentation Review
- [ ] خواندم: `AI_AGENT_QUICK_START.md` (5 دقیقه) ← **شروع از اینجا**
- [ ] خواندم: `SETUP_COMPLETE_SUMMARY.md` (5 دقیقه)
- [ ] خواندم: `AI_AGENT_WORKFLOW_GUIDE.md` (20 دقیقه)
- [ ] فهمیدم: پروژه چیست (AI trading bot با RL)
- [ ] فهمیدم: Sprint 1 چه تحویل داد (Evaluation Protocol, Signal Audit, Baseline)
- [ ] فهمیدم: Sprint 2 چه می‌خواهد (Test Coverage 60%+, Documentation)

### GitHub Review
- [ ] رفتم به: https://github.com/aminak58/freqai-futures-strategy
- [ ] دیدم: Repository structure
- [ ] خواندم: Issue #13 - [US 1.4] Test Coverage 60%+
- [ ] فهمیدم: Acceptance Criteria (Coverage ≥ 60%, All tests pass, etc.)
- [ ] فهمیدم: Technical Tasks (test strategy, gating funnel, governance, etc.)
- [ ] فهمیدم: Definition of Done (checklist برای تکمیل)

### Codebase Tour
- [ ] اجرا کردم: `tree /F /A` برای دیدن structure
- [ ] دیدم: `src/` - source code
- [ ] دیدم: `tests/` - tests (باید expand شود!)
- [ ] دیدم: `user_data/strategies/FreqAIHybridStrategy.py` - **MAIN TARGET**
- [ ] دیدم: `diagnostics/` - Sprint 1 deliverables
- [ ] دیدم: `scripts/` - automation tools

---

## 🔧 Phase 1: Environment Setup (10 دقیقه)

### Python Environment
- [ ] چک کردم: `python --version` (باید 3.11.x باشد)
- [ ] چک کردم: `where python` (باید در `.venv` باشد)
- [ ] اگر لازم بود: فعال کردم venv با `.\.venv\Scripts\Activate.ps1`

### Dependencies
- [ ] نصب کردم: `pip install -r requirements.txt`
- [ ] نصب کردم: `pip install -r requirements-dev.txt`
- [ ] تست کردم: `python -c "import pytest; print('✅ OK')"`
- [ ] تست کردم: `python -c "from github import Github; print('✅ OK')"`

### Initial Tests
- [ ] اجرا کردم: `pytest tests/ -v`
- [ ] نتیجه: همه tests pass شدند ✅
- [ ] تعداد tests: _____ tests

### Current Coverage
- [ ] اجرا کردم: `pytest tests/ --cov=src --cov=diagnostics --cov=user_data/strategies --cov-report=term`
- [ ] Coverage کل: _____% (انتظار: ~45%)
- [ ] Coverage strategy: _____% (target: 60%+)
- [ ] Gap: _____% (باید این مقدار را پر کنیم)

### GitHub Token
- [ ] چک کردم: `$env:GITHUB_TOKEN` (باید set شده باشد)
- [ ] تست کردم: `python -c "from github import Github; g = Github('$env:GITHUB_TOKEN'); print(g.get_user().login)"`
- [ ] نتیجه: `aminak58` ✅

### Sprint Status
- [ ] اجرا کردم: `python scripts/sprint_burndown.py --sprint 2`
- [ ] دیدم: Issue #13 (13 pts), Issue #14 (5 pts)
- [ ] Total: 18 story points
- [ ] Remaining: _____ points
- [ ] Days remaining: _____ days

---

## 💻 Phase 2: Development (2-3 ساعت)

### Git Branch
- [ ] ایجاد کردم: `git checkout -b feature/us-1-4-test-coverage`
- [ ] چک کردم: `git status` (باید روی branch جدید باشم)

### Code Understanding
- [ ] خواندم: `user_data/strategies/FreqAIHybridStrategy.py`
- [ ] فهمیدم: `populate_entry_trend()` چه می‌کند
- [ ] فهمیدم: `populate_exit_trend()` چه می‌کند
- [ ] فهمیدم: Gating funnel چیست (8 stages)
- [ ] فهمیدم: Governance integration چطور کار می‌کند
- [ ] فهمیدم: Regime detection چیست

### Test Gap Analysis
- [ ] خواندم: `tests/test_strategy_logic.py` (current tests)
- [ ] اجرا کردم: `pytest tests/test_strategy_logic.py --cov=user_data/strategies --cov-report=term`
- [ ] Current coverage: _____%
- [ ] شناسایی کردم: چه چیزی test نشده است
  - [ ] Entry logic edge cases?
  - [ ] Exit logic edge cases?
  - [ ] Gating funnel stages?
  - [ ] Governance integration?
  - [ ] Regime detection?
  - [ ] Error handling?

### Test Writing (تکرار برای هر test)

#### Test #1: _________________________
- [ ] نوشتم: test در `tests/test_strategy_XXX.py`
- [ ] اجرا کردم: `pytest tests/test_strategy_XXX.py::test_YYY -v`
- [ ] نتیجه: PASSED ✅
- [ ] Coverage بعد: _____%
- [ ] Commit: `git commit -m "[US 1.4] Add test_YYY (coverage +__%)"`

#### Test #2: _________________________
- [ ] نوشتم: test در `tests/test_strategy_XXX.py`
- [ ] اجرا کردم: `pytest tests/test_strategy_XXX.py::test_YYY -v`
- [ ] نتیجه: PASSED ✅
- [ ] Coverage بعد: _____%
- [ ] Commit: `git commit -m "[US 1.4] Add test_YYY (coverage +__%)"`

#### Test #3: _________________________
- [ ] نوشتم: test در `tests/test_strategy_XXX.py`
- [ ] اجرا کردم: `pytest tests/test_strategy_XXX.py::test_YYY -v`
- [ ] نتیجه: PASSED ✅
- [ ] Coverage بعد: _____%
- [ ] Commit: `git commit -m "[US 1.4] Add test_YYY (coverage +__%)"`

_[Add more test sections as needed until coverage ≥ 60%]_

### Coverage Target Met
- [ ] اجرا کردم: `pytest tests/ --cov=src --cov=diagnostics --cov=user_data/strategies --cov-report=html`
- [ ] Coverage کل: _____%
- [ ] Coverage strategy: _____%
- [ ] ✅ Coverage ≥ 60%? (YES / NO)
- [ ] دیدم: `htmlcov/index.html` برای جزئیات

---

## ✅ Phase 3: Quality & PR (30 دقیقه)

### Quality Checks

#### All Tests Pass
- [ ] اجرا کردم: `pytest tests/ -v`
- [ ] نتیجه: _____/_____  tests passed
- [ ] ✅ All tests passing?

#### Coverage Report
- [ ] اجرا کردم: `pytest tests/ --cov=src --cov=diagnostics --cov=user_data/strategies --cov-report=term`
- [ ] Coverage: _____%
- [ ] ✅ Coverage ≥ 60%?

#### Linting
- [ ] اجرا کردم: `flake8 tests/ --max-line-length=120`
- [ ] نتیجه: _____ errors
- [ ] ✅ No linting errors?

#### Code Format
- [ ] اجرا کردم: `black tests/ --check`
- [ ] نتیجه: _____ files would be reformatted
- [ ] اگر نیاز بود: `black tests/` برای format
- [ ] ✅ All files formatted?

#### Type Checking
- [ ] اجرا کردم: `mypy src/ --ignore-missing-imports`
- [ ] نتیجه: _____ errors
- [ ] ✅ No type errors?

#### Security Scan
- [ ] اجرا کردم: `bandit -r src/ diagnostics/`
- [ ] نتیجه: _____ issues
- [ ] ✅ No high-severity issues?

### Git Push

#### Final Commit
- [ ] اجرا کردم: `git add tests/`
- [ ] اجرا کردم: `git status` (چک کردم changes)
- [ ] Commit با message مناسب:
  ```
  git commit -m "[US 1.4] Complete test coverage to ___%

  - Added __ tests for FreqAIHybridStrategy
  - Tests for entry/exit logic
  - Tests for gating funnel
  - Tests for governance integration
  - Tests for edge cases
  - All __ tests passing
  - Coverage: __% (up from 45%)

  Closes #13"
  ```

#### Push Branch
- [ ] اجرا کردم: `git push origin feature/us-1-4-test-coverage`
- [ ] نتیجه: Successfully pushed ✅

### Pull Request

#### Create PR
- [ ] رفتم به: https://github.com/aminak58/freqai-futures-strategy/pulls
- [ ] کلیک کردم: "New Pull Request"
- [ ] انتخاب کردم: Base: `master`, Compare: `feature/us-1-4-test-coverage`
- [ ] Title: `[US 1.4] Increase test coverage to 60%+`
- [ ] Fill in PR template:
  - [ ] Description completed
  - [ ] Type of change checked
  - [ ] Sprint info filled
  - [ ] Code quality checklist completed
  - [ ] Testing checklist completed
  - [ ] Documentation checklist completed
  - [ ] CI/CD checklist completed
  - [ ] Security checklist completed
  - [ ] Review checklist completed
  - [ ] Added: `Closes #13`
- [ ] کلیک کردم: "Create Pull Request"

#### CI Checks (Wait 5-10 min)
- [ ] Check 1: `lint` - Status: _______
- [ ] Check 2: `security` - Status: _______
- [ ] Check 3: `test` - Status: _______
- [ ] Check 4: `coverage-check` - Status: _______
- [ ] Check 5: `build` - Status: _______
- [ ] ✅ All checks passing?

#### Handle CI Failures (if any)
- [ ] خواندم: Error logs در GitHub PR > Checks tab
- [ ] Fix کردم: Local issues
- [ ] Commit + Push: Changes
- [ ] منتظر ماندم: CI re-runs automatically
- [ ] ✅ All checks passing now?

#### Merge PR
- [ ] کلیک کردم: "Merge Pull Request" در GitHub
- [ ] Confirm: Merge
- [ ] Delete branch: `feature/us-1-4-test-coverage` در GitHub

### Local Cleanup

#### Update Master
- [ ] اجرا کردم: `git checkout master`
- [ ] اجرا کردم: `git pull origin master`
- [ ] چک کردم: Latest changes merged ✅

#### Delete Local Branch
- [ ] اجرا کردم: `git branch -d feature/us-1-4-test-coverage`
- [ ] نتیجه: Branch deleted ✅

---

## 🎉 Phase 4: Verification & Celebration

### Issue Status
- [ ] رفتم به: https://github.com/aminak58/freqai-futures-strategy/issues/13
- [ ] ✅ Issue automatically closed?
- [ ] اگر نه: manually close کردم

### Sprint Progress
- [ ] اجرا کردم: `python scripts/sprint_burndown.py --sprint 2`
- [ ] دیدم: Issue #13 marked as ✅ DONE
- [ ] Progress: _____/18 story points complete
- [ ] Percentage: _____%

### Team Velocity
- [ ] اجرا کردم: `python scripts/velocity_tracking.py`
- [ ] دیدم: Sprint 1 velocity: 16 pts
- [ ] دیدم: Sprint 2 velocity (partial): _____ pts

### Final Verification
- [ ] Coverage ≥ 60%? ✅
- [ ] All tests passing? ✅
- [ ] Issue #13 closed? ✅
- [ ] PR merged? ✅
- [ ] No regressions? ✅

---

## 📊 Summary Statistics

**تکمیل شده در تاریخ:** _____________

### Time Spent
- Phase 0 (Context): _____ دقیقه
- Phase 1 (Setup): _____ دقیقه
- Phase 2 (Dev): _____ دقیقه
- Phase 3 (PR): _____ دقیقه
- **Total:** _____ دقیقه

### Code Metrics
- Tests written: _____ tests
- Lines of test code: _____ lines
- Coverage increase: _____% → _____%
- Coverage delta: +_____%

### Quality Metrics
- Tests passing: _____/_____
- Linting errors: 0
- Type errors: 0
- Security issues: 0

### Git Metrics
- Commits: _____ commits
- Files changed: _____ files
- Lines added: _____ lines

---

## ✅ Completion Criteria

همه این موارد باید ✅ باشند:

- [ ] ✅ Coverage ≥ 60%
- [ ] ✅ All tests passing
- [ ] ✅ No linting errors
- [ ] ✅ No type errors
- [ ] ✅ No security issues
- [ ] ✅ PR created and merged
- [ ] ✅ CI checks all passing
- [ ] ✅ Issue #13 closed
- [ ] ✅ Local branch cleaned up
- [ ] ✅ Master branch updated

---

## 🎓 Lessons Learned

**چه چیزی خوب بود:**
- 
- 
- 

**چه چیزی می‌توانست بهتر باشد:**
- 
- 
- 

**برای دفعه بعد:**
- 
- 
- 

---

## 📝 Notes

[Add any additional notes, observations, or comments here]

---

**🎉 Congratulations! You successfully onboarded and completed Sprint 2 Issue #13!**

**Next task:** Issue #14 - Documentation Update (5 pts)

**Ready for more?** Check `python scripts/sprint_burndown.py --sprint 2`
