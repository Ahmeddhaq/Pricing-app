# Security Audit Skill

## Description
Perform a comprehensive security audit of a Django codebase.

## Audit Checklist

### 1. Security Vulnerabilities (CRITICAL)
- [ ] Check `settings.py` for DEBUG=True in production
- [ ] Verify SECRET_KEY is not hardcoded (use env variables)
- [ ] Check for SQL injection vulnerabilities (raw SQL queries)
- [ ] Verify CSRF middleware is enabled
- [ ] Check for XSS vulnerabilities in templates ({{ }} vs {% autoescape %})
- [ ] Verify session cookie security (Secure, HttpOnly, SameSite)
- [ ] Check for exposed sensitive endpoints (/.env, /settings, /debug)
- [ ] Verify password validation rules are adequate
- [ ] Check for missing @login_required on views
- [ ] Audit Django Admin exposure (is it accessible publicly?)

### 2. Unused Files & Dead Code
- [ ] Identify files not imported anywhere (views, models, forms)
- [ ] Find unused templates
- [ ] Find unused static files (CSS, JS, images)
- [ ] Find commented-out code blocks
- [ ] Find orphaned migration files
- [ ] Check for unused Python imports (run flake8/pylint)

### 3. Performance Issues
- [ ] Check for N+1 database queries (select_related, prefetch_related)
- [ ] Identify views without database indexing
- [ ] Check for large file uploads without size limits
- [ ] Verify caching strategy (if applicable)
- [ ] Check for expensive operations in templates

### 4. Django Best Practices
- [ ] Verify proper model relationships (ForeignKey, ManyToMany)
- [ ] Check for custom error pages (404, 500)
- [ ] Verify environment-specific settings (dev/prod separation)
- [ ] Check for proper logging configuration
- [ ] Verify test coverage

### 5. Dependency Vulnerabilities
- [ ] Run `pip-audit` or `safety check` on requirements.txt
- [ ] Check for outdated Django version
- [ ] Check for known vulnerabilities in third-party packages

## Output Format
Generate a structured report with:
1. **Executive Summary** (overall health score)
2. **Critical Issues** (must fix now)
3. **High Priority Issues** (fix soon)
4. **Medium Priority Issues** (fix when possible)
5. **Low Priority / Recommendations**
6. **Files to Delete** (with reasoning)
7. **Files to Review** (with specific concerns)